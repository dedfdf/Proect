import pygame
from main_funс import load_image
from player.Load_circle import Load_circle
from consts import PATRON_COLOR_LOAD_CIRCLE, PATRON_COLOR_BORDER_LOAD_CIRCLE
from sprite import not_visible_object_group, all_sprite, items_group


class PatronIcon:
    def __init__(self):
        self.image = load_image(f'icon/bullet_icon.png', 'items')

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
        self.image = load_image(f'icon/bullet.png', 'items')
        self.rect = self.image.get_rect(center=player.rect.center)

    def pick_up(self):
        return PatronIcon()
