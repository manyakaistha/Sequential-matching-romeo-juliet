# Extended investigation: prospective experiment registry

Registered 8 October 2026 before new-seed evaluation. Earlier artifacts remain in
`results/research`; they are not untouched test data. This registry is amended
chronologically, with amendments dated and made before the affected evaluation.

## Simulator agreement and information boundary

The shipped `kit.py` and `evaluate.py` are authoritative. Action days are 0-59;
40 further observation days collect pending outcomes. Eleven hard fields must
be observed and reciprocal eligibility verified. Hard declines are permanent.
Endpoint reuse is legal after busy periods; dyad reuse is forbidden. Exit occurs
for 12% of members total, with assigned exit day in 22-60. Availability does not
reveal future busy releases or exits. Date qualification is <=30 days from
assignment; each positive feedback must occur <=3 days from date. Both positive
answers pause endpoints even when deadlines disqualify reward. Shared dyadic
Gaussian effects enter introduction and second logits; actor response propensity
is reused at both stages. Unknown true attributes, actor effects, future arrivals,
scheduled events, exit days and regime are latent. Public generator distributions
are known mechanisms. Policies receive JSON observations only. Separate audit
code may use truth and must label it explicitly.

## Seed exclusions and partitions

Previously examined: 101-105, 201-205, 301-305, 20260926 and public generator
20261000-20261009 (source/artifact inventory). Never call these untouched.

* Development: 1001-1008, all six families, used for debugging, calibration audits,
  candidate exploration and architecture interactions.
* Candidate selection: 2001-2012, all six families. Candidate set and deterministic
  selection rule are frozen in an amendment before selection.
* Final confirmation: 3001-3040, all six families. One frozen selected policy versus
  shipped greedy, with code/config SHA256 recorded before any confirmation run.
  No retuning or sample extension after viewing confirmation results.

Each seed is an independent cluster; six scenario families sharing a seed are
averaged within seed. Public pool snapshots are descriptive, not prospective
training examples. New development snapshots are taken at assignment and used
only for validation unless training is explicitly registered before selection.

## Hypotheses and candidates

The experiment configuration will supply a named modular configuration map. Prelisted
experiments are: simple terminal control; fully integrated shared-effect terminal
model; independent-product ablation; no-learning ablation; FIFO/potential-degree/
exact-generator-entropy/one-query expected matching-value/two-query complementarity/
budgeted-random query comparators; greedy versus general-graph blossom; occupation
and retirement continuation penalties; component batching; conservative uncertainty.
Compare prior frozen product and shipped greedy as controls. Forced bipartite
allocation, if implemented, is a restricted comparator only.

Primary hypothesis: replacing uncalibrated ranking multipliers with observed-history
terminal reward estimates improves scenario-balanced qualified MSMI/100. Secondary
hypotheses: joint query lookahead improves verified edges; continuation penalties
reduce wasted busy time; complex models must outperform simpler controls to justify
their cost. Negative findings are retained. Development tests include within-new-
architecture ablations and scoring/query/allocation/waiting interactions.

## Statistics and sample size

Primary outcome: unweighted mean of the six family MSMI/100 means. Paired cluster
difference selected policy minus greedy; predefined two-sided Student t test at
alpha=.05 and 95% paired cluster CI. Cluster bootstrap CI is sensitivity analysis;
the t result remains confirmatory. A superiority claim requires positive CI lower
bound and a complete valid experiment, and is restricted to these public families.
Use Holm adjustment over exploratory candidate contrasts in each experiment, with
unadjusted estimates and CIs also supplied. No significance-driven stopping.

Prior paired SD is .2041-.2075 MSMI/100. A practical difference .10 requires about
33-34 independent seed clusters for 80% power at two-sided .05 by normal planning
`n=((1.96+.842)*SD/.10)^2`. Forty confirmation clusters (480 total episodes for two
policies) add a modest margin. This does not establish power for .05 effects, which
would require about 131-136 clusters; final uncertainty will be reported honestly.

