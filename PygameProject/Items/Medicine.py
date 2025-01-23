from main_funс import load_image
from player.Load_circle import Load_circle
from consts import MEDICINE_COLOR_LOAD_CIRCLE, MEDICINE_COLOR_BORDER_LOAD_CIRCLE, MAX_HEART
import pygame
from sprite import not_visible_object_group, all_sprite, items_group


class MedicineIcon:
    def __init__(self):
        self.image = load_image(f'icon/medicine_icon.png', 'items')

    def load(self, player):
        if player.health != MAX_HEART:
            player.load_circle = Load_circle(MEDICINE_COLOR_LOAD_CIRCLE,
                                             MEDICINE_COLOR_BORDER_LOAD_CIRCLE, player)
            return 1

    def use(self, player):
        player.health += 1


class Medicine(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__(not_visible_object_group, items_group, all_sprite)
        self.image = load_image(f'icon/medicine.png', 'items')
        self.rect = self.image.get_rect(center=player.rect.center)

    def pick_up(self):
        return MedicineIcon()
