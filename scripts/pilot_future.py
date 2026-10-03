#!/usr/bin/env python3
"""Future-counterfactual pilot (deliberately simple; documents model dependence).

V_retain(T)  = yield of dominant staple at temperature anomaly T
V_substitute = yield of best alternative crop at T, minus a switching-cost band

Method: per country, log-yield ~ country temperature anomaly linear response per
crop (country FE not needed - country-specific regression). T* solves
V_retain(T) = V_substitute(T) using each crop's fitted sensitivity, anchored to
the country's 2011-2021 mean yields. Switching cost is a SENSITIVITY PARAMETER
(class 3 per the audit), varied over {0, 10, 20}% - not estimated.
"""
import numpy as np, pandas as pd, statsmodels.api as sm

y = pd.read_csv("data/raw/owid_key_crop_yields.csv")
tas = pd.read_csv("/tmp/annual-temperature-anomalies.csv")

d = y.merge(tas[["Code", "Year", "Temperature anomaly"]],
            on=["Code", "Year"], how="inner")
crops = [c for c in y.columns if c not in ("Entity", "Code", "Year")]

rows = []
for (ent, code), g in d.groupby(["Entity", "Code"]):
    g = g.sort_values("Year")
    # dominant staple = crop with most non-missing recent observations x yield level
    recent = g[g.Year >= 2000]
    cov = {c: recent[c].notna().mean() for c in crops}
    cands = [c for c in crops if cov[c] >= 0.8]
    if len(cands) < 2:
        continue
    base = recent[[c for c in cands]].mean()
    dominant = base.idxmax()
    alt = base.drop(dominant).idxmax()
    def sens(c):
        gg = g[["Year", "Temperature anomaly", c]].dropna()
        gg = gg[gg[c] > 0]
        if len(gg) < 20:
            return np.nan
        X = sm.add_constant(gg["Temperature anomaly"].values)
        return sm.OLS(np.log(gg[c]), X).fit().params[1]
    b_dom, b_alt = sens(dominant), sens(alt)
    if np.isnan(b_dom) or np.isnan(b_alt):
        continue
    y0_dom, y0_alt = base[dominant], base[alt]
    t_now = recent["Temperature anomaly"].mean()
    def Tstar(switch_frac):
        # V_dom(T) = y0 * exp(b_dom * dT); substitute scaled by (1 - switch_frac)
        # crossing: b_dom*T = log((1-s)*y0_alt/y0_dom) + b_alt*T
        rhs = np.log((1 - switch_frac) * y0_alt / y0_dom)
        if abs(b_dom - b_alt) < 1e-6:
            return np.nan
        return rhs / (b_dom - b_alt)
    rows.append({"Entity": ent, "Code": code, "dominant": dominant,
                 "alt": alt, "b_dom": b_dom, "b_alt": b_alt,
                 "T_now": t_now,
                 "Tstar_s0": Tstar(0.0), "Tstar_s10": Tstar(0.1),
                 "Tstar_s20": Tstar(0.2),
                 "already_inferior_s0": np.log(y0_alt / y0_dom) > 0})

res = pd.DataFrame(rows)
res.to_csv("analysis/04_future_pilot.csv", index=False)
print("countries:", len(res))
for c in ["Tstar_s0", "Tstar_s10", "Tstar_s20"]:
    finite = res[(res[c] > 0) & (res[c] < 4)]
    print(f"{c}: T* in (0,4C] for {len(finite)} countries; "
          f"median {finite[c].median():.2f}; negative/inf for "
          f"{(res[c] <= 0).sum()}")
print("already inferior at s0:", res.already_inferior_s0.mean().round(3))
print(res[["Entity", "dominant", "alt", "b_dom", "b_alt",
           "Tstar_s0"]].head(10).to_string())
