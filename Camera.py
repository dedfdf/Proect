# Класс камеры, для слежки за игроком
class Camera:
    def __init__(self, player, width, height):
        self.dx = 0
        self.dy = 0

        self.player = player
        self.dark = player.dark
        self.view = player.view

        self.width, self.height = width, height

    # Двигает все объекты на карте
    def apply(self, object):
        if (object is self.player or object is self.dark or object is self.view or
                object in self.player.weapon.arr_collision):
            object.pos_center[0] += self.dx
            object.pos_center[1] += self.dy
        else:
            object.rect.x += self.dx
            object.rect.y += self.dy

    # Обновляет вектор сдвига
    def update(self, target):
        x = target.rect.centerx + target.dx
        y = target.rect.centery + target.dy
        self.dx = -(x - self.width // 2)
        self.dy = -(y - self.height // 2)
