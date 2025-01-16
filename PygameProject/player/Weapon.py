from draw import draw_circle
from player.Circle_collision import Collision


# Класс нынешнего оружея игрока
class Weapons:
    def __init__(self, arsenal):
        self.arr_weapon = arsenal

        self.weapon = self.arr_weapon[2]

        self.image = self.weapon.image
        self.rect = self.image.get_rect()

    # обновляет фрейм
    def next_frame(self, player):
        self.weapon.next_frame(player)
        self.image = self.weapon.image
        self.rect = self.image.get_rect()

    # Получает коллизию для игрока
    def get_collision(self, player):
        self.arr_collision = [Collision(draw_circle(weapon.radius, weapon.name), player)
                              for weapon in self.arr_weapon]
        self.collision = self.arr_collision[2]
