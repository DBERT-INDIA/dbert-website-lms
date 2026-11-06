from PIL import Image

# Open original targets12.png
img = Image.open('apps/portal/static/certificates/targets12.png').convert('RGBA')

# 1. Let's inspect the background around the text (Y = 180..550, X = 2000..3220)
# The background in this area is dark navy blue with very subtle geometric shading.
# Let's see the color of the vertical line at X = 3191 from Y = 180 to 550.
# The line is only 2-3 pixels wide!
# Where the line cuts through:
# - It cuts through the 'F' of 'OF' at Y around 230..300
# - It cuts through the 'P' of 'INTERNSHIP' at Y around 400..500

# What if we mask the vertical line segment from Y = 180 to 550?
# If we mask the vertical line from Y = 180 to 550 (or where the text passes), does that look intentional?
# In many certificate templates, the border line breaks for the title (a broken border frame)!
# OR what if we shift the text 50px left, and restore the vertical line?

# Let's test Method 1: Shift the text 60px to the left!
# To shift the text cleanly:
# We can isolate the text pixels (white and orange) and paste them 60px to the left,
# while restoring the line and background!

test1 = img.copy()

# The navy background color in that area:
# Let's sample pixels at X = 3205..3215 (outside the text)
bg_col = img.getpixel((3150, 150))
print("Sample background color:", bg_col)

# Let's create a test where we shift the text region
# Text is within X = 2030..3204, Y = 200..530
text_box = (2030, 200, 3205, 530)
text_crop = img.crop(text_box)

# If we shift text_crop 60px left:
# New position: (1970, 200)
# But we need to clean up the old position (from 3145 to 3205):
# That's a 60px strip!
# In that 60px strip, the vertical line at 3191 should continue all the way from Y = 200 to 530!

# Let's inspect the line color at Y=150:
line_pixels = [img.getpixel((x, 150)) for x in range(3189, 3194)]
print("Line pixels at Y=150:", line_pixels)
