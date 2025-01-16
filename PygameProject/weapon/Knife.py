from weapon.All_Weapon import AllWeapon
import pygame
from consts import VIEW

# Игрок с ножом
class Knife(AllWeapon):
    name = 'knife'
    arr_status = ['idle', 'attack', 'move']
    radius = 20
    r_view, r_shoot = VIEW, 50
    min_angle_shoot = 30
    max_angle_shoot = 30

    dx, dy = 61, 59
    dx_attack, dy_attack = 0, 0

    patron = 'infinity'
    clip_patron = 'infinity'

    def __init__(self):
        super().__init__(self.arr_status)

    def next_frame(self, player):
        clock = pygame.time.get_ticks()
        super().next_frame(player, clock, 0)

    def set_status(self, player, status):
        super().set_status(player, status)
