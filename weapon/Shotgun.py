from weapon.Frames import Frames
import pygame
from consts import VIEW, START_PATRON_SHOTGUN, CLIP_PATRON_SHOTGUN


# Игрок с дробовиком
class Shotgun(Frames):
    name = 'shotgun'
    arr_status = ['idle', 'attack', 'move', 'reload', 'shoot']
    radius = 20
    r_view, r_shoot = VIEW, 320

    idle_angle_shoot = 30
    walk_angle_shoot = 40
    run_angle_shoot = 60

    speed_set_angle = 60
    speed_aim_angle = 1

    dx, dy = 55, 45
    dx_attack, dy_attack = -8, -36

    patron = START_PATRON_SHOTGUN - CLIP_PATRON_SHOTGUN
    clip_patron = CLIP_PATRON_SHOTGUN
    max_clip_patron = clip_patron

    shoot_sound = pygame.mixer.Sound(f'sound/{name}_shoot.mp3')
    reload_sound = pygame.mixer.Sound(f'sound/{name}_reload.mp3')

    def __init__(self):
        super().__init__(self.arr_status)

    def next_frame(self, player):
        clock = pygame.time.get_ticks()
        super().next_frame(player, clock, 2)

    def set_status(self, player, status):
        super().set_status(player, status)
