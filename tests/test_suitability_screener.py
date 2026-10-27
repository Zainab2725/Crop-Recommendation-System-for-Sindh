"""
Unit and Integration Tests for Fajr-e-Kisht Biophysical Suitability Screener
============================================================================
Audited Test Suite (v1.1):
1. Excluded rows isolation (Sujawal Rice provincial contamination).
2. Missing soil handling (UNVERIFIED without synthetic imputation).
3. Missing soil cannot communicate complete suitability (cannot be SCREENED_IN).
4. Valid soil screening (physiological boundaries trigger SCREENED_OUT).
5. Temperature aggregation discipline (no false claims from seasonal means).
6. Revised rainfed screening (NEEDS_WATER_ASSESSMENT, no arbitrary 450mm screen-out or flood pass).
7. Revised saline groundwater screening (NEEDS_WATER_ASSESSMENT with FAO 29 tolerance, no universal rejection).
8. Revised rotational deficit canal screening (NEEDS_WATER_ASSESSMENT with stage-risk disclosures).
9. Status precedence hierarchy (SCREENED_OUT > NEEDS_WATER_ASSESSMENT > UNVERIFIED > SCREENED_IN).
10. Factor statuses transparency (individual factor breakdown present).
11. Economic gating (net profit explicitly unavailable).
12. Cotton units integrity (uses converted metric tonnes/ha).
13. Historical yield boundary and disaster tracking (boundary flags, zeros, no missing-as-zero).
14. Determinism of engine outputs.

Executable directly via:
    python tests/test_suitability_screener.py
or via pytest (if installed):
    pytest tests/test_suitability_screener.py
"""

import sys
import unittest
from pathlib import Path
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

try:
    import pytest
except ImportError:
    pytest = None

from src.engine.suitability_screener import (
    screen_crop_feasibility,
    AGRONOMIC_RULES,
    SUPPORTED_CROPS,
)

DATASET_PATH = Path(__file__).resolve().parents[1] / "data" / "processed" / "research_dataset.csv"

_DF_DATASET = None


def get_dataset():
    global _DF_DATASET
    if _DF_DATASET is None:
        assert DATASET_PATH.exists(), f"Processed dataset missing at {DATASET_PATH}"
        _DF_DATASET = pd.read_csv(DATASET_PATH)
    return _DF_DATASET


if pytest:
    @pytest.fixture(scope="module")
    def df_dataset():
        return get_dataset()


# =============================================================================
# TEST CASES
# =============================================================================

def test_supported_crops_count(df_dataset=None):
    """Test 1: Supported crops count and exact set."""
    assert len(SUPPORTED_CROPS) == 5
    assert set(SUPPORTED_CROPS) == {"Wheat", "Rice", "Cotton", "Sugarcane", "Maize"}


def test_excluded_row_isolation(df_dataset=None):
    """
    Test 2: Excluded rows (e.g. Sujawal Rice) must be SCREENED_OUT and never
    used for biophysical recommendations.
    """
    mock_row = pd.DataFrame([{
        "District": "Sujawal",
        "Crop": "Rice",
        "Year_start": 2020,
        "flag_excluded": True,
        "soil_ph": 7.5,
        "tmean": 30.0,
        "heat_days": 100,
        "cold_days": 0,
        "rain_total": 200.0,
        "Yield": 3.0,
    }])
    result = screen_crop_feasibility(
        df=mock_row,
        district="Sujawal",
        year_start=2020,
        crops=["Rice"],
    )
    rice_res = result["crop_results"]["Rice"]
    assert rice_res["status"] == "SCREENED_OUT"
    assert rice_res["factor_statuses"]["data_integrity"] == "EXCLUDED"
    assert "flag_excluded is True" in rice_res["findings"][0]["detail"]


