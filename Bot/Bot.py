import math
import random

import pygame
from sprite import player_group, all_sprite, wall_group, collision_circle_group, items_group, \
    not_visible_object_group, opponents_group
from consts import TILE_WIDTH, TILE_HEIGHT
from main_funс import load_image


class Bot(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, graph, weapon):
        super().__init__(opponents_group, not_visible_object_group, all_sprite)
        self.image = self.orig_image = weapon.image
        self.pos_center = [pos_x * TILE_WIDTH + TILE_WIDTH / 2,
                           pos_y * TILE_HEIGHT + TILE_HEIGHT / 2]
        self.rect = self.image.get_rect(center=self.pos_center)
        self.moves = {-1: 5, 1: -5, 0: 0}
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.memory = []
        self.memory_empty = [(4, 4), (6, 7), (9, 3)]
        self.schetchik = 0
        self.graph = graph
        self.angel = 270

    def find_way(self, coord):
        v = self.graph.bfs((self.pos_x, self.pos_y), coord)
        return v

    def update(self):
        coord_bot = self.pos_x, self.pos_y
        if self.memory:
            coord = self.memory[0]
            coords = coord_bot[0] - coord[0], coord_bot[1] - coord[1]
            self.povorot(coords)
            self.rect.center = (self.rect.center[0] + self.moves[coords[0]], self.rect.center[1] + self.moves[coords[1]])

            if (-3 < self.rect.center[0] - self.graph.map[coord[1]][coord[0]][3].rect.center[0] < 3 and
                    -3 < self.rect.center[1] - self.graph.map[coord[1]][coord[0]][3].rect.center[1] < 3):
                self.memory.pop(0)
                self.pos_x, self.pos_y = coord
                print(self.pos_x, self.pos_y)
        else:
            s = random.choice(self.graph.map_empty)
            self.memory = self.find_way((5, 7))

            if self.memory:
                self.memory = self.memory[1:]

    def where_player(self, coord_player):
        return math.sqrt((self.rect.x - coord_player[0]))

    def trigger(self):
        pass

    def povorot(self, coord):
        angels = {(0, 1): 270, (1, 1): 315, (1, 0): 0, (-1, 0): 180, (0, 0): 0, (1, -1): 45, (0, -1): 90, (-1, 1): 225,
                  (-1, -1): 135}
        if abs(angels[coord] - self.angel) >= 180 and self.angel != angels[coord]:
            self.angel -= 15
        if abs(angels[coord] - self.angel) < 180 and self.angel != angels[coord]:
            self.angel += 15
        self.image = pygame.transform.rotate(self.orig_image, self.angel)
