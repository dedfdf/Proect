from collections import defaultdict
import pygame.draw


class Graphs:  # Класс графов
    def __init__(self, w, h):
        self.graph = defaultdict(list)
        self.w = w
        self.h = h
        self.map_empty = []
        self.bot_spisok = []

    def add_edge(self, u, v):  # Добавление пути в вершины
        self.graph[u].append(v)

    def bfs(self, start, end):  # Нахождение пути
        visited = set()
        queue = []
        queue.append([start])
        if start == end:
            return
        while queue:
            path = queue.pop(0)
            node = path[-1]
            if node not in visited:
                neighbors = self.graph[node]
                for neighbor in neighbors:
                    new_path = list(path)
                    new_path.append(neighbor)
                    queue.append(new_path)
                    if neighbor == end:
                        return new_path
                visited.add(node)

    def add_in_map(self, x, y, object, circle):  # Добавление объектов на карту
        self.map[y][x] = (x, y, object, circle)
        if object == 'empty':
            self.map_empty.append((x, y))

    def create_map(self, size_x, size_y):  # Создаёт карту уровня для графов
        self.map = [[(i, j) for j in range(size_x)] for i in range(size_y)]
        self.size_x = size_x
        self.size_y = size_y

    def add_bot_coord(self, x, y, bot):  # Добавляет местоположение бота
        self.bot_spisok.append((x, y, bot))

    def graph_connect(self):  # Соединяет все графы
        for k in self.map_empty:
            i = k[1]
            j = k[0]
            flag_1 = True
            flag_2 = True
            flag_3 = True
            flag_4 = True
            if i - 1 > 0:
                if self.map[i - 1][j][2] == 'empty':
                    self.add_edge(k[:2], self.map[i - 1][j][:2])
                else:
                    flag_1 = False
                    flag_2 = False
            if i + 1 < self.size_y:
                if self.map[i + 1][j][2] == 'empty':
                    self.add_edge(k[:2], self.map[i + 1][j][:2])
                else:
                    flag_3 = False
                    flag_4 = False
            if j - 1 > 0:
                if self.map[i][j - 1][2] == 'empty':
                    self.add_edge(k[:2], self.map[i][j - 1][:2])
                else:
                    flag_1 = False
                    flag_3 = False
            if j + 1 < self.size_x:
                if self.map[i][j + 1][2] == 'empty':
                    self.add_edge(k[:2], self.map[i][j + 1][:2])
                else:
                    flag_2 = False
                    flag_4 = False
            if i - 1 > 0 and j + 1 < self.size_x:
                if self.map[i - 1][j + 1][2] == 'empty' and flag_2:
                    self.add_edge(k[:2], self.map[i - 1][j + 1][:2])
            if i + 1 < self.size_y and j + 1 < self.size_x:
                if self.map[i + 1][j + 1][2] == 'empty' and flag_4:
                    self.add_edge(k[:2], self.map[i + 1][j + 1][:2])
            if j - 1 > 0 and i + 1 < self.size_y:
                if self.map[i + 1][j - 1][2] == 'empty' and flag_3:
                    self.add_edge(k[:2], self.map[i + 1][j - 1][:2])
            if i - 1 > 0 and j - 1 > 0:
                if self.map[i - 1][j - 1][2] == 'empty' and flag_1:
                    self.add_edge(k[:2], self.map[i - 1][j - 1][:2])
