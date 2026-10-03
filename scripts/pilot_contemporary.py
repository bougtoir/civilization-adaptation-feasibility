#!/usr/bin/env python3
"""Contemporary-layer pilot.

Country panel built entirely from public APIs:
- OWID/Berkeley-Earth country temperature anomalies (env change)
- WDI urban share, agricultural-land share, GDPpc, agriculture value-added
  share (legacy proxies, controls, restructuring outcome)

Outcome: structural reallocation = decline in agriculture VA share 2000 -> 2021
(positive = more restructuring).
"""
import io, json, urllib.request
import numpy as np, pandas as pd

def wb(ind, date="2000:2022"):
    url = (f"https://api.worldbank.org/v2/country/all/indicator/{ind}"
           f"?format=json&per_page=20000&date={date}")
    data = json.load(urllib.request.urlopen(url, timeout=60))[1]
    df = pd.DataFrame(data)
    df = df[["countryiso3code", "date", "value"]].dropna()
    df["date"] = df["date"].astype(int)
    return df

out_dir = "data/raw/wb"
import os; os.makedirs(out_dir, exist_ok=True)

inds = {
    "urban_share": "SP.URB.TOTL.IN.ZS",
    "agland_share": "AG.LND.AGRI.ZS",
    "gdppc": "NY.GDP.PCAP.CD",
    "agva_share": "NV.AGR.TOTL.ZS",
}
frames = {}
for k, i in inds.items():
    df = wb(i)
    df.to_csv(f"{out_dir}/{k}.csv", index=False)
    frames[k] = df

tas = pd.read_csv("/tmp/annual-temperature-anomalies.csv")
tas.to_csv("data/raw/owid_temperature_anomaly.csv", index=False)

# --- variables ----------------------------------------------------------
def grab(k, iso, year):
    s = frames[k]
    r = s[(s.countryiso3code == iso) & (s.date == year)]
    return r.value.iloc[0] if len(r) else np.nan

isos = sorted(set(frames["agva_share"].countryiso3code) & set(tas.Code))
rows = []
for iso in isos:
    t = tas[tas.Code == iso]
    tanom = t[(t.Year >= 2011) & (t.Year <= 2021)]["Temperature anomaly"].mean()
    ag00, ag21 = grab("agva_share", iso, 2000), grab("agva_share", iso, 2021)
    rows.append({
        "iso": iso,
        "tanom_2011_21": tanom,
        "urban2000": grab("urban_share", iso, 2000),
        "agland2000": grab("agland_share", iso, 2000),
        "gdppc2000": grab("gdppc", iso, 2000),
        "agshare2000": ag00,
        "agshare2021": ag21,
        "realloc": (ag00 - ag21) if pd.notna(ag00) and pd.notna(ag21) else np.nan,
    })
df = pd.DataFrame(rows).dropna(subset=["tanom_2011_21", "realloc", "urban2000",
                                       "agland2000", "gdppc2000", "agshare2000"])
df["lngdp"] = np.log(df.gdppc2000)
df.to_csv("analysis/03_contemporary_pilot.csv", index=False)
print("N =", len(df))

import statsmodels.api as sm
def fit(y):
    X = df[["tanom_2011_21", "urban2000", "agland2000", "lngdp", "agshare2000"]].copy()
    X["tanomXurban"] = df.tanom_2011_21 * df.urban2000
    X["tanomXagland"] = df.tanom_2011_21 * df.agland2000
    X = sm.add_constant(X)
    m = sm.OLS(y, X).fit(cov_type="HC1")
    print(m.params[["tanom_2011_21", "urban2000", "agland2000", "tanomXurban", "tanomXagland"]])
    print("conf:\n", m.conf_int().loc[["tanomXurban", "tanomXagland"]])
    print("R2 =", round(m.rsquared, 3))
    return m

print("=== OLS realloc ~ dT + legacy + interactions ===")
m = fit(df.realloc)

# alternate legacy operationalization: electricity access? not pulled; use agland only as 2nd model
df2 = df.copy()
df2["legacy_urban"] = df2.urban2000
print("\n=== alternative: interaction with agland only ===")
X = df2[["tanom_2011_21", "agland2000", "lngdp", "agshare2000"]].copy()
X["tanomXagland"] = df2.tanom_2011_21 * df2.agland2000
m2 = sm.OLS(df2.realloc, sm.add_constant(X)).fit(cov_type="HC1")
print(m2.params[["tanom_2011_21", "agland2000", "tanomXagland"]])
print("conf:\n", m2.conf_int().loc[["tanomXagland"]])
print("R2 =", round(m2.rsquared, 3))
