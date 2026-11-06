from PIL import Image

def patch_certificate_template():
    base_path = "apps/portal/static/certificates/targets12.png"
    img = Image.open(base_path).convert("RGBA")

    # The background is solid dark navy in the top-right text zone:
    bg_col = (34, 38, 72, 255)

    # 1. Restore the intact loop of letter 'P' (Y: 370..430) and letter 'F' (Y: 220..300)
    # The vertical line at X=3190..3192 was previously cutting through them.
    # We heal the letters using the clean adjacent color from X=3185:
    for y in range(370, 430):
        for x in range(3188, 3195):
            p_samp = img.getpixel((3185, y))
            if p_samp[0] > 180 and p_samp[2] < 90:  # Orange text of P
                img.putpixel((x, y), p_samp)

    for y in range(220, 300):
        for x in range(3188, 3195):
            p_samp = img.getpixel((3185, y))
            if p_samp[0] > 180 and p_samp[1] > 180 and p_samp[2] > 180:  # White text of F
                img.putpixel((x, y), p_samp)

    # 2. Crop the entire "CERTIFICATE OF INTERNSHIP" text block (X: 2050..3215, Y: 200..510)
    text_crop = img.crop((2050, 200, 3215, 510))

    # 3. Clear the old text block region with navy background, preserving the vertical border line at 3190..3192
    for y in range(200, 510):
        for x in range(2050, 3215):
            if 3190 <= x <= 3192:
                img.putpixel((x, y), (80, 70, 68, 255))
            else:
                img.putpixel((x, y), bg_col)

    # 4. Paste the text block shifted 50 pixels to the left
    # This places the rightmost text at X=3153, leaving 38px of clean breathing room
    # to the golden vertical border line at X=3191.
    shift = 50
    w, h = text_crop.size
    for cy in range(h):
        for cx in range(w):
            p = text_crop.getpixel((cx, cy))
            # If not dark navy background:
            is_bg = (p[0] < 50 and p[1] < 50 and p[2] < 90)
            target_x = 2050 + cx - shift
            target_y = 200 + cy
            if not is_bg:
                img.putpixel((target_x, target_y), p)

    # Save backup and patched image
    img.save("apps/portal/static/certificates/targets12.png")
    print("Successfully patched apps/portal/static/certificates/targets12.png!")

if __name__ == "__main__":
    patch_certificate_template()
