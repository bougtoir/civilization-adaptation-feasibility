# 02 — Historical / archaeological layer feasibility

## What was actually tested

A real small-scale join was executed (`scripts/build_historical_pilot.py`,
output `analysis/02_historical_pilot.csv`):

- CrisisDB consequences dataset (169 coded crises, public CSV, downloaded and stored locally).
- Joined to a Seshat NGA via a hand-built keyword map (auditable, conservative; 168/169 = 99%).
- Joined to the Equinox social-complexity panel, taking the latest century row at least 100 years
  before the crisis midpoint → pre-shock legacy proxies (Infra, Hier, Gov, Pop).
  Success: 98% of crises.
- Joined to PAGES 2k regional annual temperature → ΔT = mean anomaly of the century preceding
  the crisis minus the century before that. Success: 62% of crises (loses African crises —
  PAGES 2k has no Africa reconstruction — and crises outside 1–2000 CE).
- **Full rows (legacy × environment): N = 101.**

## Answers to the ten critical questions

1. **Can legacy dependence be measured before a shock?** Yes for social complexity
   (Equinox infra/hierarchy/government, ≥100 y lead). No public dataset measures
   *infrastructure capital per se* before shocks at comparable coverage; HYDE urban/cropland
   grids could add a land-use-persistence proxy.
2. **Independent environmental measure?** Partially. PAGES 2k gives regional temperature but
   no Africa and no drought measure at NGA level; Euro-Med2k scPDSI covers Europe+Med only.
   Hydroclimate (drought) is the actual stressor in most crisis narratives and is the weakest
   measurable dimension.
3. **Transformational response observable after shock?** **No — this is the core failure.**
   CrisisDB codes decline/collapse/uprising/conquest/fragmentation, i.e. collapse-and-conflict
   outcomes, not reconfiguration. No public dataset codes post-crisis *transformation*
   (relocation, subsistence restructuring, institutional redesign) at crisis-event level.
   Settlement relocation could in principle be built from radiocarbon SPDs (p3k14c) or HYDE
   urban dynamics, but that measures population redistribution, not institutional transformation,
   and the timing resolution is coarse.
4. **Temporal ordering defensible?** Yes for legacy (century-lagged) and climate (preceding
   century), at century resolution only.
5. **Cross-dataset linkage?** Workable but fragile: CrisisDB lacks PolID/NGA keys; the join used
   hand-built name mapping (99% coverage, but several mappings are debatable, e.g. which NGA hosts
   Byzantine crises). For a real paper the CrisisDB web interface returns Home NGA — manual
   extraction or the Seshat API is required, a reproducibility cost.
6. **N large enough?** Effective N ≈ 101 crisis events for the interaction — *after* losing all
   African crises to the PAGES 2k gap. Crises cluster inside NGAs; effective independent units
   ≈ 25–30 NGAs. β3 would be estimable but underpowered for anything beyond a large effect.
7. **Spatial autocorrelation manageable?** Crises within one NGA share climate history and
   culture; NGA or world-region fixed effects consume most of the already-small N.
8. **Survivorship/visibility dominates signal?** Likely. CrisisDB is biased toward literate,
   state-level societies — exactly the high-legacy end. Low-legacy societies with no recorded
   crisis are absent, truncating the legacy range and biasing β3 toward zero *or* flipping its
   sign depending on selection direction. This is the deepest threat, not fixable inside CrisisDB.
9. **Population decline vs transformation?** Decline is coded; transformation is not.
   p3k14c SPD could proxy redistribution but cannot distinguish collapse from planned relocation.
10. **Persistence vs absence of measurement?** Not distinguishable in CrisisDB — an NGA without a
    coded crisis is not an NGA verified to have persisted.

## Feasibility verdict for Layer 1

**CONDITIONAL.** The environment × legacy interaction is estimable (demonstrated join, N≈100
crises / ~28 NGAs), but the outcome variable needed for the *transformational* hypothesis does not
exist in public data at event level. Viable framings:

- Test EnvChange × Legacy → crisis severity/decline (a persistence-failure outcome, not
  transformation) — honest but narrower than the Nature claim; interaction sign and power
  acceptable for a pilot-scale result.
- Build a transformation proxy from HYDE urban-land dynamics or radiocarbon SPD inflection
  (population redistribution as observable transformation) — doubles the measurement chain and
  inherits visibility biases.
- Drop to the two best-covered regions (Europe/Mediterranean + East Asia) where both Euro-Med2k
  hydroclimate and dense archaeology exist — loses cross-civilizational scope.

The cross-societal sign-reversal claim is **not** supported by this layer alone.
