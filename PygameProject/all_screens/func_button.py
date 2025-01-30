from all_screens.Button import Button
import pygame


# создаёт сразу несколько кнопок
def installation_buttons(names, width, height, d_x, size_y):
    y = height / 2 - (len(names) * size_y * 2 - size_y) / 2
    arr = []
    for en, name in enumerate(names):
        color = 1 if en == 0 else 0
        button = Button((width - d_x, y), name, color)
        arr.append(button)
        y += size_y * 2
    return arr

# присваивает группе кнопок функции
def add_funcs(funcs, version):
    for en, button in enumerate(version):
        button.add_func(funcs[en])
