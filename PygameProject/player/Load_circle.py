from draw import draw_load_circle
from consts import TIME_LOADING


class Load_circle:
    def __init__(self, color, color_border, player):
        self.angle = 271
        self.flag = 0

        self.color = color
        self.color_border = color_border

        self.player = player

    def update(self):
        draw_load_circle(self.color, self.color_border, self.angle)
        v = 360 / TIME_LOADING
        self.angle += v * self.player.dt
        self.angle %= 360
        if self.angle < 270:
            self.flag = 1
        if self.angle >= 270 and self.flag:
            self.player.load_circle = None
