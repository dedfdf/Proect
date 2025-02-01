import pygame
import time
from weapon.Knife import Knife
from weapon.Flashlight import Flashlight
from player.Weapon import Weapons
from player.Player import Player
from player.View import View
from sprite import *
from consts import TILE_WIDTH, TILE_HEIGHT, FPS, R_LOAD_CIRCLE, PERCENT_SCALE, TIME_LOAD
from main_func import load_image, player_rotate, check_visible, create_visible, terminate
from game.Camera import Camera
from game.Cursor import Cursor
from game.Dark import Dark
from Dust import Dust
from all_screens.pause import pause
from Bot.Bot import Bot
from Bot.map_graph import Graphs
from weapon.Automat import Automat

graph = Graphs(TILE_WIDTH, TILE_HEIGHT)
tile_image = {'wall': load_image('stone_2.png'), 'empty': load_image('stone_pl.jpg'), 'pl': load_image('pl.png')}


def load_level(name):
    with open('levels/' + name, 'r') as file:
        level_map = [line.strip() for line in file.readlines()]
    max_len = max(map(len, level_map))
    graph.create_map(max_len, len(level_map))
    return list(map(lambda x: x.ljust(max_len, '.'), level_map))


class Tile(pygame.sprite.Sprite):
    def __init__(self, object_type, pos_x, pos_y, *group):
        super().__init__(*group, all_sprite)

        self.image = tile_image[object_type]
        w = self.image.get_width() * PERCENT_SCALE
        h = self.image.get_height() * PERCENT_SCALE
        self.image = pygame.transform.scale(self.image, (w, h))

        self.pos_center = [pos_x * TILE_WIDTH * PERCENT_SCALE + TILE_WIDTH * PERCENT_SCALE,
                           pos_y * TILE_HEIGHT * PERCENT_SCALE + TILE_HEIGHT * PERCENT_SCALE]

        self.rect = self.image.get_rect(center=self.pos_center)
        self.x, self.y = self.rect.x, self.rect.y
        self.mask = pygame.mask.from_surface(self.image)
        graph.add_in_map(pos_x, pos_y, object_type, Circle((pos_x, pos_y), 10, self.image))

    def update(self, vector_move):
        self.rect.center = self.pos_center


