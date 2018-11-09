
#Necesary py game imports
import pygame, sys
#from pygame.locals import *
import libtcodpy as libtcod

#game files
import constants


def game_initialize():
    #initalizes the main window in pygame
    pygame.init()
    global SURFACE_MAIN
    SURFACE_MAIN = pygame.display.set_mode((constants.GAME_WIDTH,constants.GAME_HEIGHT))
    pygame.display.set_caption('Hello World!')

def draw_game():
    global SURFACE_MAIN
    #clear the surface
    SURFACE_MAIN.fill(constants.COLOR_DEFAULT_BG)
    #draw the map

    #draw the character
    SURFACE_MAIN.blit(constants.S_PLAYER,(200,200))

    #update the display
    pygame.display.flip()




def game_main_loop():
    #main game loop
    game_quit = False

    while not game_quit:

        #get player input
        events_list = pygame.event.get()

        #process input
        for event in events_list:
            if event.type == pygame.QUIT:
                game_quit = True

        #draw the game
        draw_game()

    #quit the game
    pygame.quit()
    sys.exit()



if __name__ == '__main__':
    game_initialize()
    game_main_loop()
