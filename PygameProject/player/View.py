import pygame
from PygameProject.sprite import all_sprite, view_group
from PygameProject.const import VIEW
from PygameProject.draw import draw_view
from PygameProject.main_funс import load_image


# Класс вида игрока
# И моя гордость
class View(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__(view_group, all_sprite)
        self.pos_center = list(player.rect.center)
        self.r = VIEW

        player.get_view(self)

    # Перемещает вид
    def move(self, vector_move):
        self.rect.center = self.pos_center + vector_move

    # Обновляет вид
    def set_view(self, player, arr):
        r_view = player.weapon.weapon.r_view
        draw_view(arr, r_view)
        self.image = load_image('circle_view.png')
        self.rect = self.image.get_rect(center=self.pos_center)
        self.r = r_view
