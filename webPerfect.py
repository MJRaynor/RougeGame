# 3rd party modules
import libtcodpy as libtcod
import pygame

# game files
import constants



#  ____  _                   _
# / ___|| |_ _ __ _   _  ___| |_
# \___ \| __| '__| | | |/ __| __|
#  ___) | |_| |  | |_| | (__| |_
# |____/ \__|_|   \__,_|\___|\__|


class struc_Tile:

    '''This class functions as a struct that tracks the data for each tile
    within a map.

    Attributes:
        block_path (arg, bool) : True if tile prevents actors from moving
            through it under normal circumstances.
        explored (bool): Initializes to FALSE, set to true if player
            has seen it before.

    '''

    def __init__(self, block_path):
        self.block_path = block_path
        self.explored = False

class struc_Assets:

    '''This class is a struct that holds all the assets used in the game. This
    includes sprites, sound effects, and music.

    '''

    def __init__(self):
        ## SPRITESHEETS ##
        self.charspritesheet = obj_Spritesheet("data/reptiles.png")
        self.enemyspritesheet = obj_Spritesheet("data/enemies.png")

        ## ANIMATIONS ##
        self.A_PLAYER = self.charspritesheet.get_animation('o', 5, 16, 16, 2, (32, 32))
        self.A_ENEMY = self.enemyspritesheet.get_animation('k', 1, 16, 16, 2, (32, 32))

        ## SPRITES ##
        self.S_WALL = pygame.image.load("data/wall.jpg")
        self.S_WALLEXPLORED = pygame.image.load("data/wallunseen2.png")

        self.S_FLOOR = pygame.image.load("data/floor.jpg")
        self.S_FLOOREXPLORED = pygame.image.load("data/floorunseen2.png")






#    ___  _     _           __
#   / _ \| |__ (_) ___  ___| |_ ___
#  | | | | '_ \| |/ _ \/ __| __/ __|
#  | |_| | |_) | |  __/ (__| |_\__ \
#  \___/|_.__// |\___|\___|\__|___/
#           |__/

class obj_Actor:

    '''The actor object represents every entity in the game.

    This object is anything that can appear or act within the game.  Each entity
    is made up of components that control how these objects work.

    Attributes:
        x (arg, int): position on the x axis
        y (arg, int): position on the y axis
        name_object (arg, str) : name of the object type, "chair" or
            "goblin" for example.
        animation (arg, list): sequence of images that make up the object's
            spritesheet. Created within the struc_Assets class.
        animation_speed (arg, float): time in seconds it takes to loop through
            the object animation.

    Components:
        creature: any object that has health, and generally can fight.
        ai: set of instructions an obj_Actor can follow.
        container: objects that can hold an inventory.
        item: items are items that are able to be picked up and (usually)
            usable.

    '''

    def __init__(self, x, y,
                 name_object,
                 animation,
                 animation_speed = .5,

                 # Components
                 creature = None,
                 ai = None,
                 container = None,
                 item = None):

        self.x, self.y = x, y
        self.name_object = name_object
        self.animation = animation
        # divide by 1.0 to convert ints to floats
        self.animation_speed = animation_speed / 1.0

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

        ## PRIVATE ##
        # speed -> frames conversion
        self._flickerspeed = self.animation_speed / len(self.animation)
        # timer for deciding when to flip the image
        self._flickertimer = 0.0
        # currently viewed sprite
        self._spriteimage = 0


    def draw(self):

        '''Draws the object to the screen.

        This function draws the object to the screen if it appears within the
        PLAYER fov.  It also keeps track of the timing for animations to trigger
        a transition to the next sprite in the animation.

        '''
        is_visible = libtcod.map_is_in_fov(FOV_MAP, self.x, self.y)

        if is_visible:  # if visible, check to see if animation has > 1 image
            if len(self.animation) == 1:
                # if no, just blit the image
                SURFACE_MAIN.blit(self.animation[0], (self.x * constants.CELL_WIDTH,
                                                      self.y * constants.CELL_HEIGHT))
            # does this object have multiple sprites?
            elif len(self.animation) > 1:
                # only update animation timer if we can calculate how quickly
                # the game is running.
                if CLOCK.get_fps() > 0.0:
                    self._flickertimer +=  1 / CLOCK.get_fps()

                # if the timer has reached the speed
                if self._flickertimer >= self._flickerspeed:
                    self._flickertimer = 0.0  # reset the timer

                    # is this sprite the final item in the list?
                    if self._spriteimage >= len(self.animation) - 1:
                        self._spriteimage = 0  # reset sprite to top of list

                    else:
                        self._spriteimage += 1  # advance to next sprite

                #  draw the result
                SURFACE_MAIN.blit(self.animation[self._spriteimage],
                                  (self.x * constants.CELL_WIDTH,
                                   self.y * constants.CELL_HEIGHT))

