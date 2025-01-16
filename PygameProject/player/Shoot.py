import pygame
from sprite import shoot_group, all_sprite
from main_funс import load_image
from draw import draw_shoot


# Класс направления выстрелов
class Shoot(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__(shoot_group, all_sprite)
        self.pos_center = list(player.rect.center)
        self.set_view(player)

        player.get_shoot(self)

    # Перемещает объект
    def move(self, vector_move):
        self.rect.center = self.pos_center + vector_move

    # Обновляет объект
    def set_view(self, player):
        weapon = player.weapon.weapon
        draw_shoot(weapon.max_angle_shoot, weapon.r_shoot)
        self.image = self.orig_image = load_image('shoot.png')
        self.rect = self.image.get_rect(center=self.pos_center)
