import pygame
from pygame.math import Vector2 as vec2
from sprite import player_group, all_sprite, wall_group, collision_circle_group, items_group, \
    object_block_visible_group
from consts import SPEED_PLAYER, TILE_WIDTH, TILE_HEIGHT, MAX_HEART, MAX_ARMOR, FPS, \
    TIME_MAX_BLIND, MAX_BLIND_GRENADE, ANGLE_VIEW
from main_funс import load_image, check_barrier
from items.Armor import ArmorIcon, Armor
from items.Light_grenade import LightGrenadeIcon, LightGrenade
from items.Medicine import MedicineIcon, Medicine
from items.Patron import PatronIcon, Patron
import math

ITEMS_PAIR = ((ArmorIcon, Armor), (MedicineIcon, Medicine), (PatronIcon, Patron),
              (LightGrenadeIcon, LightGrenade))


# Класс игрока
class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, weapon, w, h):
        super().__init__(player_group, all_sprite)
        self.image = self.orig_image = weapon.image
        self.weapon = weapon

        self.w, self.h = w, h

        self.vector_move = vec2(0)

        self.pos_center = [pos_x * TILE_WIDTH + TILE_WIDTH / 2,
                           pos_y * TILE_HEIGHT + TILE_HEIGHT / 2]
        self.rect = self.image.get_rect(center=self.pos_center)

        self.diag_move = 1 / 2 ** 0.5

        self.angle = 0
        self.angle_shoot = 0
        self.time = 0

        self.health = MAX_HEART
        self.armor = MAX_ARMOR

        self.weapon_icon = 'pistol'

        self.status = 'idle'
        self.status_move = 0

        self.select_cell = 0
        self.items = [ArmorIcon(), MedicineIcon(), LightGrenadeIcon(), PatronIcon(), None]

        self.load_circle = None
        self.using_item = None

        self.blind_effect = 0
        self.timer_loading = 0
        self.volume = 1

        self.sound_step = pygame.mixer.Sound('sound/step.mp3')

    # Получает вид
    def get_view(self, view):
        self.view = view

    # Получает тьму карты
    def get_dark(self, dark):
        self.dark = dark

    def set_angle_shoot(self):
        weapon = self.weapon.weapon
        speed = weapon.speed_aim_angle

        if self.status_move:
            if self.lshift:
                if self.angle_shoot > weapon.walk_angle_shoot:
                    self.angle_shoot -= speed
                else:
                    self.angle_shoot = min(weapon.walk_angle_shoot, self.angle_shoot + speed)
            else:
                self.angle_shoot = min(weapon.run_angle_shoot, self.angle_shoot + speed)
        else:
            self.angle_shoot = max(weapon.idle_angle_shoot, self.angle_shoot - speed)

    # Обновляет состояние игрока
    def update_move(self, dt):

        self.dt = dt

        speed = SPEED_PLAYER * dt * FPS
        self.lshift = 0

        if pygame.key.get_pressed()[pygame.K_LSHIFT]:
            speed /= 2
            self.lshift = 1

        self.dx = self.dy = 0

        directions = {pygame.K_w: [0, -1], pygame.K_s: [0, 1],
                      pygame.K_a: [-1, 0], pygame.K_d: [1, 0]}
        for i in directions:
            x, y = directions[i]
            if pygame.key.get_pressed()[i]:
                self.dx += x * speed
                self.dy += y * speed
        if self.dx and self.dy:
            self.dx *= self.diag_move
            self.dy *= self.diag_move

        self.image = self.orig_image = self.weapon.image
        self.rect = self.image.get_rect(center=self.rect.center)

        if self.dx or self.dy:
            self.status_move = 1
            if self.status == 'idle':
                self.weapon.weapon.set_status(self, 'move')
        elif self.dx == self.dy == 0:
            self.status_move = 0
            if self.status == 'move':
                self.weapon.weapon.set_status(self, 'idle')

        x, y = self.check_collide(self.weapon.collision)
        self.dx *= x
        self.dy *= y

        self.set_angle_shoot()

    # Перемещает игрока
    def move(self):
        self.vector_move.x += self.dx
        self.vector_move.y += self.dy

        self.rect.center = self.pos_center + self.vector_move

        all_sprite.update(self.vector_move)

        self.weapon.next_frame(self)

    # Проверяет коллизию
    def check_collide(self, circle):
        x = y = 1
        circle.rect.x += self.dx * 2
        for sprite in wall_group:
            if pygame.sprite.collide_mask(circle, sprite):
                x = 0
        circle.rect.x -= self.dx * 2
        circle.rect.y += self.dy * 2
        for sprite in wall_group:
            if pygame.sprite.collide_mask(circle, sprite):
                y = 0
        circle.rect.y -= self.dy * 2
        return x, y

    # Изменяет статус/состояние игрока
    def set_status(self, key):
        if self.status == 'idle' or self.status == 'move':
            self.weapon.weapon.set_status(self, key)

    # Меняет снаряжение
    def swich_weapon(self, num):
        if self.status == 'idle' or self.status == 'move':
            x, y = self.check_collide(self.weapon.arr_collision[num])
            if x == y == 1:
                self.weapon.weapon = self.weapon.arr_weapon[num]
                self.weapon.collision = self.weapon.arr_collision[num]
                self.set_status(self.status)
                self.angle_shoot = self.weapon.weapon.run_angle_shoot
                self.dark.set_dark(self.weapon.weapon.r_view)

    def draw_icon(self, screen):
        image = load_image(f'icon/health_{self.health}.png', 'player')
        x = self.rect.centerx - self.w / 2 + 35
        y = self.rect.centery - self.h / 2 + 10 + 25
        screen.blit(image, (x, y))

        image = load_image('icon/armor.png', 'player')
        for i in range(self.armor):
            x = self.rect.centerx - self.w / 2 + 10 * i + 50 * i + 35
            y = self.rect.centery - self.h / 2 + 95
            screen.blit(image, (x, y))

        weapon = self.weapon.weapon
        image = load_image(f'icon/{weapon.name}.png', 'player')
        x = self.rect.centerx - self.w / 2 + 35
        y = self.rect.centery + self.h / 2 - 120
        screen.blit(image, (x, y))

        x = self.rect.centerx - self.w / 2 + 35 + 150
        y = self.rect.centery + self.h / 2 - 95
        if weapon.name not in ['knife', 'flashlight']:
            patron = f'{weapon.clip_patron}/{weapon.patron}'

            font = pygame.font.Font('player/icon/Naziona.otf', 50)
            text = font.render(f'{patron}', True, 'white')
            screen.blit(text, (x, y))
        else:
            image = load_image('icon/infinity.png', 'player')
            screen.blit(image, (x, y - 30))

        x = self.rect.centerx + self.w / 2 - 125
        y = self.rect.centery + self.h / 2 - 125
        for i in range(4, -1, -1):
            color = (100, 100, 100)
            if i == self.select_cell:
                color = (40, 40, 40)
            pygame.draw.rect(screen, color, (x, y, 60, 60))
            pygame.draw.rect(screen, 'white', (x, y, 60, 60), width=5)
            x -= 55
            if self.items[i]:
                screen.blit(self.items[i].image, (x + 65, y + 10))

    def remove_health(self):
        if self.armor != 0:
            self.armor -= 1
        else:
            if self.health != 0:
                self.health -= 1

    def set_select_cell(self, y):
        self.select_cell -= y
        if self.select_cell < 0:
            self.select_cell = 4
        self.select_cell %= 5

    def use_item(self):
        if self.using_item is None:
            if self.items[self.select_cell]:
                flag = self.items[self.select_cell].load(self)
                if flag:
                    self.using_item = self.select_cell
        else:
            self.load_circle = None
            self.using_item = None

    def remove_item(self):
        select = self.using_item if self.using_item else self.select_cell
        self.items[select].use(self)
        self.items[select] = None
        self.using_item = None

    def drop_item(self):
        my_item = self.items[self.select_cell]
        for item in ITEMS_PAIR:
            if type(my_item) is item[0]:
                item[1](self)
                self.items[self.select_cell] = None
                break

    def pick_up_item(self):
        if self.items[self.select_cell] is None:
            for sprite in items_group:
                if sprite.rect.collidepoint(self.rect.center):
                    self.items[self.select_cell] = sprite.pick_up()
                    sprite.kill()
                    break

    def blind(self, grenade):
        vec = vec2(self.rect.centerx - grenade.rect.centerx,
                   (self.rect.centery - grenade.rect.centery))
        s = (vec.x ** 2 + vec.y ** 2) ** 0.5
        view = self.weapon.weapon.r_view

        if s <= view * 2:
            grenade.sound_boom.play(0)

        if check_barrier(self, grenade, object_block_visible_group):
            return

        blind = MAX_BLIND_GRENADE
        time = TIME_MAX_BLIND
        percent = 100

        if s > view:
            percent = 100 - s % view / (view / 100)

        if s != 0:
            angle = 360 - math.degrees(math.acos(vec.x / s)) - 180
            angle = 360 - angle if grenade.rect.centery > self.rect.centery else angle
            angle = abs(self.angle - angle)
            angle = 360 - angle if angle > 180 else angle
            if angle > ANGLE_VIEW / 2:
                angle_100p = 180 - ANGLE_VIEW / 2
                angle -= ANGLE_VIEW / 2
                percent -= angle / (angle_100p / 100) / 2

        blind = blind / 100 * percent
        time = time / 100 * percent

        sound = pygame.mixer.Sound('sound/light_grenade_concussion.mp3')
        raw_array = sound.get_raw()
        max_raw = len(raw_array)
        begin = round(max_raw - max_raw / 100 * percent)
        begin -= begin % 4

        raw_array = raw_array[begin:]
        cut_sound = pygame.mixer.Sound(buffer=raw_array)
        cut_sound.play(0)

        self.blind_effect = max(blind, 0)
        self.v_blind = blind / time * self.dt
        self.volume = 1 - 1 / 100 * percent

    def draw_blind(self, screen):
        surface = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
        surface.fill((255, 255, 255, min(self.blind_effect, 255)))
        screen.blit(surface, (0, 0))

        self.blind_effect -= self.v_blind
        self.blind_effect = max(0, self.blind_effect)

        percent = self.blind_effect / (MAX_BLIND_GRENADE / 100)
        self.volume = 1 - 1 / 100 * percent
