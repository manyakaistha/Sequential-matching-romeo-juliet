# Formal model, valid reductions and counterexamples

The objective is the expected number of **qualified mutual second-meeting intentions**, followed lexicographically by coverage, mutual acceptance, lower ask cost and lower latency. Each episode has 60 action days, t=0,…,59, and feedback is then collected through simulator day 100. All statements below concern the invented public simulator.

## 1. State, belief and Bellman equations

Let O_t=(M_t,A_t,B_t,H_t,L_t,P_t), with member records, observed availability, pending introductions with elapsed times, feedback, clarification log, and previously introduced dyads. Include the day and remaining budget. B_t is **not** an observed vector of true busy-release times: availability is observed, but the future date schedule may be hidden. Unknown preference fields, actor biases, response propensities, second biases, pending scheduled outcomes, exits, future arrivals and regime constitute latent Z_t. The exact decision state is the posterior b_t=P(Z_t|O_0,a_0,…,O_t). The full-information process is a finite-horizon MDP; its actual policy interface is a POMDP, or a belief-state MDP. A history containing all observations and actions is sufficient; attributes and current availability alone are not.

Use two stages per day. For valid query set Q with sum costs ≤12 and valid matching X on the refreshed verified graph:

V_t^ask(b)=max_Q E[V_t^match(Bayes(b,Y_Q))],

V_t^match(b)=max_X E[r_t+V_(t+1)^ask(Bayes(b,Y_(t+1)))].

Here r_t counts each qualifying MSMI once, at the observation of its last required feedback. At the end of action day 59:

V_60(b)=E[sum of pending qualified rewards observed by day 100 | b],

rather than zero. Equivalently, book expected eventual qualified rewards at assignment, let V_60=0 for **future assignments**, and exclude those pending rewards from subsequent immediate rewards. Linearity of expectation justifies this second bookkeeping even though retirement and busy times still affect transitions. With an artificial day-60 feedback cutoff, V_60=0 only if pending rewards are deliberately discarded.

All candidate matchings satisfy sum_(j)X_ij≤1 in each batch, reciprocal verified eligibility, no repeated dyad, and observed availability. The action space is a general graph, not gender partitions. Assigned pairs cannot be revoked: literature allowing recourse is an analogy, not an available operation.

## 2. Bandit reduction and node prices

Dyads (i,j) and (i,k) share an agent. Activating (i,j) changes the future availability and observations of (i,k), including possible retirement of i. Their transition kernels therefore do not factor into independent dyadic arms. Classical Gittins assumptions fail; Whittle's passive-subsidy monotonicity is not established merely by writing a subsidy. A Whittle-index policy would require a specified independent-arm relaxation and a proof that each arm's passive set expands with subsidy. We do not claim indexability of this coupled problem.

For a **relaxed one-step** matching LP, node multipliers yield reduced values q_ij-lambda_i-lambda_j. But node prices are insufficient for exact general-graph matching: a triangle with all edge values 1 admits the fractional solution x=1/2 on every edge, total 1.5, whereas any integer matching is worth 1. Add every odd-set inequality sum_(e⊆U)x_e≤(|U|-1)/2. Its dual needs blossom-set multipliers in addition to node prices. Dynamic continuation values also depend jointly on who remains in the pool. Thus separable prices are useful approximations, not an exact dynamic decoupling theorem.

## 3. A 60-day LP upper bound

For each oracle-feasible, non-declined pair e and valid assignment day t, let x_et be its expected assignment indicator and q_et its eventual qualified reward probability. Minimize negative expected reward (or maximize sum q_et x_et), subject to:

* 0≤x_et≤1; sum_t x_et≤1 (no repeated dyad).
* For every member i and action day d, sum_(e incident to i) sum_(t≤d<t+8)x_et≤1.
* Variables exist only when both agents have arrived and not exited at t.

This reveals non-declined hard constraints at zero cost, drops retirement and longer busy periods, and allows fractional assignments. Every realized legal schedule occupies endpoints at least eight days, so its expected indicators satisfy these inequalities. For the full latent world, future pair randomness is independent of preassignment history (fresh pair/day hash stream); hence E[R_et X_et]=q_et E[X_et] in the model's stochastic interpretation. Summing yields E[MSMI]≤LP*. The simulator itself is deterministic at a fixed seed; interpreting hash-based pseudo-randomness probabilistically is necessary for an **expected** bound. A realized episode can exceed LP*, so this is not a seedwise outcome ceiling.

q_et integrates the same shared Gaussian across **both** introduction responses and second intentions, actor-specific biases and response rates. q_et=.78×.36×(r_i r_j)^2×P(date delay≤30)×E_S[sigma(z_i+S)sigma(z_j+S)sigma(s_i+S)sigma(s_j+S)]. The last two logits include .4 for equal goal, while the first two contain the regime's soft fit and day-dependent drift. Numerical Gauss-Hermite quadrature and a sparse HiGHS LP implement the bound in upper_bound.py. This optimistic bound has no query-capacity constraint and is deliberately loose; an occupation-measure relaxation using expected busy durations could tighten it, but would need policy-dependent availability transitions handled correctly.

