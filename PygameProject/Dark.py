import pygame
from PygameProject.sprite import all_sprite, dark_group
from PygameProject.draw import draw_dark
from PygameProject.main_funс import load_image


# Класс тьмы на карте
class Dark(pygame.sprite.Sprite):
    def __init__(self, w, h, player):
        super().__init__(dark_group, all_sprite)
        draw_dark(w, h)
        self.image = load_image('dark.png')
        self.pos_center = list(player.rect.center)

        self.rect = self.image.get_rect(center=self.pos_center)

        player.get_dark(self)

    # Перемещает тень
    def move(self, vector_move):
        self.rect.center = self.pos_center + vector_move
