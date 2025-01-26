from weapon.Frames import Frames
import pygame
from consts import VIEW, START_PATRON_PISTOL, CLIP_PATRON_PISTOL


# Игрок с пистолетом
class Pistol(Frames):
    name = 'pistol'
    arr_status = ['idle', 'attack', 'move', 'reload', 'shoot']
    radius = 20
    r_view, r_shoot = VIEW, 450

    idle_angle_shoot = 5
    walk_angle_shoot = 20
    run_angle_shoot = 40

    speed_set_angle = 30
    speed_aim_angle = 2

    dx, dy = 65, 56
    dx_attack, dy_attack = -3, -2

    patron = START_PATRON_PISTOL - CLIP_PATRON_PISTOL
    clip_patron = CLIP_PATRON_PISTOL
    max_clip_patron = clip_patron

    shoot_sound = pygame.mixer.Sound(f'sound/{name}_shoot.mp3')
    reload_sound = pygame.mixer.Sound(f'sound/{name}_reload.mp3')

    def __init__(self):
        super().__init__(self.arr_status)

    def next_frame(self, player):
        clock = pygame.time.get_ticks()
        super().next_frame(player, clock, 3)

    def set_status(self, player, status):
        super().set_status(player, status)
