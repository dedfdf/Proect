import pygame
import sys
from PygameProject.weapon.Pistol import Pistol
from PygameProject.weapon.Automat import Automat
from PygameProject.weapon.Knife import Knife
from PygameProject.weapon.Shotgun import Shotgun
from PygameProject.weapon.Flashlight import Flashlight
from PygameProject.player.Weapon import Weapons
from PygameProject.player.Player import Player
from PygameProject.player.View import View
from PygameProject.player.Shoot import Shoot
from PygameProject.sprite import *
from PygameProject.const import TILE_WIDTH, TILE_HEIGHT, FPS
from PygameProject.main_funс import load_image, player_rotate, check_visible
from PygameProject.Camera import Camera
from PygameProject.Cursor import Cursor
from PygameProject.Dark import Dark

pygame.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
width, height = screen.get_width(), screen.get_height()

clock = pygame.time.Clock()

tile_image = {'wall': load_image('derevo.jpg'), 'empty': load_image('wood.png'),
              'stone': load_image('stone.png'), 'pl': load_image('pl.png')}
cursor_image = load_image('cursor.png')


def terminate():
    pygame.quit()
    sys.exit()


def load_level(name):
    with open('levls/' + name, 'r') as file:
        level_map = [line.strip() for line in file.readlines()]
    max_len = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_len, '.'), level_map))


class Tile(pygame.sprite.Sprite):
    def __init__(self, object_type, pos_x, pos_y, *group):
        super().__init__(*group, all_sprite)

        self.image = tile_image[object_type]
        self.rect = self.image.get_rect().move(pos_x * TILE_WIDTH, pos_y * TILE_HEIGHT)
        self.x, self.y = self.rect.x, self.rect.y
        self.mask = pygame.mask.from_surface(self.image)


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
                Tile('pl', x, y, wall_group, not_visible_object_group)
            elif level[y][x] == '#':
                Tile('empty', x, y, grass_group, object_group)
                new_player = Player(x, y, weapon)
    return new_player, x, y


def main():
    pygame.mouse.set_visible(False)
    weapon = Weapons([Automat(), Shotgun(), Pistol(), Knife(), Flashlight()])

    player, level_x, level_y = generate_level(load_level('level1.txt'), weapon)

    Dark(width, height, player)
    weapon.get_collision(player)
    View(player)
    Shoot(player)

    camera = Camera(player, width, height)
    cursor = Cursor(pygame.mouse.get_pos(), cursor_image)

    flag = 1

    button_num = [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_f]

    check_visible(player)

    while flag:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                flag = 0
            if event.type == pygame.MOUSEMOTION:
                cursor.move(event.pos)
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
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if type(weapon.weapon) is Knife or type(weapon.weapon) is Flashlight:
                    player.set_status('attack')
                else:
                    player.set_status('shoot')

        screen.fill('black')

        check_visible(player)
        player_group.update()
        player_rotate(player)

        camera.update(player)
        for sprite in all_sprite:
            camera.apply(sprite)

        object_group.draw(screen)
        dark_group.draw(screen)

        shoot_group.draw(screen)
        view_group.draw(screen)
        bullet_group.draw(screen)
        visible_object_group.draw(screen)
        player_group.draw(screen)
        visible_object_group.empty()
        #  collision_circle_group.draw(screen)
        #  ^--может показать коллизию персонажа

        cursor_group.draw(screen)

        clock.tick(FPS)
        pygame.display.flip()
    pygame.quit()
