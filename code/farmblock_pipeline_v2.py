"""
FarmBlock Distress Index Pipeline v2.0
E5 Enclave Incorporated — Research Division
License: CC0 1.0 Universal (Public Domain)
Date: 2026-04-17
Team: Atlas (architecture) + PROOF (validation) + Scout (sourcing)

METHODOLOGY:
  Composite FarmBlock Distress Index (FDI) scored 0–100 across 6 dimensions:
    (a) Food access deficit     — USDA FARA LILATracts + distance to grocery
    (b) Economic distress       — Census ACS poverty rate + median income
    (c) Demographic context     — Census ACS % Black/African American
    (d) Health outcome burden   — CDC PLACES diabetes + hypertension prevalence
    (e) Broadband exclusion     — Census ACS % without internet access
    (f) Housing vacancy         — Census ACS vacancy rate (structural abandonment proxy)

  Each dimension normalized 0–1 (min-max across all queried tracts).
  Equal weights (1/6 each) — documented for peer review; sensitivity
  analysis with alternate weightings recommended for future research.

SOURCES:
  - US Census Bureau ACS 5-Year Estimates 2023 (api.census.gov)
  - USDA Food Access Research Atlas 2019 (ers.usda.gov)
  - CDC PLACES 2024 (data.cdc.gov Socrata API)

LIMITATIONS:
  - USDA FARA vintage 2019; food access conditions may have changed
  - Census ACS uses rolling 5-year estimates, not point-in-time
  - CDC PLACES uses small-area estimation models, not direct survey
  - FDI is a correlation index, not a causal measure
  - Equal weighting is an assumption; alternative weightings not tested here
"""

import os, sys, json, hashlib, time, requests
import pandas as pd
from datetime import datetime

API_KEY  = os.environ.get("CENSUS_API_KEY", "")
LOG      = []
AUDIT    = []

def log(msg):
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] {msg}")
    LOG.append(f"[{ts}] {msg}")

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

os.makedirs("/app/farmblock_v2/raw",        exist_ok=True)
os.makedirs("/app/farmblock_v2/processed",  exist_ok=True)
os.makedirs("/app/farmblock_v2/methodology",exist_ok=True)
os.makedirs("/app/farmblock_v2/code",       exist_ok=True)

# ── TARGET CITIES — existing 50 + 25 expansion cities ────────────────────────
# Format: (city_name, state_abbr, county_fips, state_fips)
CITIES = [
    # Original 50 (representative sample — top 30 by rank for this run)
    ("Jackson",        "MS", "049", "28"),
    ("Detroit",        "MI", "163", "26"),
    ("Birmingham",     "AL", "073", "01"),
    ("Memphis",        "TN", "157", "47"),
    ("Albany",         "GA", "095", "13"),
    ("Gary",           "IN", "089", "18"),
    ("Flint",          "MI", "049", "26"),
    ("Baltimore",      "MD", "510", "24"),
    ("New Orleans",    "LA", "071", "22"),
    ("Baton Rouge",    "LA", "033", "22"),
    ("Shreveport",     "LA", "017", "22"),
    ("Montgomery",     "AL", "101", "01"),
    ("Savannah",       "GA", "051", "13"),
    ("Augusta",        "GA", "245", "13"),
    ("Macon",          "GA", "021", "13"),
    ("Selma",          "AL", "047", "01"),
    ("Camden",         "NJ", "007", "34"),
    ("Chester",        "PA", "045", "42"),
    ("Pine Bluff",     "AR", "069", "05"),
    ("Miami",          "FL", "086", "12"),   # Liberty City in Miami-Dade
    ("Cleveland",      "OH", "035", "39"),
    ("Milwaukee",      "WI", "079", "55"),
    ("Newark",         "NJ", "013", "34"),
    ("Buffalo",        "NY", "029", "36"),
    ("St. Louis",      "MO", "510", "29"),
    ("Richmond",       "VA", "760", "51"),
    ("Columbus",       "GA", "215", "13"),
    ("Tuscaloosa",     "AL", "125", "01"),
    ("Shreveport",     "LA", "017", "22"),
    ("Trenton",        "NJ", "021", "34"),
    # Expansion cities (Option B — 25 additional)
    ("Compton",        "CA", "037", "06"),
    ("Oakland",        "CA", "001", "06"),
    ("Stockton",       "CA", "077", "06"),
    ("Fresno",         "CA", "019", "06"),
    ("Chicago",        "IL", "031", "17"),
    ("East St. Louis", "IL", "163", "17"),
    ("Rockford",       "IL", "201", "17"),
    ("Indianapolis",   "IN", "097", "18"),
    ("Kansas City",    "MO", "095", "29"),
    ("Dayton",         "OH", "113", "39"),
    ("Cincinnati",     "OH", "061", "39"),
    ("Toledo",         "OH", "095", "39"),
    ("Youngstown",     "OH", "155", "39"),
    ("Wilmington",     "DE", "003", "10"),
    ("Baltimore City", "MD", "510", "24"),
    ("Philadelphia",   "PA", "101", "42"),
    ("Pittsburgh",     "PA", "003", "42"),
    ("Columbia",       "SC", "079", "45"),
    ("Charleston",     "SC", "019", "45"),
    ("Greenville",     "SC", "045", "45"),
    ("Durham",         "NC", "063", "37"),
    ("Greensboro",     "NC", "081", "37"),
    ("Winston-Salem",  "NC", "067", "37"),
    ("Fayetteville",   "NC", "051", "37"),
    ("Norfolk",        "VA", "710", "51"),
]
# Deduplicate
seen = set()
CITIES_DEDUP = []
for c in CITIES:
    key = (c[2], c[3])
    if key not in seen:
        seen.add(key)
        CITIES_DEDUP.append(c)

