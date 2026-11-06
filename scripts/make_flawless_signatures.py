import os
from PIL import Image, ImageDraw, ImageFont

output_dir = "apps/portal/static/certificates"
os.makedirs(output_dir, exist_ok=True)

# Generate both Edwardian Script (formal executive) and Segoe Script (clean cursive)
# Rendered at ultra-high resolution (font size 160) so ReportLab scales down with zero blur.
fonts = [
    ("edwardian", r"C:\Windows\Fonts\ITCEDSCR.TTF", 160),
    ("segoe", r"C:\Windows\Fonts\segoesc.ttf", 140)
]

for name, fpath, fsize in fonts:
    if not os.path.exists(fpath):
        continue
    font = ImageFont.truetype(fpath, fsize)
    dummy = Image.new("RGBA", (10, 10))
    d_d = ImageDraw.Draw(dummy)
    bbox = d_d.textbbox((0, 0), "Abhinav Sharma", font=font)
    w = bbox[2] - bbox[0] + 60
    h = bbox[3] - bbox[1] + 60

    # 1. Light Signature (crisp white for dark certificate background targets12.png)
    img_l = Image.new("RGBA", (w, h), (255, 255, 255, 0))
    d_l = ImageDraw.Draw(img_l)
    d_l.text((30 - bbox[0], 30 - bbox[1]), "Abhinav Sharma", font=font, fill=(255, 255, 255, 255))
    b_l = img_l.getbbox()
    if b_l:
        img_l = img_l.crop(b_l)
    path_l = os.path.join(output_dir, f"sig_light_{name}.png")
    img_l.save(path_l, "PNG")
    print(f"Saved {path_l}: {img_l.size}, aspect: {img_l.size[0]/img_l.size[1]:.2f}")

    # 2. Dark Signature (deep executive navy ink #0F2942 for white paper Evaluation & LOR)
    img_d = Image.new("RGBA", (w, h), (255, 255, 255, 0))
    d_d = ImageDraw.Draw(img_d)
    d_d.text((30 - bbox[0], 30 - bbox[1]), "Abhinav Sharma", font=font, fill=(15, 41, 66, 255))
    b_d = img_d.getbbox()
    if b_d:
        img_d = img_d.crop(b_d)
    path_d = os.path.join(output_dir, f"sig_dark_{name}.png")
    img_d.save(path_d, "PNG")
    print(f"Saved {path_d}: {img_d.size}, aspect: {img_d.size[0]/img_d.size[1]:.2f}")

print("Signature generation complete!")
