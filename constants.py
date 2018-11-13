import libtcodpy as libtcod

#game sizes
GAME_WIDTH  = 800
GAME_HEIGHT = 600
CELL_WIDTH  = 32
CELL_HEIGHT = 32

#FPS
GAME_FPS = 60


#Map Vars
MAP_WIDTH  = 20
MAP_HEIGHT = 20


#color definitions

COLOR_BLACK =   (0,0,0)
COLOR_WHITE =   (255,255,255)
COLOR_GREY  =   (100,100,100)
COLOR_RED   =   (255, 0, 0)

#game colors
COLOR_DEFAULT_BG = COLOR_GREY


#SPRITES
#S_PLAYER            = pygame.image.load("data/python.png")
#S_ENEMY             = pygame.image.load("data/crab.png")



#FOV SETTINGS
FOV_ALGO        = libtcod.FOV_BASIC
FOV_LIGHT_WALLS = True
TORCH_RADIUS    = 5


#MESSAGE DEFAULTS
NUM_MESSAGES = 4
