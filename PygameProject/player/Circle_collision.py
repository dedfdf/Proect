import pygame
from PygameProject.sprite import all_sprite, collision_circle_group
from PygameProject.main_funс import load_image


# Коллизия игрока
class Collision(pygame.sprite.Sprite):
    def __init__(self, name, player):
        super().__init__(collision_circle_group, all_sprite)
        self.image = load_image(f'circle_{name}.png', 'collision_image')
        self.pos_center = list(player.rect.center)
        self.rect = self.image.get_rect(center=self.pos_center)

    # Перемещает коллизию
    def update(self, vector_move):
        self.rect.center = self.pos_center + vector_move
