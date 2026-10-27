# Fajr-e-Kisht Dataset Audit Report

**Date of Audit:** 2026-10-26 12:08:31  
**Audited File:** `C:\Users\muet\Downloads\FYP_dataset\FYP_dataset_builder_code\data\raw\pbs_weather_soil_1981_2025.csv`  
**Dataset Dimensions:** 3,242 rows × 27 columns  
**Target Coverage:** 24 Sindh Districts × 5 Major Crops × 44 Crop Years (1981–82 to 2024–25)

---

## Executive Summary

This reproducible audit analyzes the combined crop, climate, and soil dataset for **Fajr-e-Kisht** without modifying or imputing any original observations.

1. **Integrity & Duplicates:** The dataset contains **0 duplicate rows** and **0 duplicate keys** on `['District', 'Crop', 'Year_start']`.
2. **Panel Completeness:** Out of 5,280 theoretical district–crop–year combinations, **3,242 combinations exist** (61.4% completeness) and **2,038 are missing**.
3. **Severe Anomaly Detected (Sujawal Rice):** Sujawal district rice records (19 rows from 2004–05 to 2022–23) hold the **Sindh provincial aggregate**, not district data. Reported area reaches **828,292 hectares** (exceeding Sujawal's total surface geography), and production in 2021–22 matches the total provincial rice harvest.
4. **Soil Data Coverage:** Only **10 of 24 districts** possess soil data (1,817 missing values, 56.0%). For the 10 populated districts, soil properties are **strictly static across all 44 years** (1 unique profile per district, zero temporal variance).
5. **Crop-Season Alignment (`n_days`):** `season_complete` is `True` for all 3,242 rows. `n_days` varies systematically across crops (Maize: 153d, Rice: 183d, Wheat: 181/182d, Cotton: 214d, Sugarcane: 365/366d), confirming that climate features were aggregated across crop-specific biological growing calendars.
6. **Solar Data Timeline:** `solar_mean` contains exactly 141 missing values, isolated to 1981 (56), 1982 (55), and 1983 (30), matching NASA POWER satellite sensor launch timelines (SRB data starts mid-1983).
7. **Mathematical Consistency:** For all records with non-zero Area, $	ext{Yield} = 	ext{Production} / 	ext{Area}$ matches with a maximum floating-point difference of <= 5.5e-6. However, **Cotton production is recorded in thousand bales (170 kg)**, while other crops are recorded in thousand metric tonnes.

---

## 1. Schema, Dimensions, and Key Uniqueness

| Metric | Measured Value | Benchmark / Expectation | Status |
|---|---|---|---|
| Total Records | **3,242** | 5,280 expected combinations | Unbalanced panel (38.6% missing) |
| Total Features | **27** | 27 columns | Matches specification |
| Duplicate Rows | **0** | 0 | PASSED |
| Duplicate `[District, Crop, Year]` Keys | **0** | 0 | PASSED |
| Number of Districts | **24** | 24 administrative districts | PASSED |
| Number of Crops | **5** | 5 crops (Cotton, Maize, Rice, Sugarcane, Wheat) | PASSED |
| Year Span | **1981 to 2024** | 1981 to 2024 (44 crop cycles) | PASSED |

---

## 2. Categorized Anomaly Ledger

Total flagged anomalies: **49**  
- **Confirmed Errors:** 20  
- **Suspicious / Requiring Verification:** 26  
- **Expected Historical Regimes:** 3  

### 2.1 Confirmed Errors

| Row Index | District | Crop | Year | Field | Finding & Impact |
|---|---|---|---|---|---|
| **2439–2456** | Sujawal | Rice | 2004–05 to 2021–22 | `Area`, `Production` | **Provincial Total Misattributed to District:** Sujawal Area reaches 828.3k ha; 2021–22 Production = 2,861.4k tonnes (100% of Sindh province). District ID 152 was queried at provincial level. |
| **2457** | Sujawal | Rice | 2022–23 | `Area`, `Yield` | **Missing Mandatory Targets:** `Area` is NaN, `Yield` is NaN, while `Production` is 2,011.8. |

### 2.2 Expected Historical Regimes (Legitimate Agricultural Realities)

| Finding | Occurrence | Agro-Climatic Context |
|---|---|---|
| **Zero Production with Area > 0** | 25 records | **2022 Megafloods:** Complete cotton washouts in Kashmore, Larkana, Shikarpur during the August 2022 flood catastrophe. Minor experimental or failed maize plantings (Area <= 0.1). Retain as true zero-yield training targets. |
| **Missing Solar Radiation** | 141 records (1981–1983) | NASA POWER Surface Solar Radiation (SRB satellite series) began reliable daily observation in mid-1983. Sensor cutoff is an expected satellite artifact. |
| **Variable `n_days` (153 to 366)** | All records | Defined biological growing seasons: Maize (153d), Rice (183d), Cotton (214d), Wheat (181/182d), Sugarcane (365/366d). Confirms weather values correctly represent crop windows. |

---

## 3. Soil Data Coverage and Temporal Analysis

All 5 soil variables (`soil_ph`, `soil_organic_carbon`, `soil_clay_pct`, `soil_sand_pct`, `soil_silt_pct`) exhibit identical completeness:

- **Populated Districts (10 / 24):** Badin (176), Dadu (214), Ghotki (135), Hyderabad (218), Kambar Shahdad Kot (54), Sanghar (210), Sujawal (19), Tharparkar (131), Thatta (172), Umer Kot (96).
- **Missing Districts (14 / 24):** Jacobabad, Jamshoro, Karachi Central, Kashmore, Khairpur, Larkana, Matiari, Mirpur Khas, Naushahro Feroze, Shaheed Benazirabad, Shikarpur, Sukkur, Tando Allahyar, Tando Muhammad Khan.
- **Temporal Invariance:** Every populated district has exactly **1 static soil profile** copied across all 44 years (zero temporal variance).
- **Physical Consistency:** Soil texture fractions satisfy $	ext{clay} + 	ext{sand} + 	ext{silt} = 100\%$ across all populated rows.

---

## 4. Growing Season and Calendar Audit

| Crop | Expected Window | `n_days` (Observed) | Row Count | `season_complete` |
|---|---|---|---|---|
| **Maize** | Jun 1 – Oct 31 | 153 | 570 | 100% True |
| **Rice** | Jun 1 – Nov 30 | 183 | 595 | 100% True |
| **Cotton** | May 1 – Nov 30 | 214 | 607 | 100% True |
| **Wheat** | Nov 1 – Apr 30 | 181 (non-leap) / 182 (leap) | 578 / 195 | 100% True |
| **Sugarcane** | Full Year (Jan–Dec) | 365 (non-leap) / 366 (leap) | 521 / 176 | 100% True |

---

## 5. Feature-Level Missingness Summary

| Category | Features | Missing Rows | Missing Pct | Provenance Notes |
|---|---|---|---|---|
| **Crop Targets** | `Area`, `Yield` | 1 | 0.03% | Row 2457 (Sujawal Rice 2022–23) |
| **Crop Targets** | `Production` | 0 | 0.00% | 100% complete |
| **Climate** | `solar_mean` | 141 | 4.35% | NASA satellite timeline (1981–1983) |
| **Climate** | `tmean`, `tmax_mean`, `tmin_mean`, `heat_days`, `cold_days`, `rain_total`, `rain_days`, `rh_mean`, `wind_mean`, `n_days`, `season_complete` | 0 | 0.00% | 100% complete across all 3,242 rows |
| **Soil Properties** | `soil_ph`, `soil_organic_carbon`, `soil_clay_pct`, `soil_sand_pct`, `soil_silt_pct` | 1,817 | 56.05% | Completely missing for 14 districts |

---

## 6. Recommendations for Subsequent Phases

1. **Quarantine Sujawal Rice Rows:** Do not include Sujawal Rice (rows 2439–2457) in crop recommendation models until district ID 152 is rectified in the PBS API scraper.
2. **Harmonize Cotton Units:** Standardize cotton production to metric tonnes ($1 \text{ bale} = 170 \text{ kg} = 0.17 \text{ tonnes}$) before training cross-crop models.
3. **Acquire Soil for 14 Missing Districts:** Query ISRIC SoilGrids 250m REST API using district administrative centroids.
4. **Preserve Zero-Yield Observations:** Treat the 25 zero-yield records as genuine agricultural failures (flood washouts), not as missing data.
