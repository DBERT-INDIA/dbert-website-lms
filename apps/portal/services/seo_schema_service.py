"""
DBERT Engineering — SEO Schema & Structured Data Service
Provides standardized Schema.org JobPosting, PostalAddress, and MonetaryAmount generators
compliant with Google Search Central and Google for Jobs specifications.
"""

import re
from typing import Dict, Any, Optional

# Standardized Indian City -> PostalAddress Directory
INDIAN_CITY_DIRECTORY = {
    "chennai": {
        "locality": "Chennai",
        "region": "Tamil Nadu",
        "postalCode": "600001",
        "street": "Old Mahabalipuram Rd, Tech Corridor",
    },
    "bengaluru": {
        "locality": "Bengaluru",
        "region": "Karnataka",
        "postalCode": "560001",
        "street": "Outer Ring Road, Manyata Tech Park",
    },
    "bangalore": {
        "locality": "Bengaluru",
        "region": "Karnataka",
        "postalCode": "560001",
        "street": "Outer Ring Road, Manyata Tech Park",
    },
    "mumbai": {
        "locality": "Mumbai",
        "region": "Maharashtra",
        "postalCode": "400051",
        "street": "Bandra Kurla Complex (BKC)",
    },
    "pune": {
        "locality": "Pune",
        "region": "Maharashtra",
        "postalCode": "411057",
        "street": "Hinjawadi Rajiv Gandhi Infotech Park",
    },
    "hyderabad": {
        "locality": "Hyderabad",
        "region": "Telangana",
        "postalCode": "500081",
        "street": "HITEC City, Madhapur",
    },
    "delhi": {
        "locality": "Delhi",
        "region": "Delhi",
        "postalCode": "110001",
        "street": "Connaught Place, Barakhamba Rd",
    },
    "delhi-ncr": {
        "locality": "Delhi NCR",
        "region": "Delhi",
        "postalCode": "110001",
        "street": "Barakhamba Road",
    },
    "delhi ncr": {
        "locality": "Delhi NCR",
        "region": "Delhi",
        "postalCode": "110001",
        "street": "Barakhamba Road",
    },
    "gurgaon": {
        "locality": "Gurugram",
        "region": "Haryana",
        "postalCode": "122002",
        "street": "DLF Cyber City, Sector 24",
    },
    "gurugram": {
        "locality": "Gurugram",
        "region": "Haryana",
        "postalCode": "122002",
        "street": "DLF Cyber City, Sector 24",
    },
    "noida": {
        "locality": "Noida",
        "region": "Uttar Pradesh",
        "postalCode": "201301",
        "street": "Sector 62, Electronic City",
    },
    "kolkata": {
        "locality": "Kolkata",
        "region": "West Bengal",
        "postalCode": "700091",
        "street": "Sector V, Salt Lake City",
    },
    "ahmedabad": {
        "locality": "Ahmedabad",
        "region": "Gujarat",
        "postalCode": "380015",
        "street": "SG Highway, Prahlad Nagar",
    },
    "jaipur": {
        "locality": "Jaipur",
        "region": "Rajasthan",
        "postalCode": "302017",
        "street": "Malviya Nagar Industrial Area",
    },
    "lucknow": {
        "locality": "Lucknow",
        "region": "Uttar Pradesh",
        "postalCode": "226010",
        "street": "Vibhuti Khand, Gomti Nagar",
    },
    "chandigarh": {
        "locality": "Chandigarh",
        "region": "Chandigarh",
        "postalCode": "160019",
        "street": "Rajiv Gandhi Chandigarh Technology Park",
    },
    "kochi": {
        "locality": "Kochi",
        "region": "Kerala",
        "postalCode": "682030",
        "street": "Infopark, Kakkanad",
    },
    "cochin": {
        "locality": "Kochi",
        "region": "Kerala",
        "postalCode": "682030",
        "street": "Infopark, Kakkanad",
    },
    "indore": {
        "locality": "Indore",
        "region": "Madhya Pradesh",
        "postalCode": "452001",
        "street": "Crystal IT Park, Ring Road",
    },
    "coimbatore": {
        "locality": "Coimbatore",
        "region": "Tamil Nadu",
        "postalCode": "641014",
        "street": "TIDEL Park, Civil Aerodrome Post",
    },
    "surat": {
        "locality": "Surat",
        "region": "Gujarat",
        "postalCode": "395007",
        "street": "Ring Road, Surat Textile Market",
    },
    "nagpur": {
        "locality": "Nagpur",
        "region": "Maharashtra",
        "postalCode": "440010",
        "street": "MIHAN IT SEZ",
    },
    "bhopal": {
        "locality": "Bhopal",
        "region": "Madhya Pradesh",
        "postalCode": "462001",
        "street": "MP Nagar Zone 1",
    },
    "patna": {
        "locality": "Patna",
        "region": "Bihar",
        "postalCode": "800001",
        "street": "Frazer Road, Dak Bungalow",
    },
    "bhubaneswar": {
        "locality": "Bhubaneswar",
        "region": "Odisha",
        "postalCode": "751024",
        "street": "Infocity, Chandaka Industrial Estate",
    },
    "thiruvananthapuram": {
        "locality": "Thiruvananthapuram",
        "region": "Kerala",
        "postalCode": "695581",
        "street": "Technopark Campus, Kazhakoottam",
    },
    "trivandrum": {
        "locality": "Thiruvananthapuram",
        "region": "Kerala",
        "postalCode": "695581",
        "street": "Technopark Campus, Kazhakoottam",
    },
    "visakhapatnam": {
        "locality": "Visakhapatnam",
        "region": "Andhra Pradesh",
        "postalCode": "530003",
        "street": "Rushikonda IT SEZ",
    },
    "vizag": {
        "locality": "Visakhapatnam",
        "region": "Andhra Pradesh",
        "postalCode": "530003",
        "street": "Rushikonda IT SEZ",
    },
    "vadodara": {
        "locality": "Vadodara",
        "region": "Gujarat",
        "postalCode": "390007",
        "street": "Alkapuri Business District",
    },
}


