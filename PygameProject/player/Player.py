import pygame
from pygame.math import Vector2 as vec2
from PygameProject.sprite import player_group, all_sprite, wall_group, collision_circle_group
from PygameProject.const import SPEED_PLAYER, TILE_WIDTH, TILE_HEIGHT
import math


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, weapon):
        super().__init__(player_group, all_sprite)
        self.image = self.orig_image = weapon.image
        self.weapon = weapon

        self.vector_move = vec2(0)

        self.pos_center = [pos_x * TILE_WIDTH + TILE_WIDTH / 2,
                           pos_y * TILE_HEIGHT + TILE_HEIGHT / 2]
        self.rect = self.image.get_rect(center=self.pos_center)

        self.diag_move = 1 / 2 ** 0.5
        self.angle = 0

        self.status = 'idle'

    def get_view(self, view):
        self.view = view

    def get_shoot(self, shoot):
        self.shoot = shoot

    def get_dark(self, dark):
        self.dark = dark

    def update(self):

        speed = SPEED_PLAYER

        if pygame.key.get_pressed()[pygame.K_LSHIFT]:
            speed /= 2

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

        if (self.dx or self.dy) and self.status == 'idle':
            self.weapon.weapon.set_status(self, 'move')
        elif self.dx == self.dy == 0 and self.status == 'move':
            self.weapon.weapon.set_status(self, 'idle')

        self.move()

    def move(self):
        x, y = self.check_collide(self.weapon.collision)

        self.dx *= x
        self.dy *= y

        self.vector_move.x += self.dx
        self.vector_move.y += self.dy

        self.rect.center = self.pos_center + self.vector_move

        self.view.move(self.vector_move)
        self.shoot.move(self.vector_move)
        self.dark.move(self.vector_move)
        collision_circle_group.update(self.vector_move)

        self.weapon.next_frame(self)

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

    def set_status(self, key):
        if self.status == 'idle' or self.status == 'move':
            self.weapon.weapon.set_status(self, key)

    def swich_weapon(self, num):
        if self.status == 'idle' or self.status == 'move':
            x, y = self.check_collide(self.weapon.arr_collision[num])
            if x == y == 1:
                self.weapon.weapon = self.weapon.arr_weapon[num]
                self.weapon.collision = self.weapon.arr_collision[num]
                self.shoot.set_view(self)
