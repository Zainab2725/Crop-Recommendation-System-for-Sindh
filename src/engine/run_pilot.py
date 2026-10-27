"""
Fajr-e-Kisht — Real-Data Pilot Runner (Phase 4)
==============================================
Runs the audited suitability screener against actual data from
`data/processed/research_dataset.csv` across target districts and
hypothetical water access scenarios.

Outputs:
  - reports/phase4/screener_pilot_results.csv
  - reports/phase4/screener_pilot_summary.md (generated alongside script)

Usage:
  python src/engine/run_pilot.py
"""

import os
import sys
from pathlib import Path
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.engine.suitability_screener import screen_crop_feasibility, SUPPORTED_CROPS

DATASET_PATH = REPO_ROOT / "data" / "processed" / "research_dataset.csv"
OUTPUT_CSV_PATH = REPO_ROOT / "reports" / "phase4" / "screener_pilot_results.csv"

# Target pilot configurations
PILOT_CONFIGS = [
    {
        "district": "Badin",
        "year_start": 2020,
        "description": "Available Soil Measurements (soil_ph=7.75, flag_soil_missing=False)",
    },
    {
        "district": "Larkana",
        "year_start": 2020,
        "description": "Missing Soil Measurements (soil_ph=NaN, flag_soil_missing=True)",
    },
    {
        "district": "Dadu",
        "year_start": 2004,
        "description": "Historical Boundary Instability (pre-2006 parent district, soil_ph=8.30)",
    },
    {
        "district": "Thatta",
        "year_start": 2010,
        "description": "Historical Boundary Instability (pre-2014 parent district, Thatta Rice missing)",
    },
]

WATER_SCENARIOS = [
    ("UNSPECIFIED", "Hypothetical Scenario: Water Access Unspecified (Default)"),
    ("RAINFED_ONLY", "Hypothetical Scenario: Rainfed Only (No Irrigation)"),
    ("ROTATIONAL_DEFICIT_CANAL", "Hypothetical Scenario: Rotational-Deficit Canal (Warabandi)"),
    ("SALINE_GROUNDWATER_ONLY", "Hypothetical Scenario: Saline Groundwater Tube-Well Only"),
    ("ASSURED_PERENNIAL_CANAL", "Hypothetical Scenario: Assured Perennial Canal Deliveries"),
]


def run_pilot():
    print(f"Loading research dataset from {DATASET_PATH}...")
    df = pd.read_csv(DATASET_PATH)
    print(f"Dataset loaded: {len(df)} rows across {df['District'].nunique()} districts.")

    records = []

    for cfg in PILOT_CONFIGS:
        dist = cfg["district"]
        yr = cfg["year_start"]
        cond_desc = cfg["description"]

        for water_cat, scenario_label in WATER_SCENARIOS:
            screener_out = screen_crop_feasibility(
                df=df,
                district=dist,
                year_start=yr,
                water_delivery_category=water_cat,
                crops=SUPPORTED_CROPS,
            )

            for crop in SUPPORTED_CROPS:
                c_res = screener_out["crop_results"][crop]
                top_status = c_res["status"]
                factor_st = c_res.get("factor_statuses", {})
                hy = c_res.get("historical_yield_summary")

                # Extract findings detail
                soil_finding = next((f for f in c_res.get("findings", []) if f["factor"] == "Soil pH"), {})
                temp_finding = next((f for f in c_res.get("findings", []) if f["factor"] == "Seasonal Mean Temperature"), {})
                rain_finding = next((f for f in c_res.get("findings", []) if f["factor"] == "Seasonal Rainfall"), {})
                water_finding = next((f for f in c_res.get("findings", []) if f["factor"] == "Irrigation Water Feasibility"), {})

                warnings_str = " | ".join(c_res.get("warnings", []))
                reasons_str = " | ".join(c_res.get("reasons", []))

                rec = {
                    "pilot_district": dist,
                    "district_data_condition": cond_desc,
                    "crop_year_start": yr,
                    "crop": crop,
                    "water_delivery_category": water_cat,
                    "water_scenario_label": scenario_label,
                    "top_level_status": top_status,
                    "status_data_integrity": factor_st.get("data_integrity", "UNKNOWN"),
                    "status_soil_edaphic": factor_st.get("soil_edaphic", "UNKNOWN"),
                    "status_thermal_climate": factor_st.get("thermal_climate", "UNKNOWN"),
                    "status_heat_stress": factor_st.get("heat_stress", "UNKNOWN"),
                    "status_irrigation_water": factor_st.get("irrigation_water", "UNKNOWN"),
                    "soil_ph_measured": soil_finding.get("measured_value", ""),
                    "tmean_measured": temp_finding.get("measured_value", ""),
                    "seasonal_rain_measured": rain_finding.get("measured_value", ""),
                    "water_evaluation_detail": water_finding.get("detail", ""),
                    "warnings": warnings_str,
                    "reasons": reasons_str,
                    "historical_yield_observed_years": hy["observed_crop_years"] if hy else 0,
                    "historical_yield_median_p50": hy["median_yield_p50"] if hy else "",
                    "historical_yield_mean": hy["mean_yield"] if hy else "",
                    "historical_yield_zero_years": hy["zero_yield_years"] if hy else "",
                    "historical_yield_unit": hy["yield_unit"] if hy else "N/A (Missing in Source)",
                    "boundary_instability_flagged": hy["boundary_instability_detected"] if hy else False,
                }
                records.append(rec)

    out_df = pd.DataFrame(records)
    OUTPUT_CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
    out_df.to_csv(OUTPUT_CSV_PATH, index=False)
    print(f"Pilot execution completed successfully.")
    print(f"Total scenarios evaluated: {len(out_df)} crop-scenario evaluations.")
    print(f"Results written to: {OUTPUT_CSV_PATH}")

    # Print summary table of counts
    print("\nTop-level status counts across pilot evaluations:")
    print(out_df["top_level_status"].value_counts().to_string())

    return out_df


if __name__ == "__main__":
    run_pilot()