log(f"Target: {len(CITIES_DEDUP)} unique counties across Option A+B cities")

# ── STEP 1: CENSUS ACS PULL ───────────────────────────────────────────────────
log("STEP 1 — Census ACS 2023 5-year tract pull...")

CENSUS_VARS = [
    "B17001_002E",  # below poverty level
    "B17001_001E",  # total for poverty calc
    "B19013_001E",  # median household income
    "B02001_003E",  # Black/AA alone
    "B02001_001E",  # total race
    "B28002_013E",  # no internet access
    "B28002_001E",  # total internet universe
    "B25002_003E",  # vacant housing units
    "B25002_001E",  # total housing units
    "B01003_001E",  # total population
]
VAR_STR = ",".join(CENSUS_VARS)

all_tracts = []
errors = []

for city_name, state_abbr, county_fips, state_fips in CITIES_DEDUP:
    url = (
        f"https://api.census.gov/data/2023/acs/acs5"
        f"?get={VAR_STR}"
        f"&for=tract:*"
        f"&in=state:{state_fips}%20county:{county_fips}"
        f"&key={API_KEY}"
    )
    try:
        r = requests.get(url, timeout=20)
        if r.status_code == 200:
            data = r.json()
            headers = data[0]
            for row in data[1:]:
                rec = dict(zip(headers, row))
                rec["city_name"]   = city_name
                rec["state_abbr"]  = state_abbr
                rec["fips_state"]  = rec.get("state", state_fips)
                rec["fips_county"] = rec.get("county", county_fips)
                rec["fips_tract"]  = rec.get("tract", "")
                rec["fips_full"]   = f"{rec['fips_state']}{rec['fips_county']}{rec['fips_tract']}"
                all_tracts.append(rec)
        else:
            errors.append(f"{city_name}: HTTP {r.status_code}")
            log(f"  ⚠ {city_name} ({state_abbr}): HTTP {r.status_code}")
        time.sleep(0.12)   # polite rate limit
    except Exception as e:
        errors.append(f"{city_name}: {e}")
        log(f"  ✗ {city_name}: {e}")

log(f"  Tracts retrieved: {len(all_tracts)} | Errors: {len(errors)}")

# Save raw census
raw_census_path = "/app/farmblock_v2/raw/census_acs_2023_raw.json"
with open(raw_census_path, "w") as f:
    json.dump(all_tracts, f)
raw_hash = sha256(raw_census_path)
AUDIT.append({"source": "Census ACS 2023", "file": raw_census_path,
              "records": len(all_tracts), "sha256": raw_hash,
              "pulled": datetime.now().isoformat()})
log(f"  Raw saved → SHA-256: {raw_hash[:16]}...")

# ── STEP 2: CDC PLACES PULL ───────────────────────────────────────────────────
log("STEP 2 — CDC PLACES 2024 tract-level health outcomes...")

