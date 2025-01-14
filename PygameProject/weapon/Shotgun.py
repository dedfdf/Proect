from PygameProject.weapon.All_Weapon import AllWeapon
import pygame
from PygameProject.const import VIEW


class Shotgun(AllWeapon):
    name = 'shotgun'
    arr_status = ['idle', 'attack', 'move', 'reload', 'shoot']
    radius = 20
    r_view, r_shoot = VIEW, 300
    min_angle_shoot = 15
    max_angle_shoot = 25

    dx, dy = 65, 55
    dx_attack, dy_attack = -10, -28

    def __init__(self):
        super().__init__(self.arr_status)

    def next_frame(self, player):
        clock = pygame.time.get_ticks()
        super().next_frame(player, clock, 0)

    def set_status(self, player, status):
        super().set_status(player, status)
