import pygame
from main_func import load_image
from consts import PERCENT_SCALE

# класс для кнопки с изображением
class ButtonImage:
    def __init__(self, pos, image, angle, type, color=0):
        self.im = load_image(image, 'all_screens/image')
        self.im = pygame.transform.scale(self.im, (self.im.width * PERCENT_SCALE,
                                                   self.im.height * PERCENT_SCALE))

        self.lock = load_image('zam.jpg', 'all_screens/image')
        self.lock = pygame.transform.scale(self.lock, (self.lock.width * PERCENT_SCALE,
                                                       self.lock.height * PERCENT_SCALE))

        self.size = (self.im.width, self.im.height)
        self.pos = pos
        self.angle = angle
        self.type = int(type)

        self.set_color(color)

    def set_color(self, color):
        color = (200, 200, 200) if color else (135, 135, 135)

        self.surf = pygame.Surface(self.size, pygame.SRCALPHA)
        self.surf.blit(self.im, (0, 0))

        pygame.draw.rect(self.surf, color,
                         (0, 0, 320 * PERCENT_SCALE, 295 * PERCENT_SCALE),
                         round(22 * PERCENT_SCALE))
        pygame.draw.rect(self.surf, color,
                         (0, 295 * PERCENT_SCALE, 320 * PERCENT_SCALE, 55 * PERCENT_SCALE))

        if not self.type:
            self.surf.blit(self.lock, (21 * PERCENT_SCALE, 21 * PERCENT_SCALE))

        self.surf = pygame.transform.rotate(self.surf, self.angle)

        self.rect = self.surf.get_rect().move(self.pos[0], self.pos[1])

    def set_type(self, type):
        self.type = int(type)
