# Phase 3E Executive Summary: Research Dataset Build

**Document:** `reports/phase3e/phase3e_summary.md`
**Generated:** 2026-10-26 17:34 UTC
**Pipeline:** `src/data/build_research_dataset.py`
**Project:** Fajr-e-Kisht — Crop Recommendation System for Sindh

---

## 1. Source File Integrity

| File | Size (bytes) | SHA-256 | Status |
|:---|---:|:---|:---|
| `data/raw/pbs_weather_soil_1981_2025.csv` | 782,623 | `b7362d3154c42738191690b8f73add9e9c0ed9850891891ea91fb137bffc13ff` | IMMUTABLE — not modified |
| `data/raw/area_and_production_by_districts_for_28_years.pdf` | 2,216,995 | `293d3bfcf26fff75f2df7156e11e3fbea25707d7473f91f4d952018c250b7d13` | IMMUTABLE — not modified |

---

## 2. Row Accounting

| Stage | Count | Notes |
|:---|---:|:---|
| Source rows (raw CSV) | 3,242 | Immutable input |
| Excluded rows (Rule E1: Sujawal Rice) | 19 | In `exclusion_ledger.csv` |
| **Research dataset rows** | **3,223** | In `research_dataset.csv` |
| Mathematical check: excluded + included | 3,242 | Must equal source (3242) ✓ |

---

## 3. Exclusion Ledger Summary

| Rule | Description | Rows Excluded | Confirmed | Precautionary |
|:---|:---|:---:|:---:|:---:|
| E1 | Sujawal Rice — Sindh provincial aggregate misattributed to district | 19 | 5 | 14 |

