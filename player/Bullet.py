import pygame
from pygame.math import Vector2 as vec2
from sprite import bullet_group, all_sprite, object_block_visible_group, not_visible_object_group, \
    opponents_group, player_group
from consts import PERCENT_SCALE
from image_scale import image_bullet
import math
from random import uniform


# Класс пуль
class Bullet(pygame.sprite.Sprite):
    def __init__(self, host):
        super().__init__(bullet_group, all_sprite)

        im = image_bullet
        self.host = host

        self.start_pos = host.rect.center

        start_angle = (host.angle - host.angle_shoot / 2) % 360
        angle = uniform(start_angle, start_angle + host.angle_shoot)

        self.image = pygame.transform.rotate(im, angle)
        self.pos_center = list(host.rect.center)
        self.rect = self.image.get_rect(center=self.pos_center)

        angle = math.radians(angle)
        speed = 80 * PERCENT_SCALE
        # возможно такая скорость приведет к неполадкам при слабом пк, но
        # если брать каждый кадр отдельно, существует риск прохода були сквозь объект
        x = speed * math.cos(angle)
        y = -speed * math.sin(angle)

        self.vec_speed = vec2(x, y)

    # проверяет столкновение пули с объектом
    def check(self):
        for sprite in object_block_visible_group:
            if pygame.sprite.collide_mask(self, sprite):
                return 1

        if self.host not in opponents_group:
            for sprite in opponents_group:
                if pygame.sprite.collide_mask(self, sprite):
                    pass
                    return 2

        else:
            for sprite in player_group:
                if pygame.sprite.collide_mask(self, sprite):
                    sprite.remove_health()
                    return 2

        r_shoot = self.host.weapon.weapon.r_shoot
        x_p, y_p = self.host.rect.center
        x_b, y_b = self.rect.center

        dis = ((x_p - x_b) ** 2 + (y_p - y_b) ** 2) ** 0.5
        if dis > r_shoot:
            return 2
        return 0

    def new_pos(self):
        flag = self.check()
        if flag == 1:
            self.kill()
        if flag == 2:
            self.kill()
        else:
            self.pos_center += self.vec_speed

    def update(self, vector_move):
        self.rect.center = self.pos_center
