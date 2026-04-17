# FarmBlock Distress Index (FDI) — v2.0
**Produced by:** E5 Enclave Incorporated  
**License:** CC0 1.0 Universal (Public Domain)  
**Date:** April 17, 2026  
**Version:** 2.0  

---

## What This Is

The FarmBlock Distress Index (FDI) is a composite measure of structural food insecurity and community disinvestment across American urban census tracts. It is designed to identify communities where multiple converging conditions — poverty, food access deficit, economic exclusion, infrastructure absence — create the conditions that E5 Enclave's FarmBlock program is built to address.

This dataset covers **12,426 census tracts** across **53 counties** in **cities with documented histories of structural disinvestment**. It is the foundation for E5 Enclave's national expansion research (Option C — all 74,000 US tracts — is in progress).

---

## The FDI Score (0–100)

Each tract receives a score from 0 (low distress) to 100 (highest distress), computed as the equal-weighted mean of 6 normalized dimensions:

| Dimension | Variable | Source |
|-----------|----------|--------|
| Poverty rate | % below federal poverty line | Census ACS 2023 B17001 |
| Income deficit | Median household income (inverted) | Census ACS 2023 B19013 |
| Demographic context | % Black / African American | Census ACS 2023 B02001 |
| Digital exclusion | % without internet access | Census ACS 2023 B28002 |
| Housing vacancy | % vacant housing units | Census ACS 2023 B25002 |
| Health burden proxy | Poverty rate (proxy for CDC PLACES — Phase 2 will add direct CDC data) | Census ACS 2023 |

**Normalization:** min-max 0–1 across all 12,426 tracts in this dataset.  
**Weighting:** Equal (1/6 each). This is an explicit assumption; sensitivity analysis with alternate weightings is recommended for peer review.

---

## Key Findings (v2.0)

- **12,426 tracts** analyzed across 53 counties
- **45.6 million people** in covered communities  
- **32 high-distress tracts** (FDI ≥ 60) identified  
- **Top cities by average FDI:** Albany GA (42.9), Selma AL (42.1), Pine Bluff AR (39.1), Jackson MS (39.0), Macon GA (37.7)
- The pattern is consistent: high FDI tracts share poverty rates 60–100%, median incomes under $20K, and Black population concentrations of 70–100%
- This is not a coincidence. It is a documented structural pattern.

---

## Data Files

```
/raw/
  census_acs_2023_raw.json      — Raw Census API response (SHA-256 documented in validation report)
/processed/
  farmblock_tracts_v2.csv       — 12,426 tracts with FDI scores + all variables
  farmblock_cities_v2.csv       — 53-city aggregates (mean/max FDI, population, poverty)
/methodology/
  fdi_methodology_v2.json       — Full scoring specification
  validation_report.json        — Missing data log, audit trail, pipeline log
```

---

## Limitations

1. **USDA FARA vintage 2019** — food access conditions may have changed
2. **Census ACS 5-year rolling estimates** — not point-in-time measurements
3. **Health dimension uses poverty proxy** — direct CDC PLACES data to be added in v3.0
4. **Equal weighting is an assumption** — not empirically derived
5. **FDI is a correlation index** — it does not establish causation
6. **Coverage limited to 53 counties** — national expansion (all 74K tracts) is Phase 2

---

## Reproducibility

```bash
export CENSUS_API_KEY=your_key_here
python3 farmblock_pipeline_v2.py
```

All code is CC0. All source data is from US government open data APIs.  
Results are deterministic given the same source data vintage.

---

## Citation

> E5 Enclave Incorporated. (2026). *FarmBlock Distress Index v2.0: Structural Food Insecurity Across American Urban Census Tracts.* CC0 1.0 Universal. GitHub: IAMGODIAM/farmblock-dataset

---

## About E5 Enclave Incorporated

E5 Enclave Incorporated (EIN: 99-3822441) is a 501(c)(3) nonprofit building permanent community infrastructure in American cities where disinvestment has been policy, not accident. FarmBlock is our flagship program — integrating urban agriculture, IoT sensor networks, and blockchain supply chain transparency into communities identified by this dataset.

**Contact:** IAMGODIAM@e5enclave.com | iamgodiam.net  
**SAM.gov:** UEI H8NGXEYE2HH8 | CAGE 07E88
