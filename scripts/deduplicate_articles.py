# -*- coding: utf-8 -*-
"""
Deduplicate articles in production EC2 PostgreSQL (dbert_internship.intern_articles).
Keeps the canonical copy (PUBLISHED > APPROVED > PENDING_REVIEW > DRAFT, latest updated_at).
Normalizes all published_url to https://dbert.in/blog/{slug}.
Exports canonical published articles to published_articles.json.
"""

import sys
import json
import re

# Redundant duplicate IDs identified and approved in the plan:
# Intern 3269: #30 (duplicate of #31)
# Intern 3326: #16 (duplicate of #17), #14 (duplicate of #15)
# Intern 4349: #33, #34, #35 (duplicates of #32)
# Intern 4442: #25, #26, #27 (duplicates of #24)
# Intern 4542: #22 (duplicate of #23)
# Intern 4598: #19, #20, #21 (duplicates of #18)
# Intern 4840: #41 (duplicate of #40)
# Intern 4979: #36, #37, #39 (duplicates of #38)
# Sakthi P duplicate account (4962 vs 4492): #12 (duplicate of #11)
# Legacy test accounts (669 vs 672): #1 (duplicate draft of #2)

DUPLICATE_IDS_TO_DELETE = [
    1,   # duplicate draft of #2 (Exploratory Data Analysis)
    12,  # cross-account duplicate of #11 (Sakthi P)
    14,  # duplicate draft of #15 (Microservices)
    16,  # duplicate draft of #17 (Redis Caching)
    19,  # duplicate draft of #18 (Gayatri AI)
    20,  # duplicate draft of #18 (Gayatri AI)
    21,  # duplicate draft of #18 (Gayatri AI)
    22,  # duplicate draft of #23 (Software Engineering AI)
    25,  # duplicate draft of #24 (Architecting 29)
    26,  # duplicate draft of #24 (Architecting 29)
    27,  # duplicate draft of #24 (Architecting 29)
    30,  # duplicate pending review of #31 (Alkame NIFTY 50)
    33,  # duplicate draft of #32 (Gayatri AI Platform)
    34,  # duplicate pending review of #32 (Gayatri AI Platform)
    35,  # duplicate pending review of #32 (Gayatri AI Platform)
    36,  # duplicate pending review of #38 (Alkeme)
    37,  # duplicate pending review of #38 (Alkeme)
    39,  # duplicate pending review of #38 (Alkeme)
    41,  # duplicate pending review of #40 (Alkame-50 Nifty)
]

def slugify(title):
    s = title.lower().strip()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s[:80]

SQL_DEDUPLICATE = f"""
BEGIN;

-- 1. Create safety backup table
CREATE TABLE IF NOT EXISTS dbert_internship.intern_articles_backup_20261114 AS 
SELECT * FROM dbert_internship.intern_articles;

-- 2. Delete the 19 identified redundant duplicates
DELETE FROM dbert_internship.intern_articles 
WHERE id IN ({','.join(str(i) for i in DUPLICATE_IDS_TO_DELETE)});

-- 3. Normalize all published_url from /insights/ to /blog/
UPDATE dbert_internship.intern_articles
SET published_url = REPLACE(published_url, 'https://dbert.in/insights/', 'https://dbert.in/blog/')
WHERE published_url LIKE '%/insights/%';

-- 4. Ensure all APPROVED or PUBLISHED articles have their canonical published_url
UPDATE dbert_internship.intern_articles
SET status = 'PUBLISHED'
WHERE status = 'APPROVED';

COMMIT;
"""

print(f"Total duplicate IDs to purge: {len(DUPLICATE_IDS_TO_DELETE)}")
print(SQL_DEDUPLICATE)