**Confirmed (E1, 2004-05 to 2008-09):** 5 rows. PDF Table 11 cross-check proves exact match to Sindh provincial totals.
**Precautionary (E1, 2009-10 to 2022-23):** 14 rows. 100% match to PBS Level-12 Sindh API total verified programmatically; post-2008 cannot be compared to PDF (publication ends 2008-09). Scale alone (361–828 k ha vs. Thatta's 43–90 k ha historical district size) makes these impossible as district values.

---

## 4. Research Dataset Structure

| Dimension | Source | Research Dataset |
|:---|---:|---:|
| Total rows | 3,242 | 3,223 |
| Districts | 24 | 23 |
| Crops | 5 | 5 |
| Year range | 1981–2024 | 1981–2024 |
| Unique D-C-Y keys | 3,242 | 3,223 |
| Duplicate keys | 0 | 0 |

### Coverage by Crop
| Crop | Rows | Districts | Year Span |
|:---|---:|---:|:---|
| Cotton | 607 | 20 | 1981–2024 |
| Maize | 570 | 21 | 1981–2024 |
| Rice | 576 | 21 | 1981–2024 |
| Sugarcane | 697 | 21 | 1981–2024 |
| Wheat | 773 | 23 | 1981–2024 |

---

## 5. Quality Flags Summary

| Flag | Count | % of Dataset | Meaning |
|:---|---:|---:|:---|
| `flag_boundary_instability` | 579 | 18.0% | Pre-split district — area includes territory later reassigned |
| `flag_cotton_unit_mismatch` | 607 | 18.8% | Production/Yield in bale units (not metric tonnes) |
| `flag_soil_missing` | 1817 | 56.4% | All 5 soil columns null (14 districts have no soil data) |
| `flag_zero_prod_nonzero_area` | 25 | 0.8% | Zero production with non-zero area (retained — genuine failures) |
| `flag_solar_missing_1981_83` | 141 | 4.4% | solar_mean missing (NASA satellite gap, 1981–1983 only) |
| `flag_area_missing` | 0 | 0.0% | Area is null (all excluded via E1 already) |

---

## 6. Missingness Report

| Feature | Missing Rows | Missing % | Explanation |
|:---|---:|---:|:---|
| `solar_mean` | 141 | 4.4% | NASA SRB satellite sensor gap, 1981–1983 |
| `soil_ph` | 1817 | 56.4% | 14 of 24 districts have no soil data |
| `soil_organic_carbon` | 1817 | 56.4% | Same 14 districts |
| `soil_clay_pct` | 1817 | 56.4% | Same 14 districts |
| `soil_sand_pct` | 1817 | 56.4% | Same 14 districts |
| `soil_silt_pct` | 1817 | 56.4% | Same 14 districts |
| `Area` | 0 | 0.0% | 0 after E1 exclusions |
| `Yield` | 0 | 0.0% | 0 after E1 exclusions |
| All other features | 0 | 0.0% | 100% complete |

---

## 7. Geographic and Boundary Limitations

### 7.1 Administrative Boundary Changes (Phase 3A evidence)

| Partition Wave | Districts Affected | Split Year | Comparability Impact |
|:---|:---|:---:|:---|
| Greater Hyderabad | Hyderabad → + Matiari, T.Allahyar, T.M.Khan | 2006 | Hyderabad pre-2006 values ~7x larger than post-split |
| Greater Larkana | Larkana → + Kambar Shahdad Kot | 2006 | Larkana rice area drops ~50% in 2006-07 |
| Greater Jacobabad | Jacobabad → + Kashmore | 2006 | Kashmore absent pre-2006 |
| Greater Dadu | Dadu → + Jamshoro | 2006 | Jamshoro absent pre-2006 |
| Greater Tharparkar | Tharparkar → + Umer Kot | 1996 | Umerkot absent pre-1996 |
| Greater Thatta | Thatta → + Sujawal | 2013 | Sujawal Rice data contaminated (excluded E1) |

### 7.2 Historical Thatta Rice (separate reference)

Historical Thatta Rice (1981-82 to 2008-09, 28 seasons, undivided district) is stored
separately in `reports/phase3d/thatta_rice_verified.csv`. These observations:
- Represent the **undivided** district (modern Thatta + modern Sujawal combined).
- **Must not be divided** between modern Thatta and Sujawal.
- **Must not be merged** into the research dataset without documented justification.
- Cover a different temporal period and geographic definition from all other dataset rows.

### 7.3 Whether records' geographic definitions are historically comparable

| Period | Geographic Stability | Recommendation |
|:---|:---|:---|
| 2013–14 to 2024–25 | STABLE — all 24 modern districts | Strongest comparability for modeling |
| 2006–07 to 2012–13 | MOSTLY STABLE — 23 districts (Sujawal absent or contaminated) | Usable with Sujawal Rice excluded |
| 1996–97 to 2005–06 | MODERATE — parent districts include later child areas | Flag boundary instability before using |
| 1981–82 to 1995–96 | LOW — multiple undivided parents; Umerkot absent | Aggregate to parent districts or use with caution |

---

## 8. Step 6 — Data Readiness vs. Model Readiness

### Q1: Is the dataset technically reproducible?
**YES.** The pipeline (`build_research_dataset.py`) is deterministic. Two runs on the
same source CSV produce byte-identical outputs (verified by SHA-256 comparison).

### Q2: Which records are safe to use provisionally?
- **Safest cohort:** 2013-14 to 2024-25 panel, all crops except Sujawal Rice.
  Stable boundaries, complete climate data, zero solar gaps, no unit ambiguities except Cotton.
- **Usable with caution:** 2006-07 to 2012-13 panel. Sujawal Rice excluded.
  Boundary step-down artifacts flagged but present for parent districts.
- **Requires aggregation before use:** 1981-82 to 2005-06. Administrative splits mean
  parent-district values are not directly comparable with post-split child-district values.

### Q3: Which records remain uncertain?
- **All Cotton rows:** Unit conversion factor (0.170097) is well-documented but applied
  as a secondary column; original bale values retained.
- **Sujawal non-Rice rows:** Sujawal's non-rice crops (Wheat, Cotton, Sugarcane, Maize)
  appear normal and are NOT excluded. However, their geographic comparability pre-2013
  requires the same boundary caveat as Thatta.
- **Thatta non-Rice rows:** Present in the dataset. Thatta's other crops appear in the
  PBS API. Only Rice is missing from the API entirely for Thatta.
- **14 districts with no soil data:** All soil-dependent analyses are restricted to
  the 10 districts with soil profiles.
- **141 pre-1983 rows:** solar_mean is missing; solar-dependent features require imputation
  or exclusion for this subpanel.

### Q4: Are the target labels appropriate for predicting crop suitability?
**NO — not directly.** Area, Production, and Yield describe **historical cultivation outcomes**
under the specific agronomic, economic, hydrological, and policy conditions of each year.
They reflect whether a crop was grown, not whether the land is climatically suitable.
Specifically:
- A district may show low rice area because of water scarcity, not soil unsuitability.
- A district may show high wheat area because of subsidized seed/fertilizer policy.
- Yield values reflect farmer practice, pest/disease pressure, and market incentives,
  not pure agro-climatic potential.
Any model trained directly on these targets would predict historical crop distribution,
not agronomic crop suitability. A suitability model would require separate ground-truth
labels (e.g., FAO AEZ suitability scores, experimental trial yields).

### Q5: What evidence is still needed before model training can be justified?
1. **True Sujawal and post-2013 Thatta rice data:** From MNFS&R district compendiums
   or Sindh CRS offline archives.
2. **Soil data for 14 missing districts:** ISRIC SoilGrids 250m data or field surveys.
3. **Post-2008 Thatta historical rice:** Verified district-level data for 2009-10 to 2024-25.
4. **Administrative crosswalk:** A formal taluka-level crosswalk mapping pre-2006 parent
   districts to their post-2006 child sub-territories.
5. **Suitability labels vs. production labels:** A decision on whether the model target
   is historical production or agronomic suitability — these require different labels.
6. **Cotton unit confirmation:** External verification that the bale conversion applies
   uniformly across all 44 years (Phase 3A concludes yes, but a cross-check against
   a post-2008 official compendium would strengthen this).

---

## 9. Verification Results

Pipeline validation: **14 checks**.

| Status | Count |
|:---|:---:|
| PASS | 13 |
| WARN | 0 |
| INFO | 1 |
| FAIL | 0 |

**All checks passed.**



Full validation detail: `reports/phase3e/validation_results.csv`

---

## 10. Deliverables

| File | Rows | Description |
|:---|---:|:---|
| `data/processed/research_dataset.csv` | 3,223 | Primary research dataset with quality flags |
| `data/processed/exclusion_ledger.csv` | 19 | Full traceability for every excluded row |
| `data/processed/data_dictionary.md` | — | Column definitions, units, caveats |
| `reports/phase3e/validation_results.csv` | 14 | 13 PASS / 0 WARN / 0 FAIL checks |
| `reports/phase3e/phase3e_summary.md` | — | This document |
| `reports/phase3d/thatta_rice_verified.csv` | 28 | Historical Thatta rice (stored separately, undivided district) |

---

## 11. Recommended Next Phase

**Phase 3F — Administrative Crosswalk and Panel Harmonization**
1. Build a formal taluka-level crosswalk mapping pre-2006 parent districts to post-2006
   child territories (requires provincial gazette data or CRS offline archives).
2. Decide whether to aggregate child districts back to parent polygons for longitudinal
   modeling (Phase 3B Model Track 2).
3. Acquire ISRIC SoilGrids 250m data for the 14 missing districts.
4. Investigate whether the MNFS&R post-2009 compendiums are accessible to recover
   Thatta and Sujawal rice data after 2008-09.
5. Define the formal target variable: historical cultivation distribution vs. agronomic suitability.
