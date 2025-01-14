from pygame.math import Vector2 as vec2
from PygameProject.draw import draw_circle
from PygameProject.player.Circle_collision import Collision


class Weapons:
    def __init__(self, arsenal):
        self.arr_weapon = arsenal

        self.weapon = self.arr_weapon[2]

        self.image = self.weapon.image
        self.rect = self.image.get_rect()

    def next_frame(self, player):
        self.weapon.next_frame(player)
        self.image = self.weapon.image
        self.rect = self.image.get_rect()

    def get_collision(self, player):
        self.arr_collision = [Collision(draw_circle(weapon.radius, weapon.name), player)
                              for weapon in self.arr_weapon]
        self.collision = self.arr_collision[2]
