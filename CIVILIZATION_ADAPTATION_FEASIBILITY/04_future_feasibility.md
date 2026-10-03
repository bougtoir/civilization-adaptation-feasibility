# 04 — Future climate / counterfactual layer feasibility

## V_retain(T) vs V_substitute(T): where T* is computable

**Crops (strongest).** GAEZ publishes baseline attainable yields and projected suitability
under CMIP scenarios per crop per cell. Retention = keep current dominant crop (MapSPAM/
FAOSTAT allocation); substitution = best-ranked alternative crop in the same cell. The
crossing T* is then a deterministic function of two public model outputs — no invented
values. Constraints: all results are conditional on the GAEZ agro-climatic model
(model dependence, not measurement); T* should be computed under ≥2 GCMs and reported
as a distribution.

**Settlement (partial).** V_retain = hazard-exposed population/value under in-situ
persistence (GHSL + hazard layers). V_substitute requires a *destination* for relocation,
and no public dataset defines feasible destination sites; a rule would have to be authored
(e.g. nearest cell meeting elevation/hazard/water criteria). Doable, but the counterfactual
definition becomes a major design decision reviewers can attack. The Leaving-Place case
dataset validates outcomes for ~300–400 real relocations.

**Livestock / food utilization (rejected).** No public substitution model; keep conceptual.

## Cultural switching-cost classification

| component | class | basis |
|---|---|---|
| crop switching cost (capital, replanting, infrastructure) | 3 — sensitivity parameter only | no global public data; literature gives farm-level adoption elasticities but nothing cross-country comparable |
| institutional/land-tenure friction | 4 — non-identifiable in public data | case-study only |
| settlement relocation cost | 3 — sensitivity parameter + case calibration | ~300-400 case dataset allows order-of-magnitude calibration, not estimation |
| dietary/cultural food preferences | 4 — non-identifiable at required granularity | FAOSTAT food balances show current patterns, not willingness to substitute |

Rule adopted: any parameter in class 3 enters only as a sensitivity band over a stated range
(as done in `analysis/04_future_pilot.csv`, s ∈ {0, 10, 20%}); class 4 is excluded from the
estimating equations entirely and discussed verbally.

## Pilot performed
`scripts/pilot_future.py` (OWID yields × country temperature anomalies): T* computed for
173 countries; 50/45/41 countries reach T* within +4 °C for switching costs 0/10/20%.
Result is deliberately a *straw operationalization* — "dominant crop" was chosen by yield
level, not harvested area, precisely to expose operationalization dependence; the real
study must use harvested area and GAEZ suitability. Feasibility of the pipeline: confirmed;
feasibility of credible T*: requires GAEZ + area-based dominance.
