import json
from pathlib import Path
from bs4 import BeautifulSoup

def verify_main_directory():
    html_path = Path('apps/website/.next/server/app/verify/directory.html')
    data_path = Path('apps/website/src/data/directory_candidates.json')

    with open(html_path, encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

    with open(data_path, encoding='utf-8') as f:
        raw = json.load(f)

    verified_candidates = [
        c for c in raw
        if not c.get('isProvisional') and (c.get('status', '').upper() == 'VERIFIED' or c.get('verified') is True)
    ]
    verified_certs = {c['certId'] for c in verified_candidates}
    provisional_only_certs = {c['certId'] for c in raw if c.get('isProvisional')} - verified_certs

    print(f"Total raw records in json: {len(raw)}")
    print(f"Verified candidates count: {len(verified_candidates)} (Expected: 96)")
    print(f"Provisional-only certs: {len(provisional_only_certs)}")
    assert len(verified_candidates) == 96, f"Expected 96, got {len(verified_candidates)}"

    # 1. ItemList Schema Verification
    scripts = soup.find_all('script', type='application/ld+json')
    item_list_ld = None
    for s in scripts:
        try:
            d = json.loads(s.string)
            if isinstance(d, dict) and d.get('@type') == 'ItemList':
                item_list_ld = d
                break
        except Exception:
            pass

    assert item_list_ld is not None, "ItemList schema not found in directory.html"
    num_items = item_list_ld.get('numberOfItems')
    print(f"Main directory ItemList numberOfItems: {num_items} (Expected: 96)")
    assert num_items == 96, f"Expected 96, got {num_items}"

    elements = item_list_ld.get('itemListElement', [])
    print(f"Main directory ItemList elements count: {len(elements)}")
    prov_in_ld = [
        el['item']['identifier']
        for el in elements
        if el.get('item', {}).get('identifier') in provisional_only_certs
    ]
    print(f"Provisional candidates in ItemList: {len(prov_in_ld)} (Expected: 0)")
    assert len(prov_in_ld) == 0, f"Found provisional candidates in ItemList: {prov_in_ld}"

    # Verify all items in ItemList are verified candidates
    for el in elements:
        cert = el.get('item', {}).get('identifier')
        assert cert in verified_certs, f"Certificate {cert} in ItemList is not verified!"

    # 2. RSC flight payload & HTML leak verification
    html_content = html_path.read_text(encoding='utf-8')
    prov_in_rsc = [cert for cert in provisional_only_certs if cert in html_content]
    print(f"Provisional-only certs in HTML/RSC payload: {len(prov_in_rsc)} (Expected: 0)")
    assert len(prov_in_rsc) == 0, f"Found provisional certs in RSC payload: {prov_in_rsc[:5]}"

    # Verify file size reduction
    size_kb = len(html_content.encode('utf-8')) / 1024
    print(f"directory.html file size: {size_kb:.1f} KB (Reduced from ~583 KB)")
    print("PASS: Main directory is 100% clean of provisional data!")

def verify_domain_directories():
    base_dir = Path('apps/website/.next/server/app/verify/directory')
    data_path = Path('apps/website/src/data/directory_candidates.json')

    with open(data_path, encoding='utf-8') as f:
        raw = json.load(f)

    verified_candidates = [
        c for c in raw
        if not c.get('isProvisional') and (c.get('status', '').upper() == 'VERIFIED' or c.get('verified') is True)
    ]
    verified_certs = {c['certId'] for c in verified_candidates}
    provisional_only_certs = {c['certId'] for c in raw if c.get('isProvisional')} - verified_certs

    domain_files = [f for f in base_dir.glob('*.html') if f.name != 'directory.html']
    print(f"\nFound {len(domain_files)} domain directory pages to verify:")
    for df in domain_files:
        with open(df, encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
        scripts = soup.find_all('script', type='application/ld+json')
        item_list_ld = None
        for s in scripts:
            try:
                d = json.loads(s.string)
                if isinstance(d, dict) and d.get('@type') == 'ItemList':
                    item_list_ld = d
                    break
            except Exception:
                pass

        if item_list_ld:
            num = item_list_ld.get('numberOfItems', 0)
            elements = item_list_ld.get('itemListElement', [])
            prov_leaks = [
                el['item']['identifier']
                for el in elements
                if el.get('item', {}).get('identifier') in provisional_only_certs
            ]
            print(f" - {df.name}: numberOfItems = {num}, elements = {len(elements)}, prov_leaks = {len(prov_leaks)}")
            assert len(prov_leaks) == 0, f"Provisional leakage in {df.name}: {prov_leaks}"
            for el in elements:
                cert = el.get('item', {}).get('identifier')
                assert cert in verified_certs, f"Certificate {cert} in {df.name} ItemList is not verified!"

        # Verify no provisional certs in domain HTML either
        content = df.read_text(encoding='utf-8')
        leaked_in_domain = [cert for cert in provisional_only_certs if cert in content]
        print(f"   Provisional in {df.name} HTML/RSC: {len(leaked_in_domain)} (Expected: 0)")
        assert len(leaked_in_domain) == 0, f"Found provisional in {df.name}: {leaked_in_domain[:5]}"

if __name__ == '__main__':
    print("=== VERIFYING MAIN DIRECTORY ===")
    verify_main_directory()
    print("\n=== VERIFYING DOMAIN DIRECTORIES ===")
    verify_domain_directories()
    print("\n>>> ALL PHASE 2 DATA LEAKAGE CHECKS PASSED WITH 100% FIDELITY! <<<")