class obj_Game:

    '''The obj_Game tracks game progress

    This is an object that stores all the information used by the game to 'keep
    track' of progress.  It tracks maps, objects, and game history or record of
    messages.

    Attributes:
        current_map (obj): whatever map is currently loaded.
        current_objects (list): list of objects for the current map.
        message_history (list): list of messages that have been pushed
            to the player over the course of a game.'''

    def __init__(self):
        self.current_map = map_create()
        self.current_objects = []
        self.message_history = []

class obj_Spritesheet:

    '''Class used to grab images out of a sprite sheet.  As a class, it allows
    you to access and subdivide portions of the sprite_sheet.

    Attributes:
        file_name (arg, str): String which contains the directory/filename of
            the image for use as a spritesheet.
        sprite_sheet (pygame.surface): The loaded spritesheet accessed through
            the file_name argument.

    '''

    def __init__(self, file_name):
        self.sprite_sheet = pygame.image.load(file_name).convert()

        self.tiledict = {'a': 1, 'b': 2, 'c': 3, 'd': 4,
                         'e': 5, 'f': 6, 'g': 7, 'h': 8,
                         'i': 9, 'j': 10, 'k': 11, 'l': 12,
                         'm': 13, 'n': 14, 'o': 15, 'p': 16}

    def get_image(self, column, row, width = constants.CELL_WIDTH,
                  height = constants.CELL_HEIGHT, scale = None):
        '''This method returns a single sprite.

        Args:
            column (str): Letter which gets converted into an integer, column in
                the spritesheet to be loaded.
            row (int): row in the spritesheet to be loaded.
            width (int): individual sprite width in pixels
            height (int): individual sprite height in pixels
            scale ((width, height)) = If included, scales the sprites to a new
                size.

        Returns:
            image_list (list): This method returns a single sprite contained
                within a list loaded from the spritesheet property.


        '''

        image_list = []

        image = pygame.Surface([width, height]).convert()

        image.blit(self.sprite_sheet, (0, 0),
                   (self.tiledict[column] * width,
                    row * height,
                    width, height))

        image.set_colorkey(constants.COLOR_BLACK)

        if scale:
            (new_w, new_h) = scale

            image = pygame.transform.scale(image, (new_w, new_h))

        image_list.append(image)

        return image_list

    def get_animation(self, column, row, width = constants.CELL_WIDTH,
                      height = constants.CELL_HEIGHT, num_sprites = 1,
                      scale = None):
        '''This method returns a sequence of sprites.

        Args:
            column (str): Letter which gets converted into an integer, column in
                the spritesheet to be loaded.
            row (int): row in the spritesheet to be loaded.
            width (int): individual sprite width in pixels
            height (int): individual sprite height in pixels
            num_sprites (int): number of sprites to be loaded in sequence.
            scale ((width, height)) = If included, scales the sprites to a new
                size.

        Returns:
            image_list (list): This method returns a sequence of sprites
                contained within a list loaded from the spritesheet property.

        '''

        image_list = []

        for i in range(num_sprites):
            # create blank image
            image = pygame.Surface([width, height]).convert()

            # copy image from sheet onto blank
            image.blit(self.sprite_sheet,
                       (0, 0),
                       (self.tiledict[column] * width + (width * i),
                        row * height, width, height))

            # set transparency key to black
            image.set_colorkey(constants.COLOR_BLACK)

            if scale:
                (new_w, new_h) = scale

                image = pygame.transform.scale(image, (new_w, new_h))

            image_list.append(image)

        return image_list



#   ____ ___  __  __ ____   ___  _   _ _____ _   _ _____ ____
#  / ___/ _ \|  \/  |  _ \ / _ \| \ | | ____| \ | |_   _/ ___|
# | |  | | | | |\/| | |_) | | | |  \| |  _| |  \| | | | \___ \
# | |__| |_| | |  | |  __/| |_| | |\  | |___| |\  | | |  ___) |
#  \____\___/|_|  |_|_|    \___/|_| \_|_____|_| \_| |_| |____/

