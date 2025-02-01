from player.Load_circle import Load_circle
from consts import ARMOR_COLOR_LOAD_CIRCLE, ARMOR_COLOR_BORDER_LOAD_CIRCLE, MAX_ARMOR
import pygame
from image_scale import armor_icon, armor
from sprite import not_visible_object_group, all_sprite, items_group


class ArmorIcon:
    def __init__(self):
        self.image = armor_icon

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
        self.image = armor
        self.pos_center = list(player.rect.center)
        self.rect = self.image.get_rect(center=self.pos_center)

    def pick_up(self):
        return ArmorIcon()

    def update(self, vector_move):
        self.rect.center = self.pos_center
