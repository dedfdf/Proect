from main_func import get_frame
import pygame
from player.Bullet import Bullet


# Класс для смены фреймов всех оружей
class Frames:
    def __init__(self, arr_status):
        self.arr_status = arr_status
        path = 'weapon/player_image/'

        self.frames = {}
        for status in arr_status:
            self.frames[status] = get_frame(path, self.name, status, self.dx, self.dy,
                                            self.dx_attack, self.dy_attack)
        self.cur_frame = -1
        self.status = 'idle'
        self.image = self.orig_image = self.frames[self.status][self.cur_frame]

        self.step = 1
        self.time = 0

    # Переходит на следующий фрейм
    def next_frame(self, player, clock, type):
        size_frame = len(self.frames[self.status])

        if type != 0:
            self.shoot_sound.set_volume(player.volume)
            self.reload_sound.set_volume(player.volume)
        player.sound_step.set_volume(player.volume)

        # время между анимациями берем как FPS / время 1-ого прохода по циклу и превращаем в секунды
        # и умноженный на количество кадров
        if self.time >= 1 / 100:
            self.time = 0

            if 1 > self.cur_frame + self.step:
                self.step = 1
            elif self.cur_frame + self.step == size_frame:
                self.step = -1

            if self.status == 'idle' or self.status == 'move':
                pass
            elif self.step != -1 and self.cur_frame != size_frame - 1:
                pass
            elif (type == 1 and self.status == 'shoot' and pygame.mouse.get_pressed()[0] and
                  self.clip_patron != 0):
                pass
            else:
                self.set_status(player, 'idle')
                return

            self.cur_frame = self.cur_frame + self.step

            if self.status == 'shoot':
                if self.cur_frame == 1:
                    if type == 2:
                        for _ in range(5):
                            Bullet(player)
                    else:
                        if type == 1:
                            self.shoot_sound.play(0)

                        Bullet(player)
                    player.angle_shoot = min(self.run_angle_shoot,
                                             player.angle_shoot + self.speed_set_angle)
                    self.clip_patron = max(0, self.clip_patron - 1)

                elif self.cur_frame == 0 and type != 1:
                    self.shoot_sound.play(0)

            if self.status == 'reload':
                if self.cur_frame == size_frame - 1:
                    patron = self.max_clip_patron - self.clip_patron
                    patron = min(patron, self.patron)
                    self.clip_patron += patron
                    self.patron -= patron
                elif self.cur_frame == 0:
                    self.reload_sound.play(0)

            if self.status == 'move':
                if self.cur_frame in [1, 10, 19] and not player.lshift:
                    player.sound_step.play(0)

            self.image = self.frames[self.status][self.cur_frame]
        else:
            self.time += player.dt

    # Изменяет статус/состояние игрока
    def set_status(self, player, status):
        if status in self.arr_status:
            if status == 'shoot' and self.clip_patron == 0:
                return
            if status == 'reload' and (
                    self.clip_patron == self.max_clip_patron or self.patron == 0):
                return
            self.step = 1
            self.status = status
            self.cur_frame = -1
            self.time = 0
            player.status = status
