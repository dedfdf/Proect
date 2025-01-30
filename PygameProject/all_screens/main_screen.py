import pygame
import time
from consts import FPS, PERCENT_SCALE, TIME_LOAD
from main_func import load_image, terminate
from Dust import Dust
from sprite import dust_group
from all_screens.func_button import installation_buttons, add_funcs
from all_screens.choice_level import choice_level
from weapon.Pistol import Pistol
from weapon.Automat import Automat
from weapon.Knife import Knife
from weapon.Shotgun import Shotgun
from weapon.Flashlight import Flashlight
from all_screens.warning import Warning
from all_screens.settings import settings


# главное меню
def start_screen(screen, width, height, clock):
    im_fon = load_image('main_fon.jpg', 'all_screens/image')
    fon = pygame.transform.scale(im_fon, (width, height))

    arsenal = [Automat(), Shotgun(), Pistol(), Knife(), Flashlight()]

    music = 'music/main_screen.mp3'
    max_volume = 0.3
    pygame.mixer.music.load(music)
    pygame.mixer.music.set_volume(max_volume)
    pygame.mixer.music.play(-1)

    prev = time.time()
    time_dust = 0

    text_warning = 'Заменить данное сохранение?'

    d_x = 320 * PERCENT_SCALE
    size_y = 30 * PERCENT_SCALE

    with open('all_screens/save.txt', 'r', encoding='utf-8') as file:
        saves = [[j for j in i.strip().split()] for i in file]

    names = [save[0] for save in saves]
    new_game_version = installation_buttons(names, width, height, d_x, size_y)
    load_game_version = installation_buttons(names, width, height, d_x, size_y)

    names = ['Новая игра', 'Загрузить игру', 'Настройки', 'Выйти']
    main_version = installation_buttons(names, width, height, d_x, size_y)

    version = main_version[:]
    select_button = 0

    sound_error = pygame.mixer.Sound('sound/sound_exit_game.mp3')

    funcs = [(0, new_game_version), (0, load_game_version), (1, settings), (4,)]
    add_funcs(funcs, main_version)

    funcs = [(2,), (2,), (2,), (2,), (2,)]
    add_funcs(funcs, new_game_version)

    funcs = [(3,), (3,), (3,), (3,), (3,)]
    add_funcs(funcs, load_game_version)

    warning = 0

    dark_surf = pygame.Surface((width, height), pygame.SRCALPHA)
    pygame.draw.rect(dark_surf, (0, 0, 0, 128), (0, 0, width, height))

    dark_surf_load = pygame.Surface((width, height), pygame.SRCALPHA)

    load = (0,)
    time_dark = 0

    while True:
        clock.tick(FPS)

        now = time.time()
        dt = now - prev
        prev = now
        if load:
            time_dark += dt

        event_version = warning.version[:] if warning else version[:]
        event_select = warning.select_button if warning else select_button
        type_event = 1 if warning else 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if (event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONDOWN and
                    event.button == 1 or
                    event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN):
                f = 0
                if event.type != pygame.KEYDOWN:
                    for en, button in enumerate(event_version):
                        x, y = button.pos
                        w, h = button.size
                        pos = event.pos
                        if x <= pos[0] <= x + w and y <= pos[1] <= y + h:
                            if event.type == pygame.MOUSEMOTION:
                                event_select = en
                            else:
                                f = 1
                                break
                if not load:
                    if (f and event.type == pygame.MOUSEBUTTONDOWN or
                            event.type == pygame.KEYDOWN):

                        button = event_version[event_select]

                        if button.type_func[0] == 0:
                            event_version = button.type_func[1][:]

                        if button.type_func[0] == 1:
                            button.type_func[1](screen, width, height, clock)

                        if button.type_func[0] == 2:
                            if button.text == 'Пусто':
                                with open('all_screens/save.txt', 'w', encoding='utf-8') as file:
                                    st = f'Сохранение-{event_select + 1}'
                                    saves[event_select][0] = st
                                    event_version[event_select].set_text(st)
                                    load_game_version[event_select].set_text(st)

                                    for line in saves:
                                        file.write(' '.join(line) + '\n')
                                    load = (2, (choice_level,
                                                (screen, width, height, clock, arsenal,
                                                 select_button)))
                            else:
                                warning = Warning(text_warning, 5, 6, add_funcs)

                        if button.type_func[0] == 3:
                            if button.text == 'Пусто':
                                sound_error.play()
                            else:
                                load = (2, (choice_level,
                                            (screen, width, height, clock, arsenal, select_button)))

                        if button.type_func[0] == 4:
                            load = (1,)

                        if button.type_func[0] == 5:
                            with open('all_screens/save.txt', 'w', encoding='utf-8') as file:
                                level = ['1', '0', '0']
                                saves[select_button][1:] = level[:]

                                for en, line in enumerate(saves):
                                    if en == select_button:
                                        file.write(line[0] + ' ' + ' '.join(level) + '\n')
                                    else:
                                        file.write(' '.join(line) + '\n')
                                load = (2, (choice_level,
                                            (screen, width, height, clock, arsenal, select_button)))
                                warning = 0

                        if button.type_func[0] == 6:
                            warning = 0

            my_arr = [pygame.K_UP, pygame.K_w, pygame.K_DOWN, pygame.K_s]
            if warning:
                my_arr = [pygame.K_LEFT, pygame.K_a, pygame.K_RIGHT, pygame.K_d]

            if event.type == pygame.KEYDOWN:
                if event.key in my_arr:
                    step = 1
                    if event.key in my_arr[0:2]:
                        step = -1
                    event_select = (event_select + step) % len(event_version)

                elif event.key == pygame.K_ESCAPE and not load:
                    if event_version in [new_game_version, load_game_version]:
                        event_version = main_version[:]

        for en, button in enumerate(event_version):
            if en == event_select:
                button.set_color(1)
            else:
                button.set_color(0)

        if type_event and warning:
            warning.version = event_version[:]
            warning.select_button = event_select

        elif not type_event:
            version = event_version[:]
            select_button = event_select

        screen.fill((0, 0, 0))
        screen.blit(fon, (0, 0))
        for button in version:
            screen.blit(button.surf, button.pos)

        if type_event and warning:
            size = warning.size
            screen.blit(dark_surf, (0, 0))
            screen.blit(warning.surf, (width / 2 - size[0] / 2, height / 2 - size[1] / 2))
            for button in warning.version:
                screen.blit(button.surf, button.pos)

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
                pygame.draw.rect(dark_surf_load, (0, 0, 0, transparency),
                                 (0, 0, width, height))
                screen.blit(dark_surf_load, (0, 0))

            else:
                time_dark = 0
                if load[0] == 0:
                    load = 0
                elif load[0] == 1:
                    load = 0
                    terminate()
                elif load[0] == 2:
                    pygame.mixer.music.stop()
                    load[1][0](*load[1][1])

                    pygame.mixer.music.load(music)
                    pygame.mixer.music.play()

                    load = (0,)
                    version = main_version[:]

                    prev = time.time()
                    continue

        else:
            pygame.mixer.music.set_volume(max_volume)

        pygame.display.flip()
