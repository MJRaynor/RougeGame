import pygame

pygame.init()

#game sizes
GAME_WIDTH  = 800
GAME_HEIGHT = 600
CELL_WIDTH  = 32
CELL_HEIGHT = 32


#Map Vars
MAP_WIDTH  = 20
MAP_HEIGHT = 20


#color definitions

COLOR_BLACK =   (0,0,0)
COLOR_WHITE =   (255,255,255)
COLOR_GREY  =   (100,100,100)


#game colors
COLOR_DEFAULT_BG = COLOR_GREY


#SPRITES
S_PLAYER = pygame.image.load("data/python.png")
S_ENEMY  = pygame.image.load("data/crab.png")
S_WALL   = pygame.image.load("data/wall.png")
S_FLOOR  = pygame.image.load("data/floor.jpg")
