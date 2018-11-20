import libtcodpy as libtcod
import pygame

pygame.init()

# Game sizes
GAME_WIDTH = 800
GAME_HEIGHT = 600
CELL_WIDTH = 32
CELL_HEIGHT = 32

# FPS LIMIT
GAME_FPS = 60

# MAP LIMITATIONS
MAP_WIDTH = 50
MAP_HEIGHT = 30
MAP_MAX_NUM_ROOMS = 10

# ROOM LIMITATIONS
ROOM_MAX_HEIGHT = 7
ROOM_MIN_HEIGHT = 3
ROOM_MAX_WIDTH = 5
ROOM_MIN_WIDTH = 3

# Color definitions
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_GREY = (100, 100, 100)
COLOR_RED = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)

# Game colors
COLOR_DEFAULT_BG = COLOR_GREY

# FOV SETTINGS
FOV_ALGO = libtcod.FOV_BASIC  # Algorithm for FOV Calculation
FOV_LIGHT_WALLS = True        # Does the FOV shine on the walls?
TORCH_RADIUS = 10             # Sight radius for FOV

# MESSAGE DEFAULTS
NUM_MESSAGES = 4

# DEFAULT FONTS
FONT_DEBUG_MESSAGE = pygame.font.Font('data\joystix.ttf', 16)
FONT_MESSAGE_TEXT = pygame.font.Font('data\joystix.ttf', 12)
FONT_CURSOR_TEXT = pygame.font.Font('data\joystix.ttf', CELL_HEIGHT)

# DEPTHS
DEPTH_PLAYER = -100
DEPTH_CREATURE = 1
DEPTH_ITEM = 2
DEPTH_CORPSE = 100
