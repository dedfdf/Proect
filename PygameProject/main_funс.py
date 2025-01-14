import pygame
from pygame.math import Vector2 as vec2
import os
import sys
import math
from PIL import Image
from PygameProject.sprite import object_block_visible_group, not_visible_object_group, \
    visible_object_group
from PygameProject.const import ANGLE_VIEW


# Получает все фреймы
def get_frame(path, name, status, dx=0, dy=0, attack_dx=0, attack_dy=0):
    path = f'{path}{name}/{status}'
    filenames = [f for f in os.listdir(path) if f.endswith('.png')]
    images = []
    rate_x = rate_y = 0
    for name in filenames:
        if path.split('/')[-1] == 'attack':
            rate_x = attack_dx
            rate_y = attack_dy
        im = load_image(name, path)
        rect = im.get_rect()

        pygame.image.save(im, 'image/player.png')
        set_image_player((rect.x + dx + rate_x, rect.y + dy + rate_y))
        im = load_image('player.png').convert_alpha()

        images.append(im)
        rate_x = rate_y = 0
    return images


# Загрузка изображений
def load_image(name, directory='image'):
    full_name = os.path.join(directory, name)
    if not os.path.isfile(full_name):
        print('Нету такого')
        print(full_name)
        sys.exit()
    image = pygame.image.load(full_name).convert_alpha()
    return image


# Поворот игрока и его компонентов
def player_rotate(player):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    rel_x, rel_y = mouse_x - player.rect.centerx, mouse_y - player.rect.centery
    angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
    for sprite in [player, player.shoot]:
        sprite.image = pygame.transform.rotate(sprite.orig_image, int(angle))
        sprite.rect = sprite.image.get_rect(center=sprite.rect.center)
    if angle < 0:
        angle = 360 + angle
    player.angle = angle


# Изменяет центр на изображении игрока
def set_image_player(pos):
    im = Image.new("RGBA", (200, 200), (0, 0, 0, 0))
    im_player = Image.open('image/player.png')

    im.paste(im_player, pos, im_player)
    im.save('image/player.png')


# Проверяет объекты на отрисовку и строит вид игрока
def check_visible(player):
    start_angle = (player.angle + ANGLE_VIEW / 2) % 360
    r = player.view.r
    vec_arr = []

    for i in range(ANGLE_VIEW):
        angle = math.radians(start_angle - i)
        x0, y0 = player.rect.center

        x = math.cos(angle) * r
        y = math.sin(angle) * r
        vec = vec2(x, y)
        s = (vec.x ** 2 + vec.y ** 2) ** 0.5

        for sprite in object_block_visible_group:
            rect = sprite.rect
            if rect.clipline(x0, y0, x0 + x, y0 - y):
                rect = rect.clipline(x0, y0, x0 + x, y0 - y)

                vec_1 = vec2(rect[0][0] - x0, y0 - rect[0][1])
                vec_2 = vec2(rect[1][0] - x0, y0 - rect[1][1])
                s1 = (vec_1.x ** 2 + vec_1.y ** 2) ** 0.5
                s2 = (vec_2.x ** 2 + vec_2.y ** 2) ** 0.5

                if min(s1, s2) < s:
                    vec = vec_1 if s1 <= s2 else vec_2
                    s = min(s1, s2)

        vec_arr.append(vec)
    player.view.set_view(player, vec_arr)

    for object in not_visible_object_group:
        vec = vec2(object.rect.centerx - player.rect.centerx,
                   object.rect.centery - player.rect.centery)
        s = (vec.x ** 2 + vec.y ** 2) ** 0.5
        angle = math.degrees(math.acos(vec.x / s))
        if object.rect.centery > player.rect.centery:
            angle = 360 - angle

        if s > player.view.r:
            continue
        if start_angle >= (start_angle - ANGLE_VIEW) % 360:
            if not start_angle >= angle >= (start_angle - ANGLE_VIEW) % 360:
                continue
        else:
            if not (start_angle >= angle or angle >= (start_angle - ANGLE_VIEW) % 360):
                continue

        flag = 0
        for sprite in object_block_visible_group:
            rect = sprite.rect
            p_x, p_y = player.rect.center
            o_x, o_y = object.rect.center
            if rect.clipline(p_x, p_y, o_x, o_y):
                flag = 1
                break
        if flag:
            continue
        visible_object_group.add(object)
