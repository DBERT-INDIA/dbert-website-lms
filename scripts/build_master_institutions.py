#!/usr/bin/env python3
"""
Builds the canonical master institutions seed (AISHE + cleaned DB entries),
generates the historical backfill mapping, and writes a detailed audit report.
"""
import csv
import json
import os
import re
from collections import Counter, defaultdict
from difflib import SequenceMatcher

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DB_PATH = os.path.join(ROOT, "data", "raw_db_colleges_audit.json")
AISHE_JSON_PATH = os.path.join(ROOT, "data", "sources", "aishe_institutions.json")
AISHE_CSV_PATH = os.path.join(ROOT, "data", "sources", "aishe_colleges.csv")

SEED_OUT = os.path.join(ROOT, "data", "master_institutions_seed.json")
MAPPING_OUT = os.path.join(ROOT, "data", "college_backfill_mapping.json")
REPORT_OUT = os.path.join(ROOT, "data", "college_audit_report.md")

JUNK_EXACT = {
    "", "pending profile", "student", "n/a", "na", "none", "nil", "null",
    "test", "testing", "college", "university", "institute", "school",
    "other", "others", "not applicable", "no", "yes", "xyz", "abc", "asdf",
    "-", "--", ".", "..", "...", "0", "1", "self", "fresher", "graduate",
}

# Common Indian acronyms & shorthand -> canonical search key
ACRONYM_MAP = {
    "vit": "vellore institute of technology",
    "vit vellore": "vellore institute of technology",
    "vit chennai": "vellore institute of technology",
    "vit bhopal": "vit bhopal university",
    "vit ap": "vit-ap university",
    "lpu": "lovely professional university",
    "srm": "srm institute of science and technology",
    "srmist": "srm institute of science and technology",
    "srm university": "srm institute of science and technology",
    "kiit": "kalinga institute of industrial technology",
    "kiit university": "kalinga institute of industrial technology",
    "ignou": "indira gandhi national open university",
    "sppu": "savitribai phule pune university",
    "klu": "koneru lakshmaiah education foundation",
    "kl university": "koneru lakshmaiah education foundation",
    "cu": "chandigarh university",
    "pu": "parul university",
    "dtu": "delhi technological university",
    "nsut": "netaji subhas university of technology",
    "nsit": "netaji subhas university of technology",
    "du": "university of delhi",
    "delhi university": "university of delhi",
    "mumbai university": "university of mumbai",
    "pune university": "savitribai phule pune university",
    "anna university": "anna university",
    "jntuh": "jawaharlal nehru technological university hyderabad",
    "jntuk": "jawaharlal nehru technological university kakinada",
    "jntua": "jawaharlal nehru technological university anantapur",
    "aktu": "dr. a.p.j. abdul kalam technical university",
    "vtu": "visvesvaraya technological university",
    "gtu": "gujarat technological university",
    "rgpv": "rajiv gandhi proudyogiki vishwavidyalaya",
    "makaut": "maulana abul kalam azad university of technology",
    "ipu": "guru gobind singh indraprastha university",
    "ggsipu": "guru gobind singh indraprastha university",
    "bhu": "banaras hindu university",
    "amu": "aligarh muslim university",
    "jnu": "jawaharlal nehru university",
    "bits pilani": "birla institute of technology and science",
    "akgec": "ajay kumar garg engineering college",
    "abes": "abes engineering college",
    "abesec": "abes engineering college",
    "gl bajaj": "g.l. bajaj institute of technology and management",
    "cbit": "chaitanya bharathi institute of technology",
    "vnrvjiet": "v.n.r. vignana jyothi institute of engineering and technology",
    "griet": "gokaraju rangaraju institute of engineering and technology",
    "mrec": "malla reddy engineering college",
    "mrecw": "malla reddy engineering college for women",
    "coep": "coep technological university",
    "vjti": "veermata jijabai technological institute",
    "pict": "pune institute of computer technology",
    "rvce": "r.v. college of engineering",
    "bmsce": "b.m.s. college of engineering",
    "msrit": "ramaiah institute of technology",
    "pes": "pes university",
    "pesu": "pes university",
    "ssn": "ssn college of engineering",
    "psg": "psg college of technology",
    "thapar": "thapar institute of engineering and technology",
    "tiet": "thapar institute of engineering and technology",
    "mit wpu": "dr. vishwanath karad mit world peace university",
    "manipal": "manipal academy of higher education",
    "mahe": "manipal academy of higher education",
    "muj": "manipal university jaipur",
    "amity": "amity university",
    "lpu punjab": "lovely professional university",
    "nirma": "nirma university",
    "daiict": "dhirubhai ambani institute of information and communication technology",
    "svnit": "sardar vallabhbhai national institute of technology",
    "vnit": "visvesvaraya national institute of technology",
    "mnit": "malaviya national institute of technology jaipur",
    "mnnit": "motilal nehru national institute of technology",
    "manit": "maulana azad national institute of technology",
    "nitt": "national institute of technology tiruchirappalli",
    "nitk": "national institute of technology karnataka",
    "nitw": "national institute of technology warangal",
    "nitr": "national institute of technology rourkela",
    "iiit hyderabad": "international institute of information technology hyderabad",
    "iiith": "international institute of information technology hyderabad",
    "iiit bangalore": "international institute of information technology bangalore",
    "iiit delhi": "indraprastha institute of information technology delhi",
    "iiitd": "indraprastha institute of information technology delhi",
    "iiit allahabad": "indian institute of information technology allahabad",
}