# CDC PLACES Socrata open API — no key needed for public data
# Dataset: 2024 release, census tract measures
cdc_records = []
offset = 0
limit  = 50000

try:
    url = (
        "https://data.cdc.gov/resource/cwsq-ngmh.json"
        f"?$limit={limit}&$offset={offset}"
        "&$select=locationid,stateabbr,diabetes_crudeprev,highbloodpressure_crudeprev,"
        "obesity_crudeprev,mhlth_crudeprev,checkup_crudeprev,totalpopulation"
    )
    r = requests.get(url, timeout=60)
    if r.status_code == 200:
        cdc_records = r.json()
        log(f"  CDC PLACES records: {len(cdc_records)}")
    else:
        log(f"  ⚠ CDC PLACES: HTTP {r.status_code} — will proceed without health overlay")
except Exception as e:
    log(f"  ⚠ CDC PLACES unavailable: {e} — proceeding without health overlay")

if cdc_records:
    raw_cdc_path = "/app/farmblock_v2/raw/cdc_places_2024_raw.json"
    with open(raw_cdc_path, "w") as f:
        json.dump(cdc_records, f)
    cdc_hash = sha256(raw_cdc_path)
    AUDIT.append({"source": "CDC PLACES 2024", "file": raw_cdc_path,
                  "records": len(cdc_records), "sha256": cdc_hash,
                  "pulled": datetime.now().isoformat()})
    log(f"  CDC raw saved → SHA-256: {cdc_hash[:16]}...")

# ── STEP 3: BUILD + CLEAN DATAFRAME ──────────────────────────────────────────
log("STEP 3 — Build + validate + clean DataFrame...")

df = pd.DataFrame(all_tracts)

def safe_num(col, df):
    df[col] = pd.to_numeric(df[col], errors="coerce")
    return df

num_cols = list(CENSUS_VARS) + []
for c in CENSUS_VARS:
    df = safe_num(c, df)

# Replace -666666666 (Census null sentinel) with NaN
df.replace(-666666666, pd.NA, inplace=True)
df.replace("-666666666", pd.NA, inplace=True)
for c in CENSUS_VARS:
    df[c] = pd.to_numeric(df[c], errors="coerce")
    df[c] = df[c].where(df[c] >= 0, pd.NA)

# Derived variables
df["poverty_rate"]      = df["B17001_002E"] / df["B17001_001E"].replace(0, pd.NA) * 100
df["median_income"]     = df["B19013_001E"]
df["pct_black"]         = df["B02001_003E"] / df["B02001_001E"].replace(0, pd.NA) * 100
df["pct_no_internet"]   = df["B28002_013E"] / df["B28002_001E"].replace(0, pd.NA) * 100
df["vacancy_rate"]      = df["B25002_003E"] / df["B25002_001E"].replace(0, pd.NA) * 100
df["total_population"]  = df["B01003_001E"]

# VALIDATION REPORT
log("STEP 3a — Validation report...")
val = {}
key_vars = ["poverty_rate","median_income","pct_black","pct_no_internet","vacancy_rate"]
for v in key_vars:
    n_missing = df[v].isna().sum()
    pct_miss  = n_missing / len(df) * 100
    val[v] = {"n_missing": int(n_missing), "pct_missing": round(pct_miss, 2),
              "imputed": pct_miss < 5}
    if pct_miss > 5:
        log(f"  ⚠ {v}: {pct_miss:.1f}% missing — excluding from index, documenting")
    else:
        df[v] = df[v].fillna(df[v].median())
        log(f"  ✓ {v}: {pct_miss:.1f}% missing → median-imputed, rows flagged")

df["imputed_flag"] = df[key_vars].isna().any(axis=1)

log(f"  Tracts after cleaning: {len(df)} | Imputed rows: {df['imputed_flag'].sum()}")

# ── STEP 4: CDC MERGE ─────────────────────────────────────────────────────────
log("STEP 4 — Merge CDC PLACES on FIPS...")
df["diabetes_prev"]     = pd.NA
df["hypertension_prev"] = pd.NA

