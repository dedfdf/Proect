from weapon.Frames import Frames
import pygame
from consts import VIEW, START_PATRON_AUTOMAT, CLIP_PATRON_AUTOMAT


# Игрок с автоматом
class Automat(Frames):
    name = 'automat'
    arr_status = ['idle', 'attack', 'move', 'reload', 'shoot']
    radius = 20
    r_view, r_shoot = VIEW, 550

    idle_angle_shoot = 2
    walk_angle_shoot = 20
    run_angle_shoot = 60

    speed_set_angle = 60
    speed_aim_angle = 6

    dx, dy = 65, 55
    dx_attack, dy_attack = -7, -29

    patron = START_PATRON_AUTOMAT - CLIP_PATRON_AUTOMAT
    clip_patron = CLIP_PATRON_AUTOMAT
    max_clip_patron = clip_patron

    shoot_sound = pygame.mixer.Sound(f'sound/{name}_shoot.mp3')
    reload_sound = pygame.mixer.Sound(f'sound/{name}_reload.mp3')

    def __init__(self):
        super().__init__(self.arr_status)

    def next_frame(self, player):
        clock = pygame.time.get_ticks()
        super().next_frame(player, clock, 1)

    def set_status(self, player, status):
        super().set_status(player, status)
