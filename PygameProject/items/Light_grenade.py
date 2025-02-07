from image_scale import light_grenade_icon, light_grenade
import pygame
from sprite import not_visible_object_group, all_sprite, items_group, grenade_group, \
    object_block_visible_group, opponents_group
from pygame.math import Vector2 as vec2
from consts import SPEEDUP_GRENADE, DISTANCE, TIME_STOP_GRENADE
import math


class LightGrenadeIcon:
    def __init__(self):
        self.image = light_grenade_icon

    def load(self, player):
        # нету лоудинг
        player.remove_item()

    def use(self, player):
        LightGrenade(player, 1)


class LightGrenade(pygame.sprite.Sprite):
    def __init__(self, player, type=0):
        super().__init__(not_visible_object_group, items_group, all_sprite)
        self.image = light_grenade
        self.pos_center = list(player.rect.center)
        self.rect = self.image.get_rect(center=self.pos_center)

        self.sound_boom = pygame.mixer.Sound('sound/light_grenade_boom.mp3')
        self.sound_conflict = pygame.mixer.Sound('sound/light_grenade_conflict.mp3')

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

        self.sound_conflict.set_volume(player.volume)

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

            self.rect.centery += vec.y

            for group in arr_spriteGroup:
                for sprite in group:
                    if sprite.rect.collidepoint(self.rect.center):
                        self.rect.centery -= vec.y
                        self.vec_x_y[1] *= -1
                        flag_y = 0

            if flag_x:
                self.pos_center[0] += vec.x
            if flag_y:
                self.pos_center[1] += vec.y

            if not flag_x or not flag_y:
                self.sound_conflict.play(0)

        if v <= 0:
            if self.time_stop == 0:
                self.sound_conflict.play(0)
            self.time_stop += player.dt
        if self.time_stop >= TIME_STOP_GRENADE:
            self.boom(player)

    def boom(self, player):
        player.blind(self)
        self.kill()

    def update(self, vector_move):
        self.rect.center = self.pos_center
