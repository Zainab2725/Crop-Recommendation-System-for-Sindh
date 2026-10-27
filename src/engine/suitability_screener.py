"""
Fajr-e-Kisht — Biophysical Suitability Screener (Version 1.1 Audited)
=====================================================================
A rule-based biophysical screening module for Sindh, Pakistan.

Core Principles:
1. Feasibility Screening vs. Guarantee:
   - "SCREENED_IN" means all verified biophysical rules pass within tolerance.
   - It does NOT guarantee agronomic success or economic viability.
2. Temporal Aggregation Discipline:
   - Seasonal aggregates (e.g. tmean, tmax_mean, heat_days) are used ONLY
     for rules matching their aggregation level.
   - We do NOT compare seasonal mean temperature directly against absolute
     daily physiological extremes as if that established feasibility.
   - Daily phenological/flowering-stage stress cannot be evaluated from
     seasonal aggregates; such checks return UNVERIFIED.
3. Explicit Gaps and Unverified Factors:
   - Missing soil data is marked UNVERIFIED (never imputed with averages).
   - Water delivery categories without physical volume/canal-gauge data
     return NEEDS_WATER_ASSESSMENT (rainfall is not treated as irrigation).
   - Economic ranking is explicitly DISABLED (prices and costs are absent).
4. No Invented Data or Arbitrary Scoring:
   - Zero synthetic weights or linear scoring formulas.
   - Historical yields are presented strictly as empirical context (percentiles,
     resilience CV), never as suitability labels.
5. Deterministic Precedence Hierarchy:
   - SCREENED_OUT: Definitive physiological/data-integrity disqualification.
   - NEEDS_WATER_ASSESSMENT: Water supply unverified, rainfed, rotational deficit,
     or unmeasured groundwater salinity in an arid irrigation-dependent regime.
   - UNVERIFIED: Water is assured, but localized soil chemistry is unmeasured.
   - SCREENED_IN: All required factors verified, present, and passing within tolerance.
"""

from typing import Dict, Any, List, Optional
import pandas as pd
import numpy as np


# =============================================================================
# AGRONOMIC REFERENCE LEDGER & TRACEABLE RULES
# =============================================================================