class com_Creature:

    '''Creatures are actors that have health and can fight.

    Attributes:
        name_instance (arg, str): name of instance. "Bob" for example.
        max_hp (arg, int): max health of the creature.
        death_function (arg, function): function to be executed when hp reaches 0.
        current_hp (int): current health of the creature.

    '''

    def __init__(self, name_instance, max_hp = 10, death_function = None):

        self.name_instance = name_instance
        self.max_hp = max_hp
        self.death_function = death_function
        self.current_hp = max_hp

    def move(self, dx, dy):

        '''Moves the object

        Args:
            dx (int): distance to move actor along x axis
            dy (int): distance to move actor along y axis

        '''

        tile_is_wall = (GAME.current_map[self.owner.x + dx]
                        [self.owner.y + dy].block_path == True)

        target = map_check_for_creature(self.owner.x + dx,
                                        self.owner.y + dy,
                                        self.owner)

        if target:
            self.attack(target, 3)

        if not tile_is_wall and target is None:
            self.owner.x += dx
            self.owner.y += dy

    def attack(self, target, damage):
        '''Creature makes an attack against another obj_Actor

        Args:
            target (obj_Actor): target to be attacked, must have creature
                component.
            damage (int): amount of damage to be done to target

        '''

        game_message(self.name_instance +
                     " attacks " +
                     target.creature.name_instance +
                     " for " +
                     str(damage) +
                     " damage!",
                     constants.COLOR_WHITE)

        target.creature.take_damage(damage)

    def take_damage(self, damage):

        """Applies damage received to self.health

        This function applies damage to the obj_Actor with the creature
        component.  If the current health level falls below 1, executes the
        death_function.

        Args:
            damage (int): amount of damage to be applied to self.

        """

        # subtract health
        self.current_hp -= damage

        # print message
        game_message(self.name_instance +
                     "'s health is " +
                     str(self.current_hp) +
                     "/" +
                     str(self.max_hp),
                     constants.COLOR_RED)

        # if health now equals < 1, execute death function
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

    ## TODO Get Names of everything in inventory

    ## TODO Get volume within container

    @property
    def volume(self):
        return 0.0

    ## TODO Get weight of everything in inventory

class com_Item:

    '''Items are components that can be picked up and used.

    Attributes:
        weight (arg, float): how much does the item weigh
        volume (arg, float): how much space does the item take up

    '''

    def __init__(self, weight = 0.0, volume = 0.0, use_function = None,
        value = None):

        self.weight = weight
        self.volume = volume
        self.value = value
        self.use_function = use_function

    def pick_up(self, actor):

        '''The item is picked up and placed into an object's inventory.

        When called, this method seeks to place the item into an object's
        inventory if there is room.  It then removes the item from a Game's
        current_objects list.

        Args:
            actor (obj_Actor): the object that is picking up the item.

        '''

        if actor.container:  # first, checks for container component

            # does the container have room for this object?
            if actor.container.volume + self.volume > actor.container.max_volume:

                # if no, print error message
                game_message("Not enough room to pick up")

            else:

                # otherwise, pick the item up, remove from GAME.current_objects
                # message the player
                game_message('Picking up')

                # add to actor inventory
                actor.container.inventory.append(self.owner)

                # remove from game active list
                GAME.current_objects.remove(self.owner)

                # tell item what container holds it
                self.current_container = actor.container

    def drop(self, new_x, new_y):

        '''Drops the item onto the ground.

        This method removes the item from the actor.container inventory and
        places it into the GAME.current_objects list.  Drops the item at the
        location defined in the args.

        Args:
            new_x (int): x coord on the map to drop item
            new_y (int): y coord on the map to drop item

        '''

        # add this item to tracked objects
        GAME.current_objects.append(self.owner)

        # remove from the inventory of whatever actor holds it
        self.current_container.inventory.remove(self.owner)

        # set item location to as defined in the args
        self.owner.x = new_x
        self.owner.y = new_y

        # confirm successful placement with game message
        game_message("Item Dropped!")

    def use(self):

        '''Use the item by producing an effect and removing it.

        '''

        if self.use_function:
            result = self.use_function(self.current_container.owner, self.value)

            if result is not None:
                print("use_function failed")

            else:
                self.current_container.inventory.remove(self.owner)






#     _    ____
#    / \  |_ _|
#   / _ \  | |
#  / ___ \ | |
# /_/   \_\___|

class ai_Test:

    '''Objects with this ai aimlessly wonder around

    '''

    def take_turn(self):
        self.owner.creature.move(libtcod.random_get_int(0, -1, 1),
            libtcod.random_get_int(0, -1, 1))







#  ____             _   _
# |  _ \  ___  __ _| |_| |__
# | | | |/ _ \/ _` | __| '_ \
# | |_| |  __/ (_| | |_| | | |
# |____/ \___|\__,_|\__|_| |_|

def death_monster(monster):
    '''Default death function for creatures.

    '''

    # print message alerting player that creature has died
    game_message(monster.creature.name_instance +
                 " is dead!",
                 constants.COLOR_GREY)

    # remove ai and creature components
    monster.creature = None
    monster.ai = None





#  __  __
# |  \/  | __ _ _ __
# | |\/| |/ _` | '_ \
# | |  | | (_| | |_) |
# |_|  |_|\__,_| .__/
#              |_|

def map_create():

    '''Creates the default map.

    Currently, the map this function creatures is a small room with 2 pillars
    within it.  It is a testing map.

    Returns:
        new_map (array): This array is populated with struc_Tile objects.

    Effects:
        Calls map_make_fov on new_map to preemptively create the fov.

    '''

    # initializes an empty map
    new_map = [[struc_Tile(False) for y in range(0, constants.MAP_HEIGHT)]
               for x in range(0, constants.MAP_WIDTH)]

    # creates 2 walls, one at (10, 10) and the other at (10, 15)
    new_map[10][10].block_path = True
    new_map[10][15].block_path = True

    # goes through map, sets left and right most tiles to walls
    for x in range(constants.MAP_WIDTH):
        new_map[x][0].block_path = True
        new_map[x][constants.MAP_HEIGHT - 1].block_path = True

    # goes through map, sets top and bottom most tiles to walls
    for y in range(constants.MAP_HEIGHT):
        new_map[0][y].block_path = True
        new_map[constants.MAP_WIDTH - 1][y].block_path = True

    # create FOV_MAP
    map_make_fov(new_map)

    # returns the created map
    return new_map