REVERSE_ALIASES = defaultdict(set)
for acr, target in ACRONYM_MAP.items():
    REVERSE_ALIASES[target].add(acr.upper())


def norm_key(s: str) -> str:
    if not s:
        return ""
    s = s.lower().strip()
    # Remove trailing/embedded parenthetical codes or pins if noisy
    s = s.replace("&", " and ")
    s = re.sub(r"[^a-z0-9\s]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def clean_city(c: str, district: str = "") -> str:
    raw = (c or "").strip()
    if not raw:
        raw = (district or "").strip()
    # Strip trailing 6-digit pincode
    raw = re.sub(r"\b\d{6}\b", "", raw).strip(" ,.-")
    if not raw:
        return ""
    # Title case if all upper or all lower
    if raw.isupper() or raw.islower():
        raw = raw.title()
    # Normalize common Indian city aliases
    city_fix = {
        "bangalore": "Bengaluru",
        "bengaluru urban": "Bengaluru",
        "new delhi": "Delhi",
        "delhi": "Delhi",
        "bombay": "Mumbai",
        "mumbai suburban": "Mumbai",
        "calcutta": "Kolkata",
        "madras": "Chennai",
        "gurgaon": "Gurugram",
        "poona": "Pune",
        "baroda": "Vadodara",
        "trivandrum": "Thiruvananthapuram",
        "cochin": "Kochi",
        "banaras": "Varanasi",
        "allahabad": "Prayagraj",
        "mysore": "Mysuru",
        "mangalore": "Mangaluru",
        "vizag": "Visakhapatnam",
        "secunderabad": "Hyderabad",
    }
    low = raw.lower()
    if low in city_fix:
        return city_fix[low]
    return raw


def clean_aishe_name(name: str) -> str:
    s = re.sub(r"\s+", " ", (name or "").strip())
    # Strip leading AISHE-style code prefixes like "D536 " or "C-1234 "
    s = re.sub(r"^[A-Z]\d{3,4}\s+", "", s)
    if s.isupper():
        # Smart title case preserving short acronyms
        words = []
        for w in s.split():
            if w in {"OF", "AND", "FOR", "IN", "AT", "TO", "THE", "ON"} and words:
                words.append(w.lower())
            elif len(w) <= 4 and w.isalpha() and w in {"IIT", "NIT", "IIIT", "IIM", "AIIMS", "SRM", "VIT", "PSG", "BMS", "RV", "MIT", "PES", "BITS", "DAV", "DIT", "KIIT", "SOA", "KL", "SR"}:
                words.append(w)
            else:
                words.append(w.title())
        s = " ".join(words)
    return s


def main():
    print("Loading raw DB export...")
    raw_db = json.load(open(RAW_DB_PATH, encoding="utf-8"))
    ia_rows = raw_db["intern_accounts"]
    app_rows = raw_db["applications"]

    print("Loading AISHE CSV (for city enrichment)...")
    csv_city_by_norm = {}
    with open(AISHE_CSV_PATH, encoding="utf-8-sig", errors="replace") as f:
        for row in csv.DictReader(f):
            nk = norm_key(row.get("name", ""))
            st = (row.get("state") or "").strip().lower()
            ct = clean_city(row.get("city", ""), row.get("district", ""))
            if nk and ct:
                csv_city_by_norm[(nk, st)] = ct
                if nk not in csv_city_by_norm:
                    csv_city_by_norm[(nk, "")] = ct

    print("Loading AISHE JSON (70,865 institutions)...")
    aishe_raw = json.load(open(AISHE_JSON_PATH, encoding="utf-8"))
    master_by_norm = {}
    master_list = []

    # Process Universities (U-) first so they take priority
    aishe_sorted = sorted(
        aishe_raw,
        key=lambda x: 0 if str(x.get("aishe_code", "")).startswith("U-") else 1
    )

    for item in aishe_sorted:
        raw_name = item.get("name", "")
        name = clean_aishe_name(raw_name)
        nk = norm_key(name)
        if not nk or len(nk) < 3:
            continue
        state = (item.get("state") or "").strip()
        district = (item.get("district") or "").strip()
        aishe_code = (item.get("aishe_code") or "").strip()
        city = csv_city_by_norm.get((nk, state.lower())) or csv_city_by_norm.get((nk, "")) or clean_city(district)

        # Universities are their own affiliated_university
        aff_univ = name if aishe_code.startswith("U-") else ""

        if nk not in master_by_norm:
            aliases = sorted(REVERSE_ALIASES.get(nk, set()))
            rec = {
                "canonical_name": name,
                "norm_key": nk,
                "aliases": aliases,
                "affiliated_university": aff_univ,
                "city": city,
                "state": state,
                "aishe_code": aishe_code,
                "source": "aishe",
                "is_verified": True,
            }
            master_by_norm[nk] = rec
            master_list.append(rec)
        else:
            # Enrich missing city or aishe_code
            existing = master_by_norm[nk]
            if not existing["city"] and city:
                existing["city"] = city
            if not existing["affiliated_university"] and aff_univ:
                existing["affiliated_university"] = aff_univ

    print(f"AISHE deduplicated master count: {len(master_list)}")

    # Build token index for fast fuzzy matching against AISHE
    token_index = defaultdict(list)
    stop_words = {"of", "and", "the", "for", "in", "at", "college", "university", "institute", "technology", "engineering", "science", "sciences", "management", "studies", "research", "education", "degree", "arts", "commerce", "govt", "government", "sri", "shri", "dr"}
    for idx, rec in enumerate(master_list):
        toks = [t for t in rec["norm_key"].split() if len(t) >= 3 and t not in stop_words]
        for t in toks[:6]:
            token_index[t].append(idx)

    # Collect all raw college + city pairs from DB
    raw_college_counts = Counter()
    raw_college_cities = defaultdict(Counter)
    for r in ia_rows + app_rows:
        c = (r.get("college") or "").strip()
        ct = clean_city(r.get("city") or "")
        if c:
            raw_college_counts[c] += 1
            if ct and ct.lower() != "other":
                raw_college_cities[c][ct] += 1

    print(f"Total unique raw college strings across DB: {len(raw_college_counts)}")

    mapping = {}
    junk_count_rows = 0
    junk_unique = 0
    exact_aishe_matched_unique = 0
    acronym_matched_unique = 0
    fuzzy_aishe_matched_unique = 0
    db_cleaned_groups = defaultdict(list)

    def find_match(raw_c: str):
        nk = norm_key(raw_c)
        if not nk or nk in JUNK_EXACT or len(nk) <= 2:
            return ("JUNK", None, 1.0)

        # 1. Acronym map
        if nk in ACRONYM_MAP:
            target_nk = norm_key(ACRONYM_MAP[nk])
            if target_nk in master_by_norm:
                return ("ACRONYM", master_by_norm[target_nk], 1.0)

        # 2. Exact norm_key match in AISHE
        if nk in master_by_norm:
            return ("EXACT_AISHE", master_by_norm[nk], 1.0)

        # 3. Fuzzy match against AISHE candidates sharing meaningful tokens
        toks = [t for t in nk.split() if len(t) >= 3 and t not in stop_words]
        cand_counts = Counter()
        for t in toks:
            for idx in token_index.get(t, []):
                cand_counts[idx] += 1

        best_rec = None
        best_score = 0.0
        for idx, _ in cand_counts.most_common(25):
            cand = master_list[idx]
            score = SequenceMatcher(None, nk, cand["norm_key"]).ratio()
            if score > best_score:
                best_score = score
                best_rec = cand

        if best_rec and best_score >= 0.88:
            return ("FUZZY_AISHE", best_rec, best_score)

        return ("UNMATCHED", None, best_score)

    unmatched_items = []
    for raw_c, cnt in raw_college_counts.items():
        mtype, rec, score = find_match(raw_c)
        top_db_city = raw_college_cities[raw_c].most_common(1)[0][0] if raw_college_cities[raw_c] else ""
        if mtype == "JUNK":
            junk_unique += 1
            junk_count_rows += cnt
            mapping[raw_c] = {"action": "CLEAR_JUNK", "canonical_name": None, "affiliated_university": None, "city": top_db_city or None}
        elif mtype in ("EXACT_AISHE", "ACRONYM", "FUZZY_AISHE"):
            if mtype == "EXACT_AISHE":
                exact_aishe_matched_unique += 1
            elif mtype == "ACRONYM":
                acronym_matched_unique += 1
            else:
                fuzzy_aishe_matched_unique += 1
            mapping[raw_c] = {
                "action": "MAP",
                "match_type": mtype,
                "score": round(score, 3),
                "canonical_name": rec["canonical_name"],
                "affiliated_university": rec["affiliated_university"] or None,
                "city": rec["city"] or top_db_city or None,
                "aishe_code": rec["aishe_code"],
            }
            if raw_c != rec["canonical_name"] and raw_c not in rec["aliases"]:
                if len(raw_c) <= 15 and raw_c.isupper():
                    rec["aliases"].append(raw_c)
        else:
            unmatched_items.append((raw_c, cnt, top_db_city))

    # Group unmatched DB strings by norm_key (and fuzzy-merge among themselves)
    unmatched_by_nk = defaultdict(list)
    for raw_c, cnt, top_db_city in unmatched_items:
        unmatched_by_nk[norm_key(raw_c)].append((raw_c, cnt, top_db_city))

    db_added_count = 0
    for nk, variants in unmatched_by_nk.items():
        # Pick the most frequent or best-cased variant as canonical
        variants_sorted = sorted(variants, key=lambda x: (x[1], not x[0].islower(), not x[0].isupper()), reverse=True)
        canon = variants_sorted[0][0].strip()
        if canon.islower() or canon.isupper():
            canon = clean_aishe_name(canon)
        city_counter = Counter()
        for rc, cnt, ct in variants:
            if ct:
                city_counter[ct] += cnt
        best_city = city_counter.most_common(1)[0][0] if city_counter else ""
        # Guess affiliated_university if "university" is in name
        aff_univ = canon if "university" in nk else ""

        rec = {
            "canonical_name": canon,
            "norm_key": nk,
            "aliases": [],
            "affiliated_university": aff_univ,
            "city": best_city,
            "state": "",
            "aishe_code": "",
            "source": "db_cleaned",
            "is_verified": True,
        }
        master_by_norm[nk] = rec
        master_list.append(rec)
        db_added_count += 1

        for rc, cnt, ct in variants:
            mapping[rc] = {
                "action": "MAP",
                "match_type": "DB_CLEANED",
                "score": 1.0,
                "canonical_name": canon,
                "affiliated_university": aff_univ or None,
                "city": best_city or ct or None,
                "aishe_code": "",
            }

    # Remove internal norm_key before saving seed
    seed_export = []
    for rec in master_list:
        seed_export.append({
            "name": rec["canonical_name"],
            "aliases": sorted(set(rec["aliases"])),
            "affiliated_university": rec["affiliated_university"],
            "city": rec["city"],
            "state": rec["state"],
            "aishe_code": rec["aishe_code"],
            "source": rec["source"],
            "is_verified": rec["is_verified"],
        })

    with open(SEED_OUT, "w", encoding="utf-8") as f:
        json.dump(seed_export, f, ensure_ascii=False)
    with open(MAPPING_OUT, "w", encoding="utf-8") as f:
        json.dump(mapping, f, ensure_ascii=False, indent=2)

    # Write Audit Report
    report = f"""# College & University Database Audit Report

## Live Database Summary (Before Cleanup)
- **`intern_accounts`**: {len(ia_rows)} rows ({sum(1 for r in ia_rows if (r.get('college') or '').strip())} non-empty `college`)
- **`applications`**: {len(app_rows)} rows ({sum(1 for r in app_rows if (r.get('college') or '').strip())} non-empty `college`)
- **Total unique raw `college` strings**: {len(raw_college_counts)}

## Normalization & AISHE Merge Results
- **AISHE Master Institutions loaded**: {len(master_list) - db_added_count} (Universities, Colleges, Standalone)
- **Additional DB-Cleaned Institutions added**: {db_added_count}
- **Total Canonical Master Directory Size**: {len(seed_export)}
- **DB Unique Strings Breakdown**:
  - Exact AISHE Matches: {exact_aishe_matched_unique}
  - Acronym/Shorthand Matches (e.g. VIT, LPU, SRM, KIIT): {acronym_matched_unique}
  - Fuzzy Misspelling/Variant Matches (>=0.88 similarity): {fuzzy_aishe_matched_unique}
  - Cleaned & Deduplicated DB-only Groups: {db_added_count} (from {len(unmatched_items)} raw variants)
  - Junk/Placeholder Strings Cleared: {junk_unique} unique strings ({junk_count_rows} total DB rows, e.g. `Pending Profile`, `Student`)
"""
    with open(REPORT_OUT, "w", encoding="utf-8") as f:
        f.write(report)

    print(report)
    print(f"Saved:\n  {SEED_OUT}\n  {MAPPING_OUT}\n  {REPORT_OUT}")


if __name__ == "__main__":
    main()
