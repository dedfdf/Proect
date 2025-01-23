from PIL import Image, ImageDraw
import math
from consts import R_LOAD_CIRCLE


# Рисует поле для разброса
def draw_shoot(angel, dis):
    angel = math.radians(angel)
    dx = math.tan(angel) * dis

    size = dis + dis / 3
    w = h = (int(size) + 1) * 2

    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im, 'RGBA')

    x = w / 2
    y = h / 2

    draw.ellipse([x - dx, y - dis - dis / 3, x + dx, y - dis + dis / 3],
                 fill=(255, 0, 0, 50), outline=None)
    draw.rectangle((x - dx, y - dis, x + dx, y - dis + dis / 3), fill=(0, 0, 0, 0))
    draw.polygon([x, y, x - dx, y - dis, x + dx, y - dis], fill=(255, 0, 0, 50),
                 outline=None)

    im = im.rotate(-90)
    im.save('image/shoot.png')


# Ресует коллизию для игрока
def draw_circle(r, name):
    w = r * 2 + 1
    h = r * 2 + 1
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    x = w / 2
    y = h / 2
    draw = ImageDraw.Draw(im, 'RGBA')
    draw.ellipse((x - r, y - r, x + r, y + r), outline=(255, 0, 0, 255))

    im.save(f'collision_image/circle_{name}.png')
    return name


# Рисует тьму на карте
def draw_dark(w, h):
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im, 'RGBA')

    draw.rectangle((0, 0, w, h), fill=(0, 0, 0, 128))

    im.save('image/dark.png')


# Рисует вид
def draw_view(arr, r):
    w = h = r * 2 + 1

    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im, 'RGBA')

    x0 = w // 2
    y0 = h // 2

    for en, vec in enumerate(arr):
        draw.line((x0, y0, x0 + vec.x, y0 - vec.y), fill=(255, 255, 255, 80))

    im.save('image/circle_view.png')


def draw_load_circle(color, color_border, e_angle):
    w = h = R_LOAD_CIRCLE

    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im, 'RGBA')

    draw.pieslice((0, 0, w, h), 270, e_angle, fill=color, outline=color_border, width=3)

    im.save('image/load_circle.png')
