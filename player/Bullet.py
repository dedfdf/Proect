import pygame
from pygame.math import Vector2 as vec2
from sprite import bullet_group, all_sprite, object_block_visible_group, not_visible_object_group
from main_funс import load_image
from consts import BULLET_SPEED, FPS
import math
from random import uniform


# Класс пуль
class Bullet(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__(bullet_group, all_sprite)

        im = load_image('bullet.png')
        self.player = player

        start_angle = (player.angle - player.angle_shoot / 2) % 360
        angle = uniform(start_angle, start_angle + player.angle_shoot)

        self.image = pygame.transform.rotate(im, angle)
        self.rect = self.image.get_rect(center=player.rect.center)

        angle = math.radians(angle)
        speed = BULLET_SPEED * player.dt
        x = speed * math.cos(angle)
        y = -speed * math.sin(angle)

        self.vec_speed = vec2(x, y)

        # Проверяет на столкновение с обектом

    def check(self):
        for sprite in object_block_visible_group:
            if pygame.sprite.collide_mask(self, sprite):
                return 1
        r_shoot = self.player.weapon.weapon.r_shoot
        x_p, y_p = self.player.rect.center
        x_b, y_b = self.rect.center

        dis = ((x_p - x_b) ** 2 + (y_p - y_b) ** 2) ** 0.5
        if dis > r_shoot:
            return 2
        return 0

    def update(self):
        flag = self.check()
        if flag == 1:
            self.kill()
        if flag == 2:
            self.kill()
        else:
            self.rect.center += self.vec_speed
