import pygame
from consts import PERCENT_SCALE


# класс обычной кнопки
class Button:
    def __init__(self, pos, text, color, size=0):
        size = size if size != 0 else 45
        size = round(size * PERCENT_SCALE)

        self.font = pygame.font.Font(None, size)
        self.first_pos = pos

        self.set_text(text)

        self.set_color(color)

    def set_color(self, color):
        self.color = color = (255, 255, 255) if color else (128, 128, 128)

        text = self.font.render(self.text, True, color)

        self.surf.fill((0, 0, 0, 0))

        w, h = text.get_size()
        x0, y0 = self.size[0] / 2, self.size[1] / 2
        self.surf.blit(text, (x0 - w / 2, y0 - h / 2))

    def add_func(self, n):
        self.type_func = n

    def set_text(self, text):
        self.text = text
        txt = self.font.render(text, True, 'white')
        self.size = size = txt.get_size()

        self.pos = self.first_pos[0] - size[0] / 2, self.first_pos[1] - size[1] / 2
        self.surf = pygame.Surface((self.size[0], self.size[1]), pygame.SRCALPHA)