## 4. Stopping thresholds and monotonicity

A single agent who may irrevocably accept one observed offer R_t, independently receives another offer tomorrow conditional on survival. The correct recursion under post-rejection exit hazard h_t is:

V_t=E[max{R_t,(1-h_t)V_(t+1)}], V_60=0,

with threshold c_t=(1-h_t)V_(t+1). V_t-E[V_(t+1)] is **not** generally the acceptance threshold. Example: one future U[0,1] offer gives V_(t+1)=1/2; the current threshold is 1/2 but V_t-V_(t+1)=1/8.

**Proposition.** For iid nonnegative stationary offers, nondecreasing hazards h_t in [0,1], no recall, and zero terminal reward, c_t is nonincreasing in calendar time.

**Proof.** Backward induction starts with V_59≥V_60=0. If V_(t+1)≥V_(t+2) and h_t≤h_(t+1), then (1-h_t)V_(t+1)≥(1-h_(t+1))V_(t+2). Since x↦E[max(R,x)] is monotone, V_t≥V_(t+1). The same product inequality gives c_t≥c_(t+1). ∎

For strictness at t one needs a strict product inequality: positive survival and V_(t+1)>V_(t+2), or a strict hazard increase with positive remaining value. A sufficient stationary regime is a nondegenerate offer distribution with positive mass above every attained threshold, survival strictly positive, and values below the distribution's upper support; each additional opportunity then strictly raises V. Deterministic offers with no exit produce flat thresholds after the first opportunity and refute unconditional strict monotonicity.

Actual market arrivals ending after day 20 and growing verified neighborhoods violate stationary iid offers. A day with no future offers followed by a high-value arrival supplies a direct counterexample to universal time monotonicity. Repeated dates return unsuccessful agents to the pool and violate the one-stop assumption. The exact pair reservation term is the opportunity loss E[V_(t+1)|wait]-E[V_(t+1)|assign(i,j)] after subtracting the pair reward, and is a function of the full belief state. The implemented degree-scaled declining threshold is therefore explicitly heuristic.

### Actual departure hazard

The generator draws an exit in {22,…,60} for **12% of members total** and no relevant exit for the other 88%. Prior exit mass per day is .12/39. Conditional on survival just before an eligible exit day d, the prior hazard is (.12/39)/(1-.12(d-22)/39), approximately .31-.35%, not 12% per day. Availability also mixes busy and paused states, so posterior hazards require history rather than counting unavailable members as exits.

### Arrival and reward deadlines

Arrivals are bounded by day 20. Response delay is U{1,…,7}. Standard date delay is max(D_i,D_j)+U{1,…,14}; delayed adds U{5,…,12}. The respective exact means are 12.642857 and 21.142857 days. The latter deadline-failure probability is 120/5488=2.186589%. The date delay has no assignment-day dependence, so ceasing introductions early does **not** fix the relative 30-day deadline cliff. Both second-feedback delays are U{1,…,5}, hence among both-yes pairs the probability of satisfying both response deadlines is (3/5)^2=.36. Date feedback can be as late as assignment+38 in delayed; assignment day 59 completes by day 97, within the official day-100 observation window.

A day-60-only completion cutoff is conditional on what is meant by “full funnel.” Exact enumeration gives tcrit=51 (standard) and 43 (delayed) for P(both feedback submissions before day 60 | date happened, both submitted yes)<.05. Unconditional completion additionally depends on latent acceptance, response rates and goals, so no universal tcrit exists. Neither conditional cutoff is an official policy stopping rule.

## 5. VoI, hard-first conditions and complementarity

For query outcome Y and action set A, EVOI=E_Y[max_(a∈A)E[U(a)|Y]]-max_(a∈A)E[U(a)]≥0 by the maximum/Jensen inequality. Query cost is subtracted separately; net value can be negative.

**Restricted zero-VoI proposition.** Fix the immediate match stage, forbid any additional hard queries, and assume a queried incomplete node's soft value is conditionally independent of rewards on all currently feasible edges. Its hard-incomplete incident edges remain inadmissible for every Y. The feasible action set and all its reward expectations are unchanged, so the two maxima are identical: EVOI=0. For the immediate decision of that **pair alone**, the only feasible action is “do not introduce,” so the same equality follows without independence of other edges. ∎

This does not prove soft elicitation has zero **dynamic** value or zero value for a compound ask-then-match decision. Example: two hard-incomplete agents have potential match value 1 or 0, each revealed by a soft observation. After learning one, one can allocate the scarce hard query to the useful agent; that observation can improve the next stage even though no edge was immediately legal before it. Information may also affect population model inference. “Howard-Blackwell Invariance Principle” is not used as the name of a universal theorem.

