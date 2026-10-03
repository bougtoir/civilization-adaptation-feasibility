# 03 — Contemporary layer: retention burden feasibility

## Domain-by-domain verdict

### Settlement / infrastructure
- Legacy dependence proxies: GHSL epochal built-surface grids (1975–2030) → settlement
  persistence and expansion rate; OSM/GRIP road density; night-lights intensity. All public
  and scriptable. **Measurable.**
- Environmental change: ERA5/WorldClim + OWID/Berkeley-Earth country anomalies (used in pilot).
  **Measurable.**
- Transformational flexibility: *not directly observable at grid level*. Observable
  surrogates: new-settlement growth vs in-situ densification (GHSL epochs), population
  redistribution (WorldPop), relocation cases (Leaving Place dataset — case catalog not a
  panel). **Weak but real.**

### Agriculture / staple dependence
- Staple/crop concentration: FAOSTAT harvested area (bulk zips) or MapSPAM grids →
  Herfindahl of crop area shares = a defensible, non-arbitrary dependence measure.
  **Measurable.**
- Outcome: crop switching / diversification change over time (FAOSTAT area panel, SPAM
  vintages) — the same outcome class used by the crop-switching literature.
  **Measurable — the strongest domain.**
- Counterfactual states (RB): GAEZ current-vs-future suitability maps let
  "retention-constrained" (keep current crop) vs "substitution-allowed" (best alternative)
  yields be computed cell-by-cell without inventing parameters. Both counterfactuals are
  definable from public model output. **RB is estimable for crops**, conditional on
  accepting GAEZ as the production model (model dependence must be reported).

### Livestock / food utilization
- Public data cover heads, production, slaughter counts (FAOSTAT) and sector emissions
  (GLEAM model outputs). Edible offal yields, carcass-utilization fractions, organ-meat
  consumption shares and by-product utilization are **not globally observed**; only
  literature ranges exist.
- **Verdict: keep livestock conceptual. Do not build an empirical layer on it** — the
  utilization counterfactual would require unverifiable assumptions.

### Retention burden (RB) estimability summary
RB = V_flexible − V_constrained is computable only where both counterfactual states are
public model outputs or estimable responses:
- crops: yes (GAEZ + MapSPAM/FAOSTAT).
- settlement: partially (GHSL + hazard layers give exposure difference between retained
  site and relocation destinations; the relocation counterfactual still needs a destination
  definition rule — feasible but design-heavy).
- livestock utilization: no.
- institutions/trade: no public counterfactual.

## Pilot performed (pipeline check)
`scripts/pilot_contemporary.py`: country-level realloc (decline in agriculture value-added
share 2000→2021) ~ mean temp anomaly 2011–21 × legacy proxies (urban share, agricultural-land
share 2000), WDI + OWID, N = 162. Interactions estimable with HC1 CIs; sign is positive
(contrary to hypothesis) with wide CIs — see Phase 6 report.
