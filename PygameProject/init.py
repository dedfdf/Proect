import pygame

pygame.init()
pygame.mixer.init()
pygame.mixer.set_num_channels(150)

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
# screen = pygame.display.set_mode((1000, 800))
width, height = screen.get_width(), screen.get_height()
clock = pygame.time.Clock()