# Phase 3D Executive Summary: Independent Validation of Historical Rice Evidence

**Document:** `reports/phase3d/phase3d_summary.md`
**Execution Date:** 2026-10-26
**Project:** Fajr-e-Kisht
**Milestone:** Phase 3D — Independent PDF Validation & Sujawal Contamination Audit

---

## 1. Executive Summary

Phase 3D conducted an **independent, from-scratch** validation of the two central claims made in the Phase 3C report:

1. That Table 13 of the official PBS publication contains 28 consecutive seasons of historical Thatta rice data (1981-82 through 2008-09).
2. That the Sujawal Rice rows in the working CSV (`pbs_weather_soil_1981_2025.csv`) are contaminated with Sindh provincial totals rather than district-level data.

**Both claims were independently confirmed** using direct PDF text extraction with an independent method (pypdf layout mode), raw column header identification, and structured comparison against the official Table 11 provincial totals.

---

## 2. Verified Facts

### 2.1 Table 13 — Independently Verified

| Claim | Verification Status |
|:---|:---:|
| Table 13 title: "DISTRICT-WISE AREA & PRODUCTION OF RICE CROP IN SINDH" | **CONFIRMED** |
| Table 13 occupies printed pages 28-30 (PDF pages 36-38) | **CONFIRMED** |
| Thatta column appears as column 5 on PDF page 37 (printed p. 29) | **CONFIRMED** |
| Column header on page 37: Tharparkar, Dadu, Hyderabad, Badin, Thatta, Mirpurkhas, Karachi, K.S.Kot | **CONFIRMED** |
| Area units: `'000' Hectares` | **CONFIRMED** |
| Production units: `"000" Tonnes` | **CONFIRMED** |
| 28 continuous area observations (1981-82 to 2008-09) | **CONFIRMED** |
| 28 continuous production observations (1981-82 to 2008-09) | **CONFIRMED** |
| All 28 Phase 3C numeric claims match independent extraction | **CONFIRMED (28/28, 0 discrepancies)** |
| District Sujawal does not appear in the publication | **CONFIRMED** |
| All Thatta values represent undivided district (pre-2013) | **CONFIRMED** |

### 2.2 Sujawal Contamination — Verified and Bounded

| Claim | Verification Status |
|:---|:---:|
| CSV Sujawal Rice area 2004-05 = 543.9 matches Sindh provincial total | **CONFIRMED** |
| CSV Sujawal Rice area 2005-06 = 593.2 matches Sindh provincial total | **CONFIRMED** |
| CSV Sujawal Rice area 2006-07 = 598.1 matches Sindh provincial total | **CONFIRMED** |
| CSV Sujawal Rice area 2007-08 = 594.0 matches Sindh provincial total | **CONFIRMED** |
| CSV Sujawal Rice area 2008-09 = 733.463 matches Sindh provincial total (within PDF rounding) | **CONFIRMED** |
| Years 2009-10 to 2022-23 (14 rows) verified against official source | **CANNOT VERIFY — post-2008-09 source required** |

> **Note on 2008-09:** The CSV shows 733.463013 k ha while Table 11 shows 733.5 k ha. The difference of 0.037 is entirely explained by PDF 1-decimal rounding. The CSV value is the API's higher-precision representation of the same figure. This is a **confirmed match**, not a mismatch.

---

## 3. Plausible Explanations (Not Verified Facts)

### 3.1 Root Cause of Sujawal Contamination

Analysis of the scraper notebook (`pbs_crops_api.ipynb`) reveals the contamination mechanism:

1. The PBS digital portal (`na.data.gov.pk`) lists Sujawal as a valid district in its geographic hierarchy (created post-2013 with its own `district_id`).
2. When the scraper queries `GetYearly` for `level=DIST_LEVEL, area=SUJAWAL_ID, crop=RICE_ID`, the portal appears to return the Sindh provincial total rather than district-level data.
3. The most plausible explanation is a **"default to parent" fallback** in the portal's backend: when no district-level record exists for a given district-crop combination, the endpoint returns the parent (provincial) aggregate.
4. **The scraper itself has no bug.** It faithfully passes through what the API returns. The data error originates in the PBS portal's backend mapping.

This conclusion is **consistent** with the observation but **not directly proven** — the portal's source code is not available for inspection.

### 3.2 Post-2008 Sujawal Rows (2009-10 to 2022-23)

The 14 post-PDF-period Sujawal Rice rows show values in the range 361-828 k ha. These are strongly inferred to also be Sindh provincial totals because:
- True Thatta district area was 43-90 k ha (from Table 13)
- Sujawal is a sub-partition of Thatta and cannot plausibly exceed Thatta
- The same API mechanism that produced confirmed contamination in 2004-09 would continue to produce it in subsequent years
- No administrative or agricultural change would explain a 6-10x increase relative to the Thatta baseline

**Status:** Strongly inferred as provincial totals. **Unverified** without an official post-2008 district-level source.

---

## 4. Unresolved Questions

1. **Post-2009 true Thatta district values:** The 28-year PDF terminates at 2008-09. No official district-level source for Thatta rice from 2009-10 onward has been identified in this project.
2. **Post-2013 Sujawal vs. Thatta split:** After the 2013 bifurcation, neither official district values for independent Sujawal nor residual Thatta have been located in digital sources.
3. **2022-23 Sujawal Area missing:** The CSV row for 2022-23 has Production = 2011.8 but Area = blank (missing). This is likely a portal-side data-entry gap.
4. **Thatta district appearance in CSV:** The CSV contains 0 Thatta Rice rows. It is not yet established whether the PBS digital portal simply has no Thatta rice data at all, or whether it has data under a different district ID that was missed during scraping.

---

## 5. Data Integrity Compliance

In strict accordance with Phase 3D directives:
- The original CSV (`data/raw/pbs_weather_soil_1981_2025.csv`) was **not modified**
- Scraper scripts were **not altered or re-run**
- No synthetic, imputed, or interpolated values were generated
- No division of undivided Thatta figures was performed
- No soil data acquisition was initiated
- No machine learning models were trained
- The original PDF files were **preserved unchanged**

---

## 6. Deliverables Created

| File | Description | Rows |
|:---|:---|:---:|
| `reports/phase3d/table13_validation.md` | Full methodology, column header, spot checks, comparison table | N/A |
| `reports/phase3d/thatta_rice_verified.csv` | 28-season independently-extracted Thatta rice data | 28 |
| `reports/phase3d/sujawal_rice_contamination_check.csv` | 19 Sujawal rows with provincial comparison and status | 19 |
| `reports/phase3d/phase3d_summary.md` | This executive summary | N/A |

---

## 7. Final Conclusion

| Question | Answer |
|:---|:---|
| **Was Table 13 independently verified?** | **YES** — using pypdf layout extraction, column header confirmation, spot checks on first/middle/last years |
| **How many historical Thatta seasons were validated?** | **28 of 28** (crop seasons 1981-82 through 2008-09, zero discrepancies) |
| **How many Sujawal Rice rows were confirmed to match Sindh provincial totals?** | **5 of 19** rows (years 2004-05 through 2008-09) are **definitively confirmed** against Table 11 of the same PDF. An additional 14 rows (2009-10 through 2022-23) are strongly inferred but cannot be PDF-verified. |
| **Were any Sujawal rows confirmed as genuine district data?** | **No.** None of the 19 Sujawal Rice rows appear to represent true Sujawal (or Thatta) district-level values. |