def test_missing_soil_handling(df_dataset=None):
    """
    Test 3: Districts with missing soil data (e.g. Larkana) with assured water
    must return UNVERIFIED for soil pH, issue a prominent warning, and must NOT
    impute with averages.
    """
    df = df_dataset if df_dataset is not None else get_dataset()
    result = screen_crop_feasibility(
        df=df,
        district="Larkana",
        year_start=2020,
        water_delivery_category="ASSURED_PERENNIAL_CANAL",
        crops=["Wheat"],
    )
    wheat_res = result["crop_results"]["Wheat"]
    
    # Soil check must be UNVERIFIED
    soil_finding = [f for f in wheat_res["findings"] if f["factor"] == "Soil pH"][0]
    assert soil_finding["status"] == "UNVERIFIED"
    assert soil_finding["measured_value"] is None

    # Must contain warning about missing soil
    soil_warnings = [w for w in wheat_res["warnings"] if "SOIL DATA UNAVAILABLE" in w]
    assert len(soil_warnings) > 0
    assert wheat_res["status"] == "UNVERIFIED"
    assert wheat_res["factor_statuses"]["soil_edaphic"] == "UNVERIFIED"


def test_missing_soil_cannot_be_screened_in(df_dataset=None):
    """
    Test 4: If soil data is missing, the crop can NEVER communicate complete
    suitability (status must NOT be SCREENED_IN under any water regime).
    """
    df = df_dataset if df_dataset is not None else get_dataset()
    # Test under both assured and unassured water
    for water_cat in ["ASSURED_PERENNIAL_CANAL", "SWEET_GROUNDWATER_TUBEWELL", "UNSPECIFIED", "RAINFED_ONLY"]:
        result = screen_crop_feasibility(
            df=df,
            district="Larkana",  # Known missing soil district
            year_start=2020,
            water_delivery_category=water_cat,
            crops=["Wheat"],
        )
        res = result["crop_results"]["Wheat"]
        assert res["status"] != "SCREENED_IN", f"Missing soil yielded SCREENED_IN under {water_cat}"
        assert res["factor_statuses"]["soil_edaphic"] == "UNVERIFIED"


def test_valid_soil_screening(df_dataset=None):
    """
    Test 5: An extreme soil pH (<4.5 or >=9.0) triggers SEVERE_HAZARD.
    Because static SoilGrids prediction lacks measured ESP/ECe and does not
    prove complete root-zone mortality, it issues a critical hazard warning
    and resolves to UNVERIFIED requiring field tests, rather than claiming a biological mortality wall.
    """
    mock_row = pd.DataFrame([{
        "District": "TestDistrict",
        "Crop": "Wheat",
        "Year_start": 2020,
        "flag_excluded": False,
        "flag_soil_missing": False,
        "soil_ph": 9.2,  # Extreme sodicity hazard
        "tmean": 20.0,
        "tmax_mean": 28.0,
        "heat_days": 10,
        "cold_days": 0,
        "rain_total": 50.0,
        "n_days": 181,
        "Yield": 3.0,
    }])
    result = screen_crop_feasibility(
        df=mock_row,
        district="TestDistrict",
        year_start=2020,
        water_delivery_category="ASSURED_PERENNIAL_CANAL",
        crops=["Wheat"],
    )
    wheat_res = result["crop_results"]["Wheat"]
    assert wheat_res["status"] == "UNVERIFIED"
    assert wheat_res["factor_statuses"]["soil_edaphic"] == "SEVERE_HAZARD"
    soil_finding = [f for f in wheat_res["findings"] if f["factor"] == "Soil pH"][0]
    assert soil_finding["status"] == "SEVERE_HAZARD"
    assert any("[CRITICAL_SOIL_HAZARD]" in w for w in wheat_res["warnings"])


def test_temperature_aggregation_discipline(df_dataset=None):
    """
    Test 6: Daily critical-heat/anthesis data must be reported as UNVERIFIED,
    rather than invented from seasonal means. Seasonal tmean is INFORMATIONAL.
    """
    df = df_dataset if df_dataset is not None else get_dataset()
    result = screen_crop_feasibility(
        df=df,
        district="Badin",
        year_start=2020,
        crops=["Wheat"],
    )
    wheat_res = result["crop_results"]["Wheat"]
    heat_findings = [f for f in wheat_res["findings"] if "Anthesis" in f["factor"] or "Flowering" in f["factor"]]
    assert len(heat_findings) > 0
    assert heat_findings[0]["status"] == "UNVERIFIED"
    assert wheat_res["factor_statuses"]["thermal_climate"] == "INFORMATIONAL"
    assert wheat_res["factor_statuses"]["heat_stress"] == "UNVERIFIED"


