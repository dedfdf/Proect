from draw import draw_dark
from main_funс import load_image


# Класс тьмы на карте
class Dark:
    def __init__(self, w, h, player):
        draw_dark(w, h, player.weapon.weapon.r_view)
        self.w, self.h = w, h
        self.image = load_image('dark.png')

        player.get_dark(self)

    def set_dark(self, r):
        draw_dark(self.w, self.h, r)
        self.image = load_image('dark.png')
