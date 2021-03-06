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

class struc_Assets:
    def __init__(self):
        #sprties
        self.charspritesheet  = obj_Spritesheet("data/reptiles.png")
        self.enemyspritesheet = obj_Spritesheet("data/enemys.png")

        self.A_PLAYER = self.charspritesheet.get_animation ('o',5 ,16 ,16 ,2 , (32, 32))
        self.A_ENEMY  = self.enemyspritesheet.get_animation('k',1 ,16 ,16 ,2 ,(32, 32))

        self.S_WALL              = pygame.image.load("data/wall.jpg")
        self.S_WALLEXPLORED      = pygame.image.load("data/wallunseen.png")

        self.S_FLOOR             = pygame.image.load("data/floor.jpg")
        self.S_FLOOREXPLORED     = pygame.image.load("data/floorunseen.png")

        #FONTS
        self.FONT_DEBUG_MESSAGE  = pygame.font.Font("data/joystix.ttf", 16)
        self.FONT_MESSAGE_TEXT   = pygame.font.Font("data/joystix.ttf", 12)



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
    def __init__(self, x, y, name_object, animation, animation_speed = .5, creature = None, ai = None, container = None):
        self.x = x
        self.y = y
        self.animation = animation #list of images
        self.animation_speed = animation_speed / 1.0 # in seconds

        #animation flicker speed
        self.flicker_speed = self.animation_speed / len(self.animation)
        self.flicker_timer = 0.0
        self.sprite_image = 0

        self.creature = creature
        if self.creature:
            self.creature.owner = self

        self.ai = ai
        if self.ai:
            self.ai.owner = self

        self.container = container
        if self.container:
            self.container.owner = self



    def draw(self):
        is_visible = libtcod.map_is_in_fov(FOV_MAP, self.x, self.y)

        if is_visible:
            if len(self.animation) == 1:
                SURFACE_MAIN.blit(self.animation[0], (self.x*constants.CELL_WIDTH, self.y*constants.CELL_HEIGHT))

            elif len(self.animation) > 1:

                if CLOCK.get_fps() > 0.0:
                    self.flicker_timer += 1 / CLOCK.get_fps()

                if self.flicker_timer >= self.flicker_speed:
                    self.flicker_timer = 0.0

                    if self.sprite_image >= len(self.animation) -1:
                        self.sprite_image = 0

                    else:
                        self.sprite_image += 1

                SURFACE_MAIN.blit(self.animation[self.sprite_image], (self.x*constants.CELL_WIDTH, self.y*constants.CELL_HEIGHT))

class obj_Game:
    def __init__(self):

        self.current_map = map_create()
        self.current_objects = []

        self.message_history = []