Budgeted graph expansion is not generally submodular. Take two incomplete endpoints u,v with all other attributes compatible. Revealing constraints for either alone creates zero verified edges; revealing both creates one. Then marginal gain of querying v after u is 1, greater than its marginal gain from the empty set, 0. This violates diminishing returns. The correct formulation is a budgeted stochastic information/decision problem with complementary queries, not automatically submodular orienteering (there is no travel path).

The implementation scores not-yet-contradicted neighbors, weighting already verified or selected neighbors more heavily and adding an exploration bonus. It is a **proxy** for degree expansion, since unknown constraints may invalidate candidate edges. Entropy allocation computes the public generator’s conditional entropy of each missing semantic hard field given age and zone; field independence makes bundle entropy additive. It ignores ordering within preference/schedule sets, and only compares hard bundles before the common soft-budget fill. Maximizing hard-field entropy need not maximize matching value. Global algebraic connectivity lambda_2 is zero for disconnected graphs and often remains zero after a useful local reveal; for sparse's twelve immutable zone components, it cannot rank local improvements at all. query_compare.py tests this degeneracy using optimistic reveal graphs, without hidden truth.

## 6. Reciprocal probability, correlation and delayed-response EM

Let A,B be directional yes events including response. With common shared S and fixed pair attributes, outcomes are conditionally independent but depend on S. Thus P(A∩B)=E[p_A(S)p_B(S)] differs from E[p_A(S)]E[p_B(S)]. Since both are increasing functions of S, their covariance is nonnegative: with independent S', 2Cov(f(S),g(S))=E[(f(S)-f(S'))(g(S)-g(S'))]≥0. Mixing selected dyads and heterogeneous actors may add or mask this association; empirical public-pool estimates are descriptive.

The harmonic mean 2p_Ap_B/(p_A+p_B) can exceed min(p_A,p_B), which a joint probability cannot. For p_A=p_B=.5 it equals .5 while independent mutual success is .25. It must be evaluated as a ranking score. Our scorer's .10/.13 terminal multiplier is likewise uncalibrated: it does not turn harmonic fusion into P(MSMI). A correctly calibrated future model should integrate a shared random effect through all funnel stages.

For response mixture propensity p and delay CDF F(e), an unobserved pending response at age e has posterior eventual response:

P(C=1|not yet observed,e)=p(1-F(e))/(1-pF(e)).

The E-step computes this soft membership; the M-step adds expected positive mass to a Beta-smoothed response estimate. Four iterations are used. The simulator logs an explicit no-response at day 7, so after that point no-response is observed failure, not right-censoring. This is a discrete response-stage adaptation of Chapelle's mixture idea, **not** a complete multi-stage terminal-conversion DFM. Logistic acceptance updates occur only on observed yes/no responses; second intentions, date occurrence, response probability and qualification deadlines are distinct targets.

A diagonal precision logistic update is a fast approximate posterior, not an exact Bayesian regression or calibrated confidence interval. Directional events share dyadic effects; independence-based precision may overstate certainty. Assignment-time feature snapshots are serialized and removed after both responses; later clarifications cannot alter training examples retroactively. The public event name is date_happened, not date_result.

## 7. Shift information and fatigue

Holding all other latent quantities fixed, changing lifestyle from unequal to equal changes introduction logit by +.375 in development and -.375 in shift. Any fixed scorer that rewards equality cannot rank this conditional intervention correctly in both regimes. This proves model mismatch, not that every static policy loses on every finite seed.

For identifying the shift coefficient -.25 from independent fully observed direction-level trials, lifestyle predictor takes 1 (probability 1/3) or -.5, with variance .5. Logistic information after accounting for an intercept is at most .25×.5=.125 per trial. A normal-approximation planning calculation for one-sided 95% confidence and 95% detection power needs at least (z_.95+z_.95)^2/(.25²×.125)≈1386 independent labels even under this optimistic information envelope. This is a planning estimate, not a finite-sample minimax guarantee. Nuisance features, shared effects, missingness and nonrandom exploration increase the requirement. The executed randomized logistic experiment illustrates detection power; it does not claim that the deployed diagonal posterior has calibrated 95% confidence.

Drift subtracts .5 at assignment days≥35. For z=0, directional acceptance falls from .5 to .37754; independent mutual acceptance would fall from .25 to .14254, but the shared effect requires integration for actual joint probabilities. Earlier assignment weakly increases the immediate reward of the same dyad, but may sacrifice alternative partners, queries or future repeat opportunities. No universal optimal front-load percentage follows. The final report provides measured assignment shares before day 35 and batching experiments, with no claim that their best empirical rate solves the global Bellman equation.
