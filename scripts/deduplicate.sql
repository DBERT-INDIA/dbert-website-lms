BEGIN;

-- 1. Create safety backup table
CREATE TABLE IF NOT EXISTS dbert_internship.intern_articles_backup_20261114 AS 
SELECT * FROM dbert_internship.intern_articles;

-- 2. Delete the 19 identified redundant duplicates
DELETE FROM dbert_internship.intern_articles 
WHERE id IN (1, 12, 14, 16, 19, 20, 21, 22, 25, 26, 27, 30, 33, 34, 35, 36, 37, 39, 41);

-- 3. Normalize all published_url from /insights/ to /blog/
UPDATE dbert_internship.intern_articles
SET published_url = REPLACE(published_url, 'https://dbert.in/insights/', 'https://dbert.in/blog/')
WHERE published_url LIKE '%/insights/%';

-- 4. Set APPROVED to PUBLISHED
UPDATE dbert_internship.intern_articles
SET status = 'PUBLISHED'
WHERE status = 'APPROVED';

COMMIT;
