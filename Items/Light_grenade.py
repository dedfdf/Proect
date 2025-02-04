from main_funс import load_image
import pygame
from sprite import not_visible_object_group, all_sprite, items_group, grenade_group, \
    object_block_visible_group, opponents_group
from pygame.math import Vector2 as vec2
from consts import SPEEDUP_GRENADE, DISTANCE, TIME_STOP_GRENADE
import math


class LightGrenadeIcon:
    def __init__(self):
        self.image = load_image(f'icon/light_grenade_icon.png', 'items')

    def load(self, player):
        # нету лоудинг
        player.remove_item()

    def use(self, player):
        LightGrenade(player, 1)


class LightGrenade(pygame.sprite.Sprite):
    def __init__(self, player, type=0):
        super().__init__(not_visible_object_group, items_group, all_sprite)
        self.image = load_image(f'icon/light_grenade.png', 'items')
        self.rect = self.image.get_rect(center=player.rect.center)

        if type:
            self.a = -SPEEDUP_GRENADE
            self.v = (-1 * DISTANCE * self.a * 2) ** 0.5
            self.angle = player.angle

            self.time = 0
            self.time_stop = 0
            self.vec_x_y = [1, 1]

            grenade_group.add(self)

    def pick_up(self):
        return LightGrenadeIcon()

    def fly(self, player):
        v = (self.v + self.a * self.time) * player.dt
        self.time += player.dt

        if not self.time_stop:
            angle = math.radians(self.angle)
            x = math.cos(angle) * v * self.vec_x_y[0]
            y = -math.sin(angle) * v * self.vec_x_y[1]

            vec = vec2(x, y)
            self.rect.centerx += vec.x

            flag_x = flag_y = 1

            arr_spriteGroup = [object_block_visible_group, opponents_group]

            for group in arr_spriteGroup:
                for sprite in group:
                    if sprite.rect.collidepoint(self.rect.center):
                        self.rect.centerx -= vec.x
                        self.vec_x_y[0] *= -1
                        flag_x = 0

            self.rect.centerx -= vec.x
            self.rect.centery += vec.y

            for group in arr_spriteGroup:
                for sprite in group:
                    if sprite.rect.collidepoint(self.rect.center):
                        self.rect.centery -= vec.y
                        self.vec_x_y[1] *= -1
                        flag_y = 0

            if flag_x:
                self.rect.centerx += vec.x
            if not flag_y:
                self.rect.centery -= vec.y

        if v <= 0:
            self.time_stop += player.dt
        if self.time_stop >= TIME_STOP_GRENADE:
            self.boom(player)

    def boom(self, player):
        player.blind(self)
        self.kill()