def get_postal_address_for_city(city_raw: Optional[str], region_raw: Optional[str] = None) -> Dict[str, str]:
    """Returns a fully-formed Schema.org PostalAddress dict with streetAddress,
    addressLocality, addressRegion, postalCode, and addressCountry ('IN')."""
    if not city_raw:
        city_raw = "Bengaluru"

    clean_key = re.sub(r"[^a-z0-9]+", "-", city_raw.strip().lower()).strip("-")
    lookup = INDIAN_CITY_DIRECTORY.get(clean_key)

    if not lookup:
        primary_part = clean_key.split("-")[0]
        lookup = INDIAN_CITY_DIRECTORY.get(primary_part)

    if lookup:
        return {
            "@type": "PostalAddress",
            "streetAddress": lookup["street"],
            "addressLocality": lookup["locality"],
            "addressRegion": lookup["region"],
            "postalCode": lookup["postalCode"],
            "addressCountry": "IN",
        }

    # Fallback with formatted city
    city_name = city_raw.split(",")[0].strip().title() or "Bengaluru"
    reg = (region_raw or "India").strip()
    return {
        "@type": "PostalAddress",
        "streetAddress": "Commercial Business District",
        "addressLocality": city_name,
        "addressRegion": reg,
        "postalCode": "110001",
        "addressCountry": "IN",
    }


def parse_base_salary_schema(
    stipend_text: Optional[str],
    default_period: str = "MONTH",
    currency: str = "INR"
) -> Optional[Dict[str, Any]]:
    """Parses raw stipend strings (e.g. '₹25,000 / month', '15000-25000', '12000')
    into a valid Schema.org MonetaryAmount with numeric QuantitativeValue.
    Returns None if no numeric amount can be parsed (Disclosed upon interview, Unpaid, etc.)
    which avoids the Google Search Console 'Missing field value' warning."""
    if not stipend_text or not isinstance(stipend_text, str):
        return None

    cleaned = stipend_text.strip()
    if cleaned.lower() in (
        "not disclosed",
        "disclosed upon interview",
        "unpaid",
        "performance stipend",
        "negotiable",
        "as per industry standards",
    ):
        return None

    # Find integer numbers (stripping commas) >= 500
    raw_nums = re.findall(r"(?:₹|\bINR\b|\bRs\.?\b)?\s*(\d[\d,]*)", cleaned)
    amounts = []
    for num_str in raw_nums:
        val_str = num_str.replace(",", "")
        if val_str.isdigit():
            val = int(val_str)
            if val >= 500:  # ignore tiny numbers like '3' months or '1' year
                amounts.append(val)

    if not amounts:
        return None

    # Check pay period
    lower_txt = cleaned.lower()
    period = default_period.upper()
    if any(k in lower_txt for k in ("year", "annum", "lpa", "per annum")):
        period = "YEAR"
    elif "week" in lower_txt:
        period = "WEEK"
    elif "day" in lower_txt:
        period = "DAY"
    elif "hour" in lower_txt:
        period = "HOUR"

    amt_val: Dict[str, Any] = {
        "@type": "QuantitativeValue",
        "unitText": period,
    }
    if len(amounts) >= 2:
        lo = min(amounts[0], amounts[1])
        hi = max(amounts[0], amounts[1])
        if lo < hi:
            amt_val["minValue"] = lo
            amt_val["maxValue"] = hi
        else:
            amt_val["value"] = lo
    else:
        amt_val["value"] = amounts[0]

    return {
        "@type": "MonetaryAmount",
        "currency": currency,
        "value": amt_val,
    }
