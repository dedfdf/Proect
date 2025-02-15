from image_scale import patron_icon, patron
from player.Load_circle import Load_circle
from consts import PATRON_COLOR_BORDER_LOAD_CIRCLE, PATRON_COLOR_LOAD_CIRCLE
import pygame
from sprite import not_visible_object_group, all_sprite, items_group


class PatronIcon:
    def __init__(self):
        self.image = patron_icon

    def load(self, player):
        player.load_circle = Load_circle(PATRON_COLOR_LOAD_CIRCLE,
                                         PATRON_COLOR_BORDER_LOAD_CIRCLE, player)
        return 1

    def use(self, player):
        for weapon in player.weapon.arr_weapon:
            if weapon.name not in ['knife', 'flashlight']:
                weapon.patron += weapon.max_clip_patron


class Patron(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__(not_visible_object_group, items_group, all_sprite)
        self.image = patron
        self.pos_center = list(player.rect.center)
        self.rect = self.image.get_rect(center=self.pos_center)

    def pick_up(self):
        return PatronIcon()

    def update(self, vector_move):
        self.rect.center = self.pos_center