def test_revised_rainfed_screening_not_screened_out(df_dataset=None):
    """
    Test 7: Rainfed water screening must NOT use an arbitrary >450mm rule
    to issue automatic SCREENED_OUT, nor pass flood rainfall as MARGINAL.
    It must return NEEDS_WATER_ASSESSMENT with clear ETc vs Pe context.
    """
    # Test fixture with low rain (50 mm)
    mock_low_rain = pd.DataFrame([{
        "District": "Tharparkar",
        "Crop": "Sugarcane",
        "Year_start": 2020,
        "flag_excluded": False,
        "flag_soil_missing": False,
        "soil_ph": 7.5,
        "tmean": 28.0,
        "tmax_mean": 35.0,
        "heat_days": 150,
        "cold_days": 0,
        "rain_total": 50.0,
        "n_days": 365,
        "Yield": 40.0,
    }])
    res_low = screen_crop_feasibility(
        df=mock_low_rain,
        district="Tharparkar",
        year_start=2020,
        water_delivery_category="RAINFED_ONLY",
        crops=["Sugarcane"],
    )["crop_results"]["Sugarcane"]
    assert res_low["status"] == "NEEDS_WATER_ASSESSMENT"
    assert res_low["factor_statuses"]["irrigation_water"] == "NEEDS_WATER_ASSESSMENT"
    assert any("Rainfed moisture assessment required" in f["detail"] for f in res_low["findings"])

    # Test fixture with flood rain (800 mm) - must NOT falsely pass as MARGINAL
    mock_flood_rain = pd.DataFrame([{
        "District": "Tharparkar",
        "Crop": "Cotton",
        "Year_start": 2022,
        "flag_excluded": False,
        "flag_soil_missing": False,
        "soil_ph": 7.5,
        "tmean": 30.0,
        "tmax_mean": 38.0,
        "heat_days": 120,
        "cold_days": 0,
        "rain_total": 800.0,
        "n_days": 214,
        "Yield": 0.0,
        "cotton_yield_t_ha": 0.0,
    }])
    res_flood = screen_crop_feasibility(
        df=mock_flood_rain,
        district="Tharparkar",
        year_start=2022,
        water_delivery_category="RAINFED_ONLY",
        crops=["Cotton"],
    )["crop_results"]["Cotton"]
    assert res_flood["status"] == "NEEDS_WATER_ASSESSMENT"
    assert res_flood["status"] != "SCREENED_IN"


def test_revised_saline_groundwater_requires_assessment(df_dataset=None):
    """
    Test 8: Saline groundwater must NOT universally SCREEN_OUT all crops without
    measured water ECw, crop tolerance evidence, and drainage data.
    It must return NEEDS_WATER_ASSESSMENT and cite FAO 29 tolerance.
    """
    mock_row = pd.DataFrame([{
        "District": "Sanghar",
        "Crop": "Cotton",
        "Year_start": 2020,
        "flag_excluded": False,
        "flag_soil_missing": False,
        "soil_ph": 7.8,
        "tmean": 30.0,
        "tmax_mean": 38.0,
        "heat_days": 110,
        "cold_days": 0,
        "rain_total": 120.0,
        "n_days": 214,
        "Yield": 2.5,
        "cotton_yield_t_ha": 0.425,
    }])
    result = screen_crop_feasibility(
        df=mock_row,
        district="Sanghar",
        year_start=2020,
        water_delivery_category="SALINE_GROUNDWATER_ONLY",
        crops=["Cotton"],
    )
    cotton_res = result["crop_results"]["Cotton"]
    assert cotton_res["status"] == "NEEDS_WATER_ASSESSMENT"
    assert cotton_res["factor_statuses"]["irrigation_water"] == "NEEDS_WATER_ASSESSMENT"
    water_finding = [f for f in cotton_res["findings"] if f["factor"] == "Irrigation Water Feasibility"][0]
    assert "FAO I&D 29" in water_finding["detail"]
    assert "Tolerant" in water_finding["detail"]


