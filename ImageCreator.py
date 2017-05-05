from PIL import Image,ImageDraw,ImageFont
import random

def random_Char():
    return chr(random.randint(65,90))

def random_Color1():
    return (random.randint(64,255),random.randint(64,255),random.randint(64,255))

def random_Color2():
    return (random.randint(32,127),random.randint(32,127),random.randint(32,127))

def draw_verify():

    width = 60 * 4
    height = 60
    verify_image = Image.new("RGB",(width,height),(255,255,255))
    font = ImageFont.truetype("C:/Windows/Fonts/Corbel.ttf",50)
    paint = ImageDraw.Draw(verify_image)
    right_font = ""

    for x in range(width):
        for y in range(height):
            paint.point((x,y),fill=random_Color1())

    for x in range(4):
        char = random_Char()
        right_font += char
        paint.text((60 * x + 10, 10),char,fill=random_Color2(),font=font)

    #verify_image = verify_image.filter(ImageFilter.BLUR)

    return right_font,verify_image

def draw_identified_pic(char):
    width = 60 * 4
    height = 60
    verify_image = Image.new("RGB", (width, height), (255, 255, 255))
    font = ImageFont.truetype("C:/Windows/Fonts/Corbel.ttf", 50)
    paint = ImageDraw.Draw(verify_image)

    for x in range(width):
        for y in range(height):
            paint.point((x,y),fill=random_Color1())

    for x in range(4):
        paint.text((60 * x + 10, 10), char, fill=random_Color2(), font=font)

    return verify_image