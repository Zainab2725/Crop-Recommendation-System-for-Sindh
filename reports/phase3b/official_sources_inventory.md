# Phase 3B: Inventory of Official Agricultural Data Sources

**Document:** `reports/phase3b/official_sources_inventory.md`  
**Investigation Date:** 2026-10-26  
**Scope:** Evaluation of federal and provincial statistical repositories for historical crop data recovery in Sindh, Pakistan.

---

## 1. Official Sources Registry

| # | Official Title | Publishing Agency | Source URL / Location | Years Covered | Geographic Disaggregation | Crops Covered | Stated Units | Live Access Status | Relevance to Fajr-e-Kisht |
|---|---|---|---|---|---|---|---|---|---|
| **1** | **PBS National Accounts Crop Portal** | Pakistan Bureau of Statistics (PBS) | `http://na.data.gov.pk/Crops/Home` | 1981–82 to 2024–25 (variable by district) | National, Provincial (Level 12), Division (Level 13), District (Level 14) | 125 crops (Wheat, Rice, Cotton, Sugarcane, Maize, etc.) | Area: Thousand Hectares; Production: Thousand Tonnes (Cotton in Thousand Bales); Yield: Tonnes/Ha | **ACTIVE / ACCESSIBLE** (Live JSON API) | **PRIMARY SOURCE** used in current dataset. Contains the Sujawal rice provincial contamination and Thatta rice omission. |
| **2** | **Crops Area and Production by Districts (1981-82 to 2008-09)** | Federal Bureau of Statistics (Economic Wing), Ministry of Food & Agriculture (MinFA) | `https://www.pbs.gov.pk/wp-content/uploads/2020/07/area_and_production_by_districts_for_28_years.pdf` (Archived legacy Drupal path: `http://web.archive.org/web/20250707071736/https://www.pbs.gov.pk/sites/default/files/agriculture/publications/area_and_production_by_districts_for_28_years.pdf`) | 1981–82 to 2008–09 (28 continuous seasons) | Province and District (historical undivided boundaries) | All major and minor food, cash, pulse, and oilseed crops (Rice: Table 13) | Area: Thousand Hectares; Production: Thousand Tonnes; Cotton in 000 Bales | **ACTIVE / DOWNLOADED & VERIFIED** (Successfully retrieved directly from PBS live WordPress storage; 214 pages, 2,216,995 bytes, valid PDF) | **HIGH BENCHMARK VALUE.** Contains verified pre-split historical Thatta rice series (1981–2008). Proves Sujawal did not exist during this era and confirms historical undivided Thatta statistics. |
| **3** | **Crops Area & Production (District Wise) Annual Compendiums** | Ministry of National Food Security & Research (MNFS&R), Economic Wing | `https://mnfsr.gov.pk/` (Annual Releases) | 2009–10 to 2024–25 (Annual series) | Province and District | Major and minor crops | Area: 000 Hectares; Production: 000 Tonnes | **INCONSISTENT ACCESS** (Server active, but HTTPS handshake frequently rejected due to legacy TLS configuration; physical copies in Islamabad) | **POTENTIAL RECOVERY SOURCE.** Contains post-2013 Thatta and Sujawal separated reports, but requires offline access or government library retrieval. |
| **4** | **Pakistan Economic Survey (Agriculture Chapter & Statistical Appendix)** | Ministry of Finance, Government of Pakistan (Economic Adviser's Wing) | `https://www.finance.gov.pk/survey_economic.html` | 1950s to 2024–25 | National and Provincial totals only | Major Crops (Wheat, Rice, Cotton, Sugarcane, Maize) | Production: 000 Tonnes (Cotton in 000 Bales) | **ACTIVE / FULLY ACCESSIBLE** (Annual PDF release) | **PROVINCIAL VALIDATION ONLY.** Confirmed that Sujawal's 2,861.4k tonnes in 2021–22 and 2,011.8k tonnes in 2022–23 match the exact provincial totals of Sindh. |
| **5** | **Agricultural Statistics of Pakistan (Annual Compendium)** | MNFS&R / Federal Bureau of Statistics | Archived by PBS & MNFS&R | Historical annual volumes | National and Provincial; selective district tables | Comprehensive agricultural indicators | Standard federal metric and bale units | **SELECTIVELY ACCESSIBLE** (Older volumes archived; recent volumes irregular) | **REFERENCE STANDARD.** Established the official definition that 1 Cotton Bale = 375 lbs = 170.097 kg. |
| **6** | **Sindh Crop Reporting Service (CRS) Statistical Reports** | Directorate of Agriculture Statistics, Agriculture Department, Government of Sindh (Hyderabad) | Offline provincial administration archive (Thandi Sarak, Hyderabad) | 1980s to present | District and Taluka (Sub-district) | Sindh seasonal crops (Kharif & Rabi) | Provincial survey units (Acres, Hectares, Maunds, Tonnes) | **OFFLINE / IN-PERSON ONLY** (No public API or live web database) | **THE ONLY DEFINITIVE TRUTH SOURCE** for recovering Taluka-level Thatta and Sujawal historical rice splits. Not accessible via web scrapers. |

---

## 2. Technical Evaluation of Access Routes

1. **PBS Interactive Portal (`na.data.gov.pk`):**  
   - Operational and queryable via JSON POST endpoints.
   - *Limitation:* The backend database contains corrupt rice tables for Thatta (empty response) and Sujawal (provincial total). Modifying scraper queries cannot extract data that is absent from the host database.
2. **PBS Main Domain (`www.pbs.gov.pk`):**  
   - The legacy Drupal path (`/sites/default/files/agriculture/publications/...`) returns HTTP 404 following the 2020/2021 website redesign. However, deep inspection of the PBS publications directory revealed that the official 28-year compendium is actively maintained on the live server at `https://www.pbs.gov.pk/wp-content/uploads/2020/07/area_and_production_by_districts_for_28_years.pdf`. Phase 3C verified that direct downloads succeed with HTTP 200, yielding a complete, authentic 214-page PDF.
3. **MNFS&R Federal Portal (`mnfsr.gov.pk`):**  
   - Houses the post-2009 district compendiums. However, the federal server drops SSL handshakes (`SSLEOFError`) or forcibly terminates connections from non-whitelisted IPs. Web automation cannot reliably scrape this portal without manual government office file requests.
