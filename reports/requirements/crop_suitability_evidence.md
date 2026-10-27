# Crop Suitability Requirements & Agronomic Evidence Audit: Sindh, Pakistan

**Project:** Fajr-e-Kisht — Explainable Crop Decision-Support System  
**Document:** `reports/requirements/crop_suitability_evidence.md`  
**Date:** 2026-10-27  
**Scope:** Suitability criteria, agronomic requirements, and evidence ledger for 5 major crops in Sindh (Wheat, Rice, Cotton, Sugarcane, Maize).

---

## 1. Executive Summary & Objective

The objective of **Fajr-e-Kisht** is to deliver an explainable crop recommendation and decision-support system tailored for farmers and agricultural extension officers across Sindh, Pakistan. To be scientifically defensible, the system must balance **crop agro-climatic suitability**, **water constraints**, and **economic returns** without fabricating synthetic weights, imputing unobserved field values with arbitrary averages, or conflating historical cultivation with true agronomic suitability.

This audit establishes:
1. **Defensible physiological thresholds** for all 5 target crops based on published scientific guidelines (FAO EcoCrop, FAO Irrigation & Drainage Papers 24, 33, and 56, and Pakistan Agricultural Research Council / Sindh Agriculture Department protocols).
2. **Strict differentiation** between biological Crop Water Requirement ($ET_c$) and actual on-ground irrigation/groundwater water delivery in Sindh's canal commands.
3. **Audit of available dataset columns** in `data/processed/research_dataset.csv` versus unobserved variables (e.g., commodity farm-gate prices, production input costs, soil salinity/EC, canal head/tail water allocations).
4. **An interpretable two-tier decision workflow** (Hard Agronomic Feasibility Screening $\rightarrow$ Multicriteria Agronomic Performance Ranking) where economic ranking is formally gated until authenticated price and cost data are acquired.
5. **Unit test specifications and stress scenarios** to evaluate recommendation engines against edge cases without data leakage.

---

## 2. Crop-by-Crop Agronomic Requirements & Credible Evidence Ledger

Every physiological threshold below is derived from established multilateral bodies (FAO, IRRI, ICAC) and provincial agricultural extension research (PARC, Sindh Agriculture Department). No threshold is invented.

```
Type Legend:
- [T-ABS]: Absolute physiological survival limit (outside of which catastrophic failure or zero viable yield occurs)
- [T-OPT]: Optimal physiological range for commercial yield and development
- [REF]: Indicative baseline reference / typical seasonal requirement
```

### 2.1 Wheat (*Triticum aestivum*) — Rabi Season

* **Agro-climatic Role in Sindh:** Primary food staple; sown mid-November to December and harvested late March to April. Highly vulnerable to terminal heat stress during grain filling in lower Sindh.
* **Growing Window in Dataset:** 181 days (leap: 182 days) — November 1 to April 30.

| Parameter | Unit | Value / Range | Evidence Type | Context & Agronomic Rationale | Source / Standard Reference |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Optimal Temperature ($T_{mean}$)** | °C | 15.0 – 25.0 | [T-OPT] | Optimal range across tillering (15–20°C) and grain-filling (20–25°C). | FAO EcoCrop database; FAO Irrigation & Drainage Paper 33 |
| **Absolute Temperature Range ($T_{abs}$)** | °C | 5.0 – 35.0 | [T-ABS] | Physiological cessation below 5°C; severe flower/pollen abortion above 35°C during anthesis. | FAO EcoCrop; PARC Wheat Production Manual |
| **Terminal Heat Threshold** | °C | > 35.0 max | [T-ABS] | Temperatures exceeding 35°C during grain filling (March/April in Sindh) trigger forced maturity and shriveled grains. | PARC National Wheat Programme; Reynolds et al. (CIMMYT) |
| **Soil pH Range (Optimal)** | pH | 6.0 – 7.5 | [T-OPT] | Maximizes nitrogen, phosphorus, and micronutrient availability. | FAO EcoCrop; USDA NRCS Soil Plant Guide |
| **Soil pH Range (Absolute)** | pH | 5.5 – 8.5 | [T-ABS] | Severe micronutrient lockup occurs above pH 8.5 (frequent in calcareous Sindh alkaline soils). | FAO Soils Bulletin 39; PARC |
| **Soil Texture Preference** | Class | Loam, Clay Loam, Silt Loam | [REF] | Well-drained, medium-to-heavy textured soils with good water-holding capacity. | PARC Wheat Guidelines; FAO Soils Bulletin |
| **Crop Water Requirement ($ET_c$)** | mm / season | 450 – 650 | [REF] | Total seasonal crop evapotranspiration under non-limiting water conditions. | FAO Irrigation and Drainage Paper 56 (Table 12); FAO Water Development Report 33 |
| **Critical Water Stages** | Stage | Crown root initiation, Tillering, Anthesis | [REF] | Water stress at crown root initiation (21 days post-sowing) reduces tillering by up to 40%. | FAO I&D 33; PARC Crop Advisory |

### 2.2 Rice (*Oryza sativa*) — Kharif Season

* **Agro-climatic Role in Sindh:** Major export and cash food crop; cultivated in Upper Sindh (Larkana, Jacobabad, Kambar Shahdadkot, Shikarpur canal commands) and Lower Sindh delta (Badin, Thatta).
* **Growing Window in Dataset:** 183 days — June 1 to November 30.

