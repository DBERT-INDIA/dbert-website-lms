import sqlite3
import pandas as pd
from datetime import timedelta
import datetime

db_path = 'apps/portal/internship.db'

def is_empty(val):
    if pd.isna(val): return True
    if str(val).strip().lower() in ['nan', 'none', 'n/a', 'null', 'unknown', '']: return True
    return False

# 1. Load International
df_intl = pd.read_csv('master_internships_published.csv')
df_intl['Source'] = 'Global API'
df_intl['Region'] = 'International'

# 2. Load Indian (Unstop/Internshala)
df_in = pd.read_csv('indian_master_internships.csv')
df_in['Source'] = 'Unstop / Internshala'
df_in['Region'] = 'India'

# 3. Load LinkedIn
df_li = pd.read_csv('indian_internships_sourced.csv')
df_li['Source'] = 'LinkedIn'
df_li['Region'] = 'India'

# Scrub LinkedIn (it might be missing Start Date, End Date, Stipend)
if 'Start Date' not in df_li.columns:
    df_li['Start Date'] = datetime.datetime.now().strftime('%Y-%m-%d')
if 'End Date / Duration' not in df_li.columns:
    df_li['End Date / Duration'] = (datetime.datetime.now() + timedelta(days=90)).strftime('%Y-%m-%d')
if 'Stipend / Salary' not in df_li.columns:
    df_li['Stipend / Salary'] = 'Not Disclosed'

def scrub_dates(row):
    if is_empty(row.get('Start Date')):
        row['Start Date'] = datetime.datetime.now().strftime('%Y-%m-%d')
    if is_empty(row.get('End Date / Duration')):
        try:
            start_dt = pd.to_datetime(row['Start Date'])
            row['End Date / Duration'] = (start_dt + timedelta(days=90)).strftime('%Y-%m-%d')
        except:
            row['End Date / Duration'] = (datetime.datetime.now() + timedelta(days=90)).strftime('%Y-%m-%d')
    if is_empty(row.get('Stipend / Salary')):
        row['Stipend / Salary'] = 'Not Disclosed'
    return row

df_li = df_li.apply(scrub_dates, axis=1)

# Combine all
df_all = pd.concat([df_intl, df_in, df_li], ignore_index=True)

# Standardize Is Remote
df_all['Is Remote'] = df_all['Is Remote'].apply(lambda x: 'Yes' if str(x).lower() in ['yes', 'true', '1', 'remote'] else 'No')

# Rename columns to be safe for SQL
df_all.rename(columns={
    'End Date / Duration': 'End_Date',
    'Stipend / Salary': 'Stipend',
    'Is Remote': 'Is_Remote',
    'Start Date': 'Start_Date'
}, inplace=True)

# Create/Insert into DB
conn = sqlite3.connect(db_path)
c = conn.cursor()

c.execute('''
CREATE TABLE IF NOT EXISTS scraped_internships (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    Domain TEXT,
    Company TEXT,
    Role TEXT,
    Location TEXT,
    Is_Remote TEXT,
    Start_Date TEXT,
    End_Date TEXT,
    Stipend TEXT,
    URL TEXT,
    Description TEXT,
    Source TEXT,
    Region TEXT
)
''')
c.execute('DELETE FROM scraped_internships') # Clear existing if any

df_all[['Domain', 'Company', 'Role', 'Location', 'Is_Remote', 'Start_Date', 'End_Date', 'Stipend', 'URL', 'Description', 'Source', 'Region']].to_sql('scraped_internships', conn, if_exists='append', index=False)
conn.commit()

print(f"Successfully inserted {len(df_all)} rows into scraped_internships.")
conn.close()
