from consts import VIEW
from draw import draw_view
from main_func import load_image


# Класс вида игрока
# И моя гордость
class View:
    def __init__(self, player):
        self.r = VIEW

        player.get_view(self)

    # Обновляет вид
    def set_view(self, player, arr):
        r_view = player.weapon.weapon.r_view
        draw_view(arr, r_view)
        self.image = load_image('view.png')
        self.rect = self.image.get_rect()
        self.r = r_view
