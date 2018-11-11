import pygame,sys
import libtcodpy as libtcod

#game fi#les
import constants


#
#(  ____ \\__   __/(  ____ )|\     /|(  ____ \\__   __/
#| (    \/   ) (   | (    )|| )   ( || (    \/   ) (
#| (_____    | |   | (____)|| |   | || |         | |
#(_____  )   | |   |     __)| |   | || |         | |
#      ) |   | |   | (\ (   | |   | || |         | |
#/\____) |   | |   | ) \ \__| (___) || (____/\   | |
#\_______)   )_(   |/   \__/(_______)(_______/   )_(
#

class struc_Tile:
    def __init__(self, block_path):
        self.block_path = block_path
        self.explored = False


# _______  ______  _________ _______  _______ _________ _______
#(  ___  )(  ___ \ \__    _/(  ____ \(  ____ \\__   __/(  ____ \
#| (   ) || (   ) )   )  (  | (    \/| (    \/   ) (   | (    \/
#| |   | || (__/ /    |  |  | (__    | |         | |   | (_____
#| |   | ||  __ (     |  |  |  __)   | |         | |   (_____  )
#| |   | || (  \ \    |  |  | (      | |         | |         ) |
#| (___) || )___) )|\_)  )  | (____/\| (____/\   | |   /\____) |
#(_______)|/ \___/ (____/   (_______/(_______/   )_(   \_______)
#

class obj_Actor:
    def __init__(self, x, y, name_object, sprite, creature = None, ai = None):
        self.x = x
        self.y = y
        self.sprite = sprite

        self.creature = creature
        if creature:
            creature.owner = self

        self.ai = ai
        if ai:
            ai.owner = self


    def draw(self):
        is_visible = libtcod.map_is_in_fov(FOV_MAP, self.x, self.y)

        if is_visible:
            SURFACE_MAIN.blit(self.sprite, (self.x*constants.CELL_WIDTH, self.y*constants.CELL_HEIGHT))

#
#(  ____ \(  ___  )(       )(  ____ )(  ___  )( (    /|(  ____ \( (    /|
#| (    \/| (   ) || () () || (    )|| (   ) ||  \  ( || (    \/|  \  ( |
#| |      | |   | || || || || (____)|| |   | ||   \ | || (__    |   \ | |
#| |      | |   | || |(_)| ||  _____)| |   | || (\ \) ||  __)   | (\ \) |
#| |      | |   | || |   | || (      | |   | || | \   || (      | | \   |
#| (____/\| (___) || )   ( || )      | (___) || )  \  || (____/\| )  \  |
#(_______/(_______)|/     \||/       (_______)|/    )_)(_______/|/    )_)
#

class com_Creature:
    #creatures have health can attack other objects and can die
    def __init__(self, name_instance, hp=10, death_function = None):

        self.name_instance = name_instance
        self.maxhp = hp
        self.hp = hp
        self.death_function = death_function

    def move(self, dx, dy):

        tile_is_wall = (GAME_MAP[self.owner.x + dx][self.owner.y + dy].block_path == True)

        target = map_check_for_creatures(self.owner.x + dx, self.owner.y + dy, self.owner)
        #
        if target:
            self.attack(target, 3)


        if not tile_is_wall and target is None:
            self.owner.x += dx
            self.owner.y += dy

    def attack(self, target, damage):
        print (self.name_instance + " attacks " + target.creature.name_instance + " for " + str(damage) + " damage!")
        target.creature.take_damage(damage)

    def take_damage(self, damage):
        self.hp -= damage
        print (self.name_instance + "'s health is " + str(self.hp) + "/" + str(self.maxhp))

        if self.hp <= 0:
            if self.death_function is not None:
                self.death_function(self.owner)



#class com_Item:


#class com_Container:

#        ___       __
#       /   \     |  |
#      /  ^  \    |  |
#     /  /_\  \   |  |
#    /  _____  \  |  |
#   /__/     \__\ |__|
#

class ai_Test:
    #once per turn, execute
    def take_turn(self):
        self.owner.creature.move(libtcod.random_get_int(0,-1, 1,),libtcod.random_get_int(0,-1, 1,))


def death_monster(monster):
    #on death most monster stop moving
    print (monster.creature.name_instance + " is dead!")
    monster.creature = None
    monster.ai = None



#_______  _______  _______
#(       )(  ___  )(  ____ )
#| () () || (   ) || (    )|
#| || || || (___) || (____)|
#| |(_)| ||  ___  ||  _____)
#| |   | || (   ) || (
#| )   ( || )   ( || )
#|/     \||/     \||/
#