def map_check_for_creature(x, y, exclude_object = None):

    '''Check the current map for creatures at specified location.

    This function looks at that location for any object that has a creature
    component and returns it.  Optional argument allows user to exclude an
    object from the search, usually the Player

    Args:
        x (int): x map coord to check for creature
        y (int): y map coord to check for creature
        exclude_object(obj_Actor, optional): if an object is passed into this
            function, this object will be ignored by the search.

    Returns:
        target (obj_Actor): but only if found at the location specified in the
            arguments and if not excluded.

    '''

    # initialize target var to None type
    target = None

    # optionally exclude an object
    if exclude_object:

        # check objectlist to find creature at that location that isn't excluded
        for object in GAME.current_objects:
            if (object is not exclude_object and
                object.x == x and
                object.y == y and
                object.creature):

                # if object is found, set target var to object
                target = object

            if target:
                return target

    else:
    # check objectlist to find any creature at that location
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

    '''Creates an FOV map based on a map.

    Args:
        incoming_map (array): map, usually created with map_create

    Effects:
        generates the FOV_MAP

    '''

    # need to create the Global Variable
    global FOV_MAP


    FOV_MAP = libtcod.map_new(constants.MAP_WIDTH, constants.MAP_HEIGHT)

    for y in range(constants.MAP_HEIGHT):
        for x in range(constants.MAP_WIDTH):
            libtcod.map_set_properties(FOV_MAP, x, y,
                not incoming_map[x][y].block_path, not incoming_map[x][y].block_path)

def map_calculate_fov():

    '''Calculates the FOV based on the Player's perspective.

    Accesses the global variable FOV_CALCULATE, if FOV_CALCULATE is True, sets
    it to False and recalculates the FOV.

    '''

    global FOV_CALCULATE

    if FOV_CALCULATE:

        # reset FOV_CALCULATE
        FOV_CALCULATE = False

        # run the calculation function
        libtcod.map_compute_fov(FOV_MAP, PLAYER.x,
                                PLAYER.y,
                                constants.TORCH_RADIUS,
                                constants.FOV_LIGHT_WALLS,
                                constants.FOV_ALGO)

def map_objects_at_coords(coords_x, coords_y):

    '''Get a list of every object at a coordinate.

    Args:
        coords_x (int): x axis map coordinate of current map to check
        coords_y (int): y axis map coordinate of current map to check

    Returns:
        object_options (list): list of every object at the coordinate.

    '''

    object_options = [obj for obj in GAME.current_objects
                      if obj.x == coords_x and obj.y == coords_y]

    return object_options


def map_find_line(coords1, coords2):
    ''' Converts two x, y coords into a list of tiles.

    coords1 : (x1, y1)
    coords2 : (x2, y2)
    '''
    x1, y1 = coords1

    x2, y2 = coords2

    libtcod.line_init(x1, y1, x2, y2)

    calc_x, calc_y = libtcod.line_step()

    coord_list = []

    if x1 == x2 and y1 == y2:
        return [(x1, y1)]

    while (not calc_x is None):

        coord_list.append((calc_x, calc_y))

        calc_x, calc_y = libtcod.line_step()

    return coord_list




#  ____                     _
# |  _ \ _ __ __ ___      _(_)_ __   __ _
# | | | | '__/ _` \ \ /\ / / | '_ \ / _` |
# | |_| | | | (_| |\ V  V /| | | | | (_| |
# |____/|_|  \__,_| \_/\_/ |_|_| |_|\__, |
#                                   |___/

def draw_game():

    '''Main call for drawing the entirity of the game.

    This method is responsible for regularly drawing the whole game.  It starts
    by clearing the main surface, then draws elements of the screen from front
    to back.

    The order of operations is:
    1) Clear the screen
    2) Draw the map
    3) Draw the objects
    4) Draw the debug console
    5) Draw the messages console
    6) Update the display

    '''

    # clear the display surface
    SURFACE_MAIN.fill(constants.COLOR_DEFAULT_BG)

    # draw the map
    draw_map(GAME.current_map)

    # draw all objects
    for obj in GAME.current_objects:
        obj.draw()

    draw_debug()
    draw_messages()

