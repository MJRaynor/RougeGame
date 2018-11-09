import pygame,sys
import libtcodpy as libtcod

#game files
import constants
global SURFACE_MAIN


###Struct################################################################
class struc_Tile:
    def __init__(self,block_path):
        self.block_path = block_path


###Objects###############################################################
class obj_Actor:
    def __init__(self ,x, y, sprite):
        self.x = x
        self.y = y
        self.sprite = sprite

    def draw(self):
        SURFACE_MAIN.blit(self.sprite, (self.x*constants.CELL_WIDTH,self.y*constants.CELL_HEIGHT))

    def move(self,dx,dy):
        if GAME_MAP[self.x+dx][self.y+dy].block_path == False:
            self.x += dx
            self.y += dy


###Map##################################################################
def map_create():
    new_map = [[struc_Tile(False) for y in range(0,constants.MAP_HEIGHT)]for x in range(0,constants.MAP_WIDTH)]
    new_map[10][10].block_path = True
    new_map[10][15].block_path = True

    return new_map
    
####Draw################################################################
def draw_game():
    global SURFACE_MAIN
    #clear the surface
    SURFACE_MAIN.fill(constants.COLOR_DEFAULT_BG)
    #draw the map
    draw_map(GAME_MAP)
    #draw the character
    #SURFACE_MAIN.blit(constants.S_PLAYER,(200,200))
    ENEMY.draw()
    PLAYER.draw()
    #Player is drawn last so it is on top layer of display - play is always on top
    #update the display
    pygame.display.flip()

def draw_map(map_to_draw):
    for x in range(0,constants.MAP_WIDTH):
        for y in range(0,constants.MAP_HEIGHT):
            if map_to_draw[x][y].block_path == True:
                #draw a wall
                SURFACE_MAIN.blit(constants.S_WALL,(x*constants.CELL_WIDTH,y*constants.CELL_HEIGHT))
            else:
                #draw floor
                SURFACE_MAIN.blit(constants.S_FLOOR,(x*constants.CELL_WIDTH,y*constants.CELL_HEIGHT))

########################################################################
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

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    PLAYER.move(0,-1)
                if event.key == pygame.K_DOWN:
                    PLAYER.move(0,1)
                if event.key == pygame.K_LEFT:
                    PLAYER.move(-1,0)
                if event.key == pygame.K_RIGHT:
                    PLAYER.move(1,0)


        #draw the game
        draw_game()

    #quit the game
    pygame.quit()
    sys.exit()


####GAME INITIALIZE#####################################################
def game_initialize():
    global SURFACE_MAIN, GAME_MAP, PLAYER, ENEMY
    #initalizes the main window in pygame
    pygame.init()
    SURFACE_MAIN = pygame.display.set_mode((constants.GAME_WIDTH,constants.GAME_HEIGHT))
    pygame.display.set_caption('Test Game!')
    GAME_MAP = map_create()

    ENEMY  = obj_Actor(15,15,constants.S_ENEMY)
    PLAYER = obj_Actor(0,0,constants.S_PLAYER)
    


########################################################################
if __name__ == '__main__':
    game_initialize()
    game_main_loop()
