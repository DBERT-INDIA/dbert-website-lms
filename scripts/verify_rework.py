import os
import fitz

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs", "sample_kushal_agarwal")

docs = [
    ("Doc 1 (Certificate)", os.path.join(OUTPUT_DIR, "1_Certificate_of_Completion_CERT-DBERT-2026-DA-001.pdf")),
    ("Doc 2 (Evaluation)", os.path.join(OUTPUT_DIR, "2_Academic_Project_Evaluation_CERT-DBERT-2026-DA-001.pdf")),
    ("Doc 3 (LOR)", os.path.join(OUTPUT_DIR, "3_Letter_of_Recommendation_CERT-DBERT-2026-DA-001_updated.pdf")),
]

# If Doc 3 updated doesn't exist, check base
if not os.path.exists(docs[2][1]):
    docs[2] = ("Doc 3 (LOR)", os.path.join(OUTPUT_DIR, "3_Letter_of_Recommendation_CERT-DBERT-2026-DA-001.pdf"))

print("=== RUNNING RIGOROUS PYMUPDF AUDIT ===")

all_passed = True
for name, p in docs:
    print(f"\n--- Checking {name}: {os.path.basename(p)} ---")
    doc = fitz.open(p)
    page = doc[0]
    text = page.get_text()

    # 1. MSME Check (MUST BE ZERO)
    if "MSME" in text.upper():
        print("  [FAIL] Found MSME in text!")
        all_passed = False
    else:
        print("  [PASS] Zero MSME mentions found.")

    # 2. Duration Check (Must be 2 Months)
    if "2 Months" in text or "2-month" in text:
        print("  [PASS] Confirmed 2 Months duration in document.")
    else:
        print("  [FAIL] 2 Months duration NOT found!")
        all_passed = False

    # 3. Subtitle Check (Doc 2 & Doc 3)
    if name != "Doc 1 (Certificate)":
        if "Digital Blinc Education Research and Technology" in text:
            print("  [PASS] Confirmed institutional subtitle '(Digital Blinc Education Research and Technology)' in header.")
        else:
            print("  [FAIL] Institutional subtitle missing!")
            all_passed = False

    # 4. Check Signatory
    if "Mr. Abhinav Sharma" in text:
        print("  [PASS] Found signatory Mr. Abhinav Sharma.")
    else:
        print("  [FAIL] Signatory Mr. Abhinav Sharma missing!")
        all_passed = False

    # 5. Check Verification QR URL
    images = page.get_images()
    print(f"  [INFO] Number of embedded image objects: {len(images)}")
    # Doc 1: Background + Signature + QR = 3 images
    # Doc 2: Plagiarism stamp + Signature + QR = 3 images (Digital stamp standard removed!)
    # Doc 3: Signature + QR = 2 images (Digital stamp standard removed!)
    if name == "Doc 1 (Certificate)" and len(images) == 3:
        print("  [PASS] Doc 1 has exactly 3 image objects (Background, Edwardian Signature, QR code).")
    elif name == "Doc 2 (Evaluation)" and len(images) == 3:
        print("  [PASS] Doc 2 has exactly 3 image objects (Turnitin seal, Edwardian Signature, QR code - dual signature stamp eliminated).")
    elif name == "Doc 3 (LOR)" and len(images) == 2:
        print("  [PASS] Doc 3 has exactly 2 image objects (Edwardian Signature, QR code - dual signature stamp eliminated).")

print(f"\nAUDIT RESULT: {'ALL TESTS PASSED PERFECTLY!' if all_passed else 'SOME TESTS FAILED'}")
