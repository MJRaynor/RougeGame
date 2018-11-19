import pygame,sys
import libtcodpy as libtcod
import math

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
        self.enemyspritesheet = obj_Spritesheet("data/enemies.png")

        self.A_PLAYER = self.charspritesheet.get_animation ('o',5 ,16 ,16 ,2 , (32, 32))
        self.A_ENEMY  = self.enemyspritesheet.get_animation('k',1 ,16 ,16 ,2 ,(32, 32))

        self.S_WALL              = pygame.image.load("data/wall.jpg")
        self.S_WALLEXPLORED      = pygame.image.load("data/wallunseen.png")

        self.S_FLOOR             = pygame.image.load("data/floor.jpg")
        self.S_FLOOREXPLORED     = pygame.image.load("data/floorunseen.png")

        #items
        self.S_SWORD             = [pygame.transform.scale(pygame.image.load("data/sword.png"),
                                    (constants.CELL_WIDTH,constants.CELL_HEIGHT))]



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
    def __init__(self, x, y, name_object, animation, animation_speed = .5, creature = None, ai = None,
                 container = None, item = None, equipment = None):
        self.x = x
        self.y = y
        self.name_object = name_object
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

        self.item = item
        if self.item:
            self.item.owner = self

        self.equipment = equipment
        if self.equipment:
            self.equipment.owner = self

            self.item = com_Item()
            self.item.owner = self

    @property
    def display_name(self):

        if self.creature:
            return (self.creature.name_instance + " the " + self.name_object)

        if self.item:
            if self.equipment and self.equipment.equipped:
                return (self.name_object + " (equipped)")
            else:
                return self.name_object





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

    def distance_to(self, other):
        dx = other.x - self.x
        dy = other.y - self.y

        return math.sqrt(dx ** 2 + dy** 2)

    def move_towards(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        distance = math.sqrt(dx ** 2 + dy** 2)

        dx = int(round(dx/distance))
        dy  = int(round(dy/distance))

        self.creature.move(dx, dy)

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
        ### scale is a tuple

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
    def __init__(self, name_instance, max_hp=10, death_function = None):

        self.name_instance = name_instance
        self.max_hp = max_hp
        self.death_function = death_function
        self.current_hp = max_hp

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
        self.current_hp -= damage
        #print (self.name_instance + "'s health is " + str(self.hp) + "/" + str(self.maxhp))
        game_message(self.name_instance + "'s health is " + str(self.current_hp) + "/" + str(self.max_hp), constants.COLOR_RED)

        if self.current_hp <= 0:
            if self.death_function is not None:
                self.death_function(self.owner)

    def heal(self, value):
        self.current_hp += value

        if self.current_hp > self.max_hp:
            self.current_hp = self.max_hp

class com_Container:
    def __init__(self, volume = 10.0, inventory = []):
        self.inventory = inventory
        self.max_volume = volume

    # get_names_inventory()

    #get_volume_container()
    @property
    def volume(self):
        return 0.0
    #get_current_weight()

class com_Item:
    def __init__(self, weight = 0.0, volume = 0.0, use_function = None, value = None):

        self.weight = weight
        self.volume = volume
        self.value = value
        self.use_function = use_function

    ## pick_up_Item()
    def pick_up(self, actor):

        if actor.container:
            if actor.container.volume + self.volume > actor.container.max_volume:
                game_message("Not enough room to pick up")

            else:
                game_message("Pickin up")
                actor.container.inventory.append(self.owner)
                GAME.current_objects.remove(self.owner)
                self.current_container = actor.container

    ## drop_Item()
    def drop(self, new_x, new_y):
        GAME.current_objects.append(self.owner)
        self.current_container.inventory.remove(self.owner)
        self.owner.x = new_x
        self.owner.y = new_y
        game_message("Item Dropped")

    ## use_Item
    def use(self):

        if self.owner.equipment:
            self.owner.equipment.toggle_equip()
            return
        #use the item by producint and effect and removing it
        if self.use_function:
            result = self.use_function(self.current_container.owner, self.value)

        if result is not None:
            print("use_function failed")
        else:
            self.current_container.inventory.remove(self.owner)

class com_Equipment:

    def __init__ (self, attack_bonus = None , defense_bonus = None , slot = None):

        self.attack_bonus = attack_bonus
        self.defense_bonus = defense_bonus
        self.slot = slot

        self.equipped = False

    def toggle_equip(self):

        if self.equipped:
            self.unequip()
        else:
            self.equip()

    def equip(self):
        #equip item
        self.equipped = True

        game_message("Item is equipped")

    def unequip(self):

        self.equipped = False

        game_message("Item is Unequipped")






#        ___       __
#       /   \     |  |
#      /  ^  \    |  |
#     /  /_\  \   |  |
#    /  _____  \  |  |
#   /__/     \__\ |__|
#

class ai_Confuse:
    #once per turn, execute

    def __init__(self, old_ai, num_turns):
        self.old_ai = old_ai
        self.num_turns = num_turns

    def take_turn(self):

        if self.num_turns > 0:
            self.owner.creature.move(libtcod.random_get_int(0,-1, 1,),libtcod.random_get_int(0,-1, 1,))
            self.num_turns -= 1

        else:
            self.owner.ai = self.old_ai
            game_message("The creature is back to normal!", constants.COLOR_GREEN)

class ai_Chase:
    #basic monster AI which tries to harm player

    def take_turn(self):

        monster = self.owner

        if libtcod.map_is_in_fov(FOV_MAP, monster.y, monster.y):
            #move towards play if far away
            if monster.distance_to(PLAYER) >= 2:
                #move towards player
                self.owner.move_towards(PLAYER)

            #if close enough, attack player
            elif PLAYER.creature.current_hp > 0:
                monster.creature.attack(PLAYER, 3)

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

def map_check_for_wall(x, y):
    incoming_map[x][y].block_path

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

def map_objects_at_coords(coords_x, coords_y):

    object_options = [obj for obj in GAME.current_objects
                        if obj.x ==coords_x and obj.y == coords_y]
    return object_options

def map_find_line(coords1, coords2):
    #converts two x,y coords into a list of tiles
    #coords1 = (x1, y1)     coords2 = (x2,y2)

    x1, y1 = coords1
    x2, y2 = coords2

    libtcod.line_init(x1, y1 , x2 , y2)

    calc_x, calc_y = libtcod.line_step()
    coord_list = []

    if x1 == x2 and y1 == y2:
        return [(x1,y1)]

    while (not calc_x is None):
        coord_list.append((calc_x, calc_y))

        calc_x, calc_y = libtcod.line_step()

    return coord_list

def map_find_raduis(coords, radius):
    center_x, center_y = coords

    tile_list = []
    start_x = (center_x - radius)
    end_x   = (center_x + radius + 1)
    start_y = (center_y - radius)
    end_y   = (center_y + radius + 1)

    for x in range(start_x, end_x):
        for y in range(start_y, end_y):
            tile_list.append((x,y))

    return tile_list



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
    for obj in GAME.current_objects:
        obj.draw()

    draw_debug()

    draw_messages()

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

    draw_text(SURFACE_MAIN, "fps: "+ str(int(CLOCK.get_fps())), constants.FONT_DEBUG_MESSAGE,(0,0), constants.COLOR_WHITE, constants.COLOR_BLACK)

def draw_messages():

    if len(GAME.message_history) <= constants.NUM_MESSAGES:
        to_draw = GAME.message_history#(constants.NUM_MESSAGES)
    else:
        to_draw = GAME.message_history[-constants.NUM_MESSAGES:]

    text_height = helper_text_height(constants.FONT_MESSAGE_TEXT)

    start_y = (constants.MAP_HEIGHT * constants.CELL_HEIGHT - (constants.NUM_MESSAGES * text_height)) -5

    for i, (message,color) in enumerate(to_draw):

        draw_text(SURFACE_MAIN, message, constants.FONT_MESSAGE_TEXT,
            (0, start_y + (i * text_height)), color, constants.COLOR_BLACK)

def draw_text(display_surface, text_to_display, font, coords, text_color, back_color = None, center = False):
    #T stands for touple, this function takes in text and displayes it on display_surface
    text_surf, text_rect = helper_text_objects(text_to_display, font, text_color, back_color)

    if not center:
        text_rect.topleft = coords
    else:
        text_rect.center = coords

    display_surface.blit(text_surf, text_rect)

def draw_tile_rect(coords, tile_color = None, tile_alpha = None, mark = None):

    x, y = coords

    if tile_color:  local_color = tile_color
    else:   local_color = constants.COLOR_WHITE

    if tile_alpha:  local_alpha = tile_alpha
    else:   local_alpha = 200

    new_x = x * constants.CELL_WIDTH
    new_y = y * constants.CELL_HEIGHT
    new_surface = pygame.Surface((constants.CELL_WIDTH, constants.CELL_HEIGHT))
    new_surface.fill(local_color)
    new_surface.set_alpha(local_alpha)

    if mark:
        draw_text(new_surface, mark, font = constants.FONT_CURSOR_TEXT,
                  coords = (constants.CELL_WIDTH/2, constants.CELL_HEIGHT/2),
                  text_color = constants.COLOR_BLACK, center = True)


    SURFACE_MAIN.blit(new_surface, (new_x, new_y))



# __    __   _______  __      .______    _______ .______
#|  |  |  | |   ____||  |     |   _  \  |   ____||   _  \
#|  |__|  | |  |__   |  |     |  |_)  | |  |__   |  |_)  |
#|   __   | |   __|  |  |     |   ___/  |   __|  |      /
#|  |  |  | |  |____ |  `----.|  |      |  |____ |  |\  \----.
#|__|  |__| |_______||_______|| _|      |_______|| _| `._____|
#

def helper_text_objects(incoming_text, incoming_font, incoming_color, incoming_bg):

    if incoming_bg:
        Text_surface = incoming_font.render(incoming_text, False, incoming_color, incoming_bg)
    else:
        Text_surface = incoming_font.render(incoming_text, False, incoming_color)

    return Text_surface, Text_surface.get_rect()

def helper_text_height(font):

    font_object = font.render('a', False ,(0 ,0, 0))
    font_rect = font_object.get_rect()

    return font_rect.height

def helper_text_width(font):

    font_object = font.render('a', False ,(0 ,0, 0))
    font_rect = font_object.get_rect()

    return font_rect.width


#                       _
# _ __ ___   __ _  __ _(_) ___
#| '_ ` _ \ / _` |/ _` | |/ __|
#| | | | | | (_| | (_| | | (__
#|_| |_| |_|\__,_|\__, |_|\___|
#                 |___/

def cast_heal(target, value):
    if target.creature.current_hp == target.creature.max_hp:
        game_message(target.creature.name_instance + " the " + target.name_object + " is already at full health!")
        return "canceled"

    else:
        game_message(target.creature.name_instance + " the " + target.name_object + " healed for " + str(value) + " health!")
        target.creature.heal(value)
        game_message(target.creature.name_instance + "'s health is " + str(target.creature.current_hp) + "/" + str(target.creature.max_hp), constants.COLOR_RED)
        #print(target.creature.current_hp)

    return None

def cast_lightning():

    damage = 10

    player_location = (PLAYER.x, PLAYER.y)
    #get tile from player
    point_selected = menu_tile_selection(coords_origin = player_location, max_range = 5, penetrate_walls = False)

    if point_selected:
    #convert tile into list of tiles between A -> B
        list_of_tiles = map_find_line(player_location, point_selected)

        #cylye through list and damage eveything in list
        for i, (x, y) in enumerate (list_of_tiles):
            target = map_check_for_creatures(x,y)

            if target:
                target.creature.take_damage(damage)

def cast_fireball():
    damage    = 5
    local_radius    = 1
    max_r = 4
    player_location = (PLAYER.x, PLAYER.y)

    #get target tile
    point_selected = menu_tile_selection(coords_origin = player_location,
                                         max_range = max_r,
                                         penetrate_walls = False,
                                         pierce_creature = False,
                                         radius = local_radius)
    if point_selected:
        #get sequence of tiles
        tiles_to_damage = map_find_raduis(point_selected, local_radius)

        creature_hit = False

        #damages all creatures in tiles
        for (x,y) in tiles_to_damage:
            creature_to_damage = map_check_for_creatures(x,y)

            if creature_to_damage:
                creature_to_damage.creature.take_damage(damage)

                if creature_to_damage is not PLAYER:
                    creature_hit = True

        if creature_hit:
            game_message("The monster howls out in pain!", constants.COLOR_RED)

def cast_confusion():

    #select tile
    point_selected = menu_tile_selection()

    #get target from tile
    if point_selected:
        tile_x, tile_y = point_selected
        target = map_check_for_creatures(tile_x, tile_y)
        #temp confuse target
        if target:
            oldai = target.ai

            target.ai = ai_Confuse(old_ai = oldai, num_turns = 5)
            target.ai.owner = target

            game_message("The creature is confused!", constants.COLOR_GREEN)



# _______  _______  _
#(       )(  ____ \( (    /||\     /|
#| () () || (    \/|  \  ( || )   ( |
#| || || || (__    |   \ | || |   | |
#| |(_)| ||  __)   | (\ \) || |   | |
#| |   | || (      | | \   || |   | |
#| )   ( || (____/\| )  \  || (___) |
#|/     \|(_______/|/    )_)(_______)
#

def menu_pause():

    window_width  = constants.MAP_WIDTH * constants.CELL_WIDTH
    window_height = constants.MAP_HEIGHT* constants.CELL_HEIGHT

    menu_text = "PAUSED"

    menu_font = constants.FONT_DEBUG_MESSAGE

    text_height = helper_text_height(menu_font)
    text_width  = len(menu_text) * helper_text_width(menu_font)

    #menu pauses game and displays message
    menu_close = False

    while not menu_close:

        events_list = pygame.event.get()

        for event in events_list:

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_p:
                    menu_close = True

        draw_text(SURFACE_MAIN, menu_text, constants.FONT_DEBUG_MESSAGE,
                 ((window_width/2)-(text_width/2), (window_height/2)-(text_height/2)), constants.COLOR_WHITE, constants.COLOR_BLACK)

        CLOCK.tick(constants.GAME_FPS)

        pygame.display.flip()

def menu_inventory():

    menu_close = False

    window_width  = constants.MAP_WIDTH * constants.CELL_WIDTH
    window_height = constants.MAP_HEIGHT* constants.CELL_HEIGHT

    menu_width  = 200
    menu_height = 200
    menu_x      = ((window_width/2)-(menu_width/2))
    menu_y      = ((window_height/2)-(menu_height/2))

    menu_text_font = constants.FONT_MESSAGE_TEXT
    menu_text_height = helper_text_height(menu_text_font)
    menu_text_color = constants.COLOR_WHITE


    local_inventory_surface = pygame.Surface((menu_width, menu_height))

    while not menu_close:

        #clear menu
        local_inventory_surface.fill(constants.COLOR_BLACK)

        #register changes
        print_list = [obj.display_name for obj in PLAYER.container.inventory]
        events_list = pygame.event.get()

        mouse_x, mouse_y = pygame.mouse.get_pos()
        #print((mouse_x, mouse_y))
        mouse_x_rel = mouse_x - menu_x
        mouse_y_rel = mouse_y - menu_y

        mouse_in_window = (mouse_x_rel > 0 and
                            mouse_y_rel > 0 and
                            mouse_x_rel < menu_width and
                            mouse_y_rel < menu_height)

        mouse_line_selection = int(mouse_y_rel / menu_text_height)
        for event in events_list:

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_i:
                    menu_close = True

            if event.type == pygame.MOUSEBUTTONDOWN:

                if event.button == 1:

                    if (mouse_in_window and
                        mouse_line_selection <= len(print_list)-1):

                        PLAYER.container.inventory[mouse_line_selection].item.use()
        #draw list
        for line, (name) in enumerate(print_list):
            if line == (mouse_line_selection) and mouse_in_window:
                draw_text(local_inventory_surface, name, menu_text_font,
                          (0, 0 + (line * menu_text_height)), menu_text_color, constants.COLOR_GREY)
            else:
                draw_text(local_inventory_surface, name, menu_text_font,
                         (0, 0 + (line * menu_text_height)), menu_text_color)

        #render game
        draw_game()
        #draw menu
        SURFACE_MAIN.blit(local_inventory_surface, (menu_x, menu_y))

        CLOCK.tick(constants.GAME_FPS)
        pygame.display.flip()

def menu_tile_selection(coords_origin = None, max_range = None, radius = None, penetrate_walls = True, pierce_creature = True):

    menu_close = False

    while not menu_close:

        #get mouse pos
        mouse_x, mouse_y = pygame.mouse.get_pos()
        #get button press
        events_list = pygame.event.get()
        #mouse map selection
        map_coord_x = int(mouse_x/constants.CELL_WIDTH)
        map_coord_y = int(mouse_y/constants.CELL_HEIGHT)
        valid_tiles = []
        if coords_origin:
            full_list_tiles = map_find_line(coords_origin, (map_coord_x,map_coord_y))

            for i, (x, y) in enumerate(full_list_tiles):
                valid_tiles.append((x,y))

                #stop at max range
                if max_range and i == max_range - 1:
                    break

                #stop at wall
                if not penetrate_walls and GAME.current_map[x][y].block_path:
                        break

                #stop at creature
                if not pierce_creature and map_check_for_creatures(x,y):
                    break


        else:
            valid_tiles=[(map_coord_x, map_coord_y)]

        #return map_coords when left mouse click
        for event in events_list:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_l:
                    menu_close = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    #returns coord selected
                    return (valid_tiles[-1])

        #draw game
        draw_game()

        #draw rectangle at mouse pos on top of game
        for (tile_x, tile_y) in valid_tiles:
            if (tile_x, tile_y) == valid_tiles[-1]:
                draw_tile_rect(coords = (tile_x, tile_y), mark = "X")
            else:
                draw_tile_rect(coords = (tile_x, tile_y))

        if radius:
            area_effect = map_find_raduis(valid_tiles[-1], radius)
            for(tile_x, tile_y) in area_effect:
                draw_tile_rect(coords = (tile_x, tile_y),
                               tile_color = constants.COLOR_RED,
                               tile_alpha = 150)

        pygame.display.flip()

        CLOCK.tick(constants.GAME_FPS)


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

        pygame.display.flip()

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

    pygame.key.set_repeat(200,70)#set key repeat
    #SURFACE_MAIN = pygame.display.set_mode((constants.GAME_WIDTH,constants.GAME_HEIGHT))
    SURFACE_MAIN = pygame.display.set_mode((constants.MAP_WIDTH*constants.CELL_WIDTH, constants.MAP_HEIGHT*constants.CELL_HEIGHT))

    GAME = obj_Game()

    CLOCK = pygame.time.Clock()

    pygame.display.set_caption('Test Game!')

    FOV_CALCULATE = True

    ASSETS = struc_Assets()

    container_com1 = com_Container()
    creature_com1 = com_Creature("Hero Greg")
    PLAYER = obj_Actor(1, 1, "python", ASSETS.A_PLAYER ,animation_speed = 1.0, creature = creature_com1, container = container_com1)

    item_com1 = com_Item(value = 4, use_function = cast_heal)
    creature_com2 = com_Creature("jackie", death_function = death_monster)
    ai_com1 = ai_Chase()
    ENEMY  = obj_Actor(5, 5, "smart crab", ASSETS.A_ENEMY, animation_speed = 1.0,
                    creature = creature_com2, ai = ai_com1, item = item_com1)

    item_com2 = com_Item(value = 5, use_function = cast_heal)
    ai_com2 = ai_Chase()
    creature_com3 = com_Creature("bob", death_function = death_monster)
    ENEMY2  = obj_Actor(14, 15, "dumb crab", ASSETS.A_ENEMY, animation_speed = 1.0,
                     creature = creature_com3, ai = ai_com2, item = item_com2)

    #create a sword
    equipment_com1 = com_Equipment()
    SWORD = obj_Actor(2, 2, "Short Sword", ASSETS.S_SWORD,
                     equipment = equipment_com1)


    GAME.current_objects = [PLAYER, ENEMY, ENEMY2, SWORD]

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

            if event.key == pygame.K_g:
                objects_at_player = map_objects_at_coords(PLAYER.x, PLAYER.y)

                for obj in objects_at_player:
                    if obj.item:
                        obj.item.pick_up(PLAYER)

            if event.key == pygame.K_d:
                if len(PLAYER.container.inventory) > 0:
                    PLAYER.container.inventory[-1].item.drop(PLAYER.x, PLAYER.y)

            if event.key == pygame.K_p:
                menu_pause()

            if event.key == pygame.K_i:
                menu_inventory()

            if event.key == pygame.K_l:
                cast_confusion()

    return "no-action"

def game_message(game_msg, msg_color = constants.COLOR_GREY):#T means tuple

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
