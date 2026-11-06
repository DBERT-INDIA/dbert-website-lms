import requests
import re
from bs4 import BeautifulSoup

url = 'https://docs.google.com/forms/d/e/1FAIpQLSeHCTK_HO5ZbNHNcPiyW-04Y4bBeZ0RvQP7I4koQnW91d6phA/viewform?usp=header'
resp = requests.get(url, timeout=10)
print('Status:', resp.status_code)

soup = BeautifulSoup(resp.text, 'html.parser')
# Find form title
title = soup.find('div', role='heading')
print('Form Title:', title.get_text() if title else 'No title')

# Find questions
questions = soup.find_all('div', role='listitem')
print(f'Total question listitems: {len(questions)}')
for i, q in enumerate(questions):
    heading = q.find('div', role='heading')
    desc = q.find('div', id=lambda x: x and 'desc' in x)
    h_text = heading.get_text().strip() if heading else 'No heading'
    d_text = desc.get_text().strip() if desc else ''
    print(f"[{i+1}] {h_text}")
    if d_text:
        print(f"    Desc: {d_text}")
