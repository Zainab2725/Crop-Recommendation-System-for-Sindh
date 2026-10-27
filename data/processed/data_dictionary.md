# Fajr-e-Kisht: Research Dataset Data Dictionary
**File:** `data/processed/research_dataset.csv`
**Generated:** 2026-10-26
**Pipeline:** `src/data/build_research_dataset.py`
**Source:** `data/raw/pbs_weather_soil_1981_2025.csv` (SHA-256: b7362d3154c42738191690b8f73add9e9c0ed9850891891ea91fb137bffc13ff)

---

## Column Definitions

### Traceability
| Column | Type | Description |
|:---|:---|:---|
| `source_row` | int | 1-based row number in the source CSV (including header). Row 2 = first data row. |

### Geographic & Crop Identifiers (from PBS API)
| Column | Type | Unit / Values | Notes |
|:---|:---|:---|:---|
| `Province` | str | "Sindh" | All rows are Sindh province |
| `Division` | str | Division name | PBS API division label |
| `District` | str | District name | PBS API district label. 24 unique districts in source. |
| `District_ID` | str | PBS numeric code | E.g. "069" = Thatta, "152" = Sujawal |
| `Crop` | str | Wheat / Rice / Cotton / Sugarcane / Maize | 5 crops |
| `Year` | str | "1981-82" to "2024-25" | Pakistani fiscal crop year (Kharif or Rabi) |
| `Year_start` | int | 1981–2024 | Start calendar year of the crop season |

### Crop Production Targets (from PBS API)
| Column | Type | Unit | Notes |
|:---|:---|:---|:---|
| `Area` | float | '000 Hectares (thousand ha) | Sown/harvested area. Missing only for excluded rows. |
| `Production` | float | '000 Metric Tonnes (Wheat, Rice, Sugarcane, Maize) OR '000 Bales-170kg (Cotton) | **UNIT HETEROGENEITY: Cotton is in thousand 375-lb lint bales, not metric tonnes.** See `cotton_prod_k_tonnes` for converted value. |
| `Yield` | float | MT/Ha (Wheat, Rice, Sugarcane, Maize) OR Bales/Ha (Cotton) | Derived as Production/Area. **Cotton yield is in bales/ha, not t/ha.** |

### Cotton Unit Conversions (derived, not original)
| Column | Type | Unit | Notes |
|:---|:---|:---|:---|
| `cotton_prod_k_tonnes` | float | '000 Metric Tonnes | Cotton Production × 0.170097. Empty for non-Cotton rows. |
| `cotton_yield_t_ha` | float | Metric Tonnes/Ha | Cotton Yield × 0.170097. Empty for non-Cotton rows. |

### Climate Features (from NASA MERRA-2 / POWER, aggregated over crop growing window)
| Column | Type | Unit | Notes |
|:---|:---|:---|:---|
| `tmean` | float | °C | Mean daily temperature over crop season |
| `tmax_mean` | float | °C | Mean daily maximum temperature |
| `tmin_mean` | float | °C | Mean daily minimum temperature |
| `heat_days` | int | Days | Days with Tmax > 35°C |
| `cold_days` | int | Days | Days with Tmin < 5°C |
| `rain_total` | float | mm | Total seasonal rainfall |
| `rain_days` | int | Days | Days with rainfall > 0 mm |
| `rh_mean` | float | % | Mean relative humidity |
| `solar_mean` | float | MJ/m²/day | Mean solar radiation (NASA SRB). Missing for ~141 rows in 1981–1983 (satellite gap). |
| `wind_mean` | float | m/s | Mean wind speed |
| `n_days` | int | Days | Length of crop growing window (Maize:153, Rice:183, Cotton:214, Wheat:181-182, Sugarcane:365-366) |
| `season_complete` | bool | True/False | True for all 3,242 rows (all seasons fully observed) |

### Soil Properties (static per district, from ISRIC/SoilGrids — 10 of 24 districts only)
| Column | Type | Unit | Notes |
|:---|:---|:---|:---|
| `soil_ph` | float | pH units | Missing for 14 districts (structural gap). |
| `soil_organic_carbon` | float | g/kg | Static per district (zero temporal variation). |
| `soil_clay_pct` | float | % | clay + sand + silt = 100% verified |
| `soil_sand_pct` | float | % | |
| `soil_silt_pct` | float | % | |

### Quality Flags (derived in Phase 3E pipeline)
| Column | Type | Description |
|:---|:---|:---|
| `flag_excluded` | bool | True = row excluded from primary research dataset (appears in exclusion_ledger.csv) |
| `flag_sujawal_rice_contaminated` | bool | True = Sujawal Rice row known/suspected to contain Sindh provincial aggregate |
| `flag_zero_prod_nonzero_area` | bool | True = Production=0 with Area>0 (genuine agricultural failure, retained) |
| `flag_solar_missing_1981_83` | bool | True = solar_mean is missing due to satellite sensor gap (1981–1983) |
| `flag_boundary_instability` | bool | True = district reporting regime changed during the panel (administrative split) |
| `flag_cotton_unit_mismatch` | bool | True = Production/Yield are in bale units, not metric tonnes (all Cotton rows) |
| `flag_area_missing` | bool | True = Area is null/missing |
| `flag_yield_missing` | bool | True = Yield is null/missing (and Area is not null) |
| `flag_soil_missing` | bool | True = all 5 soil columns are null for this row |
| `geographic_comparability` | str | STABLE / PRE_SPLIT_PARENT | Whether district boundary was stable in this year |
| `reporting_regime_note` | str | Human-readable explanation of boundary change, if any | |

---

## Known Limitations and Caveats

1. **Sujawal Rice (19 rows):** Excluded. Provincial aggregate, not district data.
2. **Thatta Rice (0 rows in this dataset):** The PBS API returns no Thatta Rice data.
   Historical Thatta Rice (1981-82 to 2008-09) is available separately in
   `reports/phase3d/thatta_rice_verified.csv` (28 rows, undivided district).
3. **Cotton units:** Production and Yield are in bale units. Use `cotton_prod_k_tonnes`
   and `cotton_yield_t_ha` for metric comparisons.
4. **Soil data:** Missing for 14 of 24 districts. Do not treat as zero.
5. **Boundary instability:** Multiple administrative splits occurred in 2004-2006 and 2013.
   Pre-split parent districts contain area for territories later assigned to child districts.
   ML models must not treat the resulting step-changes as agronomic signals.
6. **Solar gap:** 141 rows (1981–1983) lack `solar_mean`. This is a known satellite
   sensor artifact, not a data collection failure.
7. **Missing combinations:** 2,038+ theoretical district-crop-year combinations are absent
   from the source. Absence cannot be equated to zero cultivation without additional evidence.
8. **Labels vs. Suitability:** Area, Production, and Yield describe historical cultivation
   outcomes, not agronomic potential. They are influenced by water access, market prices,
   government policy, climate, and technology. They are NOT equivalent to crop suitability scores.