def map_create():
    new_map = [[struc_Tile(False) for y in range(0,constants.MAP_HEIGHT)]for x in range(0,constants.MAP_WIDTH)]
    new_map[10][10].block_path = True
    new_map[10][15].block_path = True

    for x in range(constants.MAP_WIDTH):
        new_map[x][0].block_path = True
        new_map[x][constants.MAP_HEIGHT-1].block_path = True

    for y in range(constants.MAP_HEIGHT):
        new_map[0][y].block_path = True
        new_map[constants.MAP_WIDTH-1][y].block_path = True

    map_make_fov(new_map)

    return new_map

def map_check_for_creatures(x, y, exclude_object = None):

    target = None

    if exclude_object:
        #check to find creature at that location that isnt excluded
        for object in GAME_OBJECTS:
            if (object is not exclude_object and
                object.x == x and
                object.y == y and
                object.creature):

                target = object


            if target:
                return target

    else:
        #check to find creature at that location
        for object in GAME_OBJECTS:
            if (object.x == x and
                object.y == y and
                object.creature):

                target = object


            if target:
                return target

def map_make_fov(incoming_map):
    global FOV_MAP

    FOV_MAP = libtcod.map_new(constants.MAP_HEIGHT, constants.MAP_HEIGHT)

    for y in range(constants.MAP_HEIGHT):
        for x in range(constants.MAP_WIDTH):
            libtcod.map_set_properties(FOV_MAP, x, y, not incoming_map[x][y].block_path, not incoming_map[x][y].block_path)

def map_calculate_fov():
    global FOV_CALCULATE

    if FOV_CALCULATE:
        FOV_CALCULATE = False
        libtcod.map_compute_fov(FOV_MAP, PLAYER.x, PLAYER.y, constants.TORCH_RADIUS, constants.FOV_LIGHT_WALLS, constants.FOV_ALGO)



# ______   _______  _______
#(  __  \ (  ____ )(  ___  )|\     /|
#| (  \  )| (    )|| (   ) || )   ( |
#| |   ) || (____)|| (___) || | _ | |
#| |   | ||     __)|  ___  || |( )| |
#| |   ) || (\ (   | (   ) || || || |
#| (__/  )| ) \ \__| )   ( || () () |
#(______/ |/   \__/|/     \|(_______)
#

def draw_game():
    #clear the surface
    SURFACE_MAIN.fill(constants.COLOR_DEFAULT_BG)
    #draw the map
    draw_map(GAME_MAP)
    #draw the character
    #SURFACE_MAIN.blit(constants.S_PLAYER,(200,200))
    #ENEMY.draw()
    #PLAYER.draw()
    #Draw all objects
    for obj in GAME_OBJECTS:
        obj.draw()
    #Player is drawn last so it is on top layer of display - play is always on top
    #update the display
    pygame.display.flip()

def draw_map(map_to_draw):

    for x in range(0,constants.MAP_WIDTH):
        for y in range(0,constants.MAP_HEIGHT):

            is_visible = libtcod.map_is_in_fov(FOV_MAP, x, y)

            if is_visible:

                map_to_draw[x][y].explored = True

                if map_to_draw[x][y].block_path == True:
                    #draw a wall
                    SURFACE_MAIN.blit(constants.S_WALL, (x*constants.CELL_WIDTH, y*constants.CELL_HEIGHT))
                else:
                    #draw floor
                    SURFACE_MAIN.blit(constants.S_FLOOR, (x*constants.CELL_WIDTH, y*constants.CELL_HEIGHT))

            elif map_to_draw[x][y].explored:
                if map_to_draw[x][y].block_path == True:
                    #draw a wall
                    SURFACE_MAIN.blit(constants.S_WALLEXPLORED, (x*constants.CELL_WIDTH, y*constants.CELL_HEIGHT))
                else:
                    #draw floor
                    SURFACE_MAIN.blit(constants.S_FLOOREXPLORED, (x*constants.CELL_WIDTH, y*constants.CELL_HEIGHT))




########################################################################
#   _______  _______  _______  _______    _        _______  _______  _______
#  (  ____ \(  ___  )(       )(  ____ \  ( \      (  ___  )(  ___  )(  ____ )
#  | (    \/| (   ) || () () || (    \/  | (      | (   ) || (   ) || (    )|
#  | |      | (___) || || || || (__      | |      | |   | || |   | || (____)|
#  | | ____ |  ___  || |(_)| ||  __)     | |      | |   | || |   | ||  _____)
#  | | \_  )| (   ) || |   | || (        | |      | |   | || |   | || (
#  | (___) || )   ( || )   ( || (____/\  | (____/\| (___) || (___) || )
#  (_______)|/     \||/     \|(_______/  (_______/(_______)(_______)|/
#
########################################################################

