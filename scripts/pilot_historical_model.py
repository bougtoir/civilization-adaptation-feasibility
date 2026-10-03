#!/usr/bin/env python3
"""Historical interaction pilot on the joined dataset.

Outcome: decline coded 1 vs 0 (U/uncertain rows dropped).
Model: logit decline ~ delta_T + Infra + delta_T x Infra + century,
cluster-robust SE by NGA. Pilot only - not causal.
"""
import numpy as np, pandas as pd, statsmodels.api as sm

d = pd.read_csv("analysis/02_historical_pilot.csv")
d["decline"] = pd.to_numeric(d["decline"], errors="coerce")
d = d[d["decline"].isin([0, 1])].copy()
d["decline"] = d["decline"].astype(float)
full = d[d.Infra.notna() & d.delta_T_preceding.notna()].copy()
full["century"] = (full.crisis_mid_ce / 100).round()
print("pilot N =", len(full), "| NGAs =", full.NGA.nunique(),
      "| decline=1 share =", round(full.decline.mean(), 3))

def logit(df, z=True):
    X = df[["delta_T_preceding", "Infra"]].copy()
    if z:
        X["delta_T_preceding"] = (X.delta_T_preceding - X.delta_T_preceding.mean()) / X.delta_T_preceding.std()
        X["Infra"] = (X.Infra - X.Infra.mean()) / X.Infra.std()
    X["dTxInfra"] = X.delta_T_preceding * X.Infra
    X["century"] = (df.crisis_mid_ce / 1000)
    X = sm.add_constant(X)
    m = sm.Logit(df.decline, X).fit(disp=0, cov_type="cluster",
                                  cov_kwds={"groups": df.NGA})
    return m

m = logit(full)
print(m.params[["delta_T_preceding", "Infra", "dTxInfra", "century"]])
print("95% CI dTxInfra:", m.conf_int().loc["dTxInfra"].tolist())

# alternate operationalizations: legacy = Hier; outcome = severity>=5
alt = full.copy(); alt["Infra"] = alt["Hier"]
m2 = logit(alt)
print("\nalt legacy (Hier): dTxInfra =", round(m2.params["dTxInfra"], 3),
      m2.conf_int().loc["dTxInfra"].tolist())
full2 = full.copy(); full2["decline"] = (full2.Severity >= 5).astype(int)
m3 = logit(full2)
print("alt outcome (Severity>=5): dTxInfra =", round(m3.params["dTxInfra"], 3),
      m3.conf_int().loc["dTxInfra"].tolist())

# Moran-style diagnostic: mean residual correlation within NGA
full["resid"] = m.resid_response
print("\nmean |NGA|-share of crises:", full.NGA.value_counts(normalize=True).head(5).round(2).to_dict())
