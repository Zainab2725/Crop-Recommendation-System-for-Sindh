# Phase 3C: Official Historical PBS Evidence for Thatta Rice (1981–82 to 2008–09)

**Document:** `reports/phase3c/historical_thatta_evidence.md`  
**Investigation Date:** 2026-10-26  
**Investigator:** Fajr-e-Kisht Research Team  
**Primary Source:** Government of Pakistan, Statistics Division, Federal Bureau of Statistics (Economic Wing), Islamabad  
**Publication Title:** *Crops Area and Production (By Districts) (1981-82 to 2008-09), Volume I: Food and Cash Crops*  
**Archived Location:** `data/raw/area_and_production_by_districts_for_28_years.pdf` and `reports/phase3c/area_and_production_by_districts_for_28_years.pdf`  

---

## 1. Technical Audit of Official Document Access

### 1.1 Direct URL Probing
* **Legacy Drupal Route:** `https://www.pbs.gov.pk/sites/default/files/agriculture/publications/area_and_production_by_districts_for_28_years.pdf`
  * **HTTP Status:** `404 Not Found`
  * **Cause:** Deprecated directory tree following PBS portal CMS migration (Drupal to WordPress in July 2020).
  * **Archival Status:** Fully captured and preserved in the Internet Archive Wayback Machine (`http://web.archive.org/web/20250707071736/https://www.pbs.gov.pk/sites/default/files/agriculture/publications/area_and_production_by_districts_for_28_years.pdf`).

### 1.2 Publications Directory Discovery & Active Link Retrieval
* **PBS Active Agriculture Directory:** `https://www.pbs.gov.pk/publications/agriculture`
* **Active WordPress Download Endpoint:** `https://www.pbs.gov.pk/wp-content/uploads/2020/07/area_and_production_by_districts_for_28_years.pdf`
* **HTTP Status:** `200 OK`
* **Content-Type:** `application/pdf`
* **Content-Length:** `2,216,995 bytes` (~2.11 MB)
* **Magic Header:** `%PDF-1.3`
* **Validation Outcome:** Opens cleanly as a valid, intact, fully indexed 214-page PDF.
* **Document Metadata:**
  * Title: `Editorial Board.doc`
  * Author: `DP-III`
  * Creator / Producer: `pdfFactory Pro 3.40 (Windows 7)`
  * Creation Date: `2011-12-26 12:15:01+05:00`
  * Mod Date: `2011-12-26 14:40:27+05:00`

---

## 2. Table of Contents & Relevant Table Mapping

The publication compiles 28 continuous years of district-level agricultural data (1981–82 to 2008–09) gathered by provincial Crop Reporting Services (CRS) and compiled by the Economic Wing of the devolved Ministry of Food and Agriculture (MinFA) / Federal Bureau of Statistics (FBS).

| Table Identifier | Published Table Title | Printed Page | PDF Page | Geographic Scope | Crops / Details |
|---|---|---|---|---|---|
| **Table 11** | `PROVINCE-WISE AREA & PRODUCTION OF RICE CROP IN PAKISTAN` | 23 | 31 | National & Provincial | Rice totals for Pakistan, Punjab, Sindh, KP, Balochistan |
| **Table 12** | `DISTRICT-WISE AREA & PRODUCTION OF RICE CROP IN PUNJAB` | 24–27 | 32–35 | Punjab Districts | Rice Area & Production |
| **Table 13** | `DISTRICT-WISE AREA & PRODUCTION OF RICE CROP IN SINDH` | **28–30** | **36–38** | **Sindh Districts** | **Rice Area & Production across 23 Sindh Districts** |
| **Table 14** | `DISTRICT-WISE AREA & PRODUCTION OF RICE CROP IN KHYBER PAKHTUNKHWA` | 31–34 | 39–42 | KP Districts | Rice Area & Production |
| **Table 15** | `DISTRICT-WISE AREA & PRODUCTION OF RICE CROP IN BALOCHISTAN` | 35–37 | 43–45 | Balochistan Districts | Rice Area & Production |

### Stated Units of Measurement in Table 13
* **Area Unit:** `'000' Hectares` (Thousand Hectares)
* **Production Unit:** `"000" Tonnes` (Thousand Metric Tonnes)
* **Derived Yield:** Metric Tonnes per Hectare ($\text{Yield} = \frac{\text{Production}}{\text{Area}}$)

### Footnotes & Symbols in Document
* **Footnotes on Table 13:** None. The table presents direct numerical entries for all 28 seasons without asterisks or suppressing qualifications for Thatta.
* **Symbol `*` in broader document:** Defined in statistical conventions as "Nil or Insignificant (less than 0.05 thousand units)".