def draw_map(map_to_draw):

    '''Main call for drawing a map to the screen.

    draw_map loops through every tile within the map and draws it's
    corresponding tile to the screen.

    Args:
        map_to_draw (array): the map to draw in the background.  Under most
            circumstances, should be the GAME.current_map object.

    '''

    # Loop through every object in the map
    for x in range(0, constants.MAP_WIDTH):
        for y in range(0, constants.MAP_HEIGHT):

            # Does this tile appear within the current FOV?
            is_visible = libtcod.map_is_in_fov(FOV_MAP, x, y)

            if is_visible:

                # once the tile appears within the FOV, set to explored
                map_to_draw[x][y].explored = True

                # if tile is blocked, draw a wall.
                if map_to_draw[x][y].block_path == True:

                    # draw wall
                    SURFACE_MAIN.blit(ASSETS.S_WALL,
                                      (x * constants.CELL_WIDTH,
                                       y * constants.CELL_HEIGHT))
                else: # otherwise, draw a floor
                    SURFACE_MAIN.blit(ASSETS.S_FLOOR,
                                      (x * constants.CELL_WIDTH,
                                       y * constants.CELL_HEIGHT))

            # if tile is not visible, is it explored?
            elif map_to_draw[x][y].explored:

                # if yes, and the tile is blocked, draw an explored wall.
                if map_to_draw[x][y].block_path == True:

                    # draw wall
                    SURFACE_MAIN.blit(ASSETS.S_WALLEXPLORED,
                                      (x * constants.CELL_WIDTH,
                                       y * constants.CELL_HEIGHT))
                else: #otherwise, draw a floor
                    SURFACE_MAIN.blit(ASSETS.S_FLOOREXPLORED,
                                      (x * constants.CELL_WIDTH,
                                       y * constants.CELL_HEIGHT))

def draw_debug():

    '''Draw the debug console to the display surface.

    This method draws a debug console to the upper left corner of the window.
    For now, this debug console is limited to the current FPS.

    '''

    draw_text(SURFACE_MAIN,
              "fps: " + str(int(CLOCK.get_fps())),
              constants.FONT_DEBUG_MESSAGE,
              (0, 0),
              constants.COLOR_WHITE,
              constants.COLOR_BLACK)

def draw_messages():

    '''Draw the messages console to the display surface.

    This method generates a list of messages to display in the lower left-hand
    corner of the display surface, and then displays them.

    '''

    # if the number of messages available is < than the number of messages we
    # are allowed to display, just display all messages
    if len(GAME.message_history) <= constants.NUM_MESSAGES:
        to_draw = GAME.message_history
    else:
        to_draw = GAME.message_history[-(constants.NUM_MESSAGES):]

    text_height = helper_text_height(constants.FONT_MESSAGE_TEXT)

    start_y = (constants.MAP_HEIGHT * constants.CELL_HEIGHT -
               (constants.NUM_MESSAGES * text_height)) - 5

    for i, (message, color) in enumerate(to_draw):

        draw_text(SURFACE_MAIN,
                  message,
                  constants.FONT_MESSAGE_TEXT,
                  (0, start_y + (i * text_height)),
                  color, constants.COLOR_BLACK)

def draw_text(display_surface, text_to_display, font,
              coords, text_color, back_color = None):
    ''' Displays text on the desired surface.

    Args:
        display_surface (pygame.Surface): the surface the text is to be
            displayed on.
        text_to_display (str): what is the text to be written
        font (pygame.font.Font): font object the text will be written using
        coords ((int, int)): where on the display_surface will the object be
            written, the text will be drawn from the upper left corner of the
            text.
        text_color ((int, int, int)): (R, G, B) color code for the desired color
            of the text.
        back_color ((int, int, int), optional): (R, G, B) color code for the
            background.  If not included, the background is transparent.

    '''

    # get both the surface and rectangle of the desired message
    text_surf, text_rect = helper_text_objects(text_to_display, font, text_color, back_color)

    # adjust the location of the surface based on the coordinates
    text_rect.topleft = coords

    # draw the text onto the display surface.
    display_surface.blit(text_surf, text_rect)

def draw_tile_rect(coords):

    x, y = coords

    new_x = x * constants.CELL_WIDTH
    new_y = y * constants.CELL_WIDTH

    new_surface = pygame.Surface((constants.CELL_WIDTH, constants.CELL_HEIGHT))

    new_surface.fill(constants.COLOR_WHITE)

    new_surface.set_alpha(200)

    SURFACE_MAIN.blit(new_surface, (new_x, new_y))







#  _   _      _
# | | | | ___| |_ __   ___ _ __ ___
# | |_| |/ _ \ | '_ \ / _ \ '__/ __|
# |  _  |  __/ | |_) |  __/ |  \__ \
# |_| |_|\___|_| .__/ \___|_|  |___/
#              |_|