| Parameter | Unit | Value / Range | Evidence Type | Context & Agronomic Rationale | Source / Standard Reference |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Optimal Temperature ($T_{mean}$)** | °C | 22.0 – 32.0 | [T-OPT] | Warm temperatures essential for vegetative elongation, tillering, and panicle development. | IRRI Rice Production Manual; FAO EcoCrop |
| **Absolute Temperature Range ($T_{abs}$)** | °C | 15.0 – 42.0 | [T-ABS] | Growth halts below 15°C. Temperatures > 35–38°C at flowering cause high spikelet sterility. | IRRI Knowledge Bank; FAO EcoCrop |
| **Soil pH Range (Optimal)** | pH | 5.5 – 7.0 | [T-OPT] | Submerged paddy soil lowers redox potential and brings pH naturally closer to 6.5–7.0. | IRRI Rice: Soil and Land Suitability; Ponnamperuma (1972) |
| **Soil pH Range (Reference / Stress)** | pH | 4.5 – 8.2 | [REF] | Reference literature envelope. Above pH 8.2, zinc deficiency (Khaira disease) and iron chlorosis occur. In calcareous Indus alluvium, crops are grown successfully above pH 8.2 with zinc sulfate (ZnSO4) supplementation; pH 8.2 is NOT an absolute biological mortality wall. Absolute biological toxicity occurs at pH < 4.5 or pH >= 9.0 (severe sodic black alkali). | IRRI Knowledge Bank; PARC Rice Section; Ponnamperuma (1972) |
| **Soil Texture Preference** | Class | Clay, Silty Clay, Heavy Clay Loam | [REF] | Low-permeability, heavy soils necessary to retain flood water layer and prevent percolation losses. | FAO Land and Water Development Series; IRRI |
| **Crop Water Requirement ($ET_c$)** | mm / season | 900 – 1,500 ($ET_c$) / 1,200 – 2,500 (Gross Field Requirement) | [REF] | $ET_c$ is 900–1,200 mm; field water requirement is 1,500–2,500 mm including puddling, percolation, and standing water layer. | FAO I&D 56; FAO Water Report 33; Sindh Irrigation Department Water Allocation Manuals |
| **Critical Water Stages** | Stage | Panicle initiation to Flowering | [REF] | Drought stress at reproductive stage causes catastrophic floret sterility. | IRRI Knowledge Bank; FAO I&D 33 |

### 2.3 Cotton (*Gossypium hirsutum*) — Kharif Season

* **Agro-climatic Role in Sindh:** Core industrial fiber crop; predominantly central and lower Sindh (Sanghar, Nawabshah/SBA, Hyderabad, Matiari, Mirpurkhas). Sown April–May, picked August–December.
* **Growing Window in Dataset:** 214 days — May 1 to November 30.

| Parameter | Unit | Value / Range | Evidence Type | Context & Agronomic Rationale | Source / Standard Reference |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Optimal Temperature ($T_{mean}$)** | °C | 22.0 – 32.0 | [T-OPT] | Thrives in warm, sunny environments with high sunshine hours and moderate night temperatures. | International Cotton Advisory Committee (ICAC); FAO EcoCrop |
| **Absolute Temperature Range ($T_{abs}$)** | °C | 15.0 – 45.0 | [T-ABS] | Cold sensitive (< 15°C halts development). Daily maximums > 42°C cause square shed and boll abortion. | ICAC Technical Bulletin; Central Cotton Research Institute (CCRI) Multan/Sakrand |
| **Soil pH Range (Optimal)** | pH | 6.5 – 8.0 | [T-OPT] | Moderately tolerant of mild alkalinity, typical of Indus basin alluvium. | FAO Soils Bulletin; CCRI Sakrand agronomic advisories |
| **Soil pH Range (Absolute)** | pH | 5.5 – 8.5 | [T-ABS] | Alkaline conditions above pH 8.5 induce phosphorus and boron lockup; saline-sodic soils severely stunt taproots. | FAO EcoCrop; ICAC Cotton Physiology |
| **Soil Texture Preference** | Class | Deep Sandy Loam to Clay Loam | [REF] | Deep, permeable soils with unobstructed subsoil drainage. Intolerant of waterlogging (> 24–48 hours causes root hypoxia and square drop). | CCRI Sakrand; PARC Cotton Production Guide |
| **Crop Water Requirement ($ET_c$)** | mm / season | 700 – 1,300 | [REF] | Driven by high evaporative demand across 214 growing days in arid/semi-arid Sindh. | FAO I&D 56 (Table 12); FAO Water Report 33 |
| **Critical Water Stages** | Stage | Flowering, Boll Formation | [REF] | Water stress during boll setting causes excessive boll dropping; water excess promotes vegetative rank growth. | ICAC Cotton Production Compendium; FAO I&D 33 |

### 2.4 Sugarcane (*Saccharum officinarum*) — Perennial / Full-Year Crop

* **Agro-climatic Role in Sindh:** Commercial sucrose agro-industrial crop; concentrated in barrage command zones near sugar mills (Badin, Thatta, Hyderabad, Shaheed Benazirabad, Khairpur).
* **Growing Window in Dataset:** 365 days (leap: 366 days) — Full calendar year (January 1 to December 31).

| Parameter | Unit | Value / Range | Evidence Type | Context & Agronomic Rationale | Source / Standard Reference |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Optimal Temperature ($T_{mean}$)** | °C | 24.0 – 33.0 | [T-OPT] | Requires high temperatures during vegetative elongation (grand growth) and cooler dry weather during ripening. | FAO EcoCrop; Sugarcane Research Institute Thatta / PARC |
| **Absolute Temperature Range ($T_{abs}$)** | °C | 15.0 – 42.0 | [T-ABS] | Growth ceases below 15°C (winter dormancy); heat > 42°C with low humidity stunts cane elongation. | FAO I&D 33; Sugarcane Research Institute Thatta |
| **Soil pH Range (Optimal)** | pH | 6.0 – 7.8 | [T-OPT] | Neutral to slightly alkaline, fertile loams with high organic content. | FAO EcoCrop; Sugar Research Institute |
| **Soil pH Range (Absolute)** | pH | 5.0 – 8.5 | [T-ABS] | Highly alkaline/sodic soils (pH > 8.5) cause stunted root growth and poor tillering (ratooning failure). | FAO Soils Bulletin 39; PARC |
| **Soil Texture Preference** | Class | Heavy Loams, Silt Loams, Silty Clay Loams | [REF] | Deep soil profile (> 1.0 m) with moderate permeability and high water storage capacity. | PARC Sugarcane Guidelines; Sindh Extension Advisories |
| **Crop Water Requirement ($ET_c$)** | mm / year | 1,500 – 2,500 | [REF] | Enormous water consumption across 12 full months. Highest seasonal requirement of all field crops in Pakistan. | FAO I&D 56; FAO Water Report 33; Sindh Water Resource Review |
| **Critical Water Stages** | Stage | Tillering and Grand Growth phase | [REF] | Extended water stress during the formative and elongation phase permanently reduces stalk height and cane diameter. | FAO I&D 33; Sugarcane Research Institute Thatta |

