from PygameProject.weapon.All_Weapon import AllWeapon
import pygame
from PygameProject.const import VIEW


class Pistol(AllWeapon):
    name = 'pistol'
    arr_status = ['idle', 'attack', 'move', 'reload', 'shoot']
    radius = 20
    r_view, r_shoot = VIEW, 350
    min_angle_shoot = 5
    max_angle_shoot = 20
    dx, dy = 65, 56
    dx_attack, dy_attack = 0, 0

    def __init__(self):
        super().__init__(self.arr_status)

    def next_frame(self, player):
        clock = pygame.time.get_ticks()
        super().next_frame(player, clock, 0)

    def set_status(self, player, status):
        super().set_status(player, status)
