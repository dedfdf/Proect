import pygame
from PygameProject.sprite import cursor_group


# Класс курсора
class Cursor(pygame.sprite.Sprite):
    def __init__(self, pos, im):
        super().__init__(cursor_group)

        self.image = im
        self.rect = self.image.get_rect(center=pos)

    # Перемещает курсор
    def move(self, pos):
        self.rect.center = pos
