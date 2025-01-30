import time
import pygame
from consts import FPS, PERCENT_SCALE, TIME_LOAD
from main_func import load_image, terminate
from all_screens.Button_image import ButtonImage
from Dust import Dust
from sprite import dust_group
from game.game import game_cycle
from all_screens.screen_death import screen_death
from all_screens.screen_win import screen_win

# экран выбора уровня
def choice_level(screen, width, height, clock, arsenal, num_save):
    im_fon = load_image('fon_choice_level.jpg', 'all_screens/image')
    fon = pygame.transform.scale(im_fon, (width, height))

    music = 'music/choice_level.mp3'
    max_volume = 0.3
    pygame.mixer.music.load(music)
    pygame.mixer.music.set_volume(max_volume)
    pygame.mixer.music.play(-1)

    prev = time.time()

    dark_surf = pygame.Surface((width, height), pygame.SRCALPHA)

    with open('all_screens/save.txt', 'r', encoding='utf-8') as file:
        save_file = file.readlines()[num_save].strip().split(' ')[1:]

    time_dark = 0
    load = (0,)

    time_dust = 0

    pos1 = (150 * PERCENT_SCALE, 400 * PERCENT_SCALE)
    pos2 = (800 * PERCENT_SCALE, 500 * PERCENT_SCALE)
    pos3 = (1400 * PERCENT_SCALE, 200 * PERCENT_SCALE)
    levels = [ButtonImage(pos1, 'im_level1.jpg', -5, save_file[0], 1),
              ButtonImage(pos2, 'im_level2.jpg', 15, save_file[1]),
              ButtonImage(pos3, 'im_level3.jpg', -10, save_file[2])]

    im = load_image('left_button.png', 'all_screens/image')
    l_button = pygame.transform.scale(im,
                                      (im.width * PERCENT_SCALE, im.height * PERCENT_SCALE))
    im = load_image('right_button.png', 'all_screens/image')
    r_button = pygame.transform.scale(im,
                                      (im.width * PERCENT_SCALE, im.height * PERCENT_SCALE))

    select_level = 0

    while True:
        clock.tick(FPS)

        now = time.time()
        dt = now - prev
        prev = now
        if load:
            time_dark += dt
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if (event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONDOWN and
                    event.button == 1 or
                    event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN):
                f = 0
                if event.type != pygame.KEYDOWN:
                    for en, level in enumerate(levels):
                        if not level.type:
                            continue
                        if level.rect.collidepoint(event.pos):
                            if event.type == pygame.MOUSEMOTION:
                                select_level = en
                            else:
                                f = 1
                            break
                if not load:
                    if f and event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                        load = (2, (game_cycle,
                                    (screen, width, height, clock, arsenal,
                                     select_level + 1, num_save)))

            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_a, pygame.K_d]:
                    step = 1
                    if event.key in [pygame.K_LEFT, pygame.K_a]:
                        step = -1
                    prev_select = select_level
                    select_level = (select_level + step) % len(levels)
                    if not levels[select_level].type:
                        select_level = prev_select

                elif event.key == pygame.K_ESCAPE and not load:
                    load = (1,)

        for en, button in enumerate(levels):
            if en == select_level:
                button.set_color(1)
            else:
                button.set_color(0)

        screen.fill((0, 0, 0))
        screen.blit(fon, (0, 0))
        for level in levels:
            screen.blit(level.surf, level.pos)

        pygame.draw.line(screen, (204, 0, 0), (0, 300 * PERCENT_SCALE),
                         (380 * PERCENT_SCALE, 427 * PERCENT_SCALE), 5)
        pygame.draw.line(screen, (204, 0, 0),
                         (380 * PERCENT_SCALE, 427 * PERCENT_SCALE),
                         (1050 * PERCENT_SCALE, 527 * PERCENT_SCALE), 5)
        pygame.draw.line(screen, (204, 0, 0),
                         (1050 * PERCENT_SCALE, 527 * PERCENT_SCALE),
                         (1600 * PERCENT_SCALE, 235 * PERCENT_SCALE), 5)
        pygame.draw.line(screen, (204, 0, 0),
                         (1600 * PERCENT_SCALE, 235 * PERCENT_SCALE),
                         (width, 150 * PERCENT_SCALE), 5)

        screen.blit(r_button, (350 * PERCENT_SCALE, 397 * PERCENT_SCALE))
        screen.blit(l_button, (1025 * PERCENT_SCALE, 500 * PERCENT_SCALE))
        screen.blit(l_button, (1570 * PERCENT_SCALE, 210 * PERCENT_SCALE))

        if time_dust > 0.4:
            time_dust = 0
            Dust(width, height)
        else:
            time_dust += dt
        for sprite in dust_group:
            surf = sprite.render(dt)
            x, y = sprite.center
            r = sprite.r
            screen.blit(surf, (x - r, y - r))
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
                elif load[0] == 2:
                    pygame.mixer.music.stop()
                    res = load[1][0](*load[1][1])
                    if res == 1:
                        screen_death(screen, width, height, clock)
                    if type(res) is tuple:
                        screen_win(screen, width, height, clock, res[1])

                        if res[0] != len(save_file) - 1:
                            save_file[res[0]] = '1'

                        for en, button in enumerate(levels):
                            button.set_type(save_file[en])

                        with open('all_screens/save.txt', 'r', encoding='utf-8') as file_read:
                            file_read = file_read.readlines()

                        with open('all_screens/save.txt', 'w', encoding='utf-8') as file:
                            for en, line in enumerate(file_read):
                                line = line.strip()
                                if en == num_save:
                                    file.write(
                                        f'Сохранение-{num_save + 1} ' + ' '.join(save_file) + '\n')
                                else:
                                    file.write(line + '\n')

                    pygame.mixer.music.load(music)
                    pygame.mixer.music.play()

                    load = (0,)

                    prev = time.time()
                    continue
        else:
            pygame.mixer.music.set_volume(max_volume)

        pygame.display.flip()
