# Reproducibility

All analyses are scripted. Run order (from repo subdir `civilization_adaptation_feasibility/`):

```
python3 scripts/build_historical_pilot.py   # -> analysis/02_historical_pilot.csv + join report
python3 scripts/pilot_historical_model.py   # -> interaction estimates (printed)
python3 scripts/pilot_contemporary.py       # -> analysis/03_contemporary_pilot.csv + estimates
python3 scripts/pilot_future.py             # -> analysis/04_future_pilot.csv + T* summary
```

## Data acquisition
Raw public data are stored under `data/raw/` with a ledger in
`../CIVILIZATION_ADAPTATION_FEASIBILITY/DATA_SOURCE_LEDGER.csv` (URLs, access dates,
licenses, SHA-256). Re-acquisition commands:
- Equinox: `curl -L "https://zenodo.org/api/records/6642230/files/seshatdb/Equinox_Data-v.1.zip/content" -o data/raw/seshat/Equinox_Data-v.1.zip`
- CrisisDB: `curl -L https://raw.githubusercontent.com/datasets/seshat/main/CrisisConsequencesData_NavigatingPolycrisis_2023.03.csv`
- PAGES 2k S2: `curl -L https://www.ncei.noaa.gov/pub/data/paleo/pages2k/DatabaseS2-Regional-Temperature-Reconstructions.xlsx`
- OWID: `curl -L https://ourworldindata.org/grapher/annual-temperature-anomalies.csv` and `.../key-crop-yields.csv`
- WDI: fetched by `pilot_contemporary.py` via REST (no key).

Not redistributed: Seshat data are CC BY-NC-SA; the mirror CSV is fetched at runtime —
if the public-mirror sync policy applies, keep raw dumps out of the public repo and rely
on the acquisition commands above.

## Environment
Python 3.10, pandas, numpy, openpyxl, statsmodels (HC1 and cluster-robust SEs).
Seeds: no stochastic components (all joins deterministic).

## Known reproducibility limits
- CrisisDB→NGA uses a hand-built regex map in `build_historical_pilot.py` (audited, but a
  research decision; alternatives should be sensitivity-checked).
- GitHub mirror of CrisisDB may drift from the Seshat release.
- FAOSTAT bulk endpoint was unreachable from this VM during the audit (timeout) — flagged;
  acquisition scripts for the final study must be tested where FAO hosts are reachable.
