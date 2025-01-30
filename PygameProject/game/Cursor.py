import pygame
from sprite import cursor_group
from main_func import load_image
from consts import PERCENT_SCALE


# Класс курсора
class Cursor(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__(cursor_group)

        self.image = load_image('cursor.png')
        self.image = pygame.transform.scale(self.image,
                                            (self.image.width * PERCENT_SCALE,
                                             self.image.height * PERCENT_SCALE))
        self.rect = self.image.get_rect(center=pos)

    # Перемещает курсор
    def move(self, pos):
        self.rect.center = pos
