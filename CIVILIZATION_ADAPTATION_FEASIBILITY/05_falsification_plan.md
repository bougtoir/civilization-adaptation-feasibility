# 05 — Identification & falsification plan

## Fatal flaws found in the naive design

1. **CrisisDB samples crises, not exposures.** Regressing crisis outcomes on environmental
   change over a crisis-frame conditions on having a crisis. Correct frame: NGA×century
   panel with exposure constructed from the climate product alone (env-driven ΔT droughts),
   with transformation/abandonment as outcome; crisis coding becomes a validation layer.
2. **PAGES 2k has no Africa** → the env join drops African crises, selecting on data
   availability in a way correlated with colonial bias in both datasets. Remedy: LMR
   gridded reconstruction or TRENMay products.
3. **No public transformation outcome at event level** (see 02 report). The study cannot
   claim "transformational flexibility" from CrisisDB alone.
4. **Contemporary pilot sign is positive** (higher urban share → *more* realloc under
   warming), opposite to the strong hypothesis. With N=162 and wide CIs the direction is
   not established, but there is no evidence yet for the sign the paper needs.

## Falsification design (what could kill the claim)

| test | dataset | interpretation |
|---|---|---|
| placebo time window | assign crisis outcomes to climate anomalies 200 y AFTER the crisis | β3 near zero required; if comparable, join is picking up trends not mechanism |
| future climate predicting prior transformations | PAGES regional series shifted +200y | same |
| unrelated environmental variable | e.g. cyclone/volcanic proxy or arbitrary gridded product uncorrelated with mechanism | should not interact with legacy |
| random spatial displacement | permute NGA → climate mapping | destroys real β3 if mechanism is real |
| alternative legacy indices | Infra vs Hier vs settlement persistence (GHSL/HYDE) | β3 sign must be stable across preregistered dimensions; pilot already shows sign flip (Infra +, Hier −) → hypothesis is fragile under legitimate alternative operationalizations |
| alternative transformation outcomes | decline vs severity vs sectoral reallocation | same |
| leave-one-region-out | drop Latium/Paris Basin clusters | β3 must not be driven by two NGAs |

## Effective-N warnings (measured)
- Historical pilot: 72 usable crisis rows over 21 NGAs; 3 NGAs contribute 37% of rows.
  Effective independent units ≈ 21.
- Contemporary pilot: 162 countries; 1 obs each → no clustering correction needed at
  country level, but spatial correlation unaccounted (Moran's I on residuals recommended).

## Can the design be falsified? 
Yes — conditionally. If the analysis is rebuilt on an exposure frame (not crisis frame)
with preregistered separate legacy dimensions and a real transformation outcome, the
interaction is a testable, falsifiable claim. In the pilot form the claim is not yet
well-posed.
