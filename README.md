# FarmBlock Food Distress Index — Phase 2
**Published by:** E5 Enclave Incorporated | EIN: 99-3822441
**License:** CC0 1.0 Universal — Public Domain
**Version:** v2.0 | **DAG:** farmblock-phase2-complete-2026-0417
**Website:** iamgodiam.net

---

## IMPORTANT — RELEASE SCOPE

**This repository contains a pilot release of 24 top-distress counties** from a broader corpus of 1,200+ counties ingested across 17 target states.

The 24 counties published here represent the highest-distress slice of the Phase 2 ingested corpus. They are not a random sample — they are the priority tier for FarmBlock program deployment.

The full county corpus (all 3,222 US counties with ACS 5-Year data) is available in the BDI Raw Data Vault:
→ `github.com/IAMGODIAM/bdi-raw-data-vault` — `economic/tier3_county_economics_ACS5Y_2015-2022_RAW.json`

**For the canonical stack architecture, see [STACK.md](https://github.com/IAMGODIAM/bdi-raw-data-vault/blob/main/STACK.md)**

---

## WHAT THIS IS

The FarmBlock Food Distress Index (FDI) is a county-resolution composite dataset combining economic, demographic, and public health data to identify communities most vulnerable to food apartheid and structural disinvestment.

This is **Layer 3** of the IAMGODIAM data stack — the county-level publication layer.

---

## PUBLISHED DATA FILES

| File | Contents | Status |
|------|----------|--------|
| `farmblock_fdi_phase2.csv` | 24-county pilot release, FDI scored | ✅ Published |
| `farmblock_fdi_phase2.json` | Same 24 counties + methodology metadata | ✅ Published |
| `farmblock_fdi_phase3_scored.json` | Phase 3: 42 counties scored, top 20 detailed | ✅ Published |
| `processed/farmblock_cities_v2.csv` | City-level aggregates | ✅ Published |
| `methodology/fdi_methodology_v2.json` | Full scoring methodology | ✅ Published |

---

## DATA SOURCES

| Layer | Source | Vintage |
|-------|--------|---------|
| Economic | BLS Local Area Unemployment Statistics | 2025 |
| Demographic | US Census Bureau ACS 5-Year Estimates | 2022 |
| Health | CDC PLACES County Data | 2023 |

---

## FDI SCORE METHODOLOGY

Composite score 0–100. Higher = more distressed.

| Dimension | Weight | Metric |
|-----------|--------|--------|
| Poverty | 25% | ACS poverty rate |
| Health Burden | 25% | CDC diabetes + hypertension + obesity (normalized) |
| Digital Exclusion | 20% | % households no internet |
| Housing Vacancy | 15% | ACS vacancy rate |
| Black % (structural exposure proxy) | 15% | ACS % Black population |

**Note on `% Black` variable:** This is a structural exposure proxy — not a biological or causal variable. It captures geographic concentration of populations with documented disproportionate exposure to structural disinvestment, consistent with a 100-year federal data record. The index does not claim racial composition causes distress.

---

## TOP 10 MOST DISTRESSED COUNTIES (Phase 2 Pilot)

| Rank | County | State | FDI Score | Poverty | Black % | Hypertension % |
|------|--------|-------|-----------|---------|---------|----------------|
| 1 | Humphreys | MS | 87.25 | 35.0% | 80.0% | 51.7% |
| 2 | Holmes | MS | 86.40 | 41.2% | 83.0% | 54.1% |
| 3 | Claiborne | MS | 84.90 | 38.7% | 83.1% | 52.8% |
| 4 | Quitman | MS | 83.70 | 37.9% | 73.0% | 50.4% |
| 5 | Jefferson | MS | 82.10 | 40.1% | 79.0% | 53.2% |
| 6 | East Carroll | LA | 81.80 | 36.8% | 72.0% | 49.6% |
| 7 | Tensas | LA | 80.50 | 34.9% | 68.0% | 48.7% |
| 8 | Greene | AL | 79.90 | 33.1% | 81.8% | 51.1% |
| 9 | Sunflower | MS | 79.30 | 35.5% | 72.0% | 50.9% |
| 10 | Tunica | MS | 78.60 | 36.2% | 80.6% | 52.4% |

---

## CITATION

E5 Enclave Incorporated. (2026). *FarmBlock Food Distress Index Phase 2 — 24-County Pilot Release*.
GitHub. https://github.com/IAMGODIAM/farmblock-dataset | License: CC0 1.0 Universal.

---

*By Grace, perfect ways.*