def game_main_loop():
    #main game loop
    game_quit = False

    player_action = "no-action"



    while not game_quit:
        #player action definition

        #handle player input
        player_action = game_handle_keys()

        map_calculate_fov()

        if player_action == "QUIT":
            game_quit = True

        if player_action != "no-action":
            for obj in GAME_OBJECTS:
                if obj.ai:
                    obj.ai.take_turn()



        #draw the game
        draw_game()

    #quit the game
    pygame.quit()
    sys.exit()

# _______  _______  _______  _______   _________ _       __________________
#(  ____ \(  ___  )(       )(  ____ \  \__   __/( (    /|\__   __/\__   __/
#| (    \/| (   ) || () () || (    \/     ) (   |  \  ( |   ) (      ) (
#| |      | (___) || || || || (__         | |   |   \ | |   | |      | |
#| | ____ |  ___  || |(_)| ||  __)        | |   | (\ \) |   | |      | |
#| | \_  )| (   ) || |   | || (           | |   | | \   |   | |      | |
#| (___) || )   ( || )   ( || (____/\  ___) (___| )  \  |___) (___   | |
#(_______)|/     \||/     \|(_______/  \_______/|/    )_)\_______/   )_(
#

def game_initialize():
    global SURFACE_MAIN, GAME_MAP, PLAYER, ENEMY, GAME_OBJECTS, FOV_CALCULATE
    #initalizes the main window in pygame
    pygame.init()

    #SURFACE_MAIN = pygame.display.set_mode((constants.GAME_WIDTH,constants.GAME_HEIGHT))
    SURFACE_MAIN = pygame.display.set_mode((constants.MAP_WIDTH*constants.CELL_WIDTH, constants.MAP_HEIGHT*constants.CELL_HEIGHT))

    pygame.display.set_caption('Test Game!')

    GAME_MAP = map_create()

    FOV_CALCULATE = True

    creature_com1 = com_Creature("greg")
    PLAYER = obj_Actor(1, 1, "python", constants.S_PLAYER ,creature = creature_com1)

    ai_com = ai_Test()
    creature_com2 = com_Creature("jackie", death_function = death_monster       )
    ENEMY  = obj_Actor(15, 15, "crab", constants.S_ENEMY, creature = creature_com2, ai = ai_com)

    #ai_com2 = ai_Test()
    #creature_com3 = com_Creature("jackie2", death_function = death_monster       )
    #ENEMY2  = obj_Actor(5, 10, "crab", constants.S_ENEMY, creature = creature_com3, ai = ai_com2)

    GAME_OBJECTS = [PLAYER, ENEMY]

def game_handle_keys():
    global FOV_CALCULATE

    #get player input
    events_list = pygame.event.get()

    #process input
    for event in events_list:
        if event.type == pygame.QUIT:
            return "QUIT"
            #game_quit = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                PLAYER.creature.move(0,-1)
                FOV_CALCULATE = True
                return "player_moved"

            if event.key == pygame.K_DOWN:
                PLAYER.creature.move(0,1)
                FOV_CALCULATE = True
                return "player_moved"

            if event.key == pygame.K_LEFT:
                PLAYER.creature.move(-1,0)
                FOV_CALCULATE = True
                return "player_moved"

            if event.key == pygame.K_RIGHT:
                PLAYER.creature.move(1,0)
                FOV_CALCULATE = True
                return "player_moved"
    return "no-action"

# _______  _______ _________ _          _        _______  _______  _______
#(       )(  ___  )\__   __/( (    /|  ( \      (  ___  )(  ___  )(  ____ )
#| () () || (   ) |   ) (   |  \  ( |  | (      | (   ) || (   ) || (    )|
#| || || || (___) |   | |   |   \ | |  | |      | |   | || |   | || (____)|
#| |(_)| ||  ___  |   | |   | (\ \) |  | |      | |   | || |   | ||  _____)
#| |   | || (   ) |   | |   | | \   |  | |      | |   | || |   | || (
#| )   ( || )   ( |___) (___| )  \  |  | (____/\| (___) || (___) || )
#|/     \||/     \|\_______/|/    )_)  (_______/(_______)(_______)|/

if __name__ == '__main__':
    game_initialize()
    game_main_loop()
