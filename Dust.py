from random import uniform, randint
import pygame
from pygame.math import Vector2 as vec2
from sprite import all_sprite, dust_group
from consts import TIME_ONE_DUST, PERCENT_SCALE


# класс пыли, которая присутсвует на всех основных экранах
class Dust(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__(dust_group, all_sprite)
        self.r = r = uniform(1, 5.5) * PERCENT_SCALE

        self.pos_center = [uniform(0 + r, width - r), uniform(0 + r, height - r)]
        self.center = self.pos_center[:]
        self.time = 0

        self.dx = randint(-2, 2)
        self.dy = randint(-2, 2)
        diag_speed = (self.dx ** 2 + self.dy ** 2) ** 0.5
        if self.dx and self.dy:
            self.dx *= diag_speed
            self.dy *= diag_speed

        self.vec = vec2(0)

    def render(self, dt):
        time_d = TIME_ONE_DUST
        speed = 3 * TIME_ONE_DUST * dt
        self.vec.x += self.dx * speed
        self.vec.y += self.dy * speed

        if self.time != 0:
            percent = self.time / (time_d / 100)
        else:
            percent = 0
        percent = 100 - percent if self.time > time_d / 2 else percent

        surf = pygame.Surface((self.r * 2, self.r * 2), pygame.SRCALPHA)
        pygame.draw.circle(surf, (255, 255, 255, int(200 / 100 * percent)),
                           (self.r, self.r), self.r)
        self.time += dt

        self.center = self.pos_center + self.vec

        if self.time >= time_d:
            self.kill()
        return surf

    def update(self, vector_move):
        pass