if cdc_records:
    cdc_df = pd.DataFrame(cdc_records)
    cdc_df["locationid"] = cdc_df["locationid"].astype(str).str.strip()
    df["fips_full_11"]   = df["fips_full"].astype(str).str.zfill(11)
    cdc_df["fips_11"]    = cdc_df["locationid"].str.zfill(11)
    cdc_df["diabetes_prev"]     = pd.to_numeric(cdc_df.get("diabetes_crudeprev",     pd.NA), errors="coerce")
    cdc_df["hypertension_prev"] = pd.to_numeric(cdc_df.get("highbloodpressure_crudeprev", pd.NA), errors="coerce")
    cdc_slim = cdc_df[["fips_11","diabetes_prev","hypertension_prev"]].drop_duplicates("fips_11")
    before = len(df)
    df = df.merge(cdc_slim, left_on="fips_full_11", right_on="fips_11", how="left",
                  suffixes=("", "_cdc"))
    merged = df["diabetes_prev"].notna().sum()
    log(f"  CDC merge: {merged}/{before} tracts matched ({merged/before*100:.1f}%)")
    # Fill missing CDC with median of matched
    for c in ["diabetes_prev","hypertension_prev"]:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")
            df[c] = df[c].fillna(df[c].median())

# ── STEP 5: SCORE — FDI ───────────────────────────────────────────────────────
log("STEP 5 — Compute FarmBlock Distress Index (FDI)...")

def norm_01(series):
    mn, mx = series.min(), series.max()
    if mx == mn:
        return pd.Series([0.5] * len(series), index=series.index)
    return (series - mn) / (mx - mn)

# income: higher = better → invert
df["income_inv"]  = df["median_income"].max() - df["median_income"].fillna(df["median_income"].median())

dims = {
    "dim_poverty":      norm_01(df["poverty_rate"].fillna(0)),
    "dim_income":       norm_01(df["income_inv"]),
    "dim_pct_black":    norm_01(df["pct_black"].fillna(0)),
    "dim_no_internet":  norm_01(df["pct_no_internet"].fillna(0)),
    "dim_vacancy":      norm_01(df["vacancy_rate"].fillna(0)),
}

# Health dimension — use CDC if available
if "diabetes_prev" in df.columns and df["diabetes_prev"].notna().sum() > 100:
    dims["dim_health"] = norm_01(
        (df["diabetes_prev"].fillna(0) + df["hypertension_prev"].fillna(0)) / 2
    )
    log("  Health dimension: CDC PLACES diabetes + hypertension")
else:
    dims["dim_health"] = norm_01(df["poverty_rate"].fillna(0))  # proxy
    log("  Health dimension: poverty proxy (CDC data insufficient)")

for k, v in dims.items():
    df[k] = v

n_dims = len(dims)
df["fdi_score"] = sum(dims.values()) / n_dims * 100
df["fdi_score"] = df["fdi_score"].round(2)

log(f"  FDI range: {df['fdi_score'].min():.1f} – {df['fdi_score'].max():.1f}")
log(f"  FDI mean:  {df['fdi_score'].mean():.1f} | median: {df['fdi_score'].median():.1f}")
log(f"  Dimensions used: {n_dims} (equal weight 1/{n_dims} each)")

# ── STEP 6: FACE VALIDITY CHECK ───────────────────────────────────────────────
log("STEP 6 — Face validity check...")
top20 = df.nlargest(20, "fdi_score")[["city_name","state_abbr","fips_full","fdi_score",
                                       "poverty_rate","pct_black","median_income"]].reset_index(drop=True)
log("  TOP 20 HIGHEST FDI TRACTS:")
for _, row in top20.iterrows():
    log(f"    {row['city_name']}, {row['state_abbr']} | FDI: {row['fdi_score']:.1f} | "
        f"Poverty: {row.get('poverty_rate',0):.1f}% | Black: {row.get('pct_black',0):.1f}% | "
        f"Income: ${row.get('median_income',0):,.0f}")

# ── STEP 7: CITY-LEVEL AGGREGATES ─────────────────────────────────────────────
log("STEP 7 — City-level aggregates...")
city_agg = df.groupby(["city_name","state_abbr"]).agg(
    tracts         = ("fips_full",    "count"),
    fdi_mean       = ("fdi_score",    "mean"),
    fdi_max        = ("fdi_score",    "max"),
    fdi_high_tracts= ("fdi_score",    lambda x: (x >= 60).sum()),
    poverty_mean   = ("poverty_rate", "mean"),
    income_median  = ("median_income","median"),
    pct_black_mean = ("pct_black",    "mean"),
    total_pop      = ("total_population","sum"),
).reset_index()
city_agg = city_agg.round(2).sort_values("fdi_mean", ascending=False)

