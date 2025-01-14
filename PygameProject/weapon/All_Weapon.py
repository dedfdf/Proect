from PygameProject.main_funс import get_frame
import pygame


class AllWeapon:
    def __init__(self, arr_status, ):
        self.arr_status = arr_status
        path = 'weapon/player_image/'

        self.frames = {}
        for status in arr_status:
            self.frames[status] = get_frame(path, self.name, status, self.dx, self.dy,
                                            self.dx_attack, self.dy_attack)

        self.speed_frame = {'idle': 90,
                            'attack': 90,
                            'move': 50,
                            'reload': 80,
                            'shoot': 100}
        self.cur_frame = -1
        self.status = 'idle'
        self.image = self.orig_image = self.frames[self.status][self.cur_frame]

        self.step = 1
        self.time = 0

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
            elif type == 1 and self.status == 'shoot' and pygame.mouse.get_pressed()[0]:
                pass
            else:
                self.set_status(player, 'idle')
                return
            self.cur_frame = self.cur_frame + self.step

            self.image = self.frames[self.status][self.cur_frame]

    def set_status(self, player, status):
        if status in self.arr_status:
            self.step = 1
            self.status = status
            self.cur_frame = -1
            player.status = status