AGRONOMIC_RULES = {
    "Wheat": {
        "season_type": "Rabi",
        "soil_ph": {
            "opt_min": 6.0,
            "opt_max": 7.5,
            "abs_min": 5.5,
            "abs_max": 8.5,
            "source": "FAO EcoCrop Database; FAO Soils Bulletin 39; PARC National Wheat Programme",
            "intended_use": "Screen out severe micronutrient lockup or extreme sodicity/acidity in topsoil.",
            "limitations": "Evaluates static topsoil pH only; does not capture subsoil compaction or dynamic salinity/EC.",
        },
        "salinity_tolerance": {
            "threshold_ece_ds_m": 6.0,
            "classification": "Moderately Tolerant",
            "source": "FAO Irrigation and Drainage Paper 29 (Table 4); Maas and Hoffman (1977)",
            "intended_use": "Benchmark root zone electrical conductivity tolerance.",
            "limitations": "Dataset lacks measured water ECw, SAR, and soil salinity profiles. Saline groundwater cannot be screened deterministically without measured water quality and soil drainage.",
        },
        "temperature_season": {
            "opt_tmean_min": 15.0,
            "opt_tmean_max": 25.0,
            "source": "FAO EcoCrop; FAO Irrigation and Drainage Paper 33",
            "intended_use": "Informational check on seasonal mean temperature alignment with broad vegetative-to-maturity thermal range.",
            "limitations": "Seasonal tmean reflects a 181-day average; daily heat shocks during grain fill require stage-specific daily data.",
        },
        "heat_stress": {
            "critical_threshold_degC": 35.0,
            "source": "PARC National Wheat Programme; Reynolds et al. (CIMMYT)",
            "intended_use": "Track exposure to terminal heat (>35C) during spring maturity.",
            "limitations": "The dataset contains seasonal `heat_days` count (days >35C) across the entire 181-day window. "
                           "Because precise anthesis/grain-filling timing is not recorded in PBS data, "
                           "critical flowering-stage heat shock cannot be deterministically pinned to the reproductive phase.",
        },
        "water_requirement": {
            "seasonal_etc_mm_min": 450.0,
            "seasonal_etc_mm_max": 650.0,
            "source": "FAO Irrigation and Drainage Paper 56 (Table 12); FAO Water Report 33",
            "intended_use": "Benchmark biological crop evapotranspiration demand (ETc).",
            "limitations": "ETc represents biological water demand under non-limiting moisture, not water supply. In arid Sindh, winter Rabi rainfall (~10–30 mm) meets <5% of ETc. Rainfed wheat in Sindh requires verified riverine sailaba or residual flood moisture.",
        },
    },
    "Rice": {
        "season_type": "Kharif",
        "soil_ph": {
            "opt_min": 5.5,
            "opt_max": 7.0,
            "abs_min": 4.5,
            "abs_max": 8.2,
            "source": "IRRI Rice: Soil and Land Suitability; Ponnamperuma (1972); FAO EcoCrop",
            "intended_use": "Screen topsoil reaction. Flooding moderates pH, but pH > 8.2 causes severe zinc deficiency.",
            "limitations": "Evaluates static topsoil pH only; does not evaluate infiltration rate or hardpan depth.",
        },
        "salinity_tolerance": {
            "threshold_ece_ds_m": 3.0,
            "classification": "Sensitive",
            "source": "FAO Irrigation and Drainage Paper 29 (Table 4); IRRI Rice Knowledge Bank",
            "intended_use": "Benchmark salinity tolerance. High sensitivity during seedling and panicle initiation stages.",
            "limitations": "Dataset lacks measured water ECw. Saline tube-well irrigation causes rapid spikelet sterility and stunting.",
        },
        "temperature_season": {
            "opt_tmean_min": 22.0,
            "opt_tmean_max": 32.0,
            "source": "IRRI Rice Knowledge Bank; FAO EcoCrop",
            "intended_use": "Informational check on mean Kharif thermal regime suitability.",
            "limitations": "Does not replace spikelet sterility evaluation at flowering.",
        },
        "heat_stress": {
            "critical_threshold_degC": 35.0,
            "source": "IRRI Knowledge Bank (Spikelet sterility occurs when Tmax > 35C at anthesis)",
            "intended_use": "Track high temperature days.",
            "limitations": "Seasonal heat_days indicates total days >35C, but flowering occurs in a narrow 5-10 day window. "
                           "Without crop-stage phenology dates, exact anthesis sterility cannot be established.",
        },
        "water_requirement": {
            "seasonal_etc_mm_min": 900.0,
            "seasonal_etc_mm_max": 1500.0,
            "field_requirement_mm_min": 1200.0,
            "field_requirement_mm_max": 2500.0,
            "source": "FAO I&D 56; FAO Water Report 33; Sindh Irrigation Department Water Allocation Manuals",
            "intended_use": "Benchmark ETc demand and gross field water requirement (including puddling, standing flood layer, and percolation).",
            "limitations": "Lowland rice requires continuous standing water. Kharif rainfall (~100–180 mm) cannot support rice in arid Sindh without assured canal deliveries.",
        },
    },
    "Cotton": {
        "season_type": "Kharif",
        "soil_ph": {
            "opt_min": 6.5,
            "opt_max": 8.0,
            "abs_min": 5.5,
            "abs_max": 8.5,
            "source": "International Cotton Advisory Committee (ICAC); CCRI Sakrand; FAO Soils Bulletin",
            "intended_use": "Screen topsoil suitability. Sensitive to severe sodicity (pH > 8.5) and aluminum toxicity.",
            "limitations": "Static pH only; does not measure soil aeration, water table depth, or subsoil salinity.",
        },
        "salinity_tolerance": {
            "threshold_ece_ds_m": 7.7,
            "classification": "Tolerant",
            "source": "FAO Irrigation and Drainage Paper 29 (Table 4); ICAC Cotton Physiology",
            "intended_use": "Benchmark salinity tolerance. Moderately tolerant provided soil drainage permits leaching.",
            "limitations": "Dataset lacks measured water ECw and soil drainage profile. Even tolerant crops fail under poorly drained saline conditions.",
        },
        "temperature_season": {
            "opt_tmean_min": 22.0,
            "opt_tmean_max": 32.0,
            "source": "ICAC Technical Bulletins; FAO EcoCrop",
            "intended_use": "Informational check on seasonal thermal suitability.",
            "limitations": "Cannot capture episodic square shedding triggered by brief extreme temperature spikes.",
        },
        "heat_stress": {
            "critical_threshold_degC": 42.0,
            "source": "Central Cotton Research Institute (CCRI); ICAC Cotton Physiology",
            "intended_use": "Identify square shedding and boll abortion risk when temperatures exceed 42C.",
            "limitations": "Dataset heat_days threshold is fixed at >35C; days exceeding 42C are not individually recorded in seasonal aggregates.",
        },
        "water_requirement": {
            "seasonal_etc_mm_min": 700.0,
            "seasonal_etc_mm_max": 1300.0,
            "source": "FAO I&D 56; FAO Water Report 33",
            "intended_use": "Benchmark seasonal evapotranspiration demand across 214 growing days.",
            "limitations": "Sensitive to both water deficit at boll development and waterlogging hypoxia (>24–48 hours causes square shedding).",
        },
    },
    "Sugarcane": {
        "season_type": "Annual",
        "soil_ph": {
            "opt_min": 6.0,
            "opt_max": 7.8,
            "abs_min": 5.0,
            "abs_max": 8.5,
            "source": "FAO EcoCrop; Sugarcane Research Institute Thatta; PARC",
            "intended_use": "Screen for severe alkaline/sodic root stunting.",
            "limitations": "Evaluates topsoil pH only; sugarcane roots extend >1m and depend on subsoil drainage.",
        },
        "salinity_tolerance": {
            "threshold_ece_ds_m": 1.7,
            "classification": "Moderately Sensitive",
            "source": "FAO Irrigation and Drainage Paper 29 (Table 4); Sugarcane Research Institute Thatta",
            "intended_use": "Benchmark salinity tolerance.",
            "limitations": "Dataset lacks measured water ECw. Saline water impairs cane elongation, tillering, and sucrose synthesis.",
        },
        "temperature_season": {
            "opt_tmean_min": 24.0,
            "opt_tmean_max": 33.0,
            "source": "FAO EcoCrop; Sugarcane Research Institute Thatta",
            "intended_use": "Informational check on annual thermal regime.",
            "limitations": "Year-round aggregate smooths over critical cold winter dormancy and summer heat waves.",
        },
        "heat_stress": {
            "critical_threshold_degC": 42.0,
            "source": "FAO I&D 33; Sugarcane Research Institute Thatta",
            "intended_use": "Identify thermal elongation stoppage.",
            "limitations": "Days >42C are smoothed in annual means and cannot be separated from >35C heat_days.",
        },
        "water_requirement": {
            "seasonal_etc_mm_min": 1500.0,
            "seasonal_etc_mm_max": 2500.0,
            "source": "FAO I&D 56; FAO Water Report 33; Sindh Water Resource Review",
            "intended_use": "Benchmark massive annual water demand across 12 full months.",
            "limitations": "Enormous water consumption demands assured year-round canal entitlements or reliable sweet groundwater.",
        },
    },
    "Maize": {
        "season_type": "Kharif",
        "soil_ph": {
            "opt_min": 5.8,
            "opt_max": 7.2,
            "abs_min": 5.0,
            "abs_max": 8.2,
            "source": "CIMMYT Maize Manual; FAO EcoCrop; USDA NRCS",
            "intended_use": "Screen topsoil reaction. Susceptible to zinc and iron chlorosis above pH 8.0.",
            "limitations": "Static pH only; does not evaluate waterlogging risk to which maize is hypersensitive.",
        },
        "salinity_tolerance": {
            "threshold_ece_ds_m": 1.7,
            "classification": "Moderately Sensitive",
            "source": "FAO Irrigation and Drainage Paper 29 (Table 4); CIMMYT Maize Guidelines",
            "intended_use": "Benchmark salinity tolerance.",
            "limitations": "Dataset lacks measured water ECw. Osmotic stress during silking severely curtails grain formation.",
        },
        "temperature_season": {
            "opt_tmean_min": 18.0,
            "opt_tmean_max": 28.0,
            "source": "CIMMYT Maize Program; FAO EcoCrop",
            "intended_use": "Informational check on seasonal thermal suitability.",
            "limitations": "Seasonal aggregate obscures extreme heat at tasseling/silking.",
        },
        "heat_stress": {
            "critical_threshold_degC": 38.0,
            "source": "CIMMYT Maize Guidelines; Nielsen (Purdue Extension)",
            "intended_use": "Pollen desiccation and tassel blast threshold.",
            "limitations": "Dataset heat_days threshold is >35C; silking-window daily temperatures are not resolved in seasonal aggregates.",
        },
        "water_requirement": {
            "seasonal_etc_mm_min": 500.0,
            "seasonal_etc_mm_max": 800.0,
            "source": "FAO I&D 56; FAO Water Report 33; CIMMYT",
            "intended_use": "Benchmark water consumption over 153 growing days.",
            "limitations": "Extremely sensitive to moisture stress at silking; 2–4 days of moisture stress during flowering causes asynchronous pollen shed and severe yield loss.",
        },
    },
}

