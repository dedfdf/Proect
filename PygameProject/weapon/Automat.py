from weapon.All_Weapon import AllWeapon
import pygame
from consts import VIEW, START_PATRON_AUTOMAT, CLIP_PATRON_AUTOMAT


# Игрок с автоматом
class Automat(AllWeapon):
    name = 'automat'
    arr_status = ['idle', 'attack', 'move', 'reload', 'shoot']
    radius = 20
    r_view, r_shoot = VIEW, 450
    min_angle_shoot = 5
    max_angle_shoot = 25

    dx, dy = 65, 55
    dx_attack, dy_attack = -10, -28

    patron = START_PATRON_AUTOMAT - CLIP_PATRON_AUTOMAT
    clip_patron = CLIP_PATRON_AUTOMAT

    def __init__(self):
        super().__init__(self.arr_status)

    def next_frame(self, player):
        clock = pygame.time.get_ticks()
        super().next_frame(player, clock, 1)

    def set_status(self, player, status):
        super().set_status(player, status)
