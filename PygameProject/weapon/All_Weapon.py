from main_funс import get_frame
import pygame
from player.Bullet import Bullet


# Класс для смены фреймов всех оружей
class AllWeapon:
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

        self.speed_frame['idle'] = 70
        self.speed_frame['move'] = 50

    # Переходит на следующий фрейм
    def next_frame(self, player, clock, type):
        size_frame = len(self.frames[self.status])
        if clock - self.time > self.speed_frame[self.status]:
            self.time = clock

            if 2 > self.cur_frame + self.step:
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

            if self.status == 'shoot' and self.cur_frame == 1:
                if type == 2:
                    for _ in range(5):
                        Bullet(player)
                else:
                    Bullet(player)
                self.clip_patron = max(0, self.clip_patron - 1)

            if self.status == 'reload' and self.cur_frame == size_frame - 1:
                patron = self.max_clip_patron - self.clip_patron
                patron = min(patron, self.patron)
                self.clip_patron += patron
                self.patron -= patron
            # print(self.status, self.cur_frame)
            self.image = self.frames[self.status][self.cur_frame]

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
            player.status = status