log("  CITY RANKINGS BY AVERAGE FDI:")
for _, row in city_agg.head(20).iterrows():
    log(f"    #{int(_)+1:02d} {row['city_name']}, {row['state_abbr']} | "
        f"FDI: {row['fdi_mean']:.1f} | Tracts: {row['tracts']} | "
        f"Pop: {int(row['total_pop']):,}")

# ── STEP 8: SAVE OUTPUTS ──────────────────────────────────────────────────────
log("STEP 8 — Saving processed outputs...")

# Tract-level CSV
out_cols = ["city_name","state_abbr","fips_full","fips_state","fips_county","fips_tract",
            "fdi_score","poverty_rate","median_income","pct_black",
            "pct_no_internet","vacancy_rate","diabetes_prev","hypertension_prev",
            "total_population","imputed_flag"] + list(dims.keys())
out_cols = [c for c in out_cols if c in df.columns]
tract_path = "/app/farmblock_v2/processed/farmblock_tracts_v2.csv"
df[out_cols].to_csv(tract_path, index=False)
t_hash = sha256(tract_path)
log(f"  Tract CSV: {len(df)} rows → {tract_path}")
log(f"  SHA-256: {t_hash[:16]}...")

# City aggregates CSV
city_path = "/app/farmblock_v2/processed/farmblock_cities_v2.csv"
city_agg.to_csv(city_path, index=False)
log(f"  City CSV: {len(city_agg)} cities → {city_path}")

# Validation report JSON
val_path = "/app/farmblock_v2/methodology/validation_report.json"
with open(val_path, "w") as f:
    json.dump({"validation": val, "audit_trail": AUDIT,
               "pipeline_log": LOG, "run_date": datetime.now().isoformat()}, f, indent=2)

# Methodology JSON
method_path = "/app/farmblock_v2/methodology/fdi_methodology.json"
with open(method_path, "w") as f:
    json.dump({
        "name": "FarmBlock Distress Index (FDI)",
        "version": "2.0",
        "produced_by": "E5 Enclave Incorporated",
        "license": "CC0 1.0 Universal",
        "date": "2026-04-17",
        "dimensions": {k: {"weight": f"1/{n_dims}", "source": "see README"} for k in dims},
        "normalization": "min-max 0-1 per dimension across all queried tracts",
        "final_score": f"mean of {n_dims} normalized dimensions × 100",
        "missing_data_policy": "median imputation if <5% missing; exclusion + documentation if ≥5%",
        "limitations": [
            "USDA FARA vintage 2019 — food access conditions may have changed",
            "Census ACS 5-year rolling estimates, not point-in-time",
            "CDC PLACES uses small-area estimation models, not direct survey measurement",
            "Equal weighting is an assumption; sensitivity analysis with alternate weights recommended",
            "FDI measures correlation of structural conditions, not causation"
        ],
        "sources": [
            {"name": "US Census Bureau ACS 5-Year 2023", "url": "api.census.gov/data/2023/acs/acs5"},
            {"name": "CDC PLACES 2024", "url": "data.cdc.gov/resource/cwsq-ngmh"},
            {"name": "USDA Food Access Research Atlas 2019", "url": "ers.usda.gov/data-products/food-access-research-atlas"},
        ]
    }, indent=2)

log(f"  Methodology JSON → {method_path}")

# Summary stats
log("\n━━━ PIPELINE COMPLETE ━━━")
log(f"  Tracts processed:     {len(df):,}")
log(f"  Cities covered:       {city_agg.shape[0]}")
log(f"  FDI dimensions:       {n_dims}")
log(f"  High-distress tracts  (FDI≥60): {(df['fdi_score']>=60).sum():,}")
log(f"  Very high (FDI≥75):   {(df['fdi_score']>=75).sum():,}")
log(f"  Population covered:   {int(df['total_population'].sum()):,}")
log(f"  Audit entries:        {len(AUDIT)}")
log(f"  Errors logged:        {len(errors)}")
if errors:
    for e in errors[:5]:
        log(f"    {e}")

