#!/usr/bin/env python3
"""Pilot join for the historical layer.

CrisisDB consequences (169 crises) -> Seshat NGA -> Equinox complexity panel
-> PAGES 2k regional temperature anomaly.

Produces analysis/02_historical_pilot.csv plus a join-report printed to stdout.
This is a PIPELINE feasibility pilot, not the final study.
"""
import re
import pandas as pd
import numpy as np

ROOT = "data/raw"
EQ = f"{ROOT}/seshat/equinox/seshatdb-Equinox_Data-ed8f570/Equinox_on_GitHub_June9_2022.xlsx"

# --- 1. CrisisDB -----------------------------------------------------------
crisis = pd.read_csv(
    f"{ROOT}/crisisdb/CrisisConsequencesData_NavigatingPolycrisis_2023.03.csv",
    encoding="latin1")
crisis.columns = [c.strip() for c in crisis.columns]

ROMAN = {"I":1,"V":5,"X":10,"L":50,"C":100}
def roman(s):
    s=s.upper(); tot=0; prev=0
    for ch in s[::-1]:
        v=ROMAN[ch]
        tot += v if v>=prev else -v; prev=v
    return tot

def period_midyear(p):
    """Parse 'XIV c', 'II c bce', 'X - XI c', 'XVI - XVII c', '-V-III c' -> CE midpoint."""
    p = str(p).strip()
    bce = "bce" in p.lower() or p.startswith("-")
    nums = re.findall(r"[IVXL]+(?!\w)", p.replace("-", " "))
    if not nums:
        return np.nan
    cents = [roman(n) for n in nums if set(n) <= set("IVXL")]
    if not cents:
        return np.nan
    lo, hi = min(cents), max(cents)
    # 'XVII - XIV c' means descending range spanning centuries lo..hi
    mid_c = (lo + hi) / 2
    if bce:
        return -(mid_c - 0.5) * 100  # century X bce covers [-(X*100), -((X-1)*100))
    return (mid_c - 0.5) * 100

crisis["crisis_mid_ce"] = crisis["Crisis.Period"].apply(period_midyear)

# --- 2. Polity -> NGA (hand map; audited, conservative) --------------------
# Each keyword is matched case-insensitively against Polity.Name.
NGA_MAP = [
    (r"roman|\brome\b|habsburg|austro|austria|papal|lombard|ostro|spanish|spain", "Latium"),
    (r"france|french|valois|bourbon|caroling|meroving|napoleon|plantagenet|anglo-saxon|england|britain|victorian|bohemian", "Paris Basin"),
    (r"iceland|norway", "Iceland"),
    (r"crete|greece|aegean|mycen|byzantin|armenia|konya|hatti|lydia", "Crete"),
    (r"egypt|ptolema|saite|fatimid|ayyubid|mamluk|kushit|umayyad", "Upper Egypt"),
    (r"mali|songhai|wagadu|ghana empire", "Niger Inland Delta"),
    (r"ashanti|ghana|alaouite", "Ghanaian Coast"),
    (r"assyrian|sumer|akkad|babylon|abbasid|buyid|ilkhanat|seljuk|ottoman|saffarid|timurid|qajar|safavid|achae|parthia|seleucid|sassanid|khwarezmid|judea|israel|hasmone|phoenic|galilee|levant|neo-hittite", "Southern Mesopotamia"),
    (r"judea|israel|hasmone|phoenic|galilee|levant|neo-hittite|hatti|konya|lydia", "Galilee"),
    (r"yemen|qasimid|rasulid", "Yemeni Coastal Plain"),
    (r"kachi|indus|mauryan|satavahana|mughal|delhi sultanate|kushan|bactrian", "Kachi Plain"),
    (r"ganga|sunga|magadha", "Middle Ganga"),
    (r"deccan", "Deccan"),
    (r"garo", "Garo Hills"),
    (r"angkor|chenla|ayutthaya|rattanakosin|cambod", "Cambodian Basin"),
    (r"java|medang|mataram", "Central Java"),
    (r"kapuasi|iban|brooke", "Kapuasi Basin"),
    (r"shang|zhou|han|qin|song|ming|qing|sui|tang|yuan|jin|wei state|wei,|northern wei|later jin|khitan|liao|yellow river", "Middle Yellow River Valley"),
    (r"southern china hills|yunnan", "Southern China Hills"),
    (r"japan|heian|kamakura|ashikaga|tokugawa|asuka|yayoi|kansai|unification", "Kansai"),
    (r"sogdiana|chagatai|timur|bukhara|samarkand", "Sogdiana"),
    (r"orkhon|mongol|rouran|xianbei|uighur|turkic|khaganate|oirat|zunghar|huns|xiongnu|skyth|tocharian|kiev|moscow|russia|sakha|lena|golden horde", "Orkhon Valley"),
    (r"oaxaca|monte alban|rosario", "Valley of Oaxaca"),
    (r"mexico|aztec|toltec|teotihuacan|basin of mexico|united mexican|maya", "Basin of Mexico"),
    (r"cahokia|illinois|hohokam|chaco|bonito", "Cahokia"),
    (r"iroquois|finger lakes|antebellum us|reconstruction|us ", "Finger Lakes"),
    (r"inc[a|u]|cuzco|wari|tiwanaku|chimu", "Cuzco"),
    (r"colombia|tairona", "North Colombia"),
    (r"andes|ecuador|colonial lowland", "Lowland Andes"),
    (r"hawaii", "Big Island Hawaii"),
    (r"chuuk|truk", "Chuuk Islands"),
    (r"oro png|oro$|papua|new guinea", "Oro PNG"),
]
def to_nga(name):
    n = str(name).lower()
    for pat, nga in NGA_MAP:
        if re.search(pat, n):
            return nga
    return None

