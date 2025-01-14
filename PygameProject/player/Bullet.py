import pygame
from PygameProject.sprite import bullet_group, all_sprite, shoot_group


# Класс пуль
class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(bullet_group, all_sprite)
        pass

    # Проверяет на столкновение с обектом
    def check(self):
        pass

    # Уничтожает пулю
    def kill(self):
        pass
