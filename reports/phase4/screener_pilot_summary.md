# Fajr-e-Kisht: Biophysical Suitability Screener Real-Data Pilot Report (Phase 4)

**Evaluation Date:** October 2026  
**Audited Engine Module:** [`src/engine/suitability_screener.py`](file:///c:/Users/22CS081/Downloads/FYP_dataset_builder_code/FYP_dataset_builder_code/src/engine/suitability_screener.py) (Version 1.2 Audited)  
**Pilot Execution Script:** [`src/engine/run_pilot.py`](file:///c:/Users/22CS081/Downloads/FYP_dataset_builder_code/FYP_dataset_builder_code/src/engine/run_pilot.py)  
**Detailed Results CSV:** [`reports/phase4/screener_pilot_results.csv`](file:///c:/Users/22CS081/Downloads/FYP_dataset_builder_code/FYP_dataset_builder_code/reports/phase4/screener_pilot_results.csv)  
**Unit Test Suite:** [`tests/test_suitability_screener.py`](file:///c:/Users/22CS081/Downloads/FYP_dataset_builder_code/FYP_dataset_builder_code/tests/test_suitability_screener.py) (16 / 16 Passed)  

---

## 1. Executive Summary & Objective

This report details the real-data pilot and scientific audit of the **Fajr-e-Kisht Biophysical Suitability Screener** executed against the project's primary dataset ([`data/processed/research_dataset.csv`](file:///c:/Users/22CS081/Downloads/FYP_dataset_builder_code/FYP_dataset_builder_code/data/processed/research_dataset.csv), 3,223 rows across 23 Sindh districts from 1981 to 2025).

The primary objective of this pilot is to evaluate how the audited biophysical rules, deterministic status precedence hierarchy, and data-integrity guards behave under real empirical conditions across distinct district data realities:
1. **Soil-Measured District (`Badin`, 2020–21):** Static soil pH available (7.75, non-missing), stable administrative boundaries.
2. **Missing-Soil District (`Larkana`, 2020–21):** Soil data structurally absent (`flag_soil_missing=True`, static pH unmeasured).
3. **Historical Boundary-Unstable District 1 (`Dadu`, 2004–05):** Pre-2006 parent district command area prior to Jamshoro administrative split; high alkaline soil pH (8.30).
4. **Historical Boundary-Unstable District 2 (`Thatta`, 2010–11):** Pre-2014 parent district command area prior to Sujawal split; unmeasured Thatta Rice in source API.

A total of **100 crop-scenario evaluations** (4 district configurations × 5 supported crops × 5 water scenarios) were executed strictly through the audited screener interface without modifying raw data or fabricating missing values.

---

## 2. Screener Interface & Input Categories

### 2.1 Function Signature
```python
def screen_crop_feasibility(
    df: pd.DataFrame,
    district: str,
    year_start: int,
    water_delivery_category: str = "UNSPECIFIED",
    crops: Optional[List[str]] = None,
) -> Dict[str, Any]:
```

### 2.2 Supported Crops
The screener evaluates five major crops in Sindh agriculture:
1. **Wheat** (*Triticum aestivum*, Rabi season)
2. **Rice** (*Oryza sativa*, Kharif season)
3. **Cotton** (*Gossypium hirsutum*, Kharif season)
4. **Sugarcane** (*Saccharum officinarum*, Annual 12-month season)
5. **Maize** (*Zea mays*, Kharif season)

### 2.3 Evaluated Water Delivery Scenarios
Because district-level canal gauge discharge volumes and tube-well water extraction records are absent from the underlying dataset, **all water categories are explicitly designated as hypothetical input scenarios**:
* `UNSPECIFIED`: Default scenario when the user or farm planner provides no water entitlement data.
* `RAINFED_ONLY`: Cultivation dependent solely on precipitation; assumes zero canal or tube-well irrigation.
* `ROTATIONAL_DEFICIT_CANAL`: Warabandi rotational canal delivery with periodic closure intervals and rationing.
* `SALINE_GROUNDWATER_ONLY`: Tube-well irrigation drawing exclusively from brackish/saline aquifers without canal mixing.
* `ASSURED_PERENNIAL_CANAL`: Assured, non-limiting perennial canal irrigation deliveries matching crop biological demand.

---

## 3. Pilot Scope & District Configurations

| District | Season / Year | Data Reality & Context | Soil Status (`soil_ph`) | Boundary Comparability Flag | Historical Panel Profile |
|:---|:---:|:---|:---:|:---:|:---|
| **Badin** | 2020–21 (`Year_start=2020`) | Available Soil Measurements | Measured: **7.75** (`flag_soil_missing=False`) | `STABLE` (`flag_boundary_instability=False`) | 4 crops present in 2020 (`Wheat`, `Rice`, `Sugarcane`, `Maize`). Cotton unrecorded in PBS panel. |
| **Larkana** | 2020–21 (`Year_start=2020`) | Missing Soil Measurements | Unmeasured: **NaN** (`flag_soil_missing=True`) | `STABLE` (post-2006 reporting regime) | 4 crops present in 2020 (`Wheat`, `Rice`, `Cotton`, `Sugarcane`). Maize absent in 2020. |
| **Dadu** | 2004–05 (`Year_start=2004`) | Boundary Instability & Alkaline Reaction | Measured: **8.30** (`flag_soil_missing=False`) | `PRE_SPLIT_PARENT` (`flag_boundary_instability=True`) | Pre-2006 boundary (includes Jamshoro tract). 4 crops present in 2004 (`Wheat`, `Rice`, `Cotton`, `Sugarcane`). |
| **Thatta** | 2010–11 (`Year_start=2010`) | Boundary Instability & API Rice Gap | Measured: **7.95** (`flag_soil_missing=False`) | `PRE_SPLIT_PARENT` (`flag_boundary_instability=True`) | Pre-2014 boundary (includes Sujawal tract). 3 crops present in 2010 (`Wheat`, `Cotton`, `Sugarcane`). Rice absent in PBS API. |

---

## 4. Overall Results & Top-Level Status Counts (Post-Audit Calibrated)

Across all 100 scenario evaluations with calibrated edaphic thresholds, the top-level statuses resolved as follows:

| Top-Level Screening Status | Total Count | Percentage | Agronomic & Technical Interpretation |
|:---|:---:|:---:|:---|
| **`NEEDS_WATER_ASSESSMENT`** | **60** | 60.0% | Arid climate moisture deficit, unmeasured groundwater salinity, rotational deficit canal schedule, or unspecified water supply requires farm-level verification. |
| **`UNVERIFIED`** | **29** | 29.0% | Either localized soil properties are unmeasured (`flag_soil_missing=True`, 4 evaluations under assured water), or the district-crop-year record is unobserved in the PBS panel (25 evaluations). |
| **`SCREENED_IN`** | **11** | 11.0% | All biophysical factors verified and passing within tolerance under the hypothetical `ASSURED_PERENNIAL_CANAL` scenario in soil-measured districts. |
| **`SCREENED_OUT`** | **0** | 0.0% | No evaluations in the pilot dataset had severe edaphic toxicity (pH < 4.5 or >= 9.0) or quarantined contamination (`flag_excluded=True`). |
| **Total Evaluations** | **100** | 100.0% | Fully deterministic; zero crashes, zero synthetic imputations. |

### 4.1 Cross-Tabulation: Water Delivery Scenario vs. Top-Level Status

| Water Scenario | `NEEDS_WATER_ASSESSMENT` | `UNVERIFIED` | `SCREENED_IN` | `SCREENED_OUT` | Total |
|:---|:---:|:---:|:---:|:---:|:---:|
| **`UNSPECIFIED`** | 15 | 5 | 0 | 0 | 20 |
| **`RAINFED_ONLY`** | 15 | 5 | 0 | 0 | 20 |
| **`ROTATIONAL_DEFICIT_CANAL`** | 15 | 5 | 0 | 0 | 20 |
| **`SALINE_GROUNDWATER_ONLY`** | 15 | 5 | 0 | 0 | 20 |
| **`ASSURED_PERENNIAL_CANAL`** | 0 | 9 | 11 | 0 | 20 |
| **Total** | **60** | **29** | **11** | **0** | **100** |

> [!NOTE]
> Under all four unassured/hypothetical water scenarios (`UNSPECIFIED`, `RAINFED_ONLY`, `ROTATIONAL_DEFICIT_CANAL`, `SALINE_GROUNDWATER_ONLY`), **zero crops are marked `SCREENED_IN`**. This rigorously adheres to agronomic discipline in arid Sindh, where seasonal crop evapotranspiration (450–2,500 mm) cannot be met by erratic seasonal rainfall (~10–180 mm).

---

## 5. Crop-by-Crop Pilot Results

| Crop | Season | Evaluated (`N`) | `NEEDS_WATER_ASSESSMENT` | `UNVERIFIED` | `SCREENED_IN` | `SCREENED_OUT` | Primary Factor Drivers & Constraints |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---|
| **Wheat** | Rabi | 20 | 16 | 1 | 3 | 0 | ETc 450–650 mm; soil pH tolerances pass in Badin (7.75), Dadu (8.30), and Thatta (7.95). In Larkana, soil unmeasured (`UNVERIFIED`). Screened in only under assured canal. |
| **Rice** | Kharif | 20 | 12 | 6 | 2 | 0 | Moderately alkaline reaction in Dadu (pH 8.30) issues `STRESS_WARNING` (zinc deficiency management) rather than hard exclusion; screened in under assured canal in Badin and Dadu. Unverified in Thatta (absent from API) and Larkana (missing soil). |
| **Cotton** | Kharif | 20 | 12 | 6 | 2 | 0 | Tolerant root zone salinity (threshold 7.7 dS/m). Tolerates pH up to 8.5. Unverified in Badin (not cultivated/recorded) and Larkana (missing soil). |
| **Sugarcane** | Annual | 20 | 16 | 1 | 3 | 0 | Massive ETc (1,500–2,500 mm). Moderately sensitive to salinity (1.7 dS/m). Requires assured water; flagged with `[HIGH_WATER_RISK]` under rotational deficit. |
| **Maize** | Kharif | 20 | 4 | 15 | 1 | 0 | Unobserved in panel for Larkana 2020, Dadu 2004, and Thatta 2010 (`UNVERIFIED`). Screened in for Badin 2020 under assured canal (pH 7.75 marginal but within limits). |

---

## 6. Detailed Inspection of the 11 SCREENED_IN Results

All 11 instances of `SCREENED_IN` occurred **exclusively under the hypothetical `ASSURED_PERENNIAL_CANAL` scenario** in districts with measured soil:

| # | District | Year Start | Crop | Water Delivery Scenario | Data Integrity | Soil Status | Climate Status | Heat Stress | Irrigation Status | Measured Soil pH | Measured Seasonal $T_{mean}$ |
|:---:|:---|:---:|:---|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 1 | **Badin** | 2020 | **Wheat** | ASSURED_PERENNIAL_CANAL | PASS | MARGINAL | INFORMATIONAL | UNVERIFIED | PASS | 7.75 | 23.9 °C |
| 2 | **Badin** | 2020 | **Rice** | ASSURED_PERENNIAL_CANAL | PASS | MARGINAL | INFORMATIONAL | UNVERIFIED | PASS | 7.75 | 29.5 °C |
| 3 | **Badin** | 2020 | **Sugarcane** | ASSURED_PERENNIAL_CANAL | PASS | PASS | INFORMATIONAL | UNVERIFIED | PASS | 7.75 | 27.6 °C |
| 4 | **Badin** | 2020 | **Maize** | ASSURED_PERENNIAL_CANAL | PASS | MARGINAL | INFORMATIONAL | UNVERIFIED | PASS | 7.75 | 28.5 °C |
| 5 | **Dadu** | 2004 | **Wheat** | ASSURED_PERENNIAL_CANAL | PASS | MARGINAL | INFORMATIONAL | UNVERIFIED | PASS | 8.30 | 21.9 °C |
| 6 | **Dadu** | 2004 | **Rice** | ASSURED_PERENNIAL_CANAL | PASS | STRESS_WARNING | INFORMATIONAL | UNVERIFIED | PASS | 8.30 | 30.7 °C |
| 7 | **Dadu** | 2004 | **Cotton** | ASSURED_PERENNIAL_CANAL | PASS | MARGINAL | INFORMATIONAL | UNVERIFIED | PASS | 8.30 | 32.0 °C |
| 8 | **Dadu** | 2004 | **Sugarcane** | ASSURED_PERENNIAL_CANAL | PASS | MARGINAL | INFORMATIONAL | UNVERIFIED | PASS | 8.30 | 27.7 °C |
| 9 | **Thatta** | 2010 | **Wheat** | ASSURED_PERENNIAL_CANAL | PASS | MARGINAL | INFORMATIONAL | UNVERIFIED | PASS | 7.95 | 22.6 °C |
| 10 | **Thatta** | 2010 | **Cotton** | ASSURED_PERENNIAL_CANAL | PASS | PASS | INFORMATIONAL | UNVERIFIED | PASS | 7.95 | 30.5 °C |
| 11 | **Thatta** | 2010 | **Sugarcane** | ASSURED_PERENNIAL_CANAL | PASS | MARGINAL | INFORMATIONAL | UNVERIFIED | PASS | 7.95 | 27.0 °C |

### Verification of Source Records & Scientific Guards:
1. **Source Record Verification:** Every single one of these 11 observations corresponds to a verified, unquarantined row in `research_dataset.csv` (`flag_excluded=False`).
2. **Unit Integrity:** Production and Yield fields are in standard metric units (Metric Tonnes / Hectare for Wheat, Rice, Sugarcane, Maize, and converted metric tonnes/ha via `cotton_yield_t_ha` for Cotton).
3. **No False Guarantees:** 
   - `status_heat_stress` is explicitly marked **`UNVERIFIED`** for all 11 crops. Seasonal `heat_days` are reported as informational, and the system explicitly discloses that flowering-stage heat tolerance cannot be established from seasonal aggregates.
   - `status_irrigation_water` is marked **`PASS` only under the stated assumption** of assured perennial canal supply.
   - The engine explicitly states: *"SCREENED_IN indicates only that all implemented biophysical boundary rules pass within tolerance under the provided inputs. It does NOT guarantee agronomic success or economic viability."*

---

## 7. Deep-Dive Inspection of the 29 UNVERIFIED Results

The 29 `UNVERIFIED` results fall into two distinct, well-defined categories:

| Category | Count | Distinct District-Crop Combinations | Root Cause & Scientific Rationale | Agronomic Meaning |
|:---|:---:|:---|:---|:---|
| **Absent Panel Records** | **25** | • Badin Cotton (5 scenarios)<br>• Larkana Maize 2020 (5 scenarios)<br>• Dadu Maize 2004 (5 scenarios)<br>• Thatta Rice (5 scenarios)<br>• Thatta Maize 2010 (5 scenarios) | The specific district-crop-year row is absent from the PBS source panel (`status_data_integrity = MISSING`). Thatta Rice is an API omission; others reflect unrecorded acreage. | **Absence is NOT treated as infeasibility or zero yield.** The screener records `observed_crop_years = 0` (or panel years if observed in other years) and refuses to screen without verified records. |
| **Missing Soil Measurements** | **4** | • Larkana Wheat (Assured canal)<br>• Larkana Rice (Assured canal)<br>• Larkana Cotton (Assured canal)<br>• Larkana Sugarcane (Assured canal) | While weather and crop records exist, localized SoilGrids properties are unmeasured (`flag_soil_missing = True`). | Even under assured water, missing soil prevents `SCREENED_IN`. The engine mandates on-ground soil pH/salinity testing. |
| **Total UNVERIFIED** | **29** | — | — | — |

---

## 8. Historical Yield Summaries Audit

| District | Crop | Observed Years | Median Yield ($P_{50}$) | Zero Production Years | Yield Unit | Boundary Instability Flagged | Audit Finding |
|:---|:---|:---:|:---:|:---:|:---|:---:|:---|
| **Badin** | Wheat | 44 | 1.739 | 0 | Metric Tonnes / Hectare | False | Fully observed 1981–2024. Stable boundary. Zero yield not observed. |
| **Badin** | Rice | 44 | 2.137 | 0 | Metric Tonnes / Hectare | False | Fully observed 1981–2024. Sown area reaches 150k+ ha in deltaic command. |
| **Badin** | Cotton | 0 | None | None | N/A (Missing in Source) | False | Unrecorded in source panel. Correctly returns None; zero yield NOT imputed. |
| **Badin** | Sugarcane | 44 | 51.276 | 0 | Metric Tonnes / Hectare | False | Consistent commercial cane tract. Median yield 51.3 t/ha. |
| **Badin** | Maize | 44 | 0.519 | 3 | Metric Tonnes / Hectare | False | Low acreage coarse grain. Correctly records 3 genuine agricultural failures (Area > 0, Production = 0 in 2005, 2006, 2007). |
| **Larkana** | Wheat | 44 | 1.819 | 0 | Metric Tonnes / Hectare | True | Carries pre-2006 Kambar Shahdadkot boundary split warning. |
| **Larkana** | Rice | 44 | 3.202 | 0 | Metric Tonnes / Hectare | True | Upper Sindh rice bowl. High productivity (median 3.2 t/ha). Boundary split noted. |
| **Larkana** | Cotton | 25 | 0.725 | 1 | Metric Tonnes / Hectare (Converted from Bales) | True | 25 years observed. Uses converted metric tonnes. Records 2022 flood disaster (Yield=0). |
| **Larkana** | Sugarcane | 44 | 43.286 | 0 | Metric Tonnes / Hectare | True | Fully observed. Boundary split noted. |
| **Larkana** | Maize | 1 | 0.600 | 0 | Metric Tonnes / Hectare | False | Single historical record (2008). Median computed from 1 observation without inventing zeros. |
| **Dadu** | Wheat | 44 | 2.072 | 0 | Metric Tonnes / Hectare | True | Pre-2006 Jamshoro split note preserved. |
| **Dadu** | Rice | 44 | 2.884 | 0 | Metric Tonnes / Hectare | True | 44 years observed (median 2.88 t/ha, max 4.22 t/ha). Proves empirical success despite pH 8.30. |
| **Dadu** | Cotton | 44 | 0.691 | 0 | Metric Tonnes / Hectare (Converted from Bales) | True | Fully observed. Converted units verified. |
| **Dadu** | Sugarcane | 44 | 47.192 | 0 | Metric Tonnes / Hectare | True | Fully observed. Pre-split boundary noted. |
| **Dadu** | Maize | 38 | 0.950 | 2 | Metric Tonnes / Hectare | True | 38 years observed. Records 2 zero-production disaster years without crashing. |
| **Thatta** | Wheat | 44 | 1.645 | 0 | Metric Tonnes / Hectare | True | Pre-2014 Sujawal split note preserved. |
| **Thatta** | Rice | 0 | None | None | N/A (Missing in Source) | False | API gap documented in Phase 3D. Correctly returns None; zero yield NOT imputed. |
| **Thatta** | Cotton | 42 | 0.546 | 0 | Metric Tonnes / Hectare (Converted from Bales) | True | 42 years observed. Uses converted metric units. Boundary split noted. |
| **Thatta** | Sugarcane | 44 | 53.669 | 0 | Metric Tonnes / Hectare | True | Thatta sugar mill command. Median 53.7 t/ha. Boundary split noted. |
| **Thatta** | Maize | 42 | 0.509 | 1 | Metric Tonnes / Hectare | True | 42 years observed. Records 1 zero-production year (2011 floods). |

---

## 9. Contradiction & Logic Verification Audit

A strict automated contradiction audit was performed on all 100 pilot records in [`reports/phase4/screener_pilot_results.csv`](file:///c:/Users/22CS081/Downloads/FYP_dataset_builder_code/FYP_dataset_builder_code/reports/phase4/screener_pilot_results.csv):

| Contradiction Check | Verification Rule | Audit Result | Status |
|:---|:---|:---:|:---:|
| **Check 1: False SCREENED_IN** | A crop must NEVER be marked `SCREENED_IN` if soil is unverified, data is missing, or water is unverified/deficit/saline. | **0 Violations** (All 11 `SCREENED_IN` rows have `soil_edaphic=PASS/MARGINAL/STRESS_WARNING`, `water=PASS`, `data=PASS`). | **PASSED** |
| **Check 2: Undocumented SCREENED_OUT** | A crop must NEVER be marked `SCREENED_OUT` without an explicit, authoritative physiological or data exclusion reason. | **0 Violations** (Zero undocumented exclusions). | **PASSED** |
| **Check 3: Missing Treated as Zero Yield** | Absent district-crop-year observations must NEVER be treated as zero yield in historical summaries. | **0 Violations** (Absent combinations return `None` or observed years = 0; zero zero-yield years imputed). | **PASSED** |
| **Check 4: Cotton Unit Integrity** | Cotton historical yields must use converted metric tonnes/ha, not raw bales/ha. | **0 Violations** (All Cotton summaries output unit: `Metric Tonnes / Hectare (Converted from Bales)`). | **PASSED** |
| **Check 5: Boundary Warning Integrity** | Pre-split parent districts must carry boundary instability notices in warnings. | **0 Violations** (All 45 Dadu and Thatta evaluations preserve full administrative split disclosures). | **PASSED** |

---

## 10. Reproducibility & Standalone Test Suite Execution

### 10.1 Running the Standalone Test Suite
```powershell
python tests/test_suitability_screener.py
```
**Actual Test Execution Output:**
```text
Loading dataset from C:\Users\22CS081\Downloads\FYP_dataset_builder_code\FYP_dataset_builder_code\data\processed\research_dataset.csv...
Dataset loaded: 3223 rows, 41 columns.

Running 16 audited suitability screener unit tests:
---------------------------------------------------------------------------
[01/16] test_supported_crops_count                              PASSED
[02/16] test_excluded_row_isolation                             PASSED
[03/16] test_missing_soil_handling                              PASSED
[04/16] test_missing_soil_cannot_be_screened_in                 PASSED
[05/16] test_valid_soil_screening                               PASSED
[06/16] test_temperature_aggregation_discipline                 PASSED
[07/16] test_revised_rainfed_screening_not_screened_out         PASSED
[08/16] test_revised_saline_groundwater_requires_assessment     PASSED
[09/16] test_rotational_deficit_canal_requires_assessment       PASSED
[10/16] test_status_precedence_hierarchy                        PASSED
[11/16] test_factor_statuses_schema                             PASSED
[12/16] test_economic_gating                                    PASSED
[13/16] test_cotton_unit_handling                               PASSED
[14/16] test_historical_yield_boundary_and_disaster_tracking    PASSED
[15/16] test_deterministic_output                               PASSED
[16/16] test_soil_ph_stress_warning_vs_extreme_exclusion        PASSED
---------------------------------------------------------------------------
Results: 16 passed, 0 failed out of 16 tests.
```

### 10.2 Running the Real-Data Pilot
```powershell
python src/engine/run_pilot.py
```
**Actual Output:**
```text
Loading research dataset from C:\Users\22CS081\Downloads\FYP_dataset_builder_code\FYP_dataset_builder_code\data\processed\research_dataset.csv...
Dataset loaded: 3223 rows across 23 districts.
Pilot execution completed successfully.
Total scenarios evaluated: 100 crop-scenario evaluations.
Results written to: C:\Users\22CS081\Downloads\FYP_dataset_builder_code\FYP_dataset_builder_code\reports\phase4\screener_pilot_results.csv

Top-level status counts across pilot evaluations:
top_level_status
NEEDS_WATER_ASSESSMENT    60
UNVERIFIED                29
SCREENED_IN               11
```

---

## 11. Operational Guidelines & Disclaimer

> [!CAUTION]
> **No Agricultural Advisory or Commercial Guarantee:**
> 1. Results from this pilot represent preliminary biophysical screening based on macro-level historical weather panels and static soil databases.
> 2. The output `SCREENED_IN` indicates only that none of the implemented physiological boundary rules failed under hypothetical non-limiting water conditions; it **does NOT guarantee agronomic success, pest freedom, economic profitability, or realized crop yield**.
> 3. Hypothetical water delivery scenarios (`RAINFED_ONLY`, `ROTATIONAL_DEFICIT_CANAL`, `SALINE_GROUNDWATER_ONLY`, `ASSURED_PERENNIAL_CANAL`) are scenario explorations for model validation and **must not be interpreted as actual water allocations or field recommendations for farmers**.
> 4. Farmers and local agricultural extension officers must perform localized soil testing (ECe, SAR, micro-nutrients) and canal watercourse schedule verification before planting decisions.