SUPPORTED_CROPS = list(AGRONOMIC_RULES.keys())

VALID_WATER_CATEGORIES = {
    "ASSURED_PERENNIAL_CANAL",
    "ROTATIONAL_DEFICIT_CANAL",
    "SWEET_GROUNDWATER_TUBEWELL",
    "SALINE_GROUNDWATER_ONLY",
    "RAINFED_ONLY",
    "UNSPECIFIED",
}


# =============================================================================
# SCREENING LOGIC
# =============================================================================

def screen_crop_feasibility(
    df: pd.DataFrame,
    district: str,
    year_start: int,
    water_delivery_category: str = "UNSPECIFIED",
    crops: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """
    Run biophysical suitability screening for a district and year.

    Parameters:
    -----------
    df : pd.DataFrame
        Loaded research dataset (e.g. data/processed/research_dataset.csv).
    district : str
        Target district name (e.g. "Badin", "Sanghar", "Larkana").
    year_start : int
        Crop year start (e.g. 2020 for the 2020-21 cycle).
    water_delivery_category : str
        Water supply category provided by user or irrigation zoning.
    crops : list of str, optional
        Specific crops to evaluate (defaults to all 5 supported crops).

    Returns:
    --------
    dict containing:
        - metadata (district, year_start, water_delivery_category)
        - economic_ranking_status: EXPLICITLY DISABLED
        - crop_results: dict mapping crop -> screening details
    """
    if crops is None:
        crops_to_evaluate = SUPPORTED_CROPS
    else:
        crops_to_evaluate = [c for c in crops if c in SUPPORTED_CROPS]

    norm_water_cat = water_delivery_category.strip().upper()
    if norm_water_cat not in VALID_WATER_CATEGORIES:
        norm_water_cat = "UNSPECIFIED"

    # Filter candidate rows for the district and year
    district_mask = (df["District"].str.strip().str.lower() == district.strip().lower()) & (df["Year_start"] == year_start)
    sub_df = df[district_mask].copy()

    crop_results = {}

    for crop in crops_to_evaluate:
        crop_rows = sub_df[sub_df["Crop"].str.strip() == crop]
        res = _evaluate_single_crop(
            df=df,
            crop=crop,
            district=district,
            year_start=year_start,
            crop_rows=crop_rows,
            water_category=norm_water_cat,
        )
        crop_results[crop] = res

    return {
        "screener_version": "v1.1-audited",
        "district": district,
        "year_start": year_start,
        "water_delivery_category": norm_water_cat,
        "economic_ranking": {
            "status": "DISABLED",
            "message": (
                "Economic ranking (gross revenue, net profit) is unavailable. "
                "Reliable district-level commodity farm-gate prices and input production "
                "costs (fertilizer, diesel, land prep) have not been integrated. "
                "No synthetic prices or margins are permitted."
            ),
        },
        "crop_results": crop_results,
    }


def _evaluate_single_crop(
    df: pd.DataFrame,
    crop: str,
    district: str,
    year_start: int,
    crop_rows: pd.DataFrame,
    water_category: str,
) -> Dict[str, Any]:
    """Evaluate biophysical rules for a single crop."""
    rules = AGRONOMIC_RULES[crop]
    findings = []
    reasons = []
    warnings = []
    evidence_refs = []

    # -------------------------------------------------------------------------
    # 1. Data Presence & Exclusion Checks
    # -------------------------------------------------------------------------
    if crop_rows.empty:
        return {
            "crop": crop,
            "status": "UNVERIFIED",
            "factor_statuses": {
                "data_integrity": "MISSING",
                "soil_edaphic": "UNVERIFIED",
                "thermal_climate": "UNVERIFIED",
                "heat_stress": "UNVERIFIED",
                "irrigation_water": "UNVERIFIED",
            },
            "summary": f"No data recorded for {crop} in {district} for season starting {year_start}.",
            "findings": [{"factor": "Data Record", "status": "MISSING", "detail": "District-crop-year row is absent from processed panel."}],
            "reasons": ["Historical observation missing from panel; suitability cannot be audited from this record."],
            "warnings": ["Panel combination absent from dataset."],
            "evidence": [],
            "historical_yield_summary": _compute_historical_yield_summary(df, district, crop),
        }

    row = crop_rows.iloc[0]

    # Check flag_excluded
    if bool(row.get("flag_excluded", False)):
        return {
            "crop": crop,
            "status": "SCREENED_OUT",
            "factor_statuses": {
                "data_integrity": "EXCLUDED",
                "soil_edaphic": "UNVERIFIED",
                "thermal_climate": "UNVERIFIED",
                "heat_stress": "UNVERIFIED",
                "irrigation_water": "UNVERIFIED",
            },
            "summary": f"{crop} in {district} ({year_start}) is explicitly quarantined/excluded from research dataset.",
            "findings": [{"factor": "Data Integrity", "status": "EXCLUDED", "detail": "flag_excluded is True (e.g. Sujawal Rice contamination)."}],
            "reasons": [
                "Row is flagged as contaminated or mathematically invalid in research_dataset.csv. "
                "Provincial totals or corrupted records cannot be used for local recommendation."
            ],
            "warnings": ["Quarantined observation; excluded from analysis."],
            "evidence": [{"rule": "Data Pipeline Quality Exclusion", "source": "src/data/build_research_dataset.py"}],
            "historical_yield_summary": None,
        }

    # Boundary instability warning
    if bool(row.get("flag_boundary_instability", False)):
        note = row.get("reporting_regime_note", "Administrative boundary split occurred during panel.")
        warnings.append(f"Boundary instability note: {note}")

    is_screened_out = False

    # -------------------------------------------------------------------------
    # 2. Edaphic / Soil pH Screening
    # -------------------------------------------------------------------------
    soil_missing = bool(row.get("flag_soil_missing", False)) or pd.isna(row.get("soil_ph"))
    soil_rule = rules["soil_ph"]
    evidence_refs.append({
        "factor": "Soil Reaction (pH)",
        "source": soil_rule["source"],
        "intended_use": soil_rule["intended_use"],
        "limitations": (
            "Static centroid SoilGrids 250m prediction with ±0.3 to ±0.5 pH unit model uncertainty. "
            "Evaluates topsoil reaction (0–30 cm); does not measure electrical conductivity (ECe), "
            "exchangeable sodium percentage (ESP), or subsoil drainage profile."
        ),
    })

    if soil_missing:
        soil_status = "UNVERIFIED"
        findings.append({
            "factor": "Soil pH",
            "status": "UNVERIFIED",
            "measured_value": None,
            "detail": "Measured soil pH is absent for this district (flag_soil_missing=True).",
        })
        warnings.append(
            "[WARNING: SOIL DATA UNAVAILABLE]: District-level soil properties are unmeasured. "
            "Soil suitability cannot be evaluated. The screener refuses to silently substitute regional averages. "
            "Farmers must verify localized soil pH before planting."
        )
    else:
        ph_val = float(row["soil_ph"])
        # Edaphic screening: Calibrated against FAO Soils Bulletin 39, Ponnamperuma (1972),
        # and IRRI Rice Soil Suitability. SoilGrids provides static 250m centroid predictions
        # with ±0.3 to ±0.5 pH unit model uncertainty. Static pH does not establish root-zone
        # mortality walls; extreme values represent severe chemical hazards (aluminum toxicity
        # or black-alkali sodic dispersion) requiring field-level reclamation before planting.
        if ph_val < 4.5 or ph_val >= 9.0:
            # Extreme edaphic hazard: acute hydrogen/aluminum toxicity (<4.5) or severe sodic dispersion (>=9.0).
            # Classified as SEVERE_HAZARD (cannot be marked PASS or MARGINAL).
            soil_status = "SEVERE_HAZARD"
            findings.append({
                "factor": "Soil pH",
                "status": "SEVERE_HAZARD",
                "measured_value": ph_val,
                "detail": (
                    f"SoilGrids predicted topsoil pH ({ph_val:.2f}) indicates an extreme edaphic hazard "
                    "(<4.5 severe acidity/aluminum toxicity, or >=9.0 severe black-alkali sodicity). "
                    "In the absence of measured ESP, SAR, and subsoil ECe, field-level soil testing and "
                    "chemical reclamation (e.g. agricultural gypsum, leaching) are mandatory before cultivation."
                ),
            })
            warnings.append(
                f"[CRITICAL_SOIL_HAZARD]: Predicted topsoil pH ({ph_val:.2f}) indicates severe chemical stress. "
                "Cultivation is unadvisable without laboratory-verified ESP/SAR soil testing and reclamation."
            )
        elif ph_val < soil_rule["abs_min"] or ph_val > soil_rule["abs_max"]:
            # Elevated alkaline or acidic reaction outside typical literature envelope,
            # but manageable via agronomic amendments (e.g. gypsum, zinc sulfate, sulfur).
            soil_status = "STRESS_WARNING"
            findings.append({
                "factor": "Soil pH",
                "status": "STRESS_WARNING",
                "measured_value": ph_val,
                "detail": (
                    f"Soil pH ({ph_val:.2f}) falls outside standard reference envelope "
                    f"[{soil_rule['abs_min']}, {soil_rule['abs_max']}]. "
                    f"In alkaline Indus alluvium, pH > {soil_rule['abs_max']} induces micronutrient lockup "
                    "(zinc/iron chlorosis, phosphorus precipitation) and sodicity hazard, but does NOT "
                    "constitute absolute physiological mortality. Requires zinc application or gypsum management."
                ),
            })
            warnings.append(
                f"[SOIL_REACTION_STRESS]: Measured SoilGrids pH ({ph_val:.2f}) exceeds typical reference limit "
                f"({soil_rule['abs_max']}) for {crop}. High risk of zinc/iron deficiency and calcareous sodicity; "
                "soil amendment (gypsum, ZnSO4) and on-ground EC/ESP testing strongly advised."
            )
        elif ph_val < soil_rule["opt_min"] or ph_val > soil_rule["opt_max"]:
            soil_status = "MARGINAL"
            findings.append({
                "factor": "Soil pH",
                "status": "MARGINAL",
                "measured_value": ph_val,
                "detail": f"Soil pH ({ph_val:.2f}) is within survival tolerance but outside optimal range [{soil_rule['opt_min']}, {soil_rule['opt_max']}].",
            })
        else:
            soil_status = "PASS"
            findings.append({
                "factor": "Soil pH",
                "status": "PASS",
                "measured_value": ph_val,
                "detail": f"Soil pH ({ph_val:.2f}) is within optimal agronomic range [{soil_rule['opt_min']}, {soil_rule['opt_max']}].",
            })

    # -------------------------------------------------------------------------
    # 3. Thermal & Seasonal Temperature Discipline
    # -------------------------------------------------------------------------
    # We do NOT compare seasonal tmean directly against absolute daily physiological
    # survival envelopes (e.g. 0C or 45C) because a 180-day mean smooths daily extremes.
    # We report seasonal tmean against optimal seasonal regime, and report heat_days.
    temp_rule = rules["temperature_season"]
    evidence_refs.append({
        "factor": "Seasonal Temperature (tmean)",
        "source": temp_rule["source"],
        "intended_use": temp_rule["intended_use"],
        "limitations": temp_rule["limitations"],
    })

    tmean_val = float(row["tmean"]) if not pd.isna(row.get("tmean")) else None
    heat_days_val = int(row["heat_days"]) if not pd.isna(row.get("heat_days")) else 0

    if tmean_val is not None:
        findings.append({
            "factor": "Seasonal Mean Temperature",
            "status": "INFORMATIONAL",
            "measured_value": f"{tmean_val:.1f} °C",
            "detail": f"Observed seasonal tmean is {tmean_val:.1f}°C (Optimal range: {temp_rule['opt_tmean_min']}–{temp_rule['opt_tmean_max']}°C).",
        })

    # Heat stress check: explain aggregation limitations
    heat_rule = rules["heat_stress"]
    evidence_refs.append({
        "factor": "Heat Stress Check",
        "source": heat_rule["source"],
        "intended_use": heat_rule["intended_use"],
        "limitations": heat_rule["limitations"],
    })

    # Specific rule for Wheat: extreme terminal heat in Rabi window
    if crop == "Wheat":
        findings.append({
            "factor": "Heat Exposure (Days > 35°C)",
            "status": "INFORMATIONAL",
            "measured_value": f"{heat_days_val} days",
            "detail": f"Recorded {heat_days_val} days with Tmax > 35°C across 181-day Rabi window.",
        })
        findings.append({
            "factor": "Critical Anthesis Heat Shock",
            "status": "UNVERIFIED",
            "measured_value": None,
            "detail": "Flowering/anthesis date is not recorded in PBS data. Daily temperature during the critical 10-day reproductive stage cannot be isolated from seasonal aggregate.",
        })
    else:
        findings.append({
            "factor": "Heat Exposure (Days > 35°C)",
            "status": "INFORMATIONAL",
            "measured_value": f"{heat_days_val} days",
            "detail": f"Recorded {heat_days_val} days with Tmax > 35°C across {int(row.get('n_days', 0))} growing days.",
        })
        findings.append({
            "factor": "Critical Flowering Heat Stress",
            "status": "UNVERIFIED",
            "measured_value": None,
            "detail": f"Daily critical heat stress ({heat_rule['critical_threshold_degC']}°C) at flowering cannot be evaluated from seasonal aggregate. Phenological dates required.",
        })

    # -------------------------------------------------------------------------
    # 4. Water Discipline: Crop Demand vs. Actual Irrigation Supply
    # -------------------------------------------------------------------------
    water_rule = rules["water_requirement"]
    evidence_refs.append({
        "factor": "Water Requirement (Demand)",
        "source": water_rule["source"],
        "intended_use": water_rule["intended_use"],
        "limitations": water_rule["limitations"],
    })

    sal_rule = rules.get("salinity_tolerance", {})
    if sal_rule:
        evidence_refs.append({
            "factor": "Salinity Tolerance",
            "source": sal_rule["source"],
            "intended_use": sal_rule["intended_use"],
            "limitations": sal_rule["limitations"],
        })

    rain_total = float(row["rain_total"]) if not pd.isna(row.get("rain_total")) else 0.0
    findings.append({
        "factor": "Seasonal Rainfall",
        "status": "INFORMATIONAL",
        "measured_value": f"{rain_total:.1f} mm",
        "detail": (
            f"Observed precipitation is {rain_total:.1f} mm across growing season. "
            "In Sindh's arid regime, rainfall meets only a fraction of crop evapotranspiration. "
            "Rainfall must NOT be treated as irrigation availability."
        ),
    })

    etc_min = water_rule["seasonal_etc_mm_min"]
    etc_max = water_rule["seasonal_etc_mm_max"]

    if water_category == "UNSPECIFIED":
        water_status = "NEEDS_WATER_ASSESSMENT"
        findings.append({
            "factor": "Irrigation Water Feasibility",
            "status": "NEEDS_WATER_ASSESSMENT",
            "detail": (
                f"{crop} seasonal evapotranspiration demand (ETc) is {etc_min:.0f}–{etc_max:.0f} mm. "
                "Water delivery category was not specified. Because canal discharge and tube-well "
                "access are unobserved in the dataset, irrigation feasibility cannot be evaluated without on-ground verification."
            ),
        })
        warnings.append(
            f"[NEEDS_WATER_ASSESSMENT]: {crop} requires {etc_min:.0f}–{etc_max:.0f} mm seasonal water. "
            "Actual irrigation access must be confirmed by the user before planting."
        )

    elif water_category == "RAINFED_ONLY":
        water_status = "NEEDS_WATER_ASSESSMENT"
        findings.append({
            "factor": "Irrigation Water Feasibility",
            "status": "NEEDS_WATER_ASSESSMENT",
            "detail": (
                f"Rainfed moisture assessment required. {crop} biological water demand (ETc) is "
                f"{etc_min:.0f}–{etc_max:.0f} mm, whereas seasonal rainfall is {rain_total:.1f} mm. "
                "In arid Sindh, seasonal precipitation is not equivalent to effective rainfall (Pe) and cannot "
                "guarantee sustained soil moisture. Rainfed feasibility requires on-ground soil moisture or sailaba verification."
            ),
        })
        warnings.append(
            f"[NEEDS_WATER_ASSESSMENT: RAINFED RISK]: {crop} ETc ({etc_min:.0f}–{etc_max:.0f} mm) vastly exceeds "
            f"seasonal precipitation ({rain_total:.1f} mm). Unirrigated cultivation carries severe drought hazard."
        )

    elif water_category == "SALINE_GROUNDWATER_ONLY":
        water_status = "NEEDS_WATER_ASSESSMENT"
        tol_class = sal_rule.get("classification", "Unknown")
        ec_thresh = sal_rule.get("threshold_ece_ds_m", "unspecified")
        findings.append({
            "factor": "Irrigation Water Feasibility",
            "status": "NEEDS_WATER_ASSESSMENT",
            "detail": (
                f"Saline groundwater hazard requires water testing. {crop} is classified as {tol_class} "
                f"to root zone salinity (FAO I&D 29 threshold ECe ~ {ec_thresh} dS/m). However, measured aquifer "
                "salinity (ECw, TDS, SAR) and soil drainage/leaching capacity are absent from the dataset. "
                "Irrigating exclusively with saline groundwater without fresh canal dilution or verified leaching "
                "creates acute risk of soil salinization and toxic osmotic shock."
            ),
        })
        warnings.append(
            f"[NEEDS_WATER_ASSESSMENT: HIGH SALINITY HAZARD]: Groundwater salinity (ECw) is unmeasured. "
            f"{crop} ({tol_class}, threshold ~{ec_thresh} dS/m) cannot be screened without laboratory water testing."
        )

    elif water_category == "ROTATIONAL_DEFICIT_CANAL":
        water_status = "NEEDS_WATER_ASSESSMENT"
        if crop in ("Sugarcane", "Rice"):
            findings.append({
                "factor": "Irrigation Water Feasibility",
                "status": "NEEDS_WATER_ASSESSMENT",
                "detail": (
                    f"{crop} has massive continuous water demand ({etc_min:.0f}–{etc_max:.0f} mm). "
                    "Under rotational deficit canal supply, prolonged canal closure intervals (Warabandi) "
                    "cause severe crop desiccation or failure unless supplementary sweet groundwater storage is available."
                ),
            })
            warnings.append(
                f"[HIGH_WATER_RISK]: {crop} under rotational deficit canal water faces severe moisture deficit risk."
            )
        else:
            findings.append({
                "factor": "Irrigation Water Feasibility",
                "status": "NEEDS_WATER_ASSESSMENT",
                "detail": (
                    f"{crop} seasonal ETc is {etc_min:.0f}–{etc_max:.0f} mm. Rotational canal delivery (Warabandi) "
                    "can satisfy water requirements only if canal rotation intervals align with critical phenological stages "
                    "(e.g. crown root initiation in wheat, flowering in cotton, silking in maize). "
                    "On-ground watercourse turn schedule must be verified."
                ),
            })
            warnings.append(
                f"[NEEDS_WATER_ASSESSMENT]: Rotational canal schedule must align with {crop} critical stages."
            )

    elif water_category in ("ASSURED_PERENNIAL_CANAL", "SWEET_GROUNDWATER_TUBEWELL"):
        water_status = "PASS"
        findings.append({
            "factor": "Irrigation Water Feasibility",
            "status": "PASS",
            "detail": f"Assured irrigation supply can satisfy {crop} seasonal evapotranspiration ({etc_min:.0f}–{etc_max:.0f} mm).",
        })

    # -------------------------------------------------------------------------
    # 5. Determine Factor Statuses & Overall Status Precedence
    # -------------------------------------------------------------------------
    # Deterministic Precedence Hierarchy:
    # 1. SCREENED_OUT (Documented data corruption / pipeline exclusion flag_excluded=True)
    # 2. NEEDS_WATER_ASSESSMENT (Water supply unverified, rainfed, rotational deficit, or unmeasured salinity)
    # 3. UNVERIFIED (Water assured, but soil unmeasured OR extreme edaphic hazard requiring field test)
    # 4. SCREENED_IN (All required biophysical factors verified, present, and passing within tolerance)

    factor_statuses = {
        "data_integrity": "PASS",
        "soil_edaphic": soil_status,
        "thermal_climate": "INFORMATIONAL",
        "heat_stress": "UNVERIFIED",
        "irrigation_water": water_status,
    }

    if is_screened_out:
        final_status = "SCREENED_OUT"
        summary = f"{crop} is SCREENED_OUT based on physiological or data integrity constraints."
    elif water_status == "NEEDS_WATER_ASSESSMENT":
        final_status = "NEEDS_WATER_ASSESSMENT"
        summary = (
            f"{crop} requires on-ground water assessment (NEEDS_WATER_ASSESSMENT). "
            "In arid Sindh, irrigation delivery volumes, water salinity, or rotational canal schedules "
            "must be verified by the user before planting."
        )
    elif soil_missing:
        final_status = "UNVERIFIED"
        summary = (
            f"{crop} is UNVERIFIED. Climatic regime is observed, but district-level soil properties "
            "are unmeasured in the dataset."
        )
    elif soil_status == "SEVERE_HAZARD":
        final_status = "UNVERIFIED"
        summary = (
            f"{crop} is UNVERIFIED (Critical Edaphic Hazard). Measured topsoil pH indicates extreme "
            "chemical stress (<4.5 or >=9.0). Local laboratory soil testing (ESP, ECe) is mandatory "
            "to establish biological feasibility."
        )
    else:
        final_status = "SCREENED_IN"
        summary = (
            f"{crop} is SCREENED_IN. Feasibility criteria pass within tolerance under the provided "
            "inputs. IMPORTANT: SCREENED_IN is strictly a coarse biophysical feasibility screen; "
            "it does NOT guarantee agronomic success, pest/disease freedom, actual water delivery, "
            "realized crop yield, or economic profitability. Stage-specific heat stress remains UNVERIFIED."
        )

    return {
        "crop": crop,
        "status": final_status,
        "factor_statuses": factor_statuses,
        "summary": summary,
        "findings": findings,
        "reasons": reasons,
        "warnings": warnings,
        "evidence": evidence_refs,
        "historical_yield_summary": _compute_historical_yield_summary(df, district, crop),
    }


def _compute_historical_yield_summary(df: pd.DataFrame, district: str, crop: str) -> Optional[Dict[str, Any]]:
    """
    Compute empirical historical yield distribution as supporting historical context.
    Strictly avoids treating historical yield as a suitability score.
    """
    dist_crop_mask = (
        (df["District"].str.strip().str.lower() == district.strip().lower())
        & (df["Crop"].str.strip() == crop)
        & (~df["flag_excluded"].fillna(False))
    )
    subset = df[dist_crop_mask]
    if subset.empty:
        return None

    # Use cotton converted tonnes/ha if Cotton, else Yield (MT/ha)
    if crop == "Cotton":
        col_name = "cotton_yield_t_ha" if "cotton_yield_t_ha" in subset.columns else ("Yield" if "Yield" in subset.columns else None)
        yield_series = pd.to_numeric(subset[col_name], errors="coerce").dropna() if col_name else pd.Series([], dtype=float)
        unit_str = "Metric Tonnes / Hectare (Converted from Bales)"
    else:
        yield_series = pd.to_numeric(subset["Yield"], errors="coerce").dropna() if "Yield" in subset.columns else pd.Series([], dtype=float)
        unit_str = "Metric Tonnes / Hectare"

    n_total = len(yield_series)
    if n_total == 0:
        return None

    n_zeros = int((yield_series == 0).sum())
    mean_val = float(yield_series.mean())
    std_val = float(yield_series.std(ddof=0))
    cv_val = float(std_val / mean_val) if mean_val > 0 else 0.0

    p10 = float(yield_series.quantile(0.10))
    p50 = float(yield_series.median())
    p90 = float(yield_series.quantile(0.90))

    years = pd.to_numeric(subset["Year_start"], errors="coerce").dropna()
    year_range_str = f"{int(years.min())}–{int(years.max())}" if not years.empty else "Unknown"
    has_boundary_instability = bool(subset.get("flag_boundary_instability", pd.Series([False])).fillna(False).any())
    boundary_notes = [str(n) for n in subset.get("reporting_regime_note", pd.Series([])).dropna().unique()]

    return {
        "crop": crop,
        "district": district,
        "yield_unit": unit_str,
        "observed_crop_years": n_total,
        "observed_year_range": year_range_str,
        "zero_yield_years": n_zeros,
        "boundary_instability_detected": has_boundary_instability,
        "boundary_regime_notes": boundary_notes,
        "p10_yield": round(p10, 3),
        "median_yield_p50": round(p50, 3),
        "p90_yield": round(p90, 3),
        "mean_yield": round(mean_val, 3),
        "yield_cv_stability": round(cv_val, 3),
        "disclaimer": (
            "Historical yield statistics reflect past realized output influenced by weather, "
            "subsidies, water allocation, and pest infestations. They are NOT a direct measure of "
            "biological suitability and do NOT guarantee future yields. Missing district-crop-year "
            "combinations are unobserved in the source panel and are NOT treated as zero yield."
        ),
    }