class Circle(pygame.sprite.Sprite):
    def __init__(self, position, radius, image):
        super().__init__(all_sprite)
        self.image = image
        self.position = position
        self.rect = self.image.get_rect(center=(position[0] * TILE_WIDTH + TILE_WIDTH // 2,
                                                position[1] * TILE_HEIGHT + TILE_HEIGHT // 2))
        self.pos_center = [self.rect.center[0], self.rect.center[1]]
        self.radius = radius


def generate_level(level, weapon, width, height):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y, grass_group, object_group)
            elif level[y][x] == '1':
                Tile('wall', x, y, wall_group, object_block_visible_group, object_group)
            elif level[y][x] == '2':
                Tile('empty', x, y, grass_group, object_group)
                graph.add_bot_coord(x, y, Bot(x, y, graph, Automat()))
            elif level[y][x] == '#':
                Tile('empty', x, y, grass_group, object_group)
                new_player = Player(x, y, weapon, width, height)
    return new_player, x, y


# прошу не оценивать все классы и функции, что лежат до этого момента, т. к. они были не в моём ТЗ
# игровой цикл
def game_cycle(screen, width, height, clock, arsenal, level, num_save):
    pygame.mouse.set_visible(False)
    weapon = Weapons(arsenal)

    # player, level_x, level_y = generate_level(load_level(f'level{level}.txt'), weapon, width,
    # height)z
    player, level_x, level_y = generate_level(load_level(f'level1.txt'), weapon, width,
                                              height)

    Dark(width, height, player)
    weapon.get_collision(player)
    View(player)

    camera = Camera(player, width, height)
    cursor = Cursor(pygame.mouse.get_pos())

    button_num = [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_f]

    prev = time.time()
    time_dust = 0
    time_dark = 0
    all_time = 0

    check_visible(player)

    surf_dark_load = pygame.Surface((width, height), pygame.SRCALPHA)
    load = (0,)
    graph.graph_connect()
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
            if event.type == pygame.MOUSEMOTION:
                cursor.move(event.pos)
            if not load:
                if not player.load_circle:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            player.set_status('reload')
                        elif event.key == pygame.K_q:
                            player.set_status('attack')
                        elif event.key in button_num:
                            for en, even in enumerate(button_num):
                                if even == event.key:
                                    player.swich_weapon(en)
                                    break
                        elif event.key == pygame.K_g:
                            player.drop_item()
                        elif event.key == pygame.K_e:
                            player.pick_up_item()
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if type(weapon.weapon) is Knife or type(weapon.weapon) is Flashlight:
                            player.set_status('attack')
                        else:
                            player.set_status('shoot')
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_v:
                        player.remove_health()

            if event.type == pygame.MOUSEWHEEL:
                player.set_select_cell(event.y)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                player.use_item()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE and not load:
                pygame.mouse.set_visible(True)
                quit_param = pause(screen, width, height, clock)
                pygame.mouse.set_visible(False)

                if quit_param:
                    load = (1,)

                prev = time.time()
        for x in graph.bot_spisok:
            x[2].move()
        screen.fill('black')

        create_visible(player)
        check_visible(player)
        player.update_move(dt)
        player_rotate(player)

        for sprite in grenade_group:
            sprite.fly(player)

        camera.update(player)
        for sprite in all_sprite:
            camera.apply(sprite)
        player.move()

        object_group.draw(screen)
        screen.blit(player.dark.image, (0, 0))

        view = player.view
        screen.blit(view.image, (player.rect.centerx - view.rect.w / 2 + 1,
                                 player.rect.centery - view.rect.h / 2 + 1))

        if player.load_circle:
            player.load_circle.update()
            im = load_image('load_circle.png')
            screen.blit(im, (player.rect.centerx - R_LOAD_CIRCLE / 2,
                             player.rect.centery - R_LOAD_CIRCLE / 2))
        elif not player.using_item is None:
            player.remove_item()

        items_visible_object_groups.draw(screen)
        for bullet in bullet_group:
            bullet.new_pos()
        bullet_group.draw(screen)

        visible_object_group.draw(screen)
        player_group.draw(screen)
        visible_object_group.empty()
        items_visible_object_groups.empty()
        #  collision_circle_group.draw(screen)
        #  ^--может показать коллизию персонажа

        cursor_group.draw(screen)

        player.draw_icon(screen)

        if player.health == 0 or len(opponents_group) == 0:
            load = (1,)

        if time_dust > 0.3:
            time_dust = 0
            Dust(width, height)
        else:
            time_dust += dt
        for sprite in dust_group:
            surf = sprite.render(dt)
            x, y = sprite.center
            r = sprite.r
            screen.blit(surf, (x - r, y - r))

        if player.blind_effect:
            player.draw_blind(screen)

        if load:
            if time_dark <= TIME_LOAD:
                if load[0] == 0:
                    transparency = 100 - time_dark / (TIME_LOAD / 100)
                elif load[0] in [1, 2]:
                    transparency = time_dark / (TIME_LOAD / 100)

                transparency = 255 / 100 * transparency

                surf_dark_load.fill((0, 0, 0, 0))
                pygame.draw.rect(surf_dark_load, (0, 0, 0, transparency),
                                 (0, 0, width, height))
                screen.blit(surf_dark_load, (0, 0))

            else:
                time_dark = 0
                if load[0] == 0:
                    load = 0

                elif load[0] == 1:
                    pygame.mouse.set_visible(True)

                    res = 0
                    if player.health == 0:
                        res = 1
                    elif len(opponents_group) == 0:
                        res = (level, all_time)

                    for group in all_group:
                        group.empty()

                    return res

        pygame.display.flip()
