import pygame
from sprite import cursor_group
from main_funс import load_image


# Класс курсора
class Cursor(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__(cursor_group)

        self.image = load_image('cursor.png')
        self.rect = self.image.get_rect(center=pos)

    # Перемещает курсор
    def move(self, pos):
        self.rect.center = pos
