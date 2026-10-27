# Phase 3B Investigation Summary: Historical Data Recovery & Geographic Strategy

**Date:** 2026-10-26  
**Module:** Phase 3B Feasibility of Historical Data Recovery  
**Workspace:** `c:\Users\muet\Downloads\FYP_dataset\FYP_dataset_builder_code`  
**Output Directory:** [`reports/phase3b/`](file:///c:/Users/muet/Downloads/FYP_dataset/FYP_dataset_builder_code/reports/phase3b)

---

## 1. Executive Summary in Plain English

### A. Which Official Sources Are Genuinely Accessible?
1. **PBS Interactive Crop Portal (`http://na.data.gov.pk/Crops/Home`):**  
   - **Status:** **Active & Accessible via API.**  
   - **Finding:** This is the live database from which the current dataset was scraped. However, its underlying database is missing Thatta Rice (0 bytes returned) and has Sujawal Rice corrupted with the Sindh provincial total. Querying this server with different code cannot recover the missing district data.
2. **PBS Website (`https://www.pbs.gov.pk/`):**  
   - **Status:** **Active, but legacy publication links return 404.**  
   - **Finding:** The historical Drupal page for *"Crops Area and Production by Districts (1981-82 to 2008-09)"* was decommissioned during the site's WordPress migration. The site now redirects users to the interactive portal `na.data.gov.pk`.
3. **Ministry of National Food Security & Research (`https://mnfsr.gov.pk/`):**  
   - **Status:** **Inconsistent Network Access.**  
   - **Finding:** The federal web server frequently drops SSL handshakes (`SSLEOFError`) or terminates connections. Automated scraping of recent PDF compendiums directly from `mnfsr.gov.pk` is blocked by server infrastructure issues.
4. **Pakistan Economic Survey (`finance.gov.pk`):**  
   - **Status:** **Fully Accessible.**  
   - **Finding:** Confirms provincial aggregate totals, but does not publish district-level tables.

---

### B. Can the Missing Thatta and Sujawal Rice Data Be Recovered?

| Target Entity & Period | Recovery Feasibility | Evidence & Constraint | Defensible Project Decision |
|---|---|---|---|
| **Historical Undivided Thatta (1981–2008)** | **Feasible via Offline Printed Archive** | Published in Table 13 of *Crops Area and Production by Districts (1981-82 to 2008-09)* as a single composite district. | High value for macro-district historical studies; cannot be artificially divided between modern Thatta and Sujawal. |
| **Modern Thatta Rice (2013–2025)** | **Unavailable Online** | Omitted in PBS API (0 bytes); inaccessible on MNFS&R server. Recoverable only by physically visiting the Sindh Agriculture Directorate in Hyderabad. | **Leave as NaN / Missing.** Do not impute or fabricate values. |
| **Modern Sujawal Rice (2013–2025)** | **Unavailable Online** | Corrupted in PBS API with provincial totals. Local district figures exist only in offline provincial CRS filing cabinets in Hyderabad. | **Quarantine rows from model training.** Do not train models on provincial numbers. |
| **Pre-2013 Sujawal Rice (1981–2012)** | **Categorically Impossible** | Sujawal district did not legally exist before October 12, 2013. Dividing historical Thatta retrospectively is agronomically indefensible without field-level revenue records. | **Leave as Strictly Unavailable.** |

---

### C. Which Years Have Defensible Geographic Coverage?

#### 1. Recommended for Conference Paper: **2013–14 through 2024–25 (12 Crop Cycles)**
- **100% Boundary Stability:** All 24 districts operate under their modern legal borders with zero boundary partitions during this period.
- **Pristine Atmospheric Data:** 100% complete daily temperature, rainfall, and satellite solar radiation (`solar_mean` has 0 missing values).
- **Clean Modeling Panel:** Wheat, Cotton, Sugarcane, and Maize are 100% clean across all 24 districts. Rice is 100% clean across 22 districts. Thatta and Sujawal Rice can be handled transparently as missing observations without corrupting the remaining 22 rice districts.
- **Direct Practical Utility:** Produces farmer recommendations based on contemporary climate patterns, modern canal systems, and current crop varieties.

#### 2. Recommended for Full FYP Extension: **Multi-Horizon Analysis**
- Combine the 12-year modern micro-district panel (2013–2025) with a 44-year macro-district panel (1981–2025) where child districts are re-aggregated into their 16 historical parent clusters (e.g., "Greater Hyderabad", "Greater Larkana").

---

## 2. Inventory of Phase 3B Deliverables in `reports/phase3b/`

| File | Core Content |
|---|---|
| [`reports/phase3b/official_sources_inventory.md`](file:///c:/Users/muet/Downloads/FYP_dataset/FYP_dataset_builder_code/reports/phase3b/official_sources_inventory.md) | Exhaustive registry of PBS, MNFS&R, Sindh CRS, and Economic Survey sources with URLs, coverage, units, and access statuses. |
| [`reports/phase3b/thatta_sujawal_recovery.csv`](file:///c:/Users/muet/Downloads/FYP_dataset/FYP_dataset_builder_code/reports/phase3b/thatta_sujawal_recovery.csv) | Year-by-year 44-season audit ledger documenting administrative status, recovery feasibility, and defensible research treatment for Thatta and Sujawal. |
| [`reports/phase3b/geographic_coverage_assessment.md`](file:///c:/Users/muet/Downloads/FYP_dataset/FYP_dataset_builder_code/reports/phase3b/geographic_coverage_assessment.md) | In-depth trade-off analysis between Candidate Period 1 (2013–2025) and historical panels, detailing administrative step-down hazards. |
| [`reports/phase3b/phase3b_summary.md`](file:///c:/Users/muet/Downloads/FYP_dataset/FYP_dataset_builder_code/reports/phase3b/phase3b_summary.md) | Plain-English executive briefing. |

---

## 3. What Limitations Remain

1. **No Online Public API for Missing Rice Records:** Neither PBS nor MNFS&R provides a functioning public web API to download genuine post-2013 district-level rice numbers for Thatta or Sujawal.
2. **Offline Field Archives:** Obtaining ground-truth historical rice data for Thatta and Sujawal requires manual archival retrieval from the Sindh Crop Reporting Service in Hyderabad (Thandi Sarak).
3. **Non-Destructive Integrity:** In accordance with research integrity standards, we will not fabricate, interpolate, or invent values for Thatta and Sujawal rice.
