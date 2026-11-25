# College & University Database Audit Report

## Live Database Summary (Before Cleanup)
- **`intern_accounts`**: 3104 rows (2646 non-empty `college`)
- **`applications`**: 5254 rows (5253 non-empty `college`)
- **Total unique raw `college` strings**: 3939

## Normalization & AISHE Merge Results
- **AISHE Master Institutions loaded**: 69208 (Universities, Colleges, Standalone)
- **Additional DB-Cleaned Institutions added**: 1677
- **Total Canonical Master Directory Size**: 70885
- **DB Unique Strings Breakdown**:
  - Exact AISHE Matches: 1078
  - Acronym/Shorthand Matches (e.g. VIT, LPU, SRM, KIIT): 43
  - Fuzzy Misspelling/Variant Matches (>=0.88 similarity): 687
  - Cleaned & Deduplicated DB-only Groups: 1677 (from 2124 raw variants)
  - Junk/Placeholder Strings Cleared: 7 unique strings (265 total DB rows, e.g. `Pending Profile`, `Student`)
