import pygame, gif_pygame
from consts import FPS
from game.game import terminate, main


def start_screen(screen, width, height, clock):
    gif = gif_pygame.load('image/fon.gif')
    gif_pygame.transform.scale(gif, (width, height))

    while True:
        clock.tick(FPS)
        gif.render(screen, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                main(screen, width, height, clock)

        pygame.display.flip()