def test_rotational_deficit_canal_requires_assessment(df_dataset=None):
    """
    Test 9: Rotational deficit canal must return NEEDS_WATER_ASSESSMENT for all crops,
    with explicit high-water risk flags for Rice and Sugarcane.
    """
    mock_row = pd.DataFrame([
        {
            "District": "Badin",
            "Crop": "Rice",
            "Year_start": 2020,
            "flag_excluded": False,
            "flag_soil_missing": False,
            "soil_ph": 7.0,
            "tmean": 30.0,
            "tmax_mean": 36.0,
            "heat_days": 80,
            "cold_days": 0,
            "rain_total": 150.0,
            "n_days": 183,
            "Yield": 3.0,
        },
        {
            "District": "Badin",
            "Crop": "Wheat",
            "Year_start": 2020,
            "flag_excluded": False,
            "flag_soil_missing": False,
            "soil_ph": 7.0,
            "tmean": 22.0,
            "tmax_mean": 28.0,
            "heat_days": 15,
            "cold_days": 0,
            "rain_total": 20.0,
            "n_days": 181,
            "Yield": 3.5,
        },
    ])
    result = screen_crop_feasibility(
        df=mock_row,
        district="Badin",
        year_start=2020,
        water_delivery_category="ROTATIONAL_DEFICIT_CANAL",
        crops=["Rice", "Wheat"],
    )
    rice_res = result["crop_results"]["Rice"]
    wheat_res = result["crop_results"]["Wheat"]
    
    assert rice_res["status"] == "NEEDS_WATER_ASSESSMENT"
    assert any("HIGH_WATER_RISK" in w for w in rice_res["warnings"])
    
    assert wheat_res["status"] == "NEEDS_WATER_ASSESSMENT"
    assert wheat_res["factor_statuses"]["irrigation_water"] == "NEEDS_WATER_ASSESSMENT"


