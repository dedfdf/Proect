import pygame
import time
import sys
from weapon.Pistol import Pistol
from weapon.Automat import Automat
from weapon.Knife import Knife
from weapon.Shotgun import Shotgun
from weapon.Flashlight import Flashlight
from player.Weapon import Weapons
from player.Player import Player
from player.View import View
from sprite import *
from consts import TILE_WIDTH, TILE_HEIGHT, FPS, R_LOAD_CIRCLE
from main_funс import load_image, player_rotate, check_visible, create_visible
from Camera import Camera
from Cursor import Cursor
from Dark import Dark
from Bot.map_graph import Graphs
from Bot.Bot import Bot

pygame.init()
graph = Graphs(TILE_WIDTH, TILE_HEIGHT)
screen = pygame.display.set_mode((1000, 800))
width, height = screen.get_width(), screen.get_height()

clock = pygame.time.Clock()

tile_image = {'wall': load_image('stone_2.png'), 'empty': load_image('stone_pl.jpg'),
              'stone': load_image('stone.png'), 'pl': load_image('pl.png')}
cursor_image = load_image('cursor.png')


def terminate():
    pygame.quit()
    sys.exit()


def load_level(name):
    with open('weapon/levls/' + name, 'r') as file:
        level_map = [line.strip() for line in file.readlines()]
    max_len = max(map(len, level_map))
    graph.create_map(max_len, len(level_map))
    return list(map(lambda x: x.ljust(max_len, '.'), level_map))


class Tile(pygame.sprite.Sprite):
    def __init__(self, object_type, pos_x, pos_y, *group):
        super().__init__(*group, all_sprite)
        self.image = tile_image[object_type]
        self.rect = self.image.get_rect().move(pos_x * TILE_WIDTH, pos_y * TILE_HEIGHT)
        self.x, self.y = self.rect.x, self.rect.y
        self.mask = pygame.mask.from_surface(self.image)
        graph.add_in_map(pos_x, pos_y, object_type, Circle((pos_x, pos_y), 10, self.image))


class Circle(pygame.sprite.Sprite):
    def __init__(self, position, radius, image):
        super().__init__(all_sprite)
        self.image = image
        self.position = position
        self.rect = self.image.get_rect(center=(position[0] * TILE_WIDTH + TILE_WIDTH // 2,
                                                position[1] * TILE_HEIGHT + TILE_HEIGHT // 2))
        self.radius = radius

def generate_level(level, weapon):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y, grass_group, object_group)
            elif level[y][x] == '@':
                Tile('stone', x, y, box_group, object_group)
            elif level[y][x] == '1':
                Tile('wall', x, y, wall_group, object_block_visible_group, object_group)
            elif level[y][x] == '2':
                Tile('empty', x, y, grass_group, object_group)
                graph.add_bot_coord(x, y, Bot(x, y, graph, Automat()))
            elif level[y][x] == '#':
                Tile('empty', x, y, grass_group, object_group)
                new_player = Player(x, y, weapon, width, height)
    return new_player, x, y


def main():
    pygame.mouse.set_visible(False)
    weapon = Weapons([Automat(), Shotgun(), Pistol(), Knife(), Flashlight()])

    player, level_x, level_y = generate_level(load_level('level2.txt'), weapon)

    Dark(width, height, player)
    weapon.get_collision(player)
    View(player)

    camera = Camera(player, width, height)
    cursor = Cursor(pygame.mouse.get_pos(), cursor_image)

    flag = 1

    button_num = [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_f]
    prev_time = time.time()
    dt = 0

    check_visible(player)
    graph.graph_connect()
    while flag:

        clock.tick(FPS)

        now = time.time()
        dt = now - prev_time
        prev_time = now
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                flag = 0
            if event.type == pygame.MOUSEMOTION:
                cursor.move(event.pos)
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
        for x in graph.bot_spisok:
            x[2].coord_player = [player.pos_center[0], player.pos_center[1]]
            x[2].update()
        screen.fill('black')
        not_visible_object_group.draw(screen)
        create_visible(player)
        check_visible(player)
        player_group.update(dt)
        player_rotate(player)
        for sprite in grenade_group:
            sprite.fly(player)
        camera.update(player)

        for sprite in all_sprite:
            camera.apply(sprite)

        player.move()

        object_group.draw(screen)
        dark_group.draw(screen)
        items_visible_object_groups.draw(screen)

        if player.load_circle:
            player.load_circle.update()
            im = load_image('load_circle.png')
            screen.blit(im, (player.rect.centerx - R_LOAD_CIRCLE / 2,
                             player.rect.centery - R_LOAD_CIRCLE / 2))
        elif not player.using_item is None:
            player.remove_item()

        view_group.draw(screen)
        bullet_group.update()
        bullet_group.draw(screen)
        visible_object_group.draw(screen)
        player_group.draw(screen)
        visible_object_group.empty()
        items_visible_object_groups.empty()
        #  collision_circle_group.draw(screen)
        #  ^--может показать коллизию персонажа

        cursor_group.draw(screen)

        player.draw_icon(screen)

        if player.blind_effect:
            surface = pygame.Surface((width, height), pygame.SRCALPHA)
            surface.fill((255, 255, 255, min(player.blind_effect, 255)))
            screen.blit(surface, (0, 0))

            player.blind_effect -= player.v_blind
            player.blind_effect = max(0, player.blind_effect)

        pygame.display.flip()
    pygame.quit()
