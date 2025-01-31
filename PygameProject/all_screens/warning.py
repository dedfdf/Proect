import pygame
from all_screens.Button import Button
from consts import PERCENT_SCALE
from init import width, height


# класс для повторного предупреждения
# класс был реализован один из первых в начальных экранах, из-за этого является очень плохим
# времени на исправление нету
class Warning:
    def __init__(self, text, yes, no, add_funcs):
        self.size = 500 * PERCENT_SCALE, 281.25 * PERCENT_SCALE
        size_text = round(35 * PERCENT_SCALE)

        self.surf = pygame.Surface(self.size, pygame.SRCALPHA)

        self.select_button = 0

        pygame.draw.rect(self.surf, (50, 50, 50), (0, 0, self.size[0], self.size[1]),
                         border_radius=8)

        font = pygame.font.Font(None, 40)
        text_warning = font.render('Внимание!', True, 'white')

        w, h = text_warning.get_size()
        x0 = self.size[0] / 2
        y0 = 20 * PERCENT_SCALE

        s_border = y0 + h / 3

        pos_y = width / 2 - self.size[1] / 3, height / 2 + self.size[1] / 2 - s_border
        pos_n = width / 2 + self.size[1] / 3, height / 2 + self.size[1] / 2 - s_border

        self.version = [Button(pos_y, 'Да', 1, size_text),
                        Button(pos_n, 'Нет', 0, size_text)]
        funcs = [(yes,), (no,)]
        add_funcs(funcs, self.version)

        pygame.draw.rect(self.surf, 'white',
                         (s_border, s_border, self.size[0] -
                          2 * s_border, self.size[1] - 2 * s_border), width=4, border_radius=8)

        pygame.draw.rect(self.surf, (50, 50, 50),
                         (x0 - w / 2 - s_border, y0, w + 2 * s_border, h))

        pygame.draw.rect(self.surf, (50, 50, 50),
                         (x0 - self.size[1] / 3 - s_border, self.size[1] - s_border - y0,
                          self.version[0].size[0] + s_border, self.version[0].size[1]))
        pygame.draw.rect(self.surf, (50, 50, 50),
                         (x0 + self.size[1] / 3 - s_border, self.size[1] - s_border - y0,
                          self.version[0].size[0] + s_border, self.version[0].size[1]))

        self.surf.blit(text_warning, (x0 - w / 2, y0))

        font = pygame.font.Font(None, size_text)
        text = font.render(text, True, 'white')

        w, h = text.get_size()
        x0, y0 = self.size[0] / 2, self.size[1] / 2
        self.surf.blit(text, (x0 - w / 2, y0 - h / 2))
