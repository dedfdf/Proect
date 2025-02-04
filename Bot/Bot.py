import math
import random
from pygame.math import Vector2 as vec2
import pygame
from sprite import player_group, all_sprite, wall_group, collision_circle_group, items_group, \
    not_visible_object_group, opponents_group
from consts import TILE_WIDTH, TILE_HEIGHT
from main_funс import load_image


class Bot(pygame.sprite.Sprite):  # Создаёт бота
    def __init__(self, pos_x, pos_y, graph, weapon):
        super().__init__(opponents_group, not_visible_object_group, all_sprite)
        self.image = self.orig_image = weapon.image
        self.pos_center = [pos_x * TILE_WIDTH + TILE_WIDTH / 2,
                           pos_y * TILE_HEIGHT + TILE_HEIGHT / 2]
        self.rect = self.image.get_rect(center=self.pos_center)
        self.moves = {-1: 2, 1: -2, 0: 0}
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.memory = []
        self.memory_empty = [(4, 4), (6, 7), (9, 3)]
        self.schetchik = 0
        self.graph = graph
        self.angel = 360
        self.coord_player = [0, 0]

    def find_way(self, coord):  # Находит путь
        v = self.graph.bfs((self.pos_x, self.pos_y), coord)
        return v

    def update(self):  # Обновляет действие бота
        coord_bot = self.pos_x, self.pos_y
        if not self.trigger():
            if self.memory:
                self.flag = True
                coord = self.memory[0]
                coords = coord_bot[0] - coord[0], coord_bot[1] - coord[1]
                self.povorot(coords)
                self.rect.center = (self.rect.center[0] + self.moves[coords[0]], self.rect.center[1] + self.moves[coords[1]])
                self.pos_center = (self.pos_center[0] + self.moves[coords[0]], self.pos_center[1] + self.moves[coords[1]])
                if (-2 < self.rect.center[0] - self.graph.map[coord[1]][coord[0]][3].rect.center[0] < 2 and
                        -2 < self.rect.center[1] - self.graph.map[coord[1]][coord[0]][3].rect.center[1] < 2):
                    self.memory.pop(0)
                    self.pos_x, self.pos_y = coord
            else:
                s = random.choice(self.graph.map_empty)
                self.memory = self.find_way(s)
                if self.memory:
                    self.memory = self.memory[1:]

    def where_player(self, coord_player):  # Планируется для нахождения расстояния от бота до игрока
        return math.sqrt((self.rect.x - coord_player[0]))

    def trigger(self):  # Планируется для обнаружения игрока
        angle = (self.angel + 45) % 360
        angle1 = (self.angel - 45 + 360) % 360
        radius = 100
        center = (self.rect.center[0], self.rect.center[1])
        x = center[0] + radius * math.cos(math.radians(angle))
        x1 = center[0] + radius * math.cos(math.radians(angle1))

    def povorot(self, coord):  # Поворачивает бота
        angels = {(0, 1): 90, (1, 1): 135, (1, 0): 180, (-1, 0): 0, (0, 0): 0, (1, -1): 225, (0, -1): 270, (-1, 1): 45,
                  (-1, -1): 315}
        self.flag = False
        if (angels[coord] - self.angel + 360) % 360 > 180:
            self.angel -= 15
        if (angels[coord] - self.angel + 360) % 360 < 180:
            self.angel += 15
        self.image = pygame.transform.rotate(self.orig_image, self.angel - 15)



