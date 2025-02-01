import pygame
from main_func import terminate, load_image
from consts import FPS, TIME_INFO_SCREEN, TIME_LOAD, PERCENT_SCALE
import time


# экран победы игрока
def screen_win(screen, width, height, clock, time_level):
    size = round(200 * PERCENT_SCALE)

    music = 'music/screen_win.mp3'
    max_volume = 0.3
    pygame.mixer.music.load(music)
    pygame.mixer.music.set_volume(max_volume)
    pygame.mixer.music.play(-1)

    font = pygame.font.Font('all_screens/image/Stage Wanders.ttf', size)
    text = font.render('YOU WIN!', True, 'white')

    second = str(int(time_level % 60)).rjust(2, '0')
    minute = str(int(time_level // 60)).rjust(2, '0')

    time_level = font.render(f'{minute}:{second}', True, 'white')

    dark_surf = pygame.Surface((width, height), pygame.SRCALPHA)

    prev = time.time()

    load = (0,)
    time_dark = 0
    all_time = 0

    while True:

        clock.tick(FPS)

        now = time.time()
        dt = now - prev
        prev = now
        if load:
            time_dark += dt
        all_time += dt

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                terminate()

        screen.fill((0, 0, 0))
        screen.blit(text, (width / 2 - text.width / 2, size))
        screen.blit(time_level, (width / 2 - time_level.width / 2, size * 3))

        if load:
            if time_dark <= TIME_LOAD:
                if load[0] == 0:
                    transparency = 100 - time_dark / (TIME_LOAD / 100)
                    volume = time_dark / (TIME_LOAD / 100)
                elif load[0] in [1, 2]:
                    transparency = time_dark / (TIME_LOAD / 100)
                    volume = 100 - time_dark / (TIME_LOAD / 100)

                transparency = 255 / 100 * transparency
                volume = max_volume / 100 * volume

                pygame.mixer.music.set_volume(volume)

                dark_surf.fill((0, 0, 0, 0))
                pygame.draw.rect(dark_surf, (0, 0, 0, transparency),
                                 (0, 0, width, height))
                screen.blit(dark_surf, (0, 0))

            else:
                time_dark = 0
                if load[0] == 0:
                    load = 0
                elif load[0] == 1:
                    return
        else:
            pygame.mixer.music.set_volume(max_volume)
        if all_time + TIME_LOAD >= TIME_INFO_SCREEN and not load:
            load = (1, 0)

        pygame.display.flip()
