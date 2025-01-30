import pygame
from main_func import terminate
from consts import FPS, PERCENT_SCALE
from all_screens.func_button import installation_buttons, add_funcs


# настройки
def settings(screen, width, height, clock):
    surf_fon = pygame.Surface((width, height), pygame.SRCALPHA)
    surf_fon.blit(screen, (0, 0))

    font = pygame.font.Font(None, 60)
    text = font.render('Настройки', True, 'white')
    size_txt = text.get_size()

    d_x = 960 * PERCENT_SCALE
    size_y = 30 * PERCENT_SCALE
    s_dis = 100 * PERCENT_SCALE
    y = height / 2 - (size_y * 6 - size_y) / 2

    names = []
    version = installation_buttons(names, width, height, d_x, size_y)

    select_button = 0

    surf_dark = pygame.Surface((width, height), pygame.SRCALPHA)
    pygame.draw.rect(surf_dark, (0, 0, 0, 150), (0, 0, width, height))

    surf_border = pygame.Surface((width - s_dis * 2, height - s_dis * 2), pygame.SRCALPHA)
    pygame.draw.rect(surf_border, 'white',
                     (0, 0, surf_border.width, surf_border.height), width=4, border_radius=8)
    pygame.draw.rect(surf_border, (0, 0, 0, 0),
                     (surf_border.width / 2 - size_txt[0] * 0.75, 0,
                      size_txt[0] * 1.5, 4), width=4, border_radius=8)

    while True:

        clock.tick(FPS)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                terminate()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return 0

            if (event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONDOWN and
                    event.button == 1 or
                    event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN):
                f = 0
                if event.type != pygame.KEYDOWN:
                    for en, button in enumerate(version):
                        x0, y0 = button.pos
                        w, h = button.size
                        pos = event.pos
                        if x0 <= pos[0] <= x0 + w and y0 <= pos[1] <= y0 + h:
                            if event.type == pygame.MOUSEMOTION:
                                select_button = en
                            else:
                                f = 1
                                break

                if f and event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:

                    button = version[select_button]

                    if button.type_func[0] == 0:
                        return 0

                    if button.type_func[0] == 1:
                        button.type_func[1][0](button.type_func[1][1])

                    if button.type_func[0] == 2:
                        return 1

            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_w, pygame.K_s]:
                    step = 1
                    if event.key in [pygame.K_UP, pygame.K_w]:
                        step = -1
                    select_button = (select_button + step) % len(version)

        for en, button in enumerate(version):
            if en == select_button:
                button.set_color(1)
            else:
                button.set_color(0)

        screen.fill((0, 0, 0))
        screen.blit(surf_fon, (0, 0))
        screen.blit(surf_dark, (0, 0))
        screen.blit(surf_border, (s_dis, s_dis))

        screen.blit(text, (d_x - size_txt[0] / 2, s_dis - size_txt[1] / 2))

        for button in version:
            screen.blit(button.surf, button.pos)

        pygame.display.flip()
