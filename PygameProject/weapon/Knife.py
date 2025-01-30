from weapon.Frames import Frames
import pygame
from consts import VIEW


# Игрок с ножом
class Knife(Frames):
    name = 'knife'
    arr_status = ['idle', 'attack', 'move']
    radius = 20
    r_view, r_shoot = VIEW, 50

    idle_angle_shoot = 30
    walk_angle_shoot = 30
    run_angle_shoot = 30

    speed_set_angle = 10
    speed_aim_angle = 10

    dx, dy = 51, 49
    dx_attack, dy_attack = 0, 0

    patron = 'infinity'
    clip_patron = 'infinity'
    max_clip_patron = clip_patron

    def __init__(self):
        super().__init__(self.arr_status)

    def next_frame(self, player):
        clock = pygame.time.get_ticks()
        super().next_frame(player, clock, 0)

    def set_status(self, player, status):
        super().set_status(player, status)