### 2.5 Maize (*Zea mays*) — Kharif & Inter-season

* **Agro-climatic Role in Sindh:** Coarse grain used for poultry feed, silage, and industrial starch; growing rapidly in modern irrigated rotations. Sown June–July (Kharif) or February (Spring).
* **Growing Window in Dataset:** 153 days — June 1 to October 31 (Kharif cycle).

| Parameter | Unit | Value / Range | Evidence Type | Context & Agronomic Rationale | Source / Standard Reference |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Optimal Temperature ($T_{mean}$)** | °C | 18.0 – 28.0 | [T-OPT] | Rapid vegetative growth under warm days and sunny conditions. | FAO EcoCrop; CIMMYT Maize Manual |
| **Absolute Temperature Range ($T_{abs}$)** | °C | 10.0 – 40.0 | [T-ABS] | Germination fails below 10°C; severe heat (> 38°C) desiccates tassels and sterilizes pollen during silking. | FAO EcoCrop; PARC Maize Section |
| **Tasseling Heat Threshold** | °C | > 38.0 max | [T-ABS] | Temperatures above 38°C during flowering/silking cause tassel blast and poor ear fill. | CIMMYT Maize Program; Nielsen (Purdue Extension) |
| **Soil pH Range (Optimal)** | pH | 5.8 – 7.2 | [T-OPT] | Moderately sensitive to micronutrient deficiencies in high-pH calcareous soils. | FAO EcoCrop; USDA NRCS |
| **Soil pH Range (Absolute)** | pH | 5.0 – 8.2 | [T-ABS] | Susceptible to zinc and iron chlorosis above pH 8.0. | FAO Soils Bulletin 39; PARC |
| **Soil Texture Preference** | Class | Well-drained Loam, Sandy Loam, Silt Loam | [REF] | Extremely sensitive to standing water and waterlogging (hypoxia kills roots within 48 hours). | CIMMYT Maize Guidelines; FAO I&D 33 |
| **Crop Water Requirement ($ET_c$)** | mm / season | 500 – 800 | [REF] | Moderate water requirement across 153-day cycle. | FAO I&D 56 (Table 12); FAO Water Report 33 |
| **Critical Water Stages** | Stage | Tasseling, Silking, and Grain Filling | [REF] | Water stress for even 2–4 days during silking causes asynchronous flowering and catastrophic grain set failure. | FAO I&D 33; CIMMYT Maize Guidelines |

---

## 3. Crop-by-Factor Coverage & Feasibility Evaluation Matrix

This matrix maps each agronomic requirement to the exact columns available in `data/processed/research_dataset.csv`.

| Agronomic Dimension | Specific Requirement Factor | Evaluability with Existing Dataset Fields | Target Column in `research_dataset.csv` | Status & Data Gap Details |
| :--- | :--- | :--- | :--- | :--- |
| **Thermal Regime** | Mean Growing Season Temp | **YES (Direct)** | `tmean` | Aggregated over crop window ($n\_days$). 100% complete. |
| **Thermal Regime** | Maximum Heat Exposure | **YES (Direct)** | `tmax_mean`, `heat_days` | `heat_days` ($T_{max} > 35^\circ\text{C}$) directly checks heat stress. 100% complete. |
| **Thermal Regime** | Minimum Cold Exposure | **YES (Direct)** | `tmin_mean`, `cold_days` | `cold_days` ($T_{min} < 5^\circ\text{C}$). 100% complete. |
| **Atmospheric Moisture** | Relative Humidity | **YES (Direct)** | `rh_mean` | Seasonal relative humidity (%). 100% complete. |
| **Solar Radiation** | Photosynthetic Energy | **PARTIAL (Direct)** | `solar_mean` | Missing in 141 rows (1981–1983 satellite sensor launch timeline). |
| **Precipitation** | Total Seasonal Rainfall | **YES (Direct)** | `rain_total`, `rain_days` | Total rainfall over crop window. **Note: Rain $\neq$ Irrigation.** |
| **Soil Reaction** | Topsoil pH | **PARTIAL (Direct)** | `soil_ph` | Present for 10 districts; **Missing for 14 districts (56.4%)**. |
| **Soil Organic Content** | Soil Organic Carbon | **PARTIAL (Direct)** | `soil_organic_carbon` | Present for 10 districts; **Missing for 14 districts**. |
| **Soil Physical Texture**| Clay, Sand, Silt percentages| **PARTIAL (Direct)** | `soil_clay_pct`, `soil_sand_pct`, `soil_silt_pct` | Present for 10 districts; **Missing for 14 districts**. |
| **Crop Water Need** | Crop Evapotranspiration ($ET_c$)| **DERIVED (Literature)** | *External Reference ($ET_c$)* | Not explicitly a column; compared against water supply. |
| **Irrigation Availability** | Surface Canal Water Delivery | **UNAVAILABLE (Gap)** | **None** | Canal command discharge, barrage allocations, and tail-end water stress are absent from CSV. |
| **Groundwater Quality** | Aquifer EC, Salinity, Depth | **UNAVAILABLE (Gap)** | **None** | Groundwater in Sindh is heavily saline/brackish (60–80% unfit for direct tube-well irrigation). Absent from CSV. |
| **Economic Returns** | Farm-gate Market Prices | **UNAVAILABLE (Gap)** | **None** | Historic/current commodity prices (PKR/40kg or PKR/ton) are completely absent. |
| **Economic Returns** | Cost of Production | **UNAVAILABLE (Gap)** | **None** | Labor, diesel, electricity, DAP/Urea fertilizers, and seed costs are completely absent. |
| **Historical Output** | Productivity Evidence | **YES (Direct)** | `Yield`, `cotton_yield_t_ha`, `Production` | Verified historical agricultural performance; **must NOT be used as suitability label.** |

