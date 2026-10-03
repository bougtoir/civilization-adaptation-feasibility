# 06 — Pilot report (minimal, pipeline-verifying)

Three pilots ran end-to-end on public data. They are feasibility checks, not the study.
No specification was optimized; every variant tried is reported in `06_pilot_results.csv`.

## Pilot 1 — historical interaction (CrisisDB × Equinox × PAGES 2k)
- logit `decline ~ dT + Infra + dT×Infra + century`, cluster-robust SE by NGA.
- N = 72 usable crises, 21 NGAs (3 NGAs = 37% of rows → effective N ≈ 21).
- β3 = 0.28 (95% CI −0.01, 0.56). Direction consistent with hypothesis, CI at zero edge.
- **Specification fragility: swapping Infra→Hier flips β3 to −0.21.** The interaction is
  not stable under a legitimate alternative legacy measure — decisive warning against
  index-shopping; any final study must preregister dimensions.
- Exposure frame caveat: crisis-frame sample conditions on exposure (see 05).

## Pilot 2 — contemporary spatial (WDI × OWID temperature)
- `realloc = agshare2000 − agshare2021` ~ country temp anomaly 2011–21 × legacy
  (urban2000, agland2000), controls log GDPpc + baseline ag share. N = 162, R² = 0.45.
- β3 positive for both legacy measures (+0.08, +0.07), i.e. **opposite** to the strong
  hypothesis, wide CIs. Missingness: ~40 countries dropped (non-random, poorer states).
- Conclusion: country-level environment × legacy → restructuring is estimable but does
  not currently point the hypothesized way; crop-level (FAOSTAT) or grid-level (GHSL)
  outcomes are the stronger domain.

## Pilot 3 — future counterfactual (OWID yields × temperature anomalies)
- T* solved per country for dominant-vs-alternative crop under switching-cost band
  {0,10,20%}: 50/45/41 of 173 countries cross within +4 °C; median T* ≈ 1.1–1.5 °C.
- Deliberately straw operationalization (dominant = max yield not area) — demonstrates
  both that the pipeline works and that T* is extremely sensitive to definitional and
  cost assumptions. Real analysis must use harvested-area dominance + GAEZ suitability.

## Missing-data / diagnostics
- Historical join: env data available for 62% of crises; Africa structurally missing.
- Contemporary: missing WDI outcomes concentrated in low-income countries.
- Spatial autocorrelation: historical NGA concentration reported above; contemporary
  residuals not yet Moran-tested (flagged).

## What pilots establish vs do not
- DO: all joins and estimations run; N and effective N are now known quantities;
  direction instability exposed in both fitted layers.
- DO NOT: they do not establish β3 ≠ 0, nor sign reversal, nor causality.
