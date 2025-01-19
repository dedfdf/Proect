from weapon.All_Weapon import AllWeapon
import pygame
from consts import VIEW, START_PATRON_AUTOMAT, CLIP_PATRON_AUTOMAT


# Игрок с автоматом
class Automat(AllWeapon):
    name = 'automat'
    arr_status = ['idle', 'attack', 'move', 'reload', 'shoot']
    radius = 20
    r_view, r_shoot = VIEW, 550

    idle_angle_shoot = 10
    walk_angle_shoot = 20
    run_angle_shoot = 40

    dx, dy = 65, 55
    dx_attack, dy_attack = -10, -28

    patron = START_PATRON_AUTOMAT - CLIP_PATRON_AUTOMAT
    clip_patron = CLIP_PATRON_AUTOMAT
    max_clip_patron = clip_patron

    speed_frame = {'attack': 50,
                   'reload': 60,
                   'shoot': 60}

    def __init__(self):
        super().__init__(self.arr_status)

    def next_frame(self, player):
        clock = pygame.time.get_ticks()
        super().next_frame(player, clock, 1)

    def set_status(self, player, status):
        super().set_status(player, status)