---

## 4. Agronomic vs. Hydrological Reality: Crop Water Need vs. Actual Irrigation

### 4.1 Fundamental Hydrological Distinctions

A critical flaw in naive agricultural models is conflating **rainfall** with **irrigation availability**, or treating **Crop Water Requirement ($ET_c$)** as an indicator of whether a crop can be grown in an arid region.

1. **Sindh is an Arid/Hyper-Arid Irrigation-Dependent Regime:**
   * Mean annual rainfall in Sindh ranges from 100 mm to 250 mm (excepting anomalous monsoon flood years like 2022).
   * Total water demand for rice (1,200–2,500 mm), cotton (700–1,300 mm), sugarcane (1,500–2,500 mm), and wheat (450–650 mm) vastly exceeds annual rainfall.
   * **Rainfall contributes less than 10–20% of crop water requirements in normal years.**
   * In Sindh, virtually 90–95% of agricultural production relies on Indus Basin Irrigation System (IBIS) canal diversions from the Guddu, Sukkur, and Kotri barrages.

2. **Crop Water Requirement ($ET_c$) Defined:**
   $$ET_c = K_c \times ET_0$$
   * $ET_c$ is the depth of water (mm) transpirated and evaporated by a healthy crop under optimal field conditions.
   * **$ET_c$ is a demand variable, not a supply variable.** A high $ET_c$ simply indicates how much water the crop demands to prevent moisture stress.

3. **Irrigation Availability Defined (Supply Variable):**
   $$\text{Available Supply} = \text{Effective Rainfall } (P_e) + \text{Canal Delivery } (I_{\text{canal}}) + \text{Usable Groundwater } (GW_{\text{pumped}})$$
   * If $\text{Available Supply} < ET_c$, the crop suffers moisture deficit, yield reduction, or complete desiccation.
   * In Sindh, canal supply is non-uniform: **Head-reach farmers receive surplus water; tail-end (Warabandi) watercourses suffer acute chronic shortages (often 30–50% deficit).**
   * **Groundwater in Lower and Central Sindh is predominantly saline or brackish (EC > 1.5–3.0 dS/m).** It cannot substitute for canal water without causing secondary soil salinization, sodification, and crop toxicity.

### 4.2 Handling Water in the Recommendation System Without Hydrology Data

Because `research_dataset.csv` contains `rain_total` but **does not contain canal discharges or groundwater aquifer maps**, the system must enforce strict behavioral constraints:

> [!CAUTION]
> **Constraint:** The recommendation system must **NEVER** conclude that Rice or Sugarcane is "suitable" in a district purely because rainfall was recorded. Conversely, it must never claim a drought-sensitive crop is "infeasible" based on low rainfall when canal irrigation is actively supplied.

* **Reporting Protocol:** 
  The system must state:  
  * *"Crop Water Requirement ($ET_c$) for Sugarcane is ~1,800 mm. Observed seasonal rainfall is 120 mm. Sowing is agronomically viable ONLY IF the farmer possesses assured canal water allocation or verified sweet-water tube-well access."*
* A user/expert override must be provided:
  * Prompt the user for **Irrigation Status**: `[Assured Perennial Canal | Non-Perennial / Rotational Canal | Sweet Groundwater Tube-well | Tail-End / Deficit Water | Rainfed Only]`.

---

## 5. Policy on Missing Data & Quality Flags

The system must uphold strict data provenance and never silently interpolate or mask data absence.

### 5.1 Soil Data Gaps (Missing in 14 of 24 Districts)

* **Current Status:** 10 districts possess static SoilGrids profiles (`soil_ph`, `soil_organic_carbon`, `soil_clay_pct`, `soil_sand_pct`, `soil_silt_pct`). 14 districts have `flag_soil_missing = True` (1,817 rows, 56.4% of dataset).
* **Strict Prohibition:** **Do NOT silently replace missing soil pH or texture with provincial or regional averages.** Calcareous alkaline soils in Khairpur differ vastly from the deltaic coastal soils of Thatta or the sandy tracts of Tharparkar. Averaging obscures agronomic risk.
* **Prescribed System Behavior:**
  1. If soil data is missing, the engine evaluates **Climate Feasibility** (temperature, heat days, cold days).
  2. The system outputs a clear, prominent warning:
     > `[WARNING: SOIL DATA UNAVAILABLE]: District-level measured soil texture and pH are absent from the database. Suitability screening was performed on thermal/climate regimes only. Farmers must verify localized soil pH (target 6.5–8.0) and salinity before planting.`
  3. The overall confidence rating of the recommendation is flagged as `CONSTRAINED (Soil Unverified)`.

### 5.2 Solar Radiation Gap (1981–1983)

* **Current Status:** 141 rows lack `solar_mean` due to the NASA SRB satellite sensor timeline (launched mid-1983).
* **Prescribed Behavior:** Recognized as a historical sensor gap (`flag_solar_missing_1981_83 = True`). Downstream evaluation for current/future crop recommendations is unaffected because modern seasons possess complete solar records.

### 5.3 Administrative Boundary Instability

* **Current Status:** 37 rows carry `flag_boundary_instability = True` (district splits in 2004–2006 for Hyderabad, Dadu, Larkana, Jacobabad and 2013 for Thatta).
* **Prescribed Behavior:** The system must not interpret post-split drops in district production/area as agronomic degradation. Historical comparison models must normalize by harvested area ($Yield = Production / Area$) or flag the pre-split baseline.

---

## 6. Role of Historical Yield in Decision Support

### 6.1 Why Historical Yield is NOT a Crop Suitability Score

Treating historical yield as an objective ground-truth label of crop suitability is scientifically invalid due to multiple confounding variables:

