from PIL import Image, ImageDraw
import math
from consts import R_LOAD_CIRCLE, PERCENT_SCALE


# Ресует коллизию для игрока
def draw_circle(r, name):
    r *= PERCENT_SCALE
    w = round(r * 2 + 1)
    h = round(r * 2 + 1)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    x = w / 2
    y = h / 2
    draw = ImageDraw.Draw(im, 'RGBA')
    draw.ellipse((x - r, y - r, x + r, y + r), outline=(255, 0, 0, 255))
    draw.point((x, y), fill=(255, 0, 0, 255))

    im.save(f'collision_image/circle_{name}.png')
    return name


# Рисует тьму на карте
def draw_dark(w, h, r):
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im, 'RGBA')

    x0 = w // 2
    y0 = h // 2

    draw.rectangle((0, 0, w, h), fill=(0, 0, 0, 128))
    draw.rectangle((x0 - r, y0 - r, x0 + r, y0 + r), fill=(0, 0, 0, 0))

    im.save('image/dark.png')


# Рисует вид
def draw_view(arr, r):
    w = h = r * 2 + 1

    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im, 'RGBA')

    x0 = w // 2
    y0 = h // 2

    draw.rectangle((0, 0, w, h), fill=(0, 0, 0, 128))

    for en, vec in enumerate(arr):
        draw.line((x0, y0, x0 + vec.x, y0 - vec.y), fill=(0, 0, 0, 0))

    im.save('image/view.png')

# рисует круг загрузки под игроком


def draw_load_circle(color, color_border, e_angle):
    w = h = round(R_LOAD_CIRCLE * PERCENT_SCALE)

    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im, 'RGBA')

    draw.pieslice((0, 0, w, h), 270, e_angle, fill=color, outline=color_border, width=3)

    im.save('image/load_circle.png')
