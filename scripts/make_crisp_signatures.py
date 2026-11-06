import os
from PIL import Image, ImageDraw, ImageFont

output_dir = "apps/portal/static/certificates"
os.makedirs(output_dir, exist_ok=True)

font_path = r"C:\Windows\Fonts\segoesc.ttf"  # Elegant, clean, professional cursive signature
font_size = 120  # High resolution (4x scale)

font = ImageFont.truetype(font_path, font_size)

# Measure text
dummy = Image.new("RGBA", (10, 10))
d_dummy = ImageDraw.Draw(dummy)
bbox = d_dummy.textbbox((0, 0), "Abhinav Sharma", font=font)
w = bbox[2] - bbox[0] + 40
h = bbox[3] - bbox[1] + 40

# 1. Light signature (for dark certificate background)
img_light = Image.new("RGBA", (w, h), (255, 255, 255, 0))
d_light = ImageDraw.Draw(img_light)
d_light.text((20 - bbox[0], 20 - bbox[1]), "Abhinav Sharma", font=font, fill=(255, 255, 255, 240))
bbox_light = img_light.getbbox()
if bbox_light:
    img_light = img_light.crop(bbox_light)

light_path = os.path.join(output_dir, "sig_light_abhinav_crisp.png")
img_light.save(light_path, "PNG")
print("Saved light crisp signature:", light_path, "size:", img_light.size)

# 2. Dark signature (for white paper documents: Evaluation & LOR)
# Deep executive navy / royal indigo ink: #0F2942
img_dark = Image.new("RGBA", (w, h), (255, 255, 255, 0))
d_dark = ImageDraw.Draw(img_dark)
d_dark.text((20 - bbox[0], 20 - bbox[1]), "Abhinav Sharma", font=font, fill=(15, 41, 66, 245))
bbox_dark = img_dark.getbbox()
if bbox_dark:
    img_dark = img_dark.crop(bbox_dark)

dark_path = os.path.join(output_dir, "sig_dark_abhinav_crisp.png")
img_dark.save(dark_path, "PNG")
print("Saved dark crisp signature:", dark_path, "size:", img_dark.size)