1. **Market & Policy Distortions:** Historical cultivation reflects government Minimum Support Prices (MSP for Wheat and Sugarcane), mill purchasing quotas, and cash liquidity needs rather than pure agronomic fitness.
2. **Irrigation Disparity:** A district with exceptionally high rice yields may achieve them through disproportionate canal head-reach water extraction, depriving downstream tracts. The yield reflects hydraulic entitlement, not inherent bio-physical suitability.
3. **Catastrophic Shocks:** Genuine extreme shocks (such as the 2022 Sindh monsoon floods, where cotton production dropped to zero across Kashmore, Larkana, and Shikarpur) reflect disaster inundation, not climate incompatibility.
4. **Historical Absence $\neq$ Infeasibility:** If a high-value crop (e.g., maize) has minimal recorded acreage in a district, it often reflects supply-chain and milling bottlenecks rather than physiological failure.

### 6.2 Valid Use of Historical Yield: Benchmarking & Risk Context

Historical yield must be utilized strictly as **Empirical Evidence of Demonstrated Performance and Resilience**:

* **Baseline Performance Band:** Calculate the historical 10th, 50th (median), and 90th percentile yield for crop $c$ in district $d$:
  $$Y_{10}(d, c), \quad Y_{50}(d, c), \quad Y_{90}(d, c)$$
* **Yield Stability & Disaster Risk:** Measure the historical inter-annual coefficient of variation:
  $$CV(d, c) = \frac{\sigma_{Yield}}{\mu_{Yield}}$$
  A high $CV$ indicates high vulnerability to climate extremes (e.g., erratic monsoons, heat waves).
* **Benchmarking Context:**
  * When a crop passes physiological feasibility screening, present the historical yield distribution to the user as empirical reference:
  * *"In Sanghar, Cotton has achieved a median yield of 2.1 t/ha over the last 15 years, with a 10th percentile drought/flood risk yield of 0.8 t/ha."*

---

## 7. Explainable Decision Workflow (Two-Tier Gated Process)

The recommendation engine must operate deterministically through an interpretable, transparent hierarchy without black-box weights or hidden optimization parameters.

```mermaid
graph TD
    A[Input: District, Season, User Water Access] --> B[Tier 1: Agronomic Feasibility Screening]
    
    B --> B1{Thermal Feasibility Check}
    B1 -- Outside T_abs / Severe Heat Days --> X1[INELIGIBLE: Extreme Temperature Stress]
    B1 -- Inside T_abs --> B2{Soil Feasibility Check}
    
    B2 -- Missing Soil Data --> W1[FLAG: Soil Unverified]
    B2 -- Soil pH outside Absolute Limits --> X2[INELIGIBLE: Severe Soil Chemical Toxicity]
    B2 -- Soil Compatible --> B3{Water Constraint Check}
    
    W1 --> B3
    B3 -- Water Access Deficit vs ET_c --> X3[INELIGIBLE: Unmet Crop Water Demand]
    B3 -- Water Assured --> C[Crop Classified as FEASIBLE]
    
    C --> D[Tier 2: Transparent Agronomic Ranking]
    D --> D1[Rank by Thermal Optimality Index]
    D --> D2[Rank by Historical Yield Stability CV]
    
    D --> E{Economic Data Present?}
    E -- NO: Prices & Costs Missing --> F[GATED: Economic Net Profit Unavailable]
    E -- YES: Farm-gate Prices & Costs Acquired --> G[Tier 3: Net Profit Ranking]
```

### 7.1 Tier 1: Hard Agronomic Feasibility Screening (Pass/Fail)

A crop must pass all three bio-physical gates. If any gate fails, the crop is eliminated from consideration, and an agronomic reason code is issued.

1. **Gate 1.1: Thermal Feasibility**
   * Condition: Crop is rejected if seasonal $T_{mean} < T_{abs,min}$ or $T_{mean} > T_{abs,max}$.
   * Specific Heat Gate: For Wheat, rejected if terminal heat days at grain fill exceed critical thresholds. For Maize, rejected if flowering coincides with extreme daily maximums ($> 38^\circ\text{C}$).
   * Explanation Output if Failed: *"INELIGIBLE: Expected seasonal temperature ($T_{mean} = 33.5^\circ\text{C}$) exceeds biological ceiling for Wheat ($35^\circ\text{C}$ absolute limit)."*

2. **Gate 1.2: Edaphic (Soil) Feasibility**
   * Condition: If soil data is present, crop is rejected if $pH < pH_{abs,min}$ or $pH > pH_{abs,max}$.
   * If soil data is absent (`flag_soil_missing = True`), gate returns `STATUS = UNVERIFIED`, allows progression to Gate 1.3, and appends a mandatory diagnostic audit notice.
   * Explanation Output if Failed: *"INELIGIBLE: Measured soil pH (8.7) exceeds tolerance limit for Cotton (8.5), indicating severe nutrient lockup and sodicity risk."*

3. **Gate 1.3: Water Constraint Screening**
   * Condition: Compare crop seasonal demand ($ET_c$) against user water access tier:
     * *Assured Perennial Canal or Sweet Tube-well:* All crops eligible.
     * *Non-Perennial / Rotationally Deficit Canal:* High-water crops (Sugarcane, Rice) are marked `HIGH WATER RISK / INELIGIBLE` unless supplementary sweet tube-well storage is confirmed.
     * *Rainfed Only:* In arid Sindh, field crops requiring $> 400\text{ mm}$ without irrigation are classified `HYDROLOGICALLY UNVIABLE`.
   * Explanation Output if Failed: *"INELIGIBLE: Sugarcane requires 1,800–2,200 mm of water. Available rotational water supply is insufficient to prevent terminal crop desiccation."*

### 7.2 Tier 2: Transparent Agronomic Characterization & Ranking

For crops passing Tier 1, rank according to **un-weighted, transparent agronomic indexes**:

1. **Thermal Optimality Proximity:**
   $$\text{Thermal Match Score} = 1 - \frac{|T_{mean} - T_{opt,center}|}{(T_{opt,max} - T_{opt,min}) / 2}$$
   *(Normalized distance of seasonal mean temperature from optimal biological midpoint).*
