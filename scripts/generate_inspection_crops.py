import os
import shutil
from PIL import Image

ARTIFACT_DIR = r"C:\Users\user\.gemini\antigravity\brain\542c2e0b-55d0-41c9-9b46-721bf0724211"
OUTPUT_DIR = r"c:\Users\user\Desktop\dbert-website-lms\outputs\sample_kushal_agarwal"

doc1_png = os.path.join(OUTPUT_DIR, "1_Certificate_of_Completion_CERT-DBERT-2026-DA-001.png")
doc2_png = os.path.join(OUTPUT_DIR, "2_Academic_Project_Evaluation_CERT-DBERT-2026-DA-001.png")
doc3_png = os.path.join(OUTPUT_DIR, "3_Letter_of_Recommendation_CERT-DBERT-2026-DA-001_updated.png")
if not os.path.exists(doc3_png):
    doc3_png = os.path.join(OUTPUT_DIR, "3_Letter_of_Recommendation_CERT-DBERT-2026-DA-001.png")

# Copy full PNGs to artifact directory
target_doc1 = os.path.join(ARTIFACT_DIR, "doc1_2month_georgia_rework.png")
target_doc2 = os.path.join(ARTIFACT_DIR, "doc2_2month_evaluation_rework.png")
target_doc3 = os.path.join(ARTIFACT_DIR, "doc3_2month_lor_rework.png")

shutil.copyfile(doc1_png, target_doc1)
shutil.copyfile(doc2_png, target_doc2)
shutil.copyfile(doc3_png, target_doc3)
print("Copied full previews to artifact directory.")

# Now create focused high-resolution crops
# Doc 1: Signature & Footer
im1 = Image.open(target_doc1)
w1, h1 = im1.size
# Crop bottom 40% of Doc 1 (w1 x h1)
crop1 = im1.crop((0, int(h1 * 0.55), w1, h1))
crop1.save(os.path.join(ARTIFACT_DIR, "doc1_bottom_and_sig_crop.png"))

# Doc 2: Header crop (Top 20%)
im2 = Image.open(target_doc2)
w2, h2 = im2.size
crop2_header = im2.crop((0, 0, w2, int(h2 * 0.16)))
crop2_header.save(os.path.join(ARTIFACT_DIR, "doc2_header_subtitle_crop.png"))

# Doc 2: Candidate Meta Box crop (approx 15% to 32%)
crop2_meta = im2.crop((int(w2 * 0.04), int(h2 * 0.15), int(w2 * 0.96), int(h2 * 0.32)))
crop2_meta.save(os.path.join(ARTIFACT_DIR, "doc2_metabox_crop.png"))

# Doc 2: Bottom Signature & QR crop (approx 78% to 100%)
crop2_sig = im2.crop((0, int(h2 * 0.78), w2, h2))
crop2_sig.save(os.path.join(ARTIFACT_DIR, "doc2_sig_turnitin_crop.png"))

# Doc 3: Header crop
im3 = Image.open(target_doc3)
w3, h3 = im3.size
crop3_header = im3.crop((0, 0, w3, int(h3 * 0.17)))
crop3_header.save(os.path.join(ARTIFACT_DIR, "doc3_header_subtitle_crop.png"))

# Doc 3: Paragraph 1 2-Month text crop (approx 17% to 33%)
crop3_body = im3.crop((int(w3 * 0.04), int(h3 * 0.17), int(w3 * 0.96), int(h3 * 0.33)))
crop3_body.save(os.path.join(ARTIFACT_DIR, "doc3_p1_2month_crop.png"))

# Doc 3: Bottom Single Signature & QR crop (approx 78% to 100%)
crop3_sig = im3.crop((0, int(h3 * 0.78), w3, h3))
crop3_sig.save(os.path.join(ARTIFACT_DIR, "doc3_single_sig_crop.png"))

print("All crops successfully generated in artifact directory!")
