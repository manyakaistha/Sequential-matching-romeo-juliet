"""Offline time-indexed expected-capacity LP, optimistic upper bound.

Computes the theoretical upper bound on MSMI by relaxing query budgets,
retirement, and long busy periods. Evaluates expected rewards using
32-point Gauss-Hermite numerical quadrature.
"""
import collections
import itertools
import json
import math
from pathlib import Path
import sys

# Ensure repository root is on path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix
from kit import generate, eligibility, HARD


def is_blocked(m):
    """Check if member permanently declined any hard constraint."""
    return any(m['field_status'].get(k) == 'declined' for k in HARD)


def exact_delay(delayed=False):
    """Compute exact discrete delay distribution and late date probability."""
    mass = collections.Counter()
    for a, b, d in itertools.product(range(1, 8), range(1, 8), range(1, 15)):
        for extra in (range(5, 13) if delayed else [0]):
            mass[max(a, b) + d + extra] += 1
    n = sum(mass.values())
    prob = {k: v / n for k, v in sorted(mass.items())}
    return {
        'late_date_probability': sum(p for d, p in prob.items() if d > 30),
    }


def compute_upper_bound(seed, variant):
    """Compute LP upper bound on MSMI per 100 arrived members for a given world."""
    world = generate(seed, 200, 'evaluation', variant)
    ms = [m for m in world['members'] if not is_blocked(m)]
    edges = []
    nodes, weights = np.polynomial.hermite.hermgauss(32)
    shared = np.sqrt(2) * 0.45 * nodes
    weights = weights / math.sqrt(math.pi)

    def sigmoid(z):
        return 1 / (1 + np.exp(-z))

    late = exact_delay(variant == 'delayed')['late_date_probability']

    for a, b in itertools.combinations(ms, 2):
        if eligibility(dict(a, fields=a['truth']), dict(b, fields=b['truth']))['status'] != 'feasible':
            continue
        wa = [0.25, 0.8, -0.25, 0.5] if variant == 'shift' else [0.7, 0.4, 0.25, 0.2]
        fit = sum(w * (1 if a['truth'][k] == b['truth'][k] else -0.5)
                  for w, k in zip(wa, ('relationship_goal', 'relationship_pace', 'lifestyle', 'conversations')))
        goal = (a['truth']['relationship_goal'] == b['truth']['relationship_goal'])

        def reward(drift):
            p = sigmoid(-0.25 + a['bias'] + fit + shared + drift) * sigmoid(-0.25 + b['bias'] + fit + shared + drift)
            second = sigmoid(0.15 + a['second_bias'] + shared + 0.4 * goal) * sigmoid(0.15 + b['second_bias'] + shared + 0.4 * goal)
            return float(weights @ (p * second)) * 0.78 * 0.36 * (a['response_rate'] * b['response_rate']) ** 2 * (1 - late)

        edges.append((a, b, reward(0), reward(-0.5)))

    variables = []
    rewards = []
    for e, (a, b, q, qdrift) in enumerate(edges):
        for t in range(max(a['arrived_day'], b['arrived_day']), min(60, a['exit_day'], b['exit_day'])):
            variables.append((e, t))
            rewards.append(qdrift if variant == 'drift' and t >= 35 else q)

    index = {m['member_id']: j for j, m in enumerate(ms)}
    rr = []
    cc = []
    vv = []

    # Each pair at most once; each member occupied at least 8 days per assignment
    for c, (e, t) in enumerate(variables):
        rr.append(e)
        cc.append(c)
        vv.append(1)
        a, b, *_ = edges[e]
        for m in (a, b):
            for day in range(t, min(60, t + 8)):
                rr.append(len(edges) + 60 * index[m['member_id']] + day)
                cc.append(c)
                vv.append(1)

    if not variables:
        return {'seed': seed, 'variant': variant, 'bound_msmi_per100': 0.0}

    mat = coo_matrix((vv, (rr, cc)), shape=(len(edges) + 60 * len(ms), len(variables))).tocsr()
    solution = linprog(-np.array(rewards), A_ub=mat, b_ub=np.ones(mat.shape[0]), bounds=(0, 1), method='highs')

    return {
        'seed': seed,
        'variant': variant,
        'success': bool(solution.success),
        'variables': len(variables),
        'edges': len(edges),
        'bound_msmi_per100': float(-solution.fun / 2) if solution.success else None,
        'caveat': 'Expected reward upper bound via HiGHS LP relaxation with 32-point Gauss-Hermite quadrature.'
    }


if __name__ == '__main__':
    variants = ('development', 'sparse', 'cold_start', 'delayed', 'shift', 'drift')
    rows = [compute_upper_bound(101, v) for v in variants]
    out_dir = ROOT / 'results'
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / 'upper_bound.json'
    out_file.write_text(json.dumps(rows, indent=2) + '\n')
    print(f"Computed LP upper bounds written to {out_file}:")
    for r in rows:
        print(f"  {r['variant']:12s}: {r['bound_msmi_per100']:.4f}")
