# Phase 3C Executive Summary: Inspection of the Official Historical PBS PDF

**Document:** `reports/phase3c/phase3c_summary.md`  
**Execution Date:** 2026-10-26  
**Project:** Fajr-e-Kisht  
**Milestone:** Phase 3C — Official Publication Verification & Historical Thatta Rice Series Audit  

---

## 1. Executive Summary

Phase 3C conducted a thorough empirical inspection of the official Pakistan Bureau of Statistics (PBS) compendium titled:
> **"Crops Area and Production (By Districts) (1981-82 to 2008-09), Volume I: Food and Cash Crops"**  
> *Published by: Government of Pakistan, Statistics Division, Federal Bureau of Statistics (Economic Wing), Islamabad*

This investigation successfully identified the active federal download link, retrieved and validated the intact 214-page PDF document, preserved the artifact within the project repository, located the official historical district-level rice tables for Sindh, and extracted 28 consecutive years of verified historical data for District Thatta (1981–82 to 2008–09).

---

## 2. Technical Retrieval & Verification Matrix

| Investigation Parameter | Observation / Result | Verification Detail |
|---|---|---|
| **Direct Legacy URL** | `https://www.pbs.gov.pk/sites/default/files/agriculture/publications/area_and_production_by_districts_for_28_years.pdf` | **HTTP 404 Not Found** (Legacy Drupal directory path retired after July 2020) |
| **Archive Record** | `http://web.archive.org/web/20250707071736/https://www.pbs.gov.pk/sites/default/files/agriculture/publications/area_and_production_by_districts_for_28_years.pdf` | **Available (200 OK)** in Internet Archive Wayback Machine |
| **Active Live PBS Link** | `https://www.pbs.gov.pk/wp-content/uploads/2020/07/area_and_production_by_districts_for_28_years.pdf` | **HTTP 200 OK** (Active WordPress storage endpoint discovered via PBS publications directory) |
| **Content-Type** | `application/pdf` | Valid standard binary PDF stream |
| **File Size** | `2,216,995 bytes` (2.11 MB) | Exactly matches official federal archive byte size |
| **Format Validation** | `%PDF-1.3`, 214 pages | Cleanly parsed and verified via `pypdf` |
| **Preserved Locations** | `data/raw/area_and_production_by_districts_for_28_years.pdf`<br>`reports/phase3c/area_and_production_by_districts_for_28_years.pdf` | Preserved bit-for-bit without alteration |

---

## 3. Key Findings

### 3.1 Verification of Undivided Thatta Rice Data (1981–82 to 2008–09)
* **Table Located:** Table No. 13 — `DISTRICT-WISE AREA & PRODUCTION OF RICE CROP IN SINDH`
* **Page Numbers:** Printed Pages 28, 29, 30 (PDF Pages 36, 37, 38).
* **Published Units:**
  * Area: `'000' Hectares` (Thousand Hectares)
  * Production: `"000" Tonnes` (Thousand Metric Tonnes)
  * Derived Yield: Tonnes per Hectare ($\text{Yield} = \text{Production} / \text{Area}$)
* **Thatta Time Series:** Exactly 28 continuous annual entries published on Printed Page 29 (PDF Page 37).
  * Area ranges from **43.0 to 89.5 thousand hectares** (Mean: ~62.3 k ha).
  * Production ranges from **34.3 to 203.1 thousand tonnes** (Mean: ~104.9 k tonnes).
  * Derived yield ranges from **0.63 to 2.59 tonnes/ha**, aligning with standard historical Lower Sindh rice yields.

### 3.2 Jurisdictional Clarity: Undivided Thatta
* The publication predates the bifurcation of District Thatta (which occurred on **October 12, 2013**, creating modern District Sujawal).
* District Sujawal does not appear in this 1981–2008 federal publication.
* All published Thatta values represent the **entire undivided district**.
* **Methodological Rule:** These historical values are **not divided** between Thatta and Sujawal, avoiding unverified artificial assumptions.

### 3.3 Root-Cause Proof of Project Dataset Discrepancies
1. **Thatta Rice Missingness:** The existing project CSV (`pbs_weather_soil_1981_2025.csv`) contains **0 records** for Thatta Rice. This was caused by the digital API endpoint at `na.data.gov.pk` omitting Thatta rice tables during automated scraping, despite the historical data existing in federal print records.
2. **Sujawal Provincial Contamination:** A cross-comparison between the existing CSV's Sujawal rice rows and Table 11 (`PROVINCE-WISE AREA & PRODUCTION OF RICE CROP IN PAKISTAN`, PDF Page 31) confirmed that Sujawal's reported area (e.g., 543.9 k ha in 2004–05) and production (1,499.7 k tonnes) match the **total Sindh provincial harvest** to the exact decimal. The PBS web portal mistakenly mapped the provincial aggregate into Sujawal.

---

## 4. Boundaries of Verified vs. Unavailable Data

```
1981-82                                     2008-09               2013-14               2024-25
   |===========================================|---------------------|---------------------|
     VERIFIED IN OFFICIAL PBS PDF (Phase 3C)              REMAINS UNAVAILABLE
     - Undivided Thatta Rice Area (28 yrs)                - Thatta Rice (2009-10 to 2024-25)
     - Undivided Thatta Rice Prod (28 yrs)                - Sujawal Rice (True district values)
     - Validated against federal print record             - Post-2013 split disaggregation
```

### 4.1 What Is Explicitly Verified
* 28 consecutive crop seasons (1981–82 to 2008–09) of Rice Area, Production, and Derived Yield for **undivided District Thatta**.
* Exact concordance of reporting units (`'000' Hectares` and `"000" Tonnes`) between the federal publication and the project dataset.

### 4.2 What Remains Unavailable
* **Recent 16 Crop Seasons (2009–10 through 2024–25):** The 28-year compendium concludes at 2008–09. Subsequent years are absent from this document.
* **Modern Sujawal District Series:** Because Sujawal was formed in late 2013, neither pre-2013 nor post-2013 disaggregated Sujawal data exist in this publication.
* **Separated Modern Thatta vs. Sujawal Breakdown:** Deconvolving the undivided Thatta series into separate Taluka-level figures requires offline records from the Sindh Crop Reporting Service (Hyderabad) or post-2013 MNFS&R annual compendiums.

---

## 5. Adherence to Project Governance

In strict accordance with Phase 3C directives:
* The original CSV (`data/raw/pbs_weather_soil_1981_2025.csv`) was **not modified**.
* Scraper scripts were **not altered or re-run**.
* No synthetic or imputed numbers were injected.
* No soil data acquisition was initiated.
* No machine learning models were trained.
* All newly verified information is documented in persistent project reports with verified citations and source metadata.
