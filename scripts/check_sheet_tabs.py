import urllib.request
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

url = 'https://docs.google.com/spreadsheets/d/1yacGLZGiTD_8GLOUHMphbdfsORqc8u_DrjvpVRSEDgs/edit'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req) as resp:
        html = resp.read().decode('utf-8', errors='ignore')
    
    # Save a snippet or search for tabs
    tab_matches = re.findall(r'\[\s*\"([^\"]+)\"\s*,\s*(\d+)\s*,\s*\"[^\"]*\"\s*,\s*\"[^\"]*\"\s*\]', html)
    print("Tab matches 1:", tab_matches)
    
    # Another common pattern:
    sheet_data = re.findall(r'\"name\":\s*\"([^\"]+)\"[^\{\}\[\]]*?\"sheetId\":\s*(\d+)', html)
    print("Sheet data 2:", sheet_data)
    
    # Or search for bootstrap data
    gids = set(re.findall(r'gid[=\":](\d+)', html))
    print("All gids found:", gids)
    
    # Let's search for sheet title
    title = re.findall(r'<title>([^<]+)</title>', html)
    print("Title:", title)
except Exception as e:
    print("Error:", e)
