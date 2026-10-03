# 08 — Recommended final design (if pursued)

## Lead analysis (paper's spine): crop systems
- Unit: country×crop×year panel (FAOSTAT area/production, 1961–) plus gridded MapSPAM
  × WorldClim/ERA5.
- Legacy dimensions (preregistered, separate, no index):
  1. staple concentration (Herfindahl of crop harvested-area shares);
  2. irrigation/infrastructure dependence (MIRCA/FAO irrigated share);
  3. settlement persistence (GHSL epochal built-surface stability) where spatially joined.
- Env change: decadal temperature + precipitation anomaly (ERA5), drought (SPEI product).
- Outcome (transformation): crop switching / diversification change — Δ crop-mix distance,
  new-crop adoption, area reallocation. NOT yield resilience.
- Estimand: env × legacy interaction on switching; sensitivity: alternative
  concentration measures, alternative anomaly windows, leave-region-out, placebo leads.

## Counterfactual module
- T* map: GAEZ current vs projected suitability; retained crop vs best alternative;
  switching cost as sensitivity band {0,10,20,30%} explicitly labelled class-3.
- Retention-burden map: yield gap between retention and substitution paths × current
  allocation — one clean headline map.

## Secondary layer: historical
- Rebuild on exposure frame: NGA×century panel from Equinox + LMR/TRENMay environmental
  anomalies (adds Africa); CrisisDB used as outcome validation, not sample frame.
- Outcome: SPD/redistribution inflection from p3k14c or HYDE urban dynamics; flag
  visibility biases. Report as supporting evidence only.

## Explicit exclusions
- No livestock empirical layer (data don't exist).
- No composite civilization index.
- No sign-reversal claim unless the crop domain itself shows it.

## Falsification battery (preregister)
placebo time windows, displaced spatial joins, unrelated-env controls, alternate
legacy/outcome multiverse (report all), leave-one-region-out, missingness-adjusted
weights.

## Realistic assessment for the authors
The current pilots give one direction-consistent (weak, fragile) and one
direction-opposite result. The design above can deliver a Nature-level *general empirical
test of adaptation lock-in*. It cannot — on today's public data — deliver a demonstration
of civilizational sign reversal. Plan for the former; treat the latter as a possible
finding, not the thesis.