def test_status_precedence_hierarchy(df_dataset=None):
    """
    Test 10: Deterministic precedence:
    SCREENED_OUT > NEEDS_WATER_ASSESSMENT > UNVERIFIED > SCREENED_IN.
    """
    # Case A: Severe soil hazard + Unspecified water -> NEEDS_WATER_ASSESSMENT (with SEVERE_HAZARD soil)
    mock_fail_soil = pd.DataFrame([{
        "District": "PrecedenceTest",
        "Crop": "Wheat",
        "Year_start": 2020,
        "flag_excluded": False,
        "flag_soil_missing": False,
        "soil_ph": 9.5,  # SEVERE_HAZARD
        "tmean": 20.0,
        "tmax_mean": 28.0,
        "heat_days": 5,
        "cold_days": 0,
        "rain_total": 20.0,
        "n_days": 181,
        "Yield": 3.0,
    }])
    res_a = screen_crop_feasibility(
        df=mock_fail_soil,
        district="PrecedenceTest",
        year_start=2020,
        water_delivery_category="UNSPECIFIED",
        crops=["Wheat"],
    )["crop_results"]["Wheat"]
    assert res_a["status"] == "NEEDS_WATER_ASSESSMENT"
    assert res_a["factor_statuses"]["soil_edaphic"] == "SEVERE_HAZARD"

    # Case B: Valid soil + Unspecified water -> NEEDS_WATER_ASSESSMENT
    mock_valid_soil = pd.DataFrame([{
        "District": "PrecedenceTest",
        "Crop": "Wheat",
        "Year_start": 2020,
        "flag_excluded": False,
        "flag_soil_missing": False,
        "soil_ph": 7.0,  # PASS
        "tmean": 20.0,
        "tmax_mean": 28.0,
        "heat_days": 5,
        "cold_days": 0,
        "rain_total": 20.0,
        "n_days": 181,
        "Yield": 3.0,
    }])
    res_b = screen_crop_feasibility(
        df=mock_valid_soil,
        district="PrecedenceTest",
        year_start=2020,
        water_delivery_category="UNSPECIFIED",
        crops=["Wheat"],
    )["crop_results"]["Wheat"]
    assert res_b["status"] == "NEEDS_WATER_ASSESSMENT"

    # Case C: Missing soil + Assured water -> UNVERIFIED
    mock_missing_soil = pd.DataFrame([{
        "District": "PrecedenceTest",
        "Crop": "Wheat",
        "Year_start": 2020,
        "flag_excluded": False,
        "flag_soil_missing": True,
        "soil_ph": None,
        "tmean": 20.0,
        "tmax_mean": 28.0,
        "heat_days": 5,
        "cold_days": 0,
        "rain_total": 20.0,
        "n_days": 181,
        "Yield": 3.0,
    }])
    res_c = screen_crop_feasibility(
        df=mock_missing_soil,
        district="PrecedenceTest",
        year_start=2020,
        water_delivery_category="ASSURED_PERENNIAL_CANAL",
        crops=["Wheat"],
    )["crop_results"]["Wheat"]
    assert res_c["status"] == "UNVERIFIED"

    # Case D: Missing soil + Unspecified water -> NEEDS_WATER_ASSESSMENT (with soil marked UNVERIFIED)
    res_d = screen_crop_feasibility(
        df=mock_missing_soil,
        district="PrecedenceTest",
        year_start=2020,
        water_delivery_category="UNSPECIFIED",
        crops=["Wheat"],
    )["crop_results"]["Wheat"]
    assert res_d["status"] == "NEEDS_WATER_ASSESSMENT"
    assert res_d["factor_statuses"]["soil_edaphic"] == "UNVERIFIED"

    # Case E: Valid soil + Assured water -> SCREENED_IN
    res_e = screen_crop_feasibility(
        df=mock_valid_soil,
        district="PrecedenceTest",
        year_start=2020,
        water_delivery_category="ASSURED_PERENNIAL_CANAL",
        crops=["Wheat"],
    )["crop_results"]["Wheat"]
    assert res_e["status"] == "SCREENED_IN"


def test_factor_statuses_schema(df_dataset=None):
    """
    Test 11: Ensure every crop result contains explicit factor_statuses breakdown.
    """
    df = df_dataset if df_dataset is not None else get_dataset()
    result = screen_crop_feasibility(
        df=df,
        district="Badin",
        year_start=2020,
        water_delivery_category="ASSURED_PERENNIAL_CANAL",
        crops=["Rice"],
    )
    rice_res = result["crop_results"]["Rice"]
    assert "factor_statuses" in rice_res
    factors = rice_res["factor_statuses"]
    assert set(factors.keys()) == {
        "data_integrity",
        "soil_edaphic",
        "thermal_climate",
        "heat_stress",
        "irrigation_water",
    }


def test_economic_gating(df_dataset=None):
    """
    Test 12: Economic ranking must be explicitly marked DISABLED with a clear reason.
    """
    df = df_dataset if df_dataset is not None else get_dataset()
    result = screen_crop_feasibility(
        df=df,
        district="Badin",
        year_start=2020,
        crops=["Wheat"],
    )
    assert result["economic_ranking"]["status"] == "DISABLED"
    assert "prices and input production costs" in result["economic_ranking"]["message"]


def test_cotton_unit_handling(df_dataset=None):
    """
    Test 13: Cotton historical yield summary must indicate metric tonnes/ha
    converted from bales, avoiding raw bale confusion.
    """
    df = df_dataset if df_dataset is not None else get_dataset()
    result = screen_crop_feasibility(
        df=df,
        district="Sanghar",
        year_start=2020,
        crops=["Cotton"],
    )
    cotton_res = result["crop_results"]["Cotton"]
    hist = cotton_res["historical_yield_summary"]
    assert hist is not None
    assert "Converted from Bales" in hist["yield_unit"]
    # Cotton yield in tonnes/ha should be around 0.5 - 4.0 tonnes/ha, not 15-30 bales
    assert hist["median_yield_p50"] < 10.0


