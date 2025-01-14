import pygame
from PygameProject.sprite import cursor_group
from PygameProject.main_funс import load_image


class Cursor(pygame.sprite.Sprite):
    def __init__(self, pos, im):
        super().__init__(cursor_group)

        self.image = im
        self.rect = self.image.get_rect(center=pos)

    def move(self, pos):
        self.rect.center = pos
