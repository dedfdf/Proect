from main_funс import load_image
from player.Load_circle import Load_circle
from consts import ARMOR_COLOR_LOAD_CIRCLE, ARMOR_COLOR_BORDER_LOAD_CIRCLE, MAX_ARMOR
import pygame
from sprite import not_visible_object_group, all_sprite, items_group


class ArmorIcon:
    def __init__(self):
        self.image = load_image(f'icon/armor_icon.png', 'items')

    def load(self, player):
        if player.armor != MAX_ARMOR:
            player.load_circle = Load_circle(ARMOR_COLOR_LOAD_CIRCLE,
                                             ARMOR_COLOR_BORDER_LOAD_CIRCLE, player)
            return 1

    def use(self, player):
        player.armor += 1


class Armor(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__(not_visible_object_group, items_group, all_sprite)
        self.image = load_image(f'icon/armor.png', 'items')
        self.rect = self.image.get_rect(center=player.rect.center)

    def pick_up(self):
        return ArmorIcon()