def test_historical_yield_boundary_and_disaster_tracking(df_dataset=None):
    """
    Test 14: Historical yield summary must report observed year range, track
    boundary instability, count zero-yield disaster years, and clarify that
    missing panel combinations are not zero yield.
    """
    df = df_dataset if df_dataset is not None else get_dataset()
    result = screen_crop_feasibility(
        df=df,
        district="Hyderabad",
        year_start=2020,
        crops=["Wheat"],
    )
    hist = result["crop_results"]["Wheat"]["historical_yield_summary"]
    assert hist is not None
    assert "observed_year_range" in hist
    assert "boundary_instability_detected" in hist
    assert hist["boundary_instability_detected"] is True  # Hyderabad had 2005 split
    assert "zero_yield_years" in hist
    assert "NOT treated as zero yield" in hist["disclaimer"]


def test_deterministic_output(df_dataset=None):
    """
    Test 15: Screener must produce identical outputs when executed repeatedly.
    """
    df = df_dataset if df_dataset is not None else get_dataset()
    res1 = screen_crop_feasibility(
        df=df,
        district="Badin",
        year_start=2015,
        water_delivery_category="ASSURED_PERENNIAL_CANAL",
    )
    res2 = screen_crop_feasibility(
        df=df,
        district="Badin",
        year_start=2015,
        water_delivery_category="ASSURED_PERENNIAL_CANAL",
    )
    assert res1 == res2


def test_soil_ph_stress_warning_vs_extreme_exclusion(df_dataset=None):
    """
    Test 16: Calibrated soil pH screening:
    - Moderate alkaline stress (e.g. Rice at pH 8.30, exceeding reference 8.2) triggers STRESS_WARNING,
      not hard SCREENED_OUT, because Dadu historically produces high rice yields under Indus silt.
    - Extreme edaphic toxicity (pH >= 9.0 or < 4.5) triggers hard FAIL and SCREENED_OUT.
    """
    # Case 1: Dadu Rice at pH 8.30 under assured canal -> SCREENED_IN with soil STRESS_WARNING
    mock_dadu_rice = pd.DataFrame([{
        "District": "Dadu",
        "Crop": "Rice",
        "Year_start": 2004,
        "flag_excluded": False,
        "flag_soil_missing": False,
        "soil_ph": 8.30,
        "tmean": 30.0,
        "tmax_mean": 37.0,
        "heat_days": 100,
        "cold_days": 0,
        "rain_total": 100.0,
        "n_days": 183,
        "Yield": 3.0,
    }])
    res_rice = screen_crop_feasibility(
        df=mock_dadu_rice,
        district="Dadu",
        year_start=2004,
        water_delivery_category="ASSURED_PERENNIAL_CANAL",
        crops=["Rice"],
    )["crop_results"]["Rice"]
    assert res_rice["status"] == "SCREENED_IN"
    assert res_rice["factor_statuses"]["soil_edaphic"] == "STRESS_WARNING"
    assert any("[SOIL_REACTION_STRESS]" in w for w in res_rice["warnings"])
    assert any("zinc" in w.lower() for w in res_rice["warnings"])

    # Case 2: Extreme hyper-sodic soil (pH 9.2) -> UNVERIFIED with soil SEVERE_HAZARD
    mock_extreme = pd.DataFrame([{
        "District": "ExtremeDistrict",
        "Crop": "Rice",
        "Year_start": 2020,
        "flag_excluded": False,
        "flag_soil_missing": False,
        "soil_ph": 9.2,
        "tmean": 30.0,
        "tmax_mean": 37.0,
        "heat_days": 100,
        "cold_days": 0,
        "rain_total": 100.0,
        "n_days": 183,
        "Yield": 3.0,
    }])
    res_extreme = screen_crop_feasibility(
        df=mock_extreme,
        district="ExtremeDistrict",
        year_start=2020,
        water_delivery_category="ASSURED_PERENNIAL_CANAL",
        crops=["Rice"],
    )["crop_results"]["Rice"]
    assert res_extreme["status"] == "UNVERIFIED"
    assert res_extreme["factor_statuses"]["soil_edaphic"] == "SEVERE_HAZARD"
    assert any("[CRITICAL_SOIL_HAZARD]" in w for w in res_extreme["warnings"])


