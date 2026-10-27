# Fajr-e-Kisht: A Data-Driven Crop Recommendation System for Sindh, Pakistan

**MUET Final-Year Project & Conference Paper Research Repository**

---

## 1. Project Overview

Fajr-e-Kisht is an explainable, data-driven crop suitability and recommendation system designed for the 24 agricultural districts of Sindh, Pakistan across 44 crop cycles (1981–82 to 2024–25) and five major crops: **Wheat, Rice, Cotton, Sugarcane, and Maize**.

The system integrates:
1. **Official Agricultural Production Statistics:** Pakistan Bureau of Statistics (PBS).
2. **Atmospheric & Solar Reanalysis:** NASA POWER API (MERRA-2 atmospheric model).
3. **Soil Properties:** Standardized physical and chemical profile indicators.
4. **Hydrological Factors:** Surface water and seasonal crop calendars.

---

## 2. Directory Structure

```
FYP_dataset_builder_code/
├── data/
│   └── raw/
│       └── pbs_weather_soil_1981_2025.csv      # Unchanged raw combined dataset
├── reports/                                    # Generated audit reports
│   ├── audit_summary.md                        # Primary markdown audit report
│   ├── data_anomalies.csv                      # Ledger of confirmed errors and flagged outliers
│   ├── missingness_matrix.csv                  # District x Crop temporal completeness table
│   ├── feature_missingness.csv                 # Column-by-column missing value metrics
│   ├── district_soil_status.csv                # Soil data availability & static profile check
│   ├── crop_yield_math_check.csv               # Yield formula validation & unit check
│   └── climate_season_audit.csv                # Crop calendar day counts (n_days) verification
├── src/
│   ├── __init__.py
│   └── data/
│       ├── __init__.py
│       └── audit_dataset.py                    # Standalone reproducible audit script (Phase 2)
├── pbs_crops_api.ipynb                         # PBS scraper notebook (original, untouched)
├── Subh_e_Ziraat_Sindh_Water_Hydrology.ipynb   # Hydrology notebook (original, untouched)
├── recent_climate.ipynb                        # Climate scratch notebook
└── README.md
```

---

## 3. How to Run the Dataset Audit

The audit script is completely **reproducible, deterministic, and non-destructive**. It reads the dataset, verifies schema, duplicates, mathematical relationships, and anomalies, and outputs reports to `reports/` without altering or imputing source data.

### Default Run (auto-locates dataset):
```bash
python src/data/audit_dataset.py
```

### Run with Custom Input Path and Output Directory:
```bash
python src/data/audit_dataset.py --input data/raw/pbs_weather_soil_1981_2025.csv --output-dir reports
```

### Command Line Options:
- `--input`, `-i`: Path to the CSV dataset (optional; searches standard project paths if omitted).
- `--output-dir`, `-o`: Directory to save the generated audit tables and Markdown summary (default: `reports/`).

---

## 4. Key Audit Findings Summary

- **Total records:** 3,242 rows × 27 columns (38.6% missing combinations across the theoretical $24 \times 5 \times 44$ panel).
- **Primary key duplicates:** 0 duplicate rows, 0 duplicate keys on `['District', 'Crop', 'Year_start']`.
- **Sujawal Rice Anomaly (Confirmed Error):** Sujawal district rice records (19 rows) hold the **Sindh provincial aggregate**, not district data. Reported area reaches 828.3k ha, matching the entire provincial harvest.
- **Soil Coverage:** Soil data is present for 10 districts and completely missing (1,817 NaNs, 56.0%) for 14 districts. Available soil values are time-invariant (single static profile copied across all years).
- **Yield Calculation:** For non-zero areas, $\text{Yield} = \text{Production} / \text{Area}$ holds within floating-point precision ($\le 5.5 \times 10^{-6}$). Cotton is reported in thousand bales (170 kg), whereas other crops are reported in thousand metric tonnes.
- **Growing Seasons:** `season_complete` is 100% `True` because weather was aggregated over defined crop calendar windows: Maize (153d), Rice (183d), Cotton (214d), Wheat (181/182d), Sugarcane (365/366d).

---

## 5. Running the Biophysical Suitability Screener & Tests

The project includes an audited, explainable biophysical suitability screening module (`src/engine/suitability_screener.py`) and a real-data pilot runner (`src/engine/run_pilot.py`).

### Run the Standalone Audited Test Suite:
```bash
python tests/test_suitability_screener.py
```
*Executes all 16 unit and integration tests across data isolation, soil stress calibration, temperature aggregation discipline, water assessment requirements, precedence hierarchies, and unit integrity.*

### Run the Real-Data Pilot:
```bash
python src/engine/run_pilot.py
```
*Evaluates the screener against `data/processed/research_dataset.csv` across 4 target district configurations (Badin, Larkana, Dadu, Thatta) and 5 water delivery scenarios (100 total evaluations), writing outputs to `reports/phase4/screener_pilot_results.csv`.*