Report coverage, episode mutual acceptance/assignment, date/mutual acceptance,
ask cost, latency mean/p95/p99/max, memory/request bytes, failures and invalid
episodes, family contrasts, effect size and cluster intervals. Zero denominators
use zero rates and are identified by raw counts. Invalid episodes remain visible
and make the official summary ineligible; no failed runs are silently dropped.

Calibration: assignment-time predictions; pending is not a negative, no-response
is an explicit resolved failure. Log loss/Brier/reliability with seed-bootstrap
uncertainty for response, mutual acceptance, date, both-positive feedback and
terminal qualification, including family and sparse-history slices. Full 100-day
follow-up resolves all supported delays. Truth-only numerical approximation audits
and oracle comparisons are separately labeled.

## Execution and provenance

Two worker processes, observation JSON roundtrip in fast mode through unchanged
`evaluate.episode`; subprocess and resource-limited offline Docker independently
verified. Track action digests and semantic order-insensitive actions separately.
Preserve earlier artifacts and snapshot REPORT before replacing it. Raw episode
rows, trace samples, exact simplified-model benchmarks, calibration/mechanism
figures, tests, package versions and code/config/seed hashes accompany the report.

## Amendment 1: candidate-selection rule (before completed development matrix)

8 October 2026. Development evaluates every frozen configuration in
`research/extended_candidates.py` plus shipped greedy and prior product. Code is
frozen for this matrix after smoke fixes; preliminary smoke_v1 is explicitly
debugging evidence, not the final matrix. The four configurations
simple_degree, simple_blossom, terminal_degree_blossom and terminal_degree_batching
provide scoring/query/allocation/waiting interaction controls in that same matrix.

Selection evaluates the four highest development-score eligible new configurations,
plus mandatory terminal_fifo, simple_fifo, independent_fifo and no_learning_fifo
(deduplicated), plus greedy and prior_product. Development ties use the number of
nondefault config fields, then alphabetical policy name. An eligible configuration
needs every planned episode valid and six families for each seed. No further model
fitting is permitted after development.

On selection, consider new candidates within .05 MSMI/100 of the largest primary
score. Select the candidate with the fewest nondefault configuration fields, then
higher primary score, then alphabetical name. This predefined simplicity preference
does not establish statistical equivalence of policies within .05. Greedy and prior
product are comparator policies and are not selected as the new candidate.

Freeze the selected config and all inference source hashes before confirmation.
The final comparison and sample size remain unchanged. Selection can choose a
candidate with no established improvement; confirmation still tests it once.

## Amendment 2: review corrections before selection

8 October 2026, while development is running; no completed development ranking
or selection results have been viewed. Counting configuration overrides is not
a valid proxy for model complexity: the default integrated model has zero
overrides. Replace only the simplicity ordering (within the same .05 band) with
the lexicographic cost tuple: model cost (simple aggregate=0, frozen parametric=1,
other parametric=2); lookahead/soft acquisition indicator; blossom indicator;
waiting/opportunity indicator; number of overrides; negative primary score;
alphabetical name. This is a preselection engineering preference, not a calibrated
cost model or a statistical equivalence claim. Development top-four ties retain
the original ordering, which only orders equal observed scores.

Independent production stress found an uncaught division by zero for corrupt
version-2 memory and whole scoring times close to the ten-second budget on dense
diverse-history requests. A production-only guard patch will catch arithmetic
errors and bound the entire decision by seven seconds, using a legal fallback.
Development remains the original frozen version. Before selection, preserve that
version, record the guard-only diff and new hashes, and compare all twenty new
configs on all six already-used families at seed1001 against original development
digests/outcomes. Ordinary old calls must have remained below the new deadline.
If parity fails, investigate and rerun affected development, rather than treating
changed trajectories as equivalent. Selection and confirmation both use the same
patched frozen version. This safety correction changes no score, query objective,
posterior update or parameter, and no confirmation seed is used for validation.
