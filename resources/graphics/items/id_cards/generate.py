from PIL import Image
import random


def get_base_image():
    if random.random() > 0.5:
        return Image.open("idcard_male.png")
    else:
        return Image.open("idcard_female.png")


def draw_stripe(img, sx, sy, length, color, fac1=1, fac2=-1):
    putpixel = img.im.putpixel

    for i in range(length):
        putpixel((sx+fac1*i, sy+fac2*i), color)


def draw_security_stripes(image, level=0):
    c1 = (255, 255, 255)
    c2 = (255, 255, 255)
    c3 = (255, 255, 255)

    if level >= 1:
        c1 = (255, 0, 0)

    if level >= 2:
        c2 = (255, 0, 0)

    if level >= 3:
        c3 = (255, 0, 0)

    draw_stripe(image, 2,  5,  2, c1)
    draw_stripe(image, 2,  6,  3, c1)
    draw_stripe(image, 2,  7,  4, c1)
    draw_stripe(image, 2,  8,  5, (0,0,0))
    draw_stripe(image, 2,  9,  6, c2)
    draw_stripe(image, 2, 10,  7, c2)
    draw_stripe(image, 2, 11,  8, c2)
    draw_stripe(image, 2, 12,  9, (0,0,0))
    draw_stripe(image, 2, 13, 10, c3)
    draw_stripe(image, 2, 14, 11, c3)
    draw_stripe(image, 2, 15, 12, c3)
    draw_stripe(image, 2, 16, 13, (0,0,0))


def draw_science_stripes(image, level=0):
    c1 = (255, 255, 255)
    c2 = (255, 255, 255)
    c3 = (255, 255, 255)

    if level >= 1:
        c1 = (255, 255, 0)

    if level >= 2:
        c2 = (255, 255, 0)

    if level >= 3:
        c3 = (255, 255, 0)

    draw_stripe(image, 72,  5,  2, c1, fac1=-1, fac2=-1)
    draw_stripe(image, 72,  6,  3, c1, fac1=-1, fac2=-1)
    draw_stripe(image, 72,  7,  4, c1, fac1=-1, fac2=-1)
    draw_stripe(image, 72,  8,  5, (0,0,0), fac1=-1, fac2=-1)
    draw_stripe(image, 72,  9,  6, c2, fac1=-1, fac2=-1)
    draw_stripe(image, 72, 10,  7, c2, fac1=-1, fac2=-1)
    draw_stripe(image, 72, 11,  8, c2, fac1=-1, fac2=-1)
    draw_stripe(image, 72, 12,  9, (0,0,0), fac1=-1, fac2=-1)
    draw_stripe(image, 72, 13, 10, c3, fac1=-1, fac2=-1)
    draw_stripe(image, 72, 14, 11, c3, fac1=-1, fac2=-1)
    draw_stripe(image, 72, 15, 12, c3, fac1=-1, fac2=-1)
    draw_stripe(image, 72, 16, 13, (0,0,0), fac1=-1, fac2=-1)


def draw_technican_stripes(image, level=0):
    c1 = (255, 255, 255)
    c2 = (255, 255, 255)
    c3 = (255, 255, 255)

    if level >= 3:
        c1 = (0, 255, 0)

    if level >= 2:
        c2 = (0, 255, 0)

    if level >= 1:
        c3 = (0, 255, 0)

    draw_stripe(image, 2, 33, 13, (0,0,0), fac2=1)
    draw_stripe(image, 2, 34, 12, c1, fac2=1)
    draw_stripe(image, 2, 35, 11, c1, fac2=1)
    draw_stripe(image, 2, 36, 10, c1, fac2=1)
    draw_stripe(image, 2, 37,  9, (0,0,0), fac2=1)
    draw_stripe(image, 2, 38,  8, c2, fac2=1)
    draw_stripe(image, 2, 39,  7, c2, fac2=1)
    draw_stripe(image, 2, 40,  6, c2, fac2=1)
    draw_stripe(image, 2, 41,  5, (0,0,0), fac2=1)
    draw_stripe(image, 2, 42,  4, c3, fac2=1)
    draw_stripe(image, 2, 43,  3, c3, fac2=1)
    draw_stripe(image, 2, 44,  2, c3, fac2=1)


def draw_administartion_stripes(image, level=0):
    c1 = (255, 255, 255)
    c2 = (255, 255, 255)
    c3 = (255, 255, 255)

    if level >= 3:
        c1 = (0, 0, 255)

    if level >= 2:
        c2 = (0, 0, 255)

    if level >= 1:
        c3 = (0, 0, 255)

    draw_stripe(image, 72, 33, 13, (0,0,0), fac1=-1, fac2=1)
    draw_stripe(image, 72, 34, 12, c1, fac1=-1, fac2=1)
    draw_stripe(image, 72, 35, 11, c1, fac1=-1, fac2=1)
    draw_stripe(image, 72, 36, 10, c1, fac1=-1, fac2=1)
    draw_stripe(image, 72, 37,  9, (0,0,0), fac1=-1, fac2=1)
    draw_stripe(image, 72, 38,  8, c2, fac1=-1, fac2=1)
    draw_stripe(image, 72, 39,  7, c2, fac1=-1, fac2=1)
    draw_stripe(image, 72, 40,  6, c2, fac1=-1, fac2=1)
    draw_stripe(image, 72, 41,  5, (0,0,0), fac1=-1, fac2=1)
    draw_stripe(image, 72, 42,  4, c3, fac1=-1, fac2=1)
    draw_stripe(image, 72, 43,  3, c3, fac1=-1, fac2=1)
    draw_stripe(image, 72, 44,  2, c3, fac1=-1, fac2=1)


for a in [0, 1, 2, 3]:
    for b in [0, 1, 2, 3]:
        for c in [0, 1, 2, 3]:
            for d in [0, 1, 2, 3]:
                im = get_base_image()
                stripes = Image.new("RGBA", (75, 50), "white")
                copy = Image.blend(im, stripes, 0)

                s, t, h, sc = a, b, c, d
                draw_security_stripes(copy, s)
                draw_technican_stripes(copy, t)
                draw_administartion_stripes(copy, h)
                draw_science_stripes(copy, sc)

                copy.save("id_card_%i_%i_%i_%i.png" % (s, t, h, sc))