---

## 3. Extracted Historical Rice Data for District Thatta (1981–82 to 2008–09)

The values below represent the **explicit, unmodified figures** published on **Printed Page 29 (PDF Page 37)** of Table 13 under column `Thatta`. Yield has been computed strictly as $\text{Production} / \text{Area}$.

| Crop Year | Calendar Start Year | Published Area (`'000' Ha`) | Published Production (`"000" Tonnes`) | Derived Yield (`Tonnes/Ha`) | Source Location |
|:---:|:---:|:---:|:---:|:---:|:---:|
| **1981–82** | 1981 | 74.1 | 131.1 | 1.7692 | Table 13, p. 29 (PDF p. 37) |
| **1982–83** | 1982 | 89.3 | 161.5 | 1.8085 | Table 13, p. 29 (PDF p. 37) |
| **1983–84** | 1983 | 89.5 | 103.6 | 1.1575 | Table 13, p. 29 (PDF p. 37) |
| **1984–85** | 1984 | 82.1 | 84.8 | 1.0329 | Table 13, p. 29 (PDF p. 37) |
| **1985–86** | 1985 | 52.5 | 42.5 | 0.8095 | Table 13, p. 29 (PDF p. 37) |
| **1986–87** | 1986 | 64.6 | 62.2 | 0.9628 | Table 13, p. 29 (PDF p. 37) |
| **1987–88** | 1987 | 66.9 | 65.3 | 0.9761 | Table 13, p. 29 (PDF p. 37) |
| **1988–89** | 1988 | 65.5 | 41.0 | 0.6260 | Table 13, p. 29 (PDF p. 37) |
| **1989–90** | 1989 | 52.0 | 34.3 | 0.6596 | Table 13, p. 29 (PDF p. 37) |
| **1990–91** | 1990 | 53.3 | 42.4 | 0.7955 | Table 13, p. 29 (PDF p. 37) |
| **1991–92** | 1991 | 58.3 | 61.9 | 1.0617 | Table 13, p. 29 (PDF p. 37) |
| **1992–93** | 1992 | 43.0 | 39.2 | 0.9116 | Table 13, p. 29 (PDF p. 37) |
| **1993–94** | 1993 | 60.1 | 119.4 | 1.9867 | Table 13, p. 29 (PDF p. 37) |
| **1994–95** | 1994 | 51.4 | 37.7 | 0.7335 | Table 13, p. 29 (PDF p. 37) |
| **1995–96** | 1995 | 61.4 | 144.2 | 2.3485 | Table 13, p. 29 (PDF p. 37) |
| **1996–97** | 1996 | 68.4 | 164.0 | 2.3977 | Table 13, p. 29 (PDF p. 37) |
| **1997–98** | 1997 | 65.3 | 130.6 | 2.0000 | Table 13, p. 29 (PDF p. 37) |
| **1998–99** | 1998 | 66.2 | 119.8 | 1.8097 | Table 13, p. 29 (PDF p. 37) |
| **1999–00** | 1999 | 58.1 | 132.8 | 2.2857 | Table 13, p. 29 (PDF p. 37) |
| **2000–01** | 2000 | 61.5 | 133.0 | 2.1626 | Table 13, p. 29 (PDF p. 37) |
| **2001–02** | 2001 | 54.8 | 85.8 | 1.5657 | Table 13, p. 29 (PDF p. 37) |
| **2002–03** | 2002 | 56.4 | 89.1 | 1.5798 | Table 13, p. 29 (PDF p. 37) |
| **2003–04** | 2003 | 54.8 | 77.2 | 1.4088 | Table 13, p. 29 (PDF p. 37) |
| **2004–05** | 2004 | 54.2 | 97.1 | 1.7915 | Table 13, p. 29 (PDF p. 37) |
| **2005–06** | 2005 | 54.2 | 108.7 | 2.0055 | Table 13, p. 29 (PDF p. 37) |
| **2006–07** | 2006 | 68.2 | 138.8 | 2.0352 | Table 13, p. 29 (PDF p. 37) |
| **2007–08** | 2007 | 75.6 | 192.9 | 2.5516 | Table 13, p. 29 (PDF p. 37) |
| **2008–09** | 2008 | 78.5 | 203.1 | 2.5873 | Table 13, p. 29 (PDF p. 37) |

---

## 4. Geographic Scope & Jurisdictional Analysis