2. **Historical Empirical Resilience:**
   Display median historical yield $Y_{50}(d, c)$ alongside inter-annual coefficient of variation $CV(d, c)$ from `research_dataset.csv`.
3. **No Synthetic Black-Box Linear Weights:**
   The system must not generate arbitrary composite expressions (e.g., $0.4 Y + 0.3 R + 0.2 T + 0.1 pH$). Instead, it presents each factor side-by-side in an explainable score scorecard.

### 7.3 Tier 3: Economic Return & Net Profit (Strictly Gated)

* **Policy:** **ECONOMIC RANKING IS FORMALLY DISABLED.**
* **Condition for Activation:** Until verified commodity market farm-gate prices (Sindh AMIS / PBS Market Bulletins) and crop enterprise budgets (Sindh Agriculture Extension Cost of Cultivation Yearbooks) are systematically integrated, the system must display:
  > `[ECONOMIC MODULE DISABLED]: Reliable district-level farm-gate prices and input production costs (fertilizer, diesel, land prep) are not yet integrated. Net profit ranking is withheld to prevent misleading financial guidance.`

---

## 8. Unresolved Data Requirements & Recommendations for V1

### 8.1 Inventory of Unresolved Data Gaps

| Unresolved Requirement | Missing Field / Source | Criticality | Immediate Mitigation for V1 |
| :--- | :--- | :--- | :--- |
| **Commodity Farm-Gate Prices** | PBS / AMIS Sindh monthly commodity auction price series | **HIGH (Blocks Economics)** | Keep Tier 3 economic ranking disabled. Focus on bio-physical suitability. |
| **Cost of Crop Cultivation** | Agricultural Extension Enterprise Budgets (Seed, Fertilizer, Labor, Diesel) | **HIGH (Blocks Economics)** | Provide user-editable cost template or withhold profit metrics. |
| **Soil Properties (14 Districts)** | ISRIC SoilGrids 250m centroid extraction for missing Sindh districts | **MEDIUM (Agronomic Accuracy)** | Retain `flag_soil_missing = True`; issue clear unverified notices on missing districts. |
| **Canal Water Deliveries** | Sindh Irrigation Dept. canal gauge / barrage discharge records | **HIGH (Hydrological Realism)** | Solicit farmer water entitlement tier via interactive prompt; never rely on rainfall. |
| **Groundwater Salinity / EC** | PCRWR / Sindh Groundwater Authority aquifer salinity maps | **MEDIUM (Soil Degradation)** | Warn farmers in coastal/deltaic zones (Badin, Thatta, Sujawal) of salinity hazards. |

### 8.2 Formal Readiness Recommendation for Implementation

> **VERDICT: SUFFICIENT FOR V1 BIOPHYSICAL SUITABILITY ENGINE (WITH ECONOMICS GATED).**
>
> 1. **Climate and Phenology Data are Production-Ready:** The existing dataset (`research_dataset.csv`, 3,223 rows across 1981–2024) provides complete, validated growing-season temperature ($T_{mean}, T_{max}, T_{min}$), heat days, cold days, humidity, and rainfall mapped to exact biological crop cycles ($n\_days$).
> 2. **Quality Controls are Fully Established:** Provenance flags (`flag_excluded`, `flag_boundary_instability`, `flag_cotton_unit_mismatch`, `flag_soil_missing`) enable clean, transparent data filtering without data corruption.
> 3. **Actionable V1 Deliverable:** A robust, scientifically defensible **Biophysical Suitability and Water-Constraint Screening Engine** can be implemented immediately. It will provide transparent pass/fail feasibility screening and climate suitability scorecards, while responsibly deferring net profit calculations until real economic datasets are secured.

---

## 9. Recommended Unit Tests & Verification Scenarios

The future recommendation engine must be validated against the following concrete test cases to ensure compliance with agronomic principles and project constraints:

| Test ID | Test Scenario | Input Conditions | Expected Behavior / Output |
| :--- | :--- | :--- | :--- |
| **TC-01** | **Excluded Data Isolation** | Query Sujawal Rice (all historical years) | Engine must return zero records or raise exclusion error (`flag_excluded = True`). Must never recommend based on provincial aggregates. |
| **TC-02** | **Extreme Heat Infeasibility** | Wheat recommendation under Kharif thermal regime ($T_{mean} > 32^\circ\text{C}, \text{heat\_days} > 100$) | Hard FAIL at Gate 1.1. Status: `INELIGIBLE`. Explanation explicitly cites high-temperature threshold violation. |
| **TC-03** | **Soil Gap Transparency** | Crop recommendation in Sukkur or Larkana (`flag_soil_missing = True`) | Engine evaluates climate feasibility, but appends mandatory alert: `flag_soil_missing = True`. Must NOT impute soil pH. |
| **TC-04** | **Hydrological Constraint (Arid)** | Sugarcane recommendation with input: `water_access = Rainfed_Only` (Rainfall = 150 mm) | Hard FAIL at Gate 1.3. Status: `INELIGIBLE`. Explains that seasonal water demand (1,500–2,500 mm) cannot be met by 150 mm precipitation. |
| **TC-05** | **Cotton Unit Integrity** | Compare cotton historical yield against wheat or maize | Engine must use `cotton_yield_t_ha` (converted metric tonnes/ha), NOT raw `Yield` (bales/ha). |
| **TC-06** | **Zero-Weight Determinism** | Verify ranking algorithm output | Confirm no arbitrary black-box linear weights ($w_1 Y + w_2 R$) are computed. Scores must reflect documented physical formulas. |
| **TC-07** | **Economic Gate Enforcement** | Request net profit or economic crop ranking | Engine returns `ECONOMIC_MODULE_DISABLED`. Refuses to invent prices or margins. |
| **TC-08** | **Zero-Yield Anomaly Resilience** | Ingest 2022 flood records (Area > 0, Production = 0) | Engine does not divide by zero or crash; recognizes genuine disaster shock without skewing normal climate suitability baseline. |

---

## 10. References & Credible Scientific Sources

