# FarmBlock Food Distress Index — Phase 2
**Published by:** E5 Enclave Incorporated | EIN: 99-3822441  
**License:** CC0 1.0 Universal — Public Domain  
**Version:** v2.0 | **DAG:** farmblock-phase2-complete-2026-0417  
**Website:** iamgodiam.net  

---

## What This Is

The FarmBlock Food Distress Index (FDI) is the first county-resolution composite dataset 
combining economic, demographic, and public health data to identify communities most 
vulnerable to food apartheid and structural disinvestment.

Phase 2 covers **17 target states** with ~1,200 counties across three data layers.

---

## Data Sources

| Layer | Source | Vintage |
|-------|--------|---------|
| Economic | BLS Local Area Unemployment Statistics | 2025 |
| Demographic | US Census Bureau ACS 5-Year Estimates | 2022 |
| Health | CDC PLACES County Data | 2023 |

---

## FDI Score Methodology

Composite score 0–100. Higher = more distressed.

| Dimension | Weight | Metric |
|-----------|--------|--------|
| Poverty | 25% | ACS poverty rate |
| Health Burden | 25% | CDC diabetes + hypertension + obesity (normalized) |
| Digital Exclusion | 20% | % households no internet |
| Housing Vacancy | 15% | ACS vacancy rate |
| Black % (exposure proxy) | 15% | ACS % Black population |

---

## Top 10 Most Distressed Counties (Phase 2)

| Rank | County | State | FDI Score | Poverty | Black% | HTN% |
|------|--------|-------|-----------|---------|--------|------|
| 1 | Humphreys | MS | 87.25 | 35.0% | 80.0% | 51.7% |
| 2 | Claiborne | MS | 85.26 | 35.0% | 83.0% | 50.0% |
| 3 | Sunflower | MS | 78.34 | 32.0% | 72.0% | 48.0% |
| 4 | Alexander | IL | 77.38 | 21.4% | 33.2% | 47.9% |
| 5 | Amite | MS | 70.86 | 27.1% | 40.2% | 43.2% |
| 6 | Hempstead | LA | 68.99 | 28.0% | 45.0% | 46.2% |
| 7 | Adams | MS | 68.31 | 27.2% | 53.4% | 51.7% |
| 8 | Barbour | AL | 65.68 | 24.2% | 46.9% | 46.4% |
| 9 | Ashley | AR | 59.55 | 23.3% | 24.8% | 41.4% |
| 10 | Gadsden | FL | 57.98 | 22.0% | 55.0% | 40.0% |

---

## Key Findings

- **Humphreys County, MS** (FDI 87.2): 80% Black, 35% poverty, 51.7% hypertension — highest composite distress
- **Alexander County, IL** (FDI 77.4): 38% no internet + 42% vacant housing = structural collapse signature  
- **The Bronx, NY** (FDI 56.0): Urban Black poverty carries comparable health burden to rural Deep South
- **State data masks county reality**: Alabama = 2.7% state unemployment, but Barbour County = 24.2% poverty
- **Hypertension is the dominant signal**: high-distress counties average 46.9% vs. 32% national baseline

> *"In Claiborne County, Mississippi — 83% Black, 35% poverty — the hypertension rate is 50%.  
> That is not a medical problem. That is a structural problem. FarmBlock maps it. FarmBlock targets it."*

---

## Files

- `farmblock_fdi_phase2.json` — Full scored dataset with metadata
- `farmblock_fdi_phase2.csv` — Flat CSV for analysis

---

## Phase 3

Full nation (51 jurisdictions, 3,144 counties) — in progress.

---

## Citation

> E5 Enclave Incorporated. (2026). *FarmBlock Food Distress Index, Phase 2* (v2.0) [Dataset].  
> CC0 1.0 Universal. https://github.com/IAMGODIAM/farmblock-dataset
