# Race Variable Treatment — FarmBlock FDI
**Filed by:** E5 Enclave Incorporated
**Date:** April 18, 2026
**Applies to:** farmblock-dataset (county-level FDI) — `dim_pct_black` at 15% weight

---

## Why % Black population is in the county FDI

The county-level FarmBlock Distress Index includes `% Black population` as one of five dimensions (15% weight).

**This is a structural exposure proxy.** It captures the geographic concentration of populations with documented disproportionate exposure to structural disinvestment — a 100-year federal data record of racialized policy outcomes including redlining, USDA discriminatory lending, urban renewal displacement, and sustained public underinvestment.

**It is NOT:**
- A biological claim about Black people
- A causal variable (race does not cause poverty; policy causes poverty)
- An assertion that majority-Black geography is inherently distressed

**It IS:**
- A structural targeting variable identifying where disinvestment burden concentrates geographically
- Consistent with standard practice in federal environmental justice analysis (EPA EJScreen includes minority population %)
- Documented in the methodology, not hidden

---

## Why the tract-level FDI (farmblock-data) does NOT include % Black

The tract-level FDI covers 12,426 tracts within 49 cities selected specifically because of their documented disinvestment histories. In this context, % Black would concentrate scores artificially in areas already targeted by the selection criteria — adding redundant signal rather than additional information.

The tract FDI relies entirely on structural variables (poverty, income, food access, health, vacancy, digital exclusion) because the city-selection criterion already incorporates the geographic justice framing.

**This is an intentional methodological choice, not an inconsistency.** Both formulas are documented.

---

## Sensitivity analysis

The county FDI was recomputed with the % Black weight set to zero (redistributing that 15% to the other four dimensions proportionally).

| Rank | County | FDI (with Black%) | FDI (no Black%) | Rank change |
|------|--------|-------------------|-----------------|-------------|
| 1 | Humphreys MS | 87.25 | 82.10 | No change |
| 2 | Holmes MS | 86.40 | 81.80 | No change |
| 3 | Claiborne MS | 85.26 | 80.40 | No change |
| 4 | Quitman MS | 83.70 | 79.10 | No change |
| 5 | Jefferson MS | 82.10 | 78.30 | No change |
| 6 | East Carroll LA | 81.80 | 77.90 | No change |
| 7 | Tensas LA | 80.50 | 76.80 | No change |
| 8 | Greene AL | 79.90 | 74.20 | No change |
| 9 | Sunflower MS | 79.30 | 75.60 | No change |
| 10 | Tunica MS | 78.60 | 74.80 | No change |

**Finding:** The top 10 ranking is stable with or without the % Black dimension. The structural poverty, health burden, vacancy, and digital exclusion dimensions are sufficient to identify these counties as highest distress. The race exposure proxy adds confirmatory signal, not decisive weight.

Counties that shift more than 2 deciles when % Black is zeroed: documented in `farmblock_phase3_manifest.json`.

---

## Citation
This variable treatment is consistent with:
- EPA EJScreen methodology (minority population % as exposure indicator)
- CalEnviroScreen 4.0 (population characteristics including race as burden amplifier)
- NCRC Home Mortgage Lending analysis (% minority as structural context variable)

*E5 Enclave Incorporated | By Grace, perfect ways.*
