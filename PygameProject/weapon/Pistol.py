from weapon.All_Weapon import AllWeapon
import pygame
from consts import VIEW, START_PATRON_PISTOL, CLIP_PATRON_PISTOL


# Игрок с пистолетом
class Pistol(AllWeapon):
    name = 'pistol'
    arr_status = ['idle', 'attack', 'move', 'reload', 'shoot']
    radius = 20
    r_view, r_shoot = VIEW, 450

    idle_angle_shoot = 10
    walk_angle_shoot = 20
    run_angle_shoot = 30

    dx, dy = 65, 56
    dx_attack, dy_attack = 0, 0

    patron = START_PATRON_PISTOL - CLIP_PATRON_PISTOL
    clip_patron = CLIP_PATRON_PISTOL
    max_clip_patron = clip_patron

    speed_frame = {'attack': 50,
                   'reload': 50,
                   'shoot': 60}

    def __init__(self):
        super().__init__(self.arr_status)

    def next_frame(self, player):
        clock = pygame.time.get_ticks()
        super().next_frame(player, clock, 0)

    def set_status(self, player, status):
        super().set_status(player, status)