### 4.1 Undivided District Thatta Confirmation
1. **Administrative History:** District Sujawal was officially created on **October 12, 2013** when the Sindh Provincial Government partitioned Thatta along the left bank of the Indus River.
2. **Absence of Sujawal:** Across all 214 pages of this federal publication covering 1981–82 to 2008–09, Sujawal does not appear. The 23 Sindh districts listed in Table 13 reflect the pre-2013 administrative boundaries.
3. **Territorial Extent:** All acreage and harvest figures published for Thatta represent the **undivided district** (modern Thatta plus modern Sujawal).
4. **Mandatory Methodological Rule:** In accordance with rigorous scientific integrity, these historical figures **must not be arbitrarily divided** between modern Thatta and Sujawal. Any mathematical partitioning (such as applying a constant ratio) would represent an unvalidated imputation without empirical ground truth.

---

## 5. Comparative Evaluation Against Existing Project Dataset

### 5.1 Direct Thatta Rice Comparison
* **In Existing CSV (`data/raw/pbs_weather_soil_1981_2025.csv`):**
  * Total Thatta Rice observations: **0 rows** (100% missing across all 44 years from 1981 to 2024).
  * *Finding:* There are no existing Thatta rice rows in the CSV to compare against. The 28 verified records in this official document confirm that Thatta rice data existed historically and was simply omitted or dropped during digital ingestion from `na.data.gov.pk`.

### 5.2 Cross-District Methodology Verification (Badin District Rice)
To confirm whether the numerical standards in the existing CSV match this publication, we cross-referenced Badin District rice records:
* **Badin 1981–82:**
  * Official PDF (p. 29): Area = `105.8` k ha, Production = `229.4` k tonnes
  * Existing CSV (Row 44): Area = `105.800003` k ha, Production = `229.399994` k tonnes, Yield = `2.168242` t/ha
* **Badin 1982–83:**
  * Official PDF (p. 29): Area = `94.0` k ha, Production = `193.1` k tonnes
  * Existing CSV (Row 45): Area = `94.000000` k ha, Production = `193.100006` k tonnes, Yield = `2.054255` t/ha
* **Badin 1983–84:**
  * Official PDF (p. 29): Area = `94.2` k ha, Production = `102.6` k tonnes
  * Existing CSV (Row 46): Area = `94.199997` k ha, Production = `102.599998` k tonnes, Yield = `1.089172` t/ha
* *Conclusion:* The numerical precision and units in the existing CSV match the official federal publication to the exact decimal.

### 5.3 Proof of the Sujawal Provincial Contamination
In the existing CSV, Sujawal contains rice data from 2004 onwards. A cross-comparison with **Table 11 (Sindh Provincial Total)** confirms that Sujawal's entries are the entire province of Sindh:

| Crop Year | Sujawal in Existing CSV (Area / Prod) | Thatta in Official PDF (Area / Prod) | Sindh Provincial Total in Official PDF Table 11 | Definitive Finding |
|:---:|:---:|:---:|:---:|:---|
| **2004–05** | 543.9 k ha / 1,499.7 k tonnes | **54.2 k ha / 97.1 k tonnes** | **543.9 k ha / 1,499.7 k tonnes** | CSV Sujawal is 100% Sindh Provincial Total |
| **2005–06** | 593.2 k ha / 1,721.0 k tonnes | **54.2 k ha / 108.7 k tonnes** | **593.2 k ha / 1,721.0 k tonnes** | CSV Sujawal is 100% Sindh Provincial Total |
| **2006–07** | 598.1 k ha / 1,761.8 k tonnes | **68.2 k ha / 138.8 k tonnes** | **598.1 k ha / 1,761.8 k tonnes** | CSV Sujawal is 100% Sindh Provincial Total |
| **2007–08** | 594.0 k ha / 1,817.7 k tonnes | **75.6 k ha / 192.9 k tonnes** | **594.0 k ha / 1,817.7 k tonnes** | CSV Sujawal is 100% Sindh Provincial Total |

This proves conclusively:
1. The web portal `na.data.gov.pk` mapped the provincial rice total of Sindh into Sujawal.
2. The genuine historical district values for Thatta (ranging from 43.0 to 89.5 thousand hectares) were completely bypassed.

---

## 6. Scope Limitations & Unavailability Boundaries

1. **Temporal Horizon:** This publication terminates at crop year **2008–09**. It provides **zero coverage for the subsequent 16 crop seasons (2009–10 through 2024–25)**.
2. **Post-2013 Separation:** Because the publication was compiled prior to the 2013 split, it provides **zero disaggregated data for modern Sujawal as an independent district**, nor post-split Thatta.
3. **Data Integrity Directive:** In accordance with project governance, no records in `data/raw/pbs_weather_soil_1981_2025.csv` have been altered, no scraper code was executed, and no synthetic values have been generated.