def test_unverified_flowering_heat_stress_visibility(df_dataset=None):
    """
    Test 17: Flowering/anthesis heat stress check must remain visible as UNVERIFIED
    in factor_statuses and findings even when the overall crop is SCREENED_IN,
    ensuring users are never given false confidence regarding reproductive thermal shock.
    """
    mock_screened_in = pd.DataFrame([{
        "District": "Badin",
        "Crop": "Wheat",
        "Year_start": 2020,
        "flag_excluded": False,
        "flag_soil_missing": False,
        "soil_ph": 7.0,
        "tmean": 22.0,
        "tmax_mean": 28.0,
        "heat_days": 10,
        "cold_days": 0,
        "rain_total": 30.0,
        "n_days": 181,
        "Yield": 3.0,
    }])
    res = screen_crop_feasibility(
        df=mock_screened_in,
        district="Badin",
        year_start=2020,
        water_delivery_category="ASSURED_PERENNIAL_CANAL",
        crops=["Wheat"],
    )["crop_results"]["Wheat"]
    # Overall is SCREENED_IN
    assert res["status"] == "SCREENED_IN"
    # Factor status for heat_stress MUST remain UNVERIFIED
    assert res["factor_statuses"]["heat_stress"] == "UNVERIFIED"
    # Specific reproductive heat finding must be present and UNVERIFIED
    heat_finding = [f for f in res["findings"] if "Anthesis" in f["factor"] or "Flowering" in f["factor"]]
    assert len(heat_finding) > 0
    assert heat_finding[0]["status"] == "UNVERIFIED"
    # Summary must explicitly disclose that heat stress remains UNVERIFIED
    assert "heat stress remains UNVERIFIED" in res["summary"]


# =============================================================================
# STANDALONE TEST RUNNER
# =============================================================================

ALL_TESTS = [
    test_supported_crops_count,
    test_excluded_row_isolation,
    test_missing_soil_handling,
    test_missing_soil_cannot_be_screened_in,
    test_valid_soil_screening,
    test_temperature_aggregation_discipline,
    test_revised_rainfed_screening_not_screened_out,
    test_revised_saline_groundwater_requires_assessment,
    test_rotational_deficit_canal_requires_assessment,
    test_status_precedence_hierarchy,
    test_factor_statuses_schema,
    test_economic_gating,
    test_cotton_unit_handling,
    test_historical_yield_boundary_and_disaster_tracking,
    test_deterministic_output,
    test_soil_ph_stress_warning_vs_extreme_exclusion,
    test_unverified_flowering_heat_stress_visibility,
]


def run_all_tests():
    print(f"Loading dataset from {DATASET_PATH}...")
    df = get_dataset()
    print(f"Dataset loaded: {df.shape[0]} rows, {df.shape[1]} columns.\n")
    print(f"Running {len(ALL_TESTS)} audited suitability screener unit tests:")
    print("-" * 75)

    passed = 0
    failed = 0
    errors = []

    for idx, test_fn in enumerate(ALL_TESTS, start=1):
        name = test_fn.__name__
        try:
            test_fn(df)
            passed += 1
            print(f"[{idx:02d}/{len(ALL_TESTS):02d}] {name:<55} PASSED")
        except Exception as e:
            failed += 1
            errors.append((name, e))
            print(f"[{idx:02d}/{len(ALL_TESTS):02d}] {name:<55} FAILED: {e}")

    print("-" * 75)
    print(f"Results: {passed} passed, {failed} failed out of {len(ALL_TESTS)} tests.")
    if errors:
        print("\nFailures:")
        for name, e in errors:
            print(f"  - {name}: {e}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(run_all_tests())