def helper_text_objects(incoming_text, incoming_font, incoming_color, incoming_bg):

    '''Generates the text objects used for drawing text.

    This function is most often used in conjuction with the draw_text method.
    It generates the text objects used by draw_text to actually display whatever
    string is called by the method.

    Args:
        incoming_text (str):
        incoming_font (pygame.font.Font):
        incoming_color ((int, int, int)):
        incoming_bg ((int, int, int), optional):

    Returns:
        Text_surface (pygame.Surface):
        Text_surface.get_rect() (pygame.Rect):

    '''

    # if there is a background color, render with that.
    if incoming_bg:
        Text_surface = incoming_font.render(incoming_text,
                                            False,
                                            incoming_color,
                                            incoming_bg)

    else:  # otherwise, render without a background.
        Text_surface = incoming_font.render(incoming_text,
                                            False,
                                            incoming_color)

    return Text_surface, Text_surface.get_rect()

def helper_text_height(font):

    '''Measures the height in pixels of a specified font.

    This method is used when you need the height of a font object.  Most often
    this is useful when designing UI elements where the exact height of a font
    needs to be known.

    Args:
        font (pygame.font.Font): the font whose height is desired.

    Returns:
        font_rect.height (int): the height, in pixels, of the font.

    '''

    # render the font out
    font_rect = font.render('a', False, (0, 0, 0)).get_rect()

    return font_rect.height

def helper_text_width(font):

    '''Measures the width in pixels of a specified font.

    This method is used when you need the width of a font object.  Most often
    this is useful when designing UI elements where the exact width of a font
    needs to be known.

    Args:
        font (pygame.font.Font): the font whose width is desired.

    Returns:
        font_rect.width (int): the width, in pixels, of the font.

    '''

    # render the font out
    font_rect = font.render('a', False, (0, 0, 0)).get_rect()

    return font_rect.width





#  __  __             _
# |  \/  | __ _  __ _(_) ___
# | |\/| |/ _` |/ _` | |/ __|
# | |  | | (_| | (_| | | (__
# |_|  |_|\__,_|\__, |_|\___|
#               |___/

def cast_heal(target, value):

    if target.creature.current_hp == target.creature.max_hp:
        game_message(target.creature.name_instance + " the " + target.name_object +
            " is already at full health!")
        return "canceled"
    else:
        game_message(target.creature.name_instance + " the " + target.name_object +
                " healed for " + str(value) + "health!")
        target.creature.heal(value)
        print(target.creature.current_hp)

    return None

def cast_lightning(damage):

    player_location = (PLAYER.x, PLAYER.y)

    # prompt the player for a tile
    point_selected = menu_tile_select(coords_origin = player_location,
        max_range = 5, penetrate_walls = False)

    if point_selected:
        # convert that tile into a list of tiles between A -> B
        list_of_tiles = map_find_line(player_location, point_selected)

        # cycle through list, damage everything found
        for i, (x, y) in enumerate(list_of_tiles):

            target = map_check_for_creature(x, y)

            if target:
                target.creature.take_damage(damage)




#  __  __
# |  \/  | ___ _ __  _   _ ___
# | |\/| |/ _ \ '_ \| | | / __|
# | |  | |  __/ | | | |_| \__ \
# |_|  |_|\___|_| |_|\__,_|___/

def menu_pause():

    '''This menu pauses the game and displays a simple message.'''

    # intialize to False, pause ends when set to True
    menu_close = False

    # window dimentions
    window_width = constants.MAP_WIDTH * constants.CELL_WIDTH
    window_height = constants.MAP_HEIGHT * constants.CELL_HEIGHT

    # Window Text characteristics
    menu_text = "PAUSED"
    menu_font = constants.FONT_DEBUG_MESSAGE

    # helper vars
    text_height = helper_text_height(menu_font)
    text_width = len(menu_text) * helper_text_width(menu_font)

    while not menu_close: # while False, pause continues

        # get list of inputs
        events_list = pygame.event.get()

        # evaluate for each event
        for event in events_list:

            # if a key has been pressed
            if event.type == pygame.KEYDOWN:

                # was it the 'p' key?
                if event.key == pygame.K_p:
                    menu_close = True  # if yes, close the menu.

        # Draw the pause message on the screen.
        draw_text(SURFACE_MAIN, menu_text, constants.FONT_DEBUG_MESSAGE,
            ((window_width / 2) - (text_width / 2), (window_height / 2) - (text_height / 2)),
            constants.COLOR_WHITE, constants.COLOR_BLACK)

        CLOCK.tick(constants.GAME_FPS)

        # update the display surface
        pygame.display.flip()

