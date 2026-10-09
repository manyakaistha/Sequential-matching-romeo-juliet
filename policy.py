import sys
import json
import itertools

SOFT = ['relationship_goal', 'relationship_pace', 'lifestyle', 'conversations']
HARD = ['age_min', 'age_max', 'who_to_meet', 'relationship_structure', 'smoking', 'partner_smoking', 'has_children', 'partner_children', 'wants_children', 'acceptable_zones', 'schedule']


def eligibility(a, b):
    if a['member_id'] == b['member_id']:
        return {'status': 'infeasible', 'reasons': ['same_member']}
    if a['pool_id'] != b['pool_id']:
        return {'status': 'infeasible', 'reasons': ['different_pool']}
    if min(a['age'], b['age']) < 18:
        return {'status': 'infeasible', 'reasons': ['underage']}
    fa, fb = a['fields'], b['fields']
    missing = []
    for member, f in ((a, fa), (b, fb)):
        missing += [member['member_id'] + ':' + k for k in HARD if f.get(k) is None]
    for x, y, fx, fy in ((a, b, fa, fb), (b, a, fb, fa)):
        if fx.get('age_min') is not None and y['age'] < fx['age_min']:
            return {'status': 'infeasible'}
        if fx.get('age_max') is not None and y['age'] > fx['age_max']:
            return {'status': 'infeasible'}
        w = fx.get('who_to_meet')
        if w is not None and y['gender'] not in w:
            return {'status': 'infeasible'}
        if fx.get('relationship_structure') is not None and fy.get('relationship_structure') is not None and fx['relationship_structure'] != fy['relationship_structure']:
            return {'status': 'infeasible'}
        p_smoke = fx.get('partner_smoking')
        if p_smoke is not None and fy.get('smoking') is not None and p_smoke == 'no_smoking' and fy['smoking'] != 'no':
            return {'status': 'infeasible'}
        p_child = fx.get('partner_children')
        if p_child is not None and fy.get('has_children') is not None and p_child == 'no_children' and fy['has_children']:
            return {'status': 'infeasible'}
        wants = fx.get('wants_children')
        other_wants = fy.get('wants_children')
        if wants == 'yes' and other_wants == 'no':
            return {'status': 'infeasible'}
        if wants == 'no' and other_wants == 'yes':
            return {'status': 'infeasible'}
        zones = fx.get('acceptable_zones')
        if zones is not None and y['zone'] not in zones:
            return {'status': 'infeasible'}
        sch1 = fx.get('schedule')
        sch2 = fy.get('schedule')
        if sch1 is not None and sch2 is not None and not set(sch1).intersection(set(sch2)):
            return {'status': 'infeasible'}
    return {'status': 'feasible' if not missing else 'missing_hard', 'missing': missing}


def decide(request):
    phase = request['phase']
    state = request['state']
    memory = request.get('memory') or {}
    mem_dict = {m['member_id']: m for m in state['members'] if m['available']}

    if phase == 'ask':
        budget = state['ask_budget_remaining']
        asks = []
        missing_hard = []
        for m in state['members']:
            if m['available'] and any(m['fields'].get(k) is None and m['field_status'].get(k) != 'declined' for k in HARD):
                missing_hard.append(m['member_id'])

        for m_id in missing_hard:
            if budget >= 3:
                asks.append({'member_id': m_id, 'field': 'constraints'})
                budget -= 3

        if budget > 0:
            feasible_members = set()
            past = {tuple(sorted((i['user_a'], i['user_b']))) for i in state['introductions']}
            mem_list = list(mem_dict.values())
            for a, b in itertools.combinations(mem_list, 2):
                key = tuple(sorted((a['member_id'], b['member_id'])))
                if key in past:
                    continue
                if eligibility(a, b)['status'] == 'feasible':
                    feasible_members.add(a['member_id'])
                    feasible_members.add(b['member_id'])

            for m_id in list(feasible_members):
                if budget >= 1:
                    m = mem_dict[m_id]
                    if m['fields'].get('relationship_goal') is None and m['field_status'].get('relationship_goal') != 'declined':
                        asks.append({'member_id': m_id, 'field': 'relationship_goal'})
                        budget -= 1

        return {'asks': asks, 'memory': memory}

    if phase == 'match':
        past = {tuple(sorted((i['user_a'], i['user_b']))) for i in state['introductions']}
        mem_list = list(mem_dict.values())
        edges = []
        w = {'relationship_goal': 3.0, 'relationship_pace': 1.0, 'conversations': 0.5, 'lifestyle': 0.1}

        weights_by_node = {m['member_id']: [] for m in mem_list}

        for a, b in itertools.combinations(mem_list, 2):
            key = tuple(sorted((a['member_id'], b['member_id'])))
            if key in past:
                continue
            if eligibility(a, b)['status'] != 'feasible':
                continue

            score = 0
            for k, weight in w.items():
                va = a['fields'].get(k)
                vb = b['fields'].get(k)
                if va is not None and vb is not None:
                    if va == vb:
                        score += weight
                    else:
                        score -= weight * 0.5

            if score >= 0.0:
                edges.append((score, a['member_id'], b['member_id']))
                weights_by_node[a['member_id']].append((score, key))
                weights_by_node[b['member_id']].append((score, key))

        final_edges = []
        for score, m1, m2 in edges:
            key = tuple(sorted((m1, m2)))
            cost = 0.0
            for ident in (m1, m2):
                others = [val for val, p in weights_by_node[ident] if p != key]
                if others:
                    cost += max(others) * 0.35
            adjusted = score - cost
            final_edges.append((adjusted, m1, m2))

        used = set()
        pairs = []
        for adj, m1, m2 in sorted(final_edges, reverse=True):
            if adj >= -1.0 and m1 not in used and m2 not in used:
                pairs.append([m1, m2])
                used.add(m1)
                used.add(m2)

        return {'pairs': pairs, 'memory': memory}


if __name__ == '__main__':
    request = json.load(sys.stdin)
    print(json.dumps(decide(request), allow_nan=False))
