from PIL import Image

base_img = Image.open('apps/portal/static/certificates/targets12.png').convert('RGBA')
opt = base_img.copy()

# Sample orange color of letter P
orange_p = base_img.getpixel((3180, 470))
print("Orange color of P:", orange_p)

# 1. Erase old vertical line at X = 3190..3192 from Y = 107 to Y = 2000
for y in range(107, 2000):
    for offset in range(-1, 3):
        cur_p = base_img.getpixel((3191 + offset, y))
        # If this pixel is part of the old line (grey/goldish):
        # Line color is around (75..85, 66..75, 65..75)
        is_line = (60 < cur_p[0] < 100 and 55 < cur_p[1] < 85 and 55 < cur_p[2] < 85)
        
        # Check if we are inside the letter P (Y between 400 and 530, X between 3185 and 3202)
        # In letter P, replace line with orange!
        if 400 <= y <= 530 and 3185 <= (3191 + offset) <= 3202:
            # Check adjacent pixels in P to see if we are inside P's stroke
            left_p = base_img.getpixel((3185, y))
            if left_p[0] > 200 and left_p[1] > 120 and left_p[2] < 80:
                opt.putpixel((3191 + offset, y), left_p)
                continue

        # In white text F (Y between 220 and 270)
        if 220 <= y <= 270 and 3185 <= (3191 + offset) <= 3204:
            left_p = base_img.getpixel((3185, y))
            if left_p[0] > 200 and left_p[1] > 200 and left_p[2] > 200:
                opt.putpixel((3191 + offset, y), left_p)
                continue

        # Otherwise replace with navy background
        bg_p = base_img.getpixel((3180, y))
        opt.putpixel((3191 + offset, y), bg_p)

# 2. Draw top line extension from 3191 to 3230
for x in range(3191, 3231):
    opt.putpixel((x, 107), (82, 73, 70, 255))
    opt.putpixel((x, 108), (82, 73, 70, 255))
    opt.putpixel((x, 109), (77, 69, 70, 255))

# 3. Draw new vertical line at X = 3230
for y in range(107, 1920):
    opt.putpixel((3229, y), (75, 66, 68, 255))
    opt.putpixel((3230, y), (80, 70, 68, 255))
    opt.putpixel((3231, y), (80, 70, 68, 255))

crop = opt.crop((2400, 80, 3260, 650))
crop.save('scripts/sig_previews/test_border_perfect.png')
print("Saved test_border_perfect.png!")