def menu_inventory():

    '''Opens up the inventory menu.

    The inventory menu allows the player to examine whatever items they are
    currently holding.  Selecting an item will drop it.

    '''

    # initialize to False, when True, the menu closes
    menu_close = False

    # Calculate window dimensions
    window_width = constants.MAP_WIDTH * constants.CELL_WIDTH
    window_height = constants.MAP_HEIGHT * constants.CELL_HEIGHT

    # Menu Characteristics
    menu_width = 200
    menu_height = 200
    menu_x = (window_width / 2) - (menu_width / 2)
    menu_y = (window_height / 2) - (menu_height / 2)

    # Menu Text Characteristics
    menu_text_font = constants.FONT_MESSAGE_TEXT
    menu_text_color = constants.COLOR_WHITE

    # Helper var
    menu_text_height = helper_text_height(menu_text_font)

    # create a new surface to draw on.
    local_inventory_surface = pygame.Surface((menu_width, menu_height))

    while not menu_close:

        ## Clear the menu
        local_inventory_surface.fill(constants.COLOR_BLACK)

        # collect list of item names
        print_list = [obj.name_object for obj in PLAYER.container.inventory]

        ## Get list of input events
        events_list = pygame.event.get()
        mouse_x, mouse_y = pygame.mouse.get_pos()

        mouse_x_rel = mouse_x - menu_x
        mouse_y_rel = mouse_y - menu_y

        mouse_in_window = (mouse_x_rel > 0 and
                           mouse_y_rel > 0 and
                           mouse_x_rel < menu_width and
                           mouse_y_rel < menu_height)

        mouse_line_selection = mouse_y_rel / menu_text_height



        # cycle through events
        for event in events_list:
            if event.type == pygame.KEYDOWN:
                # if player presses 'i' again, close menu
                if event.key == pygame.K_i:
                    menu_close = True

            if event.type == pygame.MOUSEBUTTONDOWN:

                if event.button == 1:

                    if (mouse_in_window and
                        mouse_line_selection <= len(print_list) - 1) :

                        PLAYER.container.inventory[mouse_line_selection].item.use()


        ## Draw the list
        for line, (name) in enumerate(print_list):

            if line == mouse_line_selection and mouse_in_window:
                draw_text(local_inventory_surface,
                          name,
                          menu_text_font,
                          (0, 0 + (line * menu_text_height)),
                          menu_text_color, constants.COLOR_GREY)
            else:
                draw_text(local_inventory_surface,
                          name,
                          menu_text_font,
                          (0, 0 + (line * menu_text_height)),
                          menu_text_color)

        ## Display Menu
        SURFACE_MAIN.blit(local_inventory_surface, (menu_x, menu_y))


        CLOCK.tick(constants.GAME_FPS)

        # update the display surface
        pygame.display.update()

def menu_tile_select(coords_origin = None, max_range = None,
    penetrate_walls = True):
    ''' This menu let's the player select a tile.

    This function pauses the game, produces an on screen rectangle and when the
    player presses the left mb, will return (message for now) the map address.
    '''

    menu_close = False

    while not menu_close:

        # Get mos position
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Get button clicks
        events_list = pygame.event.get()

        # mouse map selection
        map_coord_x = mouse_x/constants.CELL_WIDTH
        map_coord_y = mouse_y/constants.CELL_HEIGHT

        valid_tiles = []

        if coords_origin:
            full_list_tiles = map_find_line(coords_origin, (map_coord_x, map_coord_y))

            for i, (x, y) in enumerate(full_list_tiles):

                valid_tiles.append((x, y))

                if max_range and i == max_range - 1:
                    break

                if not penetrate_walls and GAME.current_map[x][y].block_path:
                    break


        else:
            valid_tiles = [(map_coord_x, map_coord_y)]

        # return map_coords when presses left mb
        for event in events_list:
            if event.type == pygame.KEYDOWN:
                # if player presses 'i' again, close menu
                if event.key == pygame.K_l:
                    menu_close = True

            if event.type == pygame.MOUSEBUTTONDOWN:

                if event.button == 1:
                    # returns coords selected
                    return (valid_tiles[-1])


        # draw game first
        draw_game()

        # Draw rectangle at mouse position on top of game
        for (tile_x, tile_y) in valid_tiles:
            draw_tile_rect((tile_x, tile_y))

        # update the display
        pygame.display.flip()

        # tick the CLOCK
        CLOCK.tick(constants.GAME_FPS)












#   ____
#  / ___| __ _ _ __ ___   ___
# | |  _ / _` | '_ ` _ \ / _ \
# | |_| | (_| | | | | | |  __/
#  \____|\__,_|_| |_| |_|\___|

def game_main_loop():

    '''In this function, we loop the main game

    '''

    game_quit = False

    # player action definition
    player_action = "no-action"

    while not game_quit:

        # handle player input
        player_action = game_handle_keys()

        map_calculate_fov()

        if player_action == "QUIT":
            game_quit = True

        if player_action != "no-action":
            for obj in GAME.current_objects:
                if obj.ai:
                    obj.ai.take_turn()

        # draw the game
        draw_game()

        # update the display
        pygame.display.flip()

        # tick the CLOCK
        CLOCK.tick(constants.GAME_FPS)

    # quit the game
    pygame.quit()
    exit()