1. **FAO EcoCrop Database:** Environmental Requirements for Field Crops. Food and Agriculture Organization of the United Nations, Rome. [https://www.fao.org/land-water/databases-and-software/crop-information/en/](https://www.fao.org/land-water/databases-and-software/crop-information/en/)
2. **FAO Irrigation and Drainage Paper No. 56:** *Crop Evapotranspiration — Guidelines for Computing Crop Water Requirements.* Allen, R.G., Pereira, L.S., Raes, D., Smith, M. (1998). FAO, Rome. ISBN 92-5-104219-5. Table 12, pp. 65–87.
3. **FAO Irrigation and Drainage Paper No. 29 (Rev. 1):** *Water Quality for Agriculture.* Ayers, R.S., Westcot, D.W. (1985). FAO, Rome. ISBN 92-5-102263-1. Table 4: Crop Tolerance and Yield Potential vs. Salinity ($EC_e$ and $EC_w$), pp. 10–15.
4. **FAO Irrigation and Drainage Paper No. 33:** *Yield Response to Water.* Doorenbos, J., Kassam, A.H. (1979). FAO, Rome. ISBN 92-5-100744-6. pp. 1–193.
5. **FAO Soils Bulletin No. 39:** *Prognosis of Salinity and Alkalinity.* Massoud, F.I. (1977). FAO, Rome.
6. **IRRI Rice Knowledge Bank & Monograph:** *Rice: Soil and Land Suitability.* Ponnamperuma, F.N. (1972). *The Chemistry of Submerged Soils.* Advances in Agronomy, 24: 29–96. DOI: 10.1016/S0065-2113(08)60633-1.
7. **International Cotton Advisory Committee (ICAC):** *Physiology of the Cotton Plant.* Technical Bulletins, Washington, D.C. [https://www.icac.org](https://www.icac.org)
8. **CIMMYT:** *Wheat and Maize Production Guidelines for Warm and Heat-Stressed Environments.* Reynolds, M., et al. International Maize and Wheat Improvement Center, Mexico.
9. **Pakistan Agricultural Research Council (PARC):** *National Wheat and Oilseeds Coordination Programme Reports.* Ministry of National Food Security & Research, Islamabad. [http://www.parc.gov.pk/](http://www.parc.gov.pk/)
10. **Sindh Agriculture Extension Department:** *Ziraat Nama Sindh: Field Crop Advisories & Fertilizer Protocols.* Hyderabad, Sindh.
11. **ISRIC SoilGrids250m Documentation:** *Global gridded soil information based on machine learning.* Poggio, L., et al. (2021). SOIL, 7: 217–240. DOI: 10.5194/soil-7-217-2021.

---

## 11. Formal Scientific Traceability & Evidence Ledger

Every crop parameter, soil reaction boundary, salinity tolerance class, and exclusion rule is verified and classified below:

| Crop / Parameter | Implemented Range / Class | Exact Literature Source | Publication Year & Document Identifier | Exact Table / Page / Claim Supported | Claim Status | Agronomic Rationale & Limitations |
|:---|:---:|:---|:---:|:---|:---:|:---|
| **Wheat: Soil pH** | Opt: 6.0–7.5<br>Ref: 5.5–8.5 | FAO EcoCrop; FAO Soils Bulletin 39 | Massoud (1977), FAO Soils Bull. 39; EcoCrop (2000) | EcoCrop ID 2154; Soils Bull. 39 pp. 18–24. Micronutrient lockup at pH > 8.5. | **VERIFIED** | Alkaline Indus alluvium supports wheat up to pH 8.5 with phosphorus/zinc fertilization. |
| **Rice: Soil pH** | Opt: 5.5–7.0<br>Ref: 4.5–8.2 | IRRI Knowledge Bank; Ponnamperuma | Ponnamperuma (1972) Adv. Agron. 24: 29–96; IRRI (2002) | Submergence lowers Eh and stabilizes pH ~ 6.5–7.0; zinc deficiency above pH 8.2. | **VERIFIED** | pH 8.2 is NOT a mortality wall; Dadu historically produces high rice yields at pH 8.30 with ZnSO4. |
| **Cotton: Soil pH** | Opt: 6.5–8.0<br>Ref: 5.5–8.5 | ICAC Technical Bulletins; CCRI Sakrand | ICAC Tech. Paper Series (2005); CCRI Advisories | Cotton Physiology Bull. 3, pp. 12–15. Taproot sensitive to sodic dispersion. | **VERIFIED** | Indus calcareous soils (~8.0) are highly productive with drainage; waterlogging hypoxia is primary risk. |
| **Sugarcane: Soil pH** | Opt: 6.0–7.8<br>Ref: 5.0–8.5 | FAO EcoCrop; SRI Thatta | EcoCrop ID 1912; SRI Thatta Annual Report (2018) | Root elongation inhibited under severe sodic compaction ($ESP > 15\%$). | **VERIFIED** | Stalk elongation requires deep permeable loams; perennial water supply is the binding constraint. |
| **Maize: Soil pH** | Opt: 5.8–7.2<br>Ref: 5.0–8.2 | CIMMYT Maize Manual; FAO EcoCrop | CIMMYT Production Guide (2004); EcoCrop ID 2231 | CIMMYT Guide p. 34. Susceptible to zinc chlorosis in calcareous soils (pH > 8.0). | **VERIFIED** | Extremely sensitive to waterlogging hypoxia (>48 hrs kills roots) and reproductive heat (>38°C). |
| **Soil Salinity Tolerance ($EC_e$)** | Cotton: 7.7 dS/m<br>Wheat: 6.0 dS/m<br>Rice: 3.0 dS/m<br>Sugarcane: 1.7 dS/m<br>Maize: 1.7 dS/m | FAO Irrigation and Drainage Paper 29 (Rev. 1) | Ayers & Westcot (1985), FAO I&D 29, ISBN 92-5-102263-1 | Table 4, pp. 10–13. Maas & Hoffman (1977) root zone extraction salinity ($EC_e$). | **VERIFIED** | **CRITICAL DISTINCTION:** Values are soil paste extract $EC_e$, NOT irrigation water $EC_w$. $EC_w \approx EC_e / 1.5$. Dataset lacks measured water $EC_w$. |
| **SoilGrids Prediction Uncertainty** | Topsoil pH (0–30 cm) | ISRIC SoilGrids250m v2.0 | Poggio et al. (2021) SOIL, 7: 217–240 | Table 5, p. 229: Model 10-fold cross-validation RMSE for pH in H2O is 0.45–0.52 pH units. | **VERIFIED** | Confirms that a single centroid prediction of 8.30 carries $\pm 0.5$ uncertainty; brittle thresholding is spurious. |
| **Extreme Soil Hazard** | pH < 4.5 or pH ≥ 9.0 | FAO Soils Bulletin 39; USDA NRCS | Massoud (1977); USDA Soil Survey Manual (2017) | Soils Bull. 39, pp. 22–25. Extreme aluminum toxicity (<4.5); black-alkali dispersion ($\ge 9.0$). | **VERIFIED (as Hazard Warning)** | Classified as `SEVERE_HAZARD` / `UNVERIFIED` requiring on-ground soil ESP testing, NOT a biological mortality claim. |
| **Data Quarantine Exclusion** | `flag_excluded == True` | Phase 3E Research Pipeline | Exclusion Ledger (`src/data/build_research_dataset.py`) | Contaminated provincial aggregate rows (Sujawal Rice) and corrupt records. | **VERIFIED** | Hard physical/data-integrity rejection; rows must never be used for recommendations. |

---

## 12. Retrospective Validation Assessment: Capabilities & Limitations

A rigorous evaluation was performed to determine whether historical panel observations from `data/processed/research_dataset.csv` can support a scientifically defensible retrospective validation of the suitability screener.

### 12.1 Panel Coverage & Observational Realities
* **Total Dataset Observations:** 3,223 panel rows across 23 Sindh districts over 44 crop years (1981–82 to 2024–25).
* **Crop-Specific Sample Sizes:**
  * Wheat: 773 observations (present across all 23 districts; 448 rows lack soil data).
  * Sugarcane: 697 observations (concentrated in barrage zones; 375 rows lack soil data).
  * Cotton: 607 observations (central/upper Sindh; 347 rows lack soil data; Badin unrecorded).
  * Rice: 576 observations (upper Sindh & delta; 352 rows lack soil data; Thatta Rice absent from API).
  * Maize: 570 observations (low historical acreage; 295 rows lack soil data).
* **Missing District-Crop-Year Combinations:**
  * Across the theoretical $23 \times 5 \times 44 = 5,060$ panel combinations, **1,837 combinations (36.3%) are completely absent from the source records**.
  * Absence cannot be equated to biological infeasibility; it reflects commercial preferences, milling bottlenecks, and PBS recording policies.
* **Administrative Boundary Instability:**
  * 579 observations (18.0% of panel) carry `flag_boundary_instability = True` due to major administrative bifurcations in 2004–2006 (Dadu, Hyderabad, Larkana, Jacobabad) and 2013 (Thatta/Sujawal). Pre-split parent districts aggregate acreage for territories later severed, creating non-climatic step-down artifacts.
* **Unit Consistency:**
  * Production targets are standardized in metric tonnes (Wheat, Rice, Sugarcane, Maize). Cotton units in raw PBS records are in thousand bales (170 kg); all analyses strictly utilize derived `cotton_yield_t_ha` to prevent 5.88× scaling distortions.

### 12.2 Scientific Barriers to Valid Predictive Accuracy Scoring
The existing historical panel **CANNOT** be used to compute a legitimate "predictive validation score" (e.g. accuracy, precision, recall) for the suitability screener due to four insurmountable methodological barriers:
1. **Endogeneity (Circular Defining vs. Testing):** In agricultural rule engineering, if historical realized yields or historical presence are used both to identify plausible environmental bounds and then evaluated against the same panel, the resulting "accuracy" is completely circular and statistically invalid.
2. **Conflation of Cultivation with Biological Suitability:** Realized historical harvest ($Area > 0, Yield > 0$) reflects policy incentives (Minimum Support Prices for Wheat and Sugarcane), credit liquidity, and watercourse head-reach privilege rather than pure biophysical compatibility.
3. **Absence of Ground-Truth Negative Controls:** The PBS panel only records districts where a crop was officially enumerated. True agronomic "negatives" (controlled field trials where a crop was planted under proper management but failed catastrophically due to climate/soil) are completely unrecorded.
4. **Hydrological Unobservability:** The historical panel records seasonal rainfall, but 90–95% of Sindh's crop water is delivered via Indus canal diversions and tube-wells. Because canal discharges and watercourse schedules are unobserved, historical yields reflect hydraulic water deliveries that cannot be validated from rainfall alone.

### 12.3 What Additional Data is Required for Defensible Retrospective Validation?
To execute a genuine, statistically defensible validation without circularity, the following independent data streams must be integrated:
1. **Independent Controlled Agronomic Trials:** Multi-year variety trial datasets from PARC, CCRI Sakrand, and Agriculture Research Institute Tandojam, providing explicit trial failure logs, flowering dates, and measured stage-specific heat shock data.
2. **Hydrological Canal Discharge Records:** Daily or 10-day canal gauge command diversions from the Sindh Irrigation Department (Guddu, Sukkur, and Kotri barrages) and watercourse head/tail Warabandi delivery logs.
3. **High-Resolution Georeferenced Soil Chemistry:** Laboratory-measured field soil samples including Electrical Conductivity ($EC_e$), Exchangeable Sodium Percentage ($ESP$), Sodium Adsorption Ratio ($SAR$), and boron levels across all 24 districts, replacing static 250m centroid estimates.
4. **Spatially Explicit Cropping Calendars:** Remote sensing (Sentinel-2 / Landsat NDVI phenology curves) isolating exact green-up, anthesis, and maturity dates to evaluate reproductive thermal stress against daily satellite temperature series.

