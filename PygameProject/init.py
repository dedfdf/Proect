import pygame
import ctypes

# инициализирует pygame, определяет разрешение экрана
pygame.init()
pygame.mixer.init()
pygame.mixer.set_num_channels(150)  # без этой команды звуки могут пропадать

ctypes.windll.user32.SetProcessDPIAware()  # делает нормальное разрешение
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
width, height = screen.get_width(), screen.get_height()
clock = pygame.time.Clock()