class obj_Spritesheet:
    #used to grab images out of a sprite sheet

    def __init__(self, file_name):
        #load the sprite sheet
        self.sprite_sheet = pygame.image.load(file_name).convert()
        self.tiledict = {'a': 1, 'b' : 2, 'c' : 3, 'd' : 4, 'e' : 5, 'f' : 6,
                        "g" : 7, "h" : 8, "i" : 9, "j" : 10, "k" : 11, "l" : 12,
                        "m" : 13, "n" : 14, "o" : 15, "p" : 16}

    def get_image(self, column, row, width = constants.CELL_WIDTH, height = constants.CELL_HEIGHT,
                    scale = None):
        ### scale is s tuple

        image_list = []

        image = pygame.Surface([width, height]).convert()

        image.blit(self.sprite_sheet, (0, 0), (self.tiledict[column]*width, row * height, width, height))

        image.set_colorkey(constants.COLOR_BLACK)

        if scale:
            (new_w, new_h) = scale
            image = pygame.transform.scale(image, (new_w, new_h))

        image_list.append(image)

        return image_list


    def get_animation(self, column, row, width = constants.CELL_WIDTH, height = constants.CELL_HEIGHT, num_sprites = 1 , scale = None):
        ### scale is s tuple

        image_list = []

        for i in range(num_sprites):
            #create blank image
            image = pygame.Surface([width, height]).convert()


            #copy image from sheet onto blank
            image.blit(self.sprite_sheet, (0, 0), (self.tiledict[column] * width + (width*i), row * height, width, height))

            #set tranparency to black
            image.set_colorkey(constants.COLOR_BLACK)


            if scale:
                (new_w, new_h) = scale
                image = pygame.transform.scale(image, (new_w, new_h))

            image_list.append(image)

        return image_list

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

        tile_is_wall = (GAME.current_map[self.owner.x + dx][self.owner.y + dy].block_path == True)

        target = map_check_for_creatures(self.owner.x + dx, self.owner.y + dy, self.owner)
        #
        if target:
            self.attack(target, 3)


        if not tile_is_wall and target is None:
            self.owner.x += dx
            self.owner.y += dy

    def attack(self, target, damage):
        #print (self.name_instance + " attacks " + target.creature.name_instance + " for " + str(damage) + " damage!")
        game_message(self.name_instance + " attacks " + target.creature.name_instance + " for " + str(damage) + " damage!", constants.COLOR_WHITE)
        target.creature.take_damage(damage)

    def take_damage(self, damage):
        self.hp -= damage
        #print (self.name_instance + "'s health is " + str(self.hp) + "/" + str(self.maxhp))
        game_message(self.name_instance + "'s health is " + str(self.hp) + "/" + str(self.maxhp), constants.COLOR_RED)


        if self.hp <= 0:
            if self.death_function is not None:
                self.death_function(self.owner)

#.current_maps com_Item:


class com_Container:
    def __init__(self, volume = 10.0, inventory = []):
        self.inventory = inventory
        self.base_volume = volume

    # get_names_inventory()

    #get_volume_container()

    #get_current_weight()

class com_Item:
    def __init__(self, weight = 0.0, volume = 0.0):
        self.weight = weight
        self.volume = volume


    ## pick_up_Item()
    def pick_up(self, actor):

        if actor.container:
            pass





    ## drop_Item()

    ## use_Item()





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
    #print (monster.creature.name_instance + " is dead!")
    game_message(monster.creature.name_instance + " is dead!", constants.COLOR_GREY)
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
        for object in GAME.current_objects:
            if (object is not exclude_object and
                object.x == x and
                object.y == y and
                object.creature):

                target = object


            if target:
                return target

    else:
        #check to find creature at that location
        for object in GAME.current_objects:
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
    draw_map(GAME.current_map)
    #draw the character
    #SURFACE_MAIN.blit(constants.S_PLAYER,(200,200))
    #ENEMY.draw()
    #PLAYER.draw()
    #Draw all objects
    for obj in GAME.current_objects:
        obj.draw()

    draw_debug()

    draw_messages()

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
                    SURFACE_MAIN.blit(ASSETS.S_WALL, (x*constants.CELL_WIDTH, y*constants.CELL_HEIGHT))
                else:
                    #draw floor
                    SURFACE_MAIN.blit(ASSETS.S_FLOOR, (x*constants.CELL_WIDTH, y*constants.CELL_HEIGHT))

            elif map_to_draw[x][y].explored:
                if map_to_draw[x][y].block_path == True:
                    #draw a wall
                    SURFACE_MAIN.blit(ASSETS.S_WALLEXPLORED, (x*constants.CELL_WIDTH, y*constants.CELL_HEIGHT))
                else:
                    #draw floor
                    SURFACE_MAIN.blit(ASSETS.S_FLOOREXPLORED, (x*constants.CELL_WIDTH, y*constants.CELL_HEIGHT))

def draw_debug():

    draw_text(SURFACE_MAIN, "fps: "+ str(int(CLOCK.get_fps())), (0,0), constants.COLOR_WHITE, constants.COLOR_BLACK)

