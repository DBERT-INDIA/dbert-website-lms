from PIL import Image, ImageDraw

base_img = Image.open('apps/portal/static/certificates/targets12.png').convert('RGBA')

# Option 1: Move the vertical line to X = 3225
opt1 = base_img.copy()
draw1 = ImageDraw.Draw(opt1)

# Erase old vertical line at X = 3190..3192 from Y = 107 to Y = 2000
# By copying the adjacent column at X = 3180..3182
for y in range(107, 2000):
    for offset in range(-1, 3):
        # sample from X = 3180
        src_p = base_img.getpixel((3180, y))
        # Don't erase white text of F or orange text of P!
        cur_p = base_img.getpixel((3191 + offset, y))
        # if not white text and not orange text:
        if not (cur_p[0] > 180 and cur_p[1] > 180) and not (cur_p[0] > 180 and cur_p[2] < 100):
            opt1.putpixel((3191 + offset, y), src_p)

# Draw top line extension from 3191 to 3225
for x in range(3191, 3226):
    opt1.putpixel((x, 107), (82, 73, 70, 255))
    opt1.putpixel((x, 108), (82, 73, 70, 255))
    opt1.putpixel((x, 109), (77, 69, 70, 255))

# Draw new vertical line at X = 3225
for y in range(107, 1920):
    opt1.putpixel((3224, y), (75, 66, 68, 255))
    opt1.putpixel((3225, y), (80, 70, 68, 255))
    opt1.putpixel((3226, y), (80, 70, 68, 255))

crop1 = opt1.crop((2400, 80, 3260, 650))
crop1.save('scripts/sig_previews/test_border_opt1_moved_line.png')

# Option 2: Mask the vertical line only where the title is (Y = 180 to Y = 560) - "Border Break"
opt2 = base_img.copy()
for y in range(180, 560):
    for offset in range(-1, 3):
        src_p = base_img.getpixel((3180, y))
        cur_p = base_img.getpixel((3191 + offset, y))
        if not (cur_p[0] > 180 and cur_p[1] > 180) and not (cur_p[0] > 180 and cur_p[2] < 100):
            opt2.putpixel((3191 + offset, y), src_p)

crop2 = opt2.crop((2400, 80, 3260, 650))
crop2.save('scripts/sig_previews/test_border_opt2_break_line.png')

# Option 3: Shift text 50px to the left
# We can isolate the text (pixels that are distinctly white or orange)
opt3 = base_img.copy()
# First erase the line at X = 3191 between Y = 180 and 560
for y in range(180, 560):
    for offset in range(-1, 3):
        src_p = base_img.getpixel((3180, y))
        opt3.putpixel((3191 + offset, y), src_p)

# Take text region from base_img, shift left by 45px
# Text mask: where pixel is text
text_area = base_img.crop((2000, 180, 3215, 550))
text_w, text_h = text_area.size
shift = 45

# Create a clean patch
for dy in range(text_h):
    for dx in range(text_w):
        p = text_area.getpixel((dx, dy))
        # If it's text (white or orange)
        is_white = p[0] > 160 and p[1] > 160 and p[2] > 160
        is_orange = p[0] > 180 and p[1] > 110 and p[2] < 100
        if is_white or is_orange:
            # erase from old position
            opt3.putpixel((2000 + dx, 180 + dy), base_img.getpixel((1980, 180 + dy)))
            # put in new shifted position
            opt3.putpixel((2000 + dx - shift, 180 + dy), p)

# Redraw vertical line at X = 3191 cleanly from Y = 107 to 600
for y in range(107, 600):
    opt3.putpixel((3190, y), (75, 66, 68, 255))
    opt3.putpixel((3191, y), (80, 70, 68, 255))
    opt3.putpixel((3192, y), (80, 70, 68, 255))

crop3 = opt3.crop((2400, 80, 3260, 650))
crop3.save('scripts/sig_previews/test_border_opt3_shift_text.png')

print("Generated all 3 test options!")