def game_initialize():

    '''This function initializes the main window, and pygame.

    '''

    global SURFACE_MAIN, GAME, CLOCK, FOV_CALCULATE, PLAYER, ENEMY, ASSETS

    # initialize pygame
    pygame.init()

    pygame.key.set_repeat(200, 70)

    # SURFACE_MAIN is the display surface, a special surface that serves as the
    # root console of the whole game.  Anything that appears in the game must be
    # drawn to this console before it will appear.
    SURFACE_MAIN = pygame.display.set_mode((constants.MAP_WIDTH * constants.CELL_WIDTH,
                                            constants.MAP_HEIGHT * constants.CELL_HEIGHT))

    # GAME tracks game progress
    GAME = obj_Game()

    # The CLOCK tracks and limits cpu cycles
    CLOCK = pygame.time.Clock()

    # when FOV_CALCULATE is true, FOV recalculates
    FOV_CALCULATE = True

    # ASSETS stores the games assets
    ASSETS = struc_Assets()

    # create the player
    container_com1 = com_Container()
    creature_com1 = com_Creature("greg")
    PLAYER = obj_Actor(1, 1, "python",
                       ASSETS.A_PLAYER,
                       animation_speed = 1,
                       creature = creature_com1,
                       container = container_com1)

    # create lobster 1
    item_com1 = com_Item(value = 4, use_function = cast_heal)
    creature_com2 = com_Creature("jackie", death_function = death_monster)
    ai_com1 = ai_Test()
    ENEMY = obj_Actor(15, 15, "smart crab", ASSETS.A_ENEMY, animation_speed = 1,
        creature = creature_com2, ai = ai_com1, item = item_com1)

    # create lobster 2
    item_com2 = com_Item(value = 5, use_function = cast_heal)
    ai_com2 = ai_Test()
    creature_com3 = com_Creature("bob", death_function = death_monster)
    ENEMY2 = obj_Actor(14, 15, "dumb crab", ASSETS.A_ENEMY, animation_speed = 1,
        creature = creature_com3, ai = ai_com2, item = item_com2)

    # initialize current_objects list with the PLAYER and both enemies
    GAME.current_objects = [PLAYER, ENEMY, ENEMY2]

def game_handle_keys():

    '''Handles player input

    '''

    global FOV_CALCULATE
    # get player input
    events_list = pygame.event.get()

    # process input
    for event in events_list:
        if event.type == pygame.QUIT:
            return "QUIT"

        if event.type == pygame.KEYDOWN:

            # arrow key up -> move player up
            if event.key == pygame.K_UP:
                PLAYER.creature.move(0, -1)
                FOV_CALCULATE = True
                return "player-moved"

            # arrow key down -> move player down
            if event.key == pygame.K_DOWN:
                PLAYER.creature.move(0, 1)
                FOV_CALCULATE = True
                return "player-moved"

            # arrow key left -> move player left
            if event.key == pygame.K_LEFT:
                PLAYER.creature.move(-1, 0)
                FOV_CALCULATE = True
                return "player-moved"

            # arrow key right -> move player right
            if event.key == pygame.K_RIGHT:
                PLAYER.creature.move(1, 0)
                FOV_CALCULATE = True
                return "player-moved"

            # key 'g' -> pick up objects
            if event.key == pygame.K_g:
                objects_at_player = map_objects_at_coords(PLAYER.x, PLAYER.y)

                for obj in objects_at_player:
                    if obj.item:
                        obj.item.pick_up(PLAYER)

            # key 'd' -> drop object from inventory
            if event.key == pygame.K_d:
                if len(PLAYER.container.inventory) > 0:
                    PLAYER.container.inventory[-1].item.drop(PLAYER.x, PLAYER.y)

            # key 'p' -> pause the game
            if event.key == pygame.K_p:
                menu_pause()

            # key 'i' ->  open inventory menu
            if event.key == pygame.K_i:
                menu_inventory()

            # key 'l' -> turn on tile selection
            if event.key == pygame.K_l:
                cast_lightning(10)

    return "no-action"

def game_message(game_msg, msg_color = constants.COLOR_GREY):

    '''Adds message to the message history

    Args:
        game_msg (str): Message to be saved
        msg_color ((int, int, int), optional) = color of the message

    '''

    GAME.message_history.append((game_msg, msg_color))






#############################################################
###################################################   #######
###############################################   /~\   #####
############################################   _- `~~~', ####
##########################################  _-~       )  ####
#######################################  _-~          |  ####
####################################  _-~            ;  #####
##########################  __---___-~              |   #####
#######################   _~   ,,                  ;  `,,  ##
#####################  _-~    ;'                  |  ,'  ; ##
###################  _~      '                    `~'   ; ###
############   __---;                                 ,' ####
########   __~~  ___                                ,' ######
#####  _-~~   -~~ _                               ,' ########
##### `-_         _                              ; ##########
#######  ~~----~~~   ;                          ; ###########
#########  /          ;                        ; ############
#######  /             ;                      ; #############
#####  /                `                    ; ##############
###  /                                      ; ###############
#                                            ################

if __name__ == '__main__':
    game_initialize()
    game_main_loop()