def draw_messages():

    if len(GAME.message_history) <= constants.NUM_MESSAGES:
        to_draw = GAME.message_history#(constants.NUM_MESSAGES)
    else:
        to_draw = GAME.message_history[-constants.NUM_MESSAGES:]


    text_height = helper_text_height(ASSETS.FONT_MESSAGE_TEXT)

    start_y = (constants.MAP_HEIGHT * constants.CELL_HEIGHT - (constants.NUM_MESSAGES * text_height)) -5

    i = 0

    for message,color in to_draw:

        draw_text(SURFACE_MAIN, message, (0, start_y + (i * text_height)), color, constants.COLOR_BLACK)

        i += 1

def draw_text(display_surface, text_to_display, T_coords, text_color, back_color = None):
    #T stands for touple, this function takes in text and displayes it on display_surface
    text_surf, text_rect = helper_text_objects(text_to_display, text_color, back_color)

    text_rect.topleft = T_coords

    display_surface.blit(text_surf, text_rect)


# __    __   _______  __      .______    _______ .______
#|  |  |  | |   ____||  |     |   _  \  |   ____||   _  \
#|  |__|  | |  |__   |  |     |  |_)  | |  |__   |  |_)  |
#|   __   | |   __|  |  |     |   ___/  |   __|  |      /
#|  |  |  | |  |____ |  `----.|  |      |  |____ |  |\  \----.
#|__|  |__| |_______||_______|| _|      |_______|| _| `._____|
#

def helper_text_objects(incoming_text, incoming_color, incoming_bg):

    if incoming_bg:
        Text_surface = ASSETS.FONT_DEBUG_MESSAGE.render(incoming_text, False, incoming_color, incoming_bg)
    else:
        Text_surface = ASSETS.FONT_DEBUG_MESSAGE.render(incoming_text, False, incoming_color)

    return Text_surface, Text_surface.get_rect()


def helper_text_height(font):

    font_object = font.render('a', False ,(0 ,0, 0))
    font_rect = font_object.get_rect()

    return font_rect.height



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
            for obj in GAME.current_objects:
                if obj.ai:
                    obj.ai.take_turn()



        #draw the game
        draw_game()

        CLOCK.tick(constants.GAME_FPS)#

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
    global SURFACE_MAIN, GAME, CLOCK, FOV_CALCULATE, PLAYER, ENEMY, ASSETS
    #initalizes the main window in pygame
    pygame.init()

    #SURFACE_MAIN = pygame.display.set_mode((constants.GAME_WIDTH,constants.GAME_HEIGHT))
    SURFACE_MAIN = pygame.display.set_mode((constants.MAP_WIDTH*constants.CELL_WIDTH, constants.MAP_HEIGHT*constants.CELL_HEIGHT))

    GAME = obj_Game()

    CLOCK = pygame.time.Clock()

    pygame.display.set_caption('Test Game!')

    #GAME.current_map = map_create()

    #GAME.message_history = []

    #test messages
    #game_message("test message", constants.COLOR_WHITE)
    #game_message("test message2", constants.COLOR_RED)
    #game_message("test message3", constants.COLOR_GREY)
    #game_message("test message4", constants.COLOR_WHITE)

    FOV_CALCULATE = True

    ASSETS = struc_Assets()



    creature_com1 = com_Creature("greg")
    PLAYER = obj_Actor(1, 1, "python", ASSETS.A_PLAYER ,animation_speed = 1.0, creature = creature_com1)


    creature_com2 = com_Creature("jackie", death_function = death_monster)
    ai_com = ai_Test()
    ENEMY  = obj_Actor(15, 15, "crab", ASSETS.A_ENEMY, animation_speed = 1.0, creature = creature_com2, ai = ai_com)

    #ai_com2 = ai_Test()
    #creature_com3 = com_Creature("jackie2", death_function = death_monster       )
    #ENEMY2  = obj_Actor(5, 10, "crab", constants.S_ENEMY, creature = creature_com3, ai = ai_com2)

    GAME.current_objects = [PLAYER, ENEMY]

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

def game_message(game_msg, msg_color):#T means tuple

    GAME.message_history.append((game_msg, msg_color))




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