crisis["NGA"] = crisis["Polity.Name"].apply(to_nga)

# --- 3. Equinox legacy proxies ---------------------------------------------
sc = pd.read_excel(EQ, sheet_name="ImpSCDat")
sc = sc[["NGA","Time","Pop","Terr","Cap","Hier","Gov","Infra","Info","Money"]]

def legacy_at(nga, year):
    """Latest century row strictly before crisis year - at least 100 y lead."""
    sub = sc[(sc.NGA == nga) & (sc.Time <= year - 100)]
    if sub.empty:
        return pd.Series({"legacy_time": np.nan, "Infra": np.nan, "Hier": np.nan,
                          "Pop": np.nan, "Gov": np.nan})
    r = sub.sort_values("Time").iloc[-1]
    return pd.Series({"legacy_time": r.Time, "Infra": r.Infra, "Hier": r.Hier,
                      "Pop": r.Pop, "Gov": r.Gov})

# --- 4. PAGES 2k regional temperature --------------------------------------
p2k = pd.read_excel(f"{ROOT}/pages2k/DatabaseS2-Regional-Temperature-Reconstructions.xlsx",
                    sheet_name="PAGES2k recon's - annual", header=0)
# Each region occupies 4 columns: Year CE | Temp | Min | Max.
p2k.columns = [str(c) for c in p2k.columns]
p2k = p2k.iloc[1:].apply(pd.to_numeric, errors="coerce")
NGAS = pd.read_excel(EQ, sheet_name="NGAs")
def p2k_region(lat, lon):
    if -30 <= lon <= 60 and lat > 35: return "Europe"
    if lon < -30 and lat > 0: return "North America - Trees"
    if lon < -30 and lat <= 0: return "South America"
    if lat <= 0: return "Australasia"
    if lat > 60: return "Arctic"
    return "Asia"
NGAS["p2k_region"] = NGAS.apply(lambda r: p2k_region(r.Latitude, r.Longitude), axis=1)

def delta_T(region, year):
    """Mean regional annual anomaly over century before crisis minus the century
    before that. PAGES2k annual sheet: region column holds reconstruction."""
    if not isinstance(region, str) or pd.isna(year):
        return np.nan
    tempcol = region + ".1"
    if region not in p2k.columns or tempcol not in p2k.columns:
        return np.nan
    y = p2k[region]
    v = p2k[tempcol]
    a = v[(y >= year-100) & (y < year)].mean()
    b = v[(y >= year-200) & (y < year-100)].mean()
    if pd.isna(a) or pd.isna(b):
        return np.nan
    return a - b

nga_region = NGAS.set_index("NGA")["p2k_region"].to_dict()

# --- 5. Assemble ------------------------------------------------------------
out = crisis.copy()
leg = out.apply(lambda r: legacy_at(r.NGA, r.crisis_mid_ce) if pd.notna(r.crisis_mid_ce) and pd.notna(r.NGA) else
                pd.Series({"legacy_time":np.nan,"Infra":np.nan,"Hier":np.nan,"Pop":np.nan,"Gov":np.nan}),
                axis=1)
out = pd.concat([out, leg], axis=1)
out["p2k_region"] = out.NGA.map(nga_region)
out["delta_T_preceding"] = out.apply(lambda r: delta_T(r.p2k_region, r.crisis_mid_ce), axis=1)

out.to_csv("analysis/02_historical_pilot.csv", index=False)

n = len(out)
print(f"rows={n}")
print(f"year parsed: {out.crisis_mid_ce.notna().mean():.0%}")
print(f"NGA mapped:  {out.NGA.notna().mean():.0%}")
print(f"legacy joined (>=100y lead): {(out.Infra.notna()).mean():.0%}")
print(f"delta_T joined: {out.delta_T_preceding.notna().mean():.0%}")
both = out[out.Infra.notna() & out.delta_T_preceding.notna()]
print(f"full rows (legacy x env): {len(both)}")
print(out[out.NGA.isna()]['Polity.Name'].unique())
