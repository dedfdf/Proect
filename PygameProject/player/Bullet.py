import pygame
from PygameProject.sprite import bullet_group, all_sprite, shoot_group


class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(bullet_group, all_sprite)
        pass

    def check(self):
        pass

    def kill(self):
        pass
