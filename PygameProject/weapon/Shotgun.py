from weapon.All_Weapon import AllWeapon
import pygame
from consts import VIEW, START_PATRON_SHOTGUN, CLIP_PATRON_SHOTGUN


# Игрок с дробовиком
class Shotgun(AllWeapon):
    name = 'shotgun'
    arr_status = ['idle', 'attack', 'move', 'reload', 'shoot']
    radius = 20
    r_view, r_shoot = VIEW, 250

    idle_angle_shoot = 25
    walk_angle_shoot = 35
    run_angle_shoot = 60

    dx, dy = 65, 55
    dx_attack, dy_attack = -10, -28

    patron = START_PATRON_SHOTGUN - CLIP_PATRON_SHOTGUN
    clip_patron = CLIP_PATRON_SHOTGUN
    max_clip_patron = clip_patron

    speed_frame = {'attack': 50,
                   'reload': 60,
                   'shoot': 100}

    def __init__(self):
        super().__init__(self.arr_status)

    def next_frame(self, player):
        clock = pygame.time.get_ticks()
        super().next_frame(player, clock, 2)

    def set_status(self, player, status):
        super().set_status(player, status)
