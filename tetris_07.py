"""
Python Tetris Game
Inspired by the classic 'Tetris' game and following
versions of the same name.

Sources:
Created using the arcade library
Link: https://arcade.academy/index.html
Code Help:
Link: https://arcade.academy/examples/tetris.html
Pygame Tetris
https://levelup.gitconnected.com/writing-tetris-in-python-2a16bddb5318
SRS -
How to Properly Rotate Tetris Pieces - Game Development Tutorial
Link: https://www.youtube.com/watch?v=yIpk5TJ_uaI
SRS wikis
Link: https://harddrop.com/wiki/SRS
Link: https://tetris.wiki/Super_Rotation_System
Music:
Tetris 99 - Main theme - "https://www.youtube.com/watch?v=63hoSNvS6Z4"
All rights of this soundtrack go to the creator "Sega".
"ES_Candy - Caponium.mp3"
"ES_Pixel - Josef Falkenskold.mp3"
"ES_High Score - Eight Bits.mp3"
Music obtained legally through a subscription to Epidemic sound
- https://www.epidemicsound.com/
"""
import arcade
import random
import PIL
import time

# Define basic sizes
# No. rows and columns
ROW_COUNT = 22
COL_COUNT = 10

# Width and height of each cell
WIDTH = 30
HEIGHT = 30

# Margin between each cell and the outside of the grid
MARGIN = 5

# Calculate the screen width and height from the no. rows and columns
# and the width and height of each cell (accounting for margin displacement)
SCREEN_WIDTH = ((WIDTH + MARGIN) * COL_COUNT + MARGIN) + 200
SCREEN_HEIGHT = (HEIGHT + MARGIN) * ROW_COUNT + MARGIN
TITLE = "My Game | Tetris"

# Text constants
LEVEL_TEXT_XY = (SCREEN_WIDTH - 180, SCREEN_HEIGHT - 100)
LEVEL_NUM_TEXT_XY = (SCREEN_WIDTH - 180, SCREEN_HEIGHT - 130)

SCORE_TEXT_XY = (SCREEN_WIDTH - 180, SCREEN_HEIGHT - 200)
SCORE_NUM_TEXT_XY = (SCREEN_WIDTH - 180, SCREEN_HEIGHT - 230)

TITLE_FONT_SIZE = 25

NEXT_SHAPE_X = 427
NEXT_SHAPE_Y = 455

MUSIC_LIST = ["resources/my_sounds/background_mixes/ES_Candy - Caponium.mp3",
              "resources/my_sounds/background_mixes/ES_Pixel - Josef Falkenskold.mp3",
              "resources/my_sounds/background_mixes/ES_High Score - Eight Bits.mp3",
              "resources/my_sounds/background_mixes/Tetris 99 - Main Theme.mp3"]

# List of colors based on the 8 custom Tetris colors - (R,B,G) format.
COLORS = [(0, 0, 0),  # black - empty squares
          (128, 0, 128),  # Pimp Purple - baseline
          (28, 209, 0),  # Lime Green - T block
          (252, 47, 0),  # Scarlet Red - L block
          (246, 140, 19),  # Dark Orange - J block
          (36, 120, 255),  # Blue Crayola - S block
          (255, 20, 181),  # Shocking Pink - Z block
          (82, 249, 255),  # Electric Blue - Square
          (255, 234, 0),  # Middle Yellow - I block
          ]

# List containing the different tetrominoes - different numbers for colouring purposes
# it is done so we know our center piece is always at for shape in shapes -> shape[1][2]
SHAPES = [[[0, 2, 0],
           [2, 2, 2]],

          [[0, 0, 3],
           [3, 3, 3]],

          [[4, 0, 0],
           [4, 4, 4]],

          [[0, 5, 5],
           [5, 5, 0]],

          [[6, 6, 0],
           [0, 6, 6]],

          [[0, 7, 7],
           [0, 7, 7]],

          [[0, 0, 0, 0],
           [8, 8, 8, 8]]
          ]

O_OFFSET_DATA = [[0, 0], [0, 1], [-1, 1], [-1, 0]]


def create_textures():
    """ Creates a list of color boxes using width + height and color list called"""
    new_textures = []
    # loop through the color list creating a image the size of our pixel for each color
    # Uses this image to create an arcade texture and add it to the list
    for color in COLORS:
        # Create a box
        # noinspection PyUnresolvedReferences
        image = PIL.Image.new('RGB', (WIDTH, HEIGHT), color)
        new_textures.append(arcade.Texture(str(color), image=image))
    return new_textures


texture_list = create_textures()


def new_board(row_count, col_count, is_next):
    """ Create a grid that is X cols by Y rows filled with 0's. """
    # Board has 0's equal to the num of columns and num of rows.
    board = [[0 for _x in range(col_count)] for _y in range(row_count)]
    if not is_next:
        # Add 1's on the bottom for easier collision checking
        board += [[1 for _x in range(col_count)]]
    # Returns a 2d list of 0's that is full of items col_count in length
    return board


def check_collision(board, shape, offset):
    """
    See if the matrix stored in variable shape will intercept with anything
    on the board based on the offset. Offset is an (x, y).
    """
    off_x, off_y = offset

    # Enumerate - "for  count, value  in enumerate(values):"
    # for each row in shape
    for count_y, row in enumerate(shape):
        # for each cell in that row
        for count_x, cell in enumerate(row):
            # Try / except to stop IndexError for error control
            try:
                # if the cell and the board's (x,y) is not a 0, return True (as it must intersect)
                if cell and board[count_y + off_y][count_x + off_x]:
                    return True
            except IndexError:
                return True
    return False


def join_matrixes(matrix_1, matrix_2, matrix_2_offset):
    """
    :param matrix_1: first matrix - the board
    :param matrix_2: second matrix - the shape
    :param matrix_2_offset: the offset of the second matrix - the x and y coordinate of shape (x,y)
    :return: Returns a new matrix containing both matrix - a new board
    """
    offset_x, offset_y = matrix_2_offset
    for count_y, row in enumerate(matrix_2):
        for count_x, value in enumerate(row):
            if value:
                matrix_1[count_y + offset_y - 1][count_x + offset_x] += value
    return matrix_1


def remove_row(board, row):
    """ Remove a row from the board, add a blank row on top. """
    del board[row]
    return [[0 for _ in range(COL_COUNT)]] + board


def check_level(level, score):
    """
    Checks current level and sees if we need to
    increase level based on score
    """
    if level == 1:
        if score > 99:
            level = 2
    elif level == 2:
        if score > 299:
            level = 3
    elif level == 3:
        if score > 499:
            level = 4
    elif level == 4:
        if score > 799:
            level = 5
    elif level == 5:
        if score > 799:
            level = 6
    elif level == 6:
        if score > 2000:
            level = 7

    return level


# ROTATION CALCULATION FUNCTIONS

def calculate_rotation_num(rotate_anticlockwise, rotation_num):
    """
    A simple loop between 0 - 3 that calculates a new rotation
    number based on a boolean of anti-clockwise
    """

    # Calculate new rotation index
    new_rotation = rotation_num
    if not rotate_anticlockwise:
        new_rotation += 1
    else:
        new_rotation -= 1

    # Do we need to loop?
    if new_rotation < 0:
        new_rotation = 3
    elif new_rotation > 3:
        new_rotation = 0

    return new_rotation


def get_tile_coordinates_global(tile_count_xy, shape_xy):
    """
    Returns a x,y of each tile's global location on the grid
    """
    # Unpack given variables
    shape_x, shape_y = shape_xy
    count_x, count_y = tile_count_xy
    # Do maths to find each tile's x and y relative to the top right hand corner of the matrix
    tile_pos_x = shape_x + count_x
    tile_pos_y = (shape_y - 1) + count_y
    return tile_pos_x, tile_pos_y


def get_rotated_tile(tile_coordinates, center_tile_coordinates, clockwise):
    """
    Find the rotated coordinates of a tile relative to the top left hand corner
    Takes center tile coordinates that it will rotate all other blocks around.
    Works by finding the relative x, y postions or vectors to the center tile and then
    them through a rotation matrix (based on which way we want to rotate) and then
    putting them back in to their correct place relative the top LH corner.
    """
    tile_x, tile_y = tile_coordinates
    center_tile_x, center_tile_y = center_tile_coordinates

    # Find the relative position (vector) of a tile to the center tile (origin)
    relative_position_x = tile_x - center_tile_x
    relative_position_y = tile_y - center_tile_y

    # Rotation matrix depending on which way we flip
    if clockwise:
        rotation_matrix = [[0, 1],
                           [-1, 0]]
    else:
        rotation_matrix = [[0, -1],
                           [1, 0]]

    # R x Vr = Vnew // Uses a rotation matrix to find the new x and y positions of our tiles
    new_postion_x = (rotation_matrix[0][0] * relative_position_x) + (rotation_matrix[0][1] * relative_position_y)
    new_postion_y = (rotation_matrix[1][0] * relative_position_x) + (rotation_matrix[0][0] * relative_position_y)

    # Put it back into it's correct place on the grid
    new_postion_x += center_tile_x
    new_postion_y += center_tile_y

    new_position = new_postion_x, new_postion_y
    return new_position


def minus_xy_array(array_a, array_b):
    """
    Function for array A - array B (coordinates).
    Used mostly for offset calculations.
    Will return a [x, y] list
    """
    a_x_value, a_y_value = array_a[0], array_a[1]
    b_x_value, b_y_value = array_b[0], array_b[1]

    new_x_value = a_x_value - b_x_value
    new_y_value = a_y_value - b_y_value

    return new_x_value, new_y_value


def locateLargest(matrix):
    """ Finds the longest length row in matrix and returns it. """
    largest_num = None
    list = []
    for count_y, row in enumerate(matrix):
        potential_num = 0

        for count_x, num in enumerate(row):
            if num:
                potential_num += 1
        list.append(potential_num)
    largest_num = max(list)
    return largest_num


def offset_o(old_rotation, new_rotation):
    """
    Function to work out the offset of the O block
    based on old and new rotations. Returns an (x, y) offset.
    """
    pos_old = O_OFFSET_DATA[old_rotation]
    pos_new = O_OFFSET_DATA[new_rotation]

    offset = minus_xy_array(pos_old, pos_new)
    return offset


class MenuView(arcade.View):
    def __init__(self):
        """ This is run once when we switch to this view """
        super().__init__()

        self.mute = False
        self.dark_mode = True

        self.background_texture = "resources/menu_view/menu.png"
        self.start_button_texture = "resources/menu_view/buttons/start_button_1.png"
        self.dark_button_texture = "resources/menu_view/buttons/dark_button_1.png"
        self.mute_button_texture = "resources/menu_view/buttons/mute_button_1.png"

        self.background = None
        self.start_button = None
        self.button = None
        self.button_sprites = None

        self.color_button_indicator = None
        self.mute_button_indicator = None
        self.indicator_sprites = None

        self.color_green = None
        self.color_dark_green = None

    def setup(self):
        """ Set up function"""
        # pre defined colors for status indicators
        self.color_green = 24, 255, 0
        self.color_dark_green = 255, 0, 32

        self.button_sprites = arcade.SpriteList()
        self.indicator_sprites = arcade.SpriteList()

        # Menu background
        self.background = arcade.Sprite(self.background_texture, 1)
        self.background.center_x = SCREEN_WIDTH / 2
        self.background.bottom = 0
        self.background.properties = "background"

        # Start button
        self.start_button = arcade.Sprite(self.start_button_texture, 0.5)
        self.start_button.center_x = SCREEN_WIDTH / 2
        self.start_button.center_y = SCREEN_HEIGHT / 2 + 75
        self.start_button.properties = "start_button"
        self.button_sprites.append(self.start_button)

        # Light or dark color mode button
        self.button = arcade.Sprite(self.dark_button_texture, 0.5)
        self.button.center_x = SCREEN_WIDTH / 2
        self.button.center_y = SCREEN_HEIGHT / 2 - 25
        self.button.properties = "color_button"
        self.button_sprites.append(self.button)

        # Mute button
        self.button = arcade.Sprite(self.mute_button_texture, 0.5)
        self.button.center_x = SCREEN_WIDTH / 2
        self.button.center_y = SCREEN_HEIGHT / 2 - 100
        self.button.properties = "mute_button"
        self.button_sprites.append(self.button)

        # indicators
        self.color_button_indicator = arcade.SpriteSolidColor(25, 62, self.color_green)
        self.color_button_indicator.center_x = SCREEN_WIDTH / 2 + 147
        self.color_button_indicator.center_y = SCREEN_HEIGHT / 2 - 25
        self.color_button_indicator.properties = "color_indicator"
        self.indicator_sprites.append(self.color_button_indicator)

        self.mute_button_indicator = arcade.SpriteSolidColor(25, 61, self.color_green)
        self.mute_button_indicator.center_x = SCREEN_WIDTH / 2 + 147
        self.mute_button_indicator.center_y = SCREEN_HEIGHT / 2 - 100
        self.mute_button_indicator.properties = "mute_indicator"
        self.indicator_sprites.append(self.mute_button_indicator)

    def on_draw(self):
        """ Draw this view """
        arcade.start_render()

        # Set background and color scheme
        arcade.set_background_color(arcade.color.LIGHT_STEEL_BLUE)
        self.button_sprites.draw()

        # Check if dark mode is enabled, then draw indicator box
        if self.dark_mode:
            self.indicator_sprites[0].draw()
            arcade.set_background_color((47, 64, 77))

        self.background.draw()

        # Check if mute is enabled, then draw indicator box
        if self.mute:
            self.indicator_sprites[1].draw()

    def on_update(self, delta_time: float):
        """ Called every frame """
        self.button_sprites.update()
        self.indicator_sprites.update()

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """ If the user presses the mouse button, re-start the game. """
        # Track if the user has pressed these buttons
        # Get all sprites near by
        hit_list = arcade.get_sprites_at_point((_x, _y), self.button_sprites)

        # if there were any sprites near by then check which one
        for sprite in hit_list:
            # Color Button
            if sprite.properties == "color_button":
                if _button == arcade.MOUSE_BUTTON_LEFT:
                    self.dark_mode = not self.dark_mode

            # Mute Button
            elif sprite.properties == "mute_button":
                if _button == arcade.MOUSE_BUTTON_LEFT:
                    self.mute = not self.mute

            # Start Button
            elif sprite.properties == "start_button":
                game_view = GameView()
                game_view.mute = self.mute
                game_view.dark_mode = self.dark_mode
                game_view.setup()
                self.window.show_view(game_view)


class GameOverView(arcade.View):
    def __init__(self):
        """ This is run once when we switch to this view """
        super().__init__()

        # Load menu texture
        self.texture = arcade.load_texture("resources/game_over_view/game_over.png")
        self.mute = bool
        self.score = 0

    def on_draw(self):
        """ Draw this view """
        arcade.start_render()

        # Display menu texture
        self.texture.draw_sized(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                                SCREEN_WIDTH, SCREEN_HEIGHT)
        arcade.draw_text("SCORE:",
                         SCREEN_WIDTH / 2 - 105, SCREEN_HEIGHT - 170,
                         (247, 147, 30), TITLE_FONT_SIZE + 15, font_name="Neuropol Nova Regular")
        arcade.draw_text(str(self.score),
                         SCREEN_WIDTH / 2 + 55, SCREEN_HEIGHT - 170,
                         (247, 147, 30), TITLE_FONT_SIZE + 15, font_name="Neuropol Nova Regular")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """ If the user presses the mouse button, re-start the game. """
        game_view = GameView()
        game_view.mute = self.mute
        game_view.setup()
        self.window.show_view(game_view)


class GameView(arcade.View):
    """
    Main Application class for game
    Has multiple in-built functions from arcade library
    """

    def __init__(self):
        """ Initializer class. Code to be ran on launch """
        super().__init__()
        # Load background colors
        self.dark_background = (47, 64, 77)
        self.light_background = arcade.color.LIGHT_STEEL_BLUE

        # Load our variables
        self.board = None
        self.board_sprite_list = None
        self.next_board = None

        self.shape = None
        self.shape_x = 0
        self.shape_y = 0
        self.next_shape = None

        self.frame_count = 0

        self.score_text = None
        self.lvl_text = None
        self.score_num_text = None
        self.level_num_text = None
        self.text_color = None

        self.game_over = False

        # Variables used to manage our music.
        # -- from https://api.arcade.academy/en/latest/examples/background_music.html#background-music
        self.current_song_index = 0
        self.current_player = None
        self.music = None
        self.volume = 0.25
        self.mute = bool
        self.clear_sound = arcade.load_sound("resources/my_sounds/ruler_swoop.mp3")

        self.dark_mode = bool

        self.level = 0
        self.score = 0
        self.rotation = 0

    def setup(self):
        """ Set up the game variables. Call to re-start the game. """
        # Create sprites and sprite lists here
        # Create a list containing the board (bunch of 0's with some 1's)
        self.board = new_board(ROW_COUNT, COL_COUNT, False)
        if not self.dark_mode:
            arcade.set_background_color(self.light_background)
        else:
            arcade.set_background_color(self.dark_background)

        # For each row, and each column in that row, create a sprite and append textures and positions
        # Just a plain board of squares
        self.board_sprite_list = arcade.SpriteList()
        for row in range(len(self.board)):
            for column in range(len(self.board[0])):
                sprite = arcade.Sprite()
                for texture in texture_list:
                    sprite.append_texture(texture)
                # Background colors
                sprite.set_texture(0)
                sprite.center_x = (MARGIN + WIDTH) * column + MARGIN + WIDTH // 2
                sprite.center_y = SCREEN_HEIGHT - (MARGIN + HEIGHT) * row + MARGIN + HEIGHT // 2
                self.board_sprite_list.append(sprite)

        # Create our next board
        self.next_board = new_board(4, 4, True)

        # Play music
        # current_song_index is what to play
        self.current_song_index = random.randint(0, len(MUSIC_LIST) - 1)
        if self.mute:
            self.volume = 0
        self.play_song()

        self.level = 1
        self.score = 0

        # Figure out our text color
        self.text_color = (247, 147, 30)
        if not self.dark_mode:
            self.text_color = (47, 64, 77)

        # Load our shapes and update board
        self.next_shape = SHAPES[random.randint(0, 6)]
        self.new_shape()
        self.update_board()

    def new_shape(self):
        """ Randomly select new shape - create at top of screen"""
        self.shape = self.next_shape
        self.next_shape = random.choice(SHAPES)

        # Work out the x value - take it from the middle of columns rounded to the left
        self.shape_x = int(COL_COUNT / 2 - len(self.shape[0]) + 1)
        self.shape_y = 0
        self.rotation = 0

        # Collision checking for game over
        if check_collision(self.board, self.shape, (self.shape_x, self.shape_y)):
            self.game_over = True

    # noinspection PyMethodMayBeStatic
    def draw_shapes(self, shape_matrix, offset_x, offset_y):
        """
        Draw the shape matrix over the board. Used to draw the falling shapes. The board is drawn
        by the sprite list. PREVIOUSLY draw_grid
        """
        # Draw the grid/shapes
        # break down the matrix into each number and draw accordingly
        for row in range(len(shape_matrix)):
            for column in range(len(shape_matrix[0])):
                # Figure out what color to draw the box
                if shape_matrix[row][column]:
                    # Gets the number of a place in the matrix (eg 1) and selects the corresponding color
                    color = COLORS[shape_matrix[row][column]]

                    # Do the math to figure out where the box is
                    x = (MARGIN + WIDTH) * (column + offset_x) + MARGIN + WIDTH // 2
                    y = SCREEN_HEIGHT - (MARGIN + HEIGHT) * (row + offset_y) + MARGIN + HEIGHT // 2

                    # Draw the box
                    arcade.draw_rectangle_filled(x, y, WIDTH, HEIGHT, color)

    def on_draw(self):
        """ Render the screen """
        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        arcade.start_render()

        # Draw main board and shapes
        self.board_sprite_list.draw()
        self.draw_shapes(self.shape, self.shape_x, self.shape_y)

        # Draw Level and Score text
        arcade.draw_text("LEVEL:",
                         LEVEL_TEXT_XY[0], LEVEL_TEXT_XY[1],
                         self.text_color, TITLE_FONT_SIZE, font_name="Neuropol Nova Regular")

        arcade.draw_text(str(self.level),
                         LEVEL_NUM_TEXT_XY[0], LEVEL_NUM_TEXT_XY[1],
                         self.text_color, TITLE_FONT_SIZE, font_name="Neuropol Nova Regular")

        arcade.draw_text("SCORE:",
                         SCORE_TEXT_XY[0], SCORE_TEXT_XY[1],
                         self.text_color, TITLE_FONT_SIZE, font_name="Neuropol Nova Regular")

        arcade.draw_text(str(self.score),
                         SCORE_NUM_TEXT_XY[0], SCORE_NUM_TEXT_XY[1],
                         self.text_color, TITLE_FONT_SIZE, font_name="Neuropol Nova Regular")

        # Draw next shape and black background to display our next shapes
        arcade.draw_text("NEXT:",
                         SCORE_NUM_TEXT_XY[0], 470,
                         self.text_color, TITLE_FONT_SIZE, font_name="Neuropol Nova Regular")
        arcade.draw_rectangle_filled(457.5, 442 - 35, 145, 105, (0, 0, 0))
        self.draw_shapes(self.next_shape, 11, 11)

        # Draw user control instructions at bottom
        arcade.draw_text("CONTROLS:\n\n"
                         "Z  X to rotate.\n\n"
                         "L  R arrow keys \n"
                         "to move sideways.\n\n"
                         "DOWN arrow key \n"
                         "to drop.\n\n"
                         "M to mute.",
                         SCORE_NUM_TEXT_XY[0], 100,
                         self.text_color, TITLE_FONT_SIZE - 7, font_name="Neuropol Nova Regular")

    def drop(self):
        """
        Drop the tetromino down one space.
        Check for collision:
        If collision:
            Join matrices
            Check if line can be cleared
            Update sprite list with new shape
            Create a new sprite
        """
        if not self.game_over:
            # Drop shape down by 1
            self.shape_y += 1
            # Check if the shape collides with anything on the board
            if check_collision(self.board, self.shape, (self.shape_x, self.shape_y)):
                self.board = join_matrixes(self.board, self.shape, (self.shape_x, self.shape_y))
                # Loop to check for line clearing
                while True:
                    # self.board[:-1] makes sure our bottom row doesnt get deleted (checks every row except the last)
                    for row_num, row in enumerate(self.board[:-1]):
                        # if row doesnt have a 0 - delete it
                        if 0 not in row:
                            self.board = remove_row(self.board, row_num)
                            self.score += int(200 / self.level)

                            arcade.play_sound(self.clear_sound, 0.5)
                            self.level = check_level(self.level, self.score)
                            break
                    else:
                        break

                self.update_board()
                self.new_shape()

    def rotate_shape(self, rotate_anticlockwise):
        """
        Rotate the shape and re-draw it
        This is done by creating a new matrix, rotating each individual tile relative to a
        center block, putting them back into the matrix and redrawing it on the board
        """
        if not self.game_over:
            # Create an empty matrix to load our rotated tiles into
            new_shape_matrix = [[0, 0, 0, 0],
                                [0, 0, 0, 0],
                                [0, 0, 0, 0],
                                [0, 0, 0, 0]]
            # Remember current rotation
            old_rotation = self.rotation
            # Find the new rotation - between 0 and 3
            new_rotation = calculate_rotation_num(rotate_anticlockwise, self.rotation)
            # Get shape type from center so we can re-color our new shape
            shape_type = self.shape[1][1]

            # Count_x, count_y is the x,y coordinates in the matrix
            # For each tile in the shape
            for count_y, row in enumerate(self.shape):
                for count_x, tile in enumerate(row):
                    # Filter out any 0's to get each tile
                    if tile:
                        # Find the new x and y coordinates of each tile
                        new_x, new_y = get_rotated_tile((count_x, count_y), (1, 1), rotate_anticlockwise)
                        # Add newly rotated tile to our matrix as the shape type
                        new_shape_matrix[new_y][new_x] = shape_type
            # Set the shape to the new matrix and update the board
            self.shape = new_shape_matrix
            self.rotation = new_rotation

            # Prevent the O shape from wobbling
            if shape_type == 7:
                # Get an offset based on shapes old and new rotation positions
                shape_x_offset, shape_y_offset = offset_o(old_rotation, self.rotation)
                self.shape_x += shape_x_offset
                self.shape_y += shape_y_offset

            # Check we didn't rotate off the board
            for count_y, y in enumerate(self.shape):
                for count_x, x in enumerate(y):
                    if x != 0:
                        if get_tile_coordinates_global((count_x, count_y), (self.shape_x, self.shape_y))[0] < 0:
                            self.shape_x = self.shape_x + 1

            # If a collision occurs - rotate shape back the opposite way.
            if check_collision(self.board, self.shape, (self.shape_x, self.shape_y)):
                self.rotate_shape(not rotate_anticlockwise)

            self.update_board()

    def update_board(self):
        """
         Update the sprite list to reflect the contents of the 2d grid
        """
        for row in range(len(self.board)):
            for column in range(len(self.board[0])):
                v = self.board[row][column]  # v = the number at each box location eg 0 or 1
                i = row * COL_COUNT + column  # i = position of each box within the sprite list
                self.board_sprite_list[i].set_texture(v)

    def on_update(self, delta_time):
        """
        Logic to keep track of time, drop the stone at set times
        Contains different times for different levels
        Game-over checking logic
        """
        self.frame_count += 1

        # Check what level we are on and drop at the corresponding frequency.
        if self.level == 1:
            if self.frame_count % 60 == 0:
                self.drop()
        elif self.level == 2:
            if self.frame_count % 45 == 0:
                self.drop()
        elif self.level == 3:
            if self.frame_count % 30 == 0:
                self.drop()
        elif self.level == 4:
            if self.frame_count % 20 == 0:
                self.drop()
        elif self.level == 5:
            if self.frame_count % 15 == 0:
                self.drop()
        elif self.level == 6:
            if self.frame_count % 10 == 0:
                self.drop()
        elif self.level == 7:
            if self.frame_count % 5 == 0:
                self.drop()

        position = self.music.get_stream_position(self.current_player)
        if position == 0.0:
            self.advance_song()
            self.play_song()

        if self.game_over:
            view = GameOverView()
            view.mute = self.mute
            view.score = self.score
            self.music.stop(self.current_player)
            self.window.show_view(view)

    def move(self, x_value):
        """
        :param x_value: delta x - the amount to move the shape across by
        :return: changes self.shape.x to the new_x value
        """
        if not self.game_over:
            # Set the new x value to current + amount to change
            new_x = self.shape_x + x_value
            # If it exceeds either boundary - set to boundary
            for count_y, y in enumerate(self.shape):
                for count_x, x in enumerate(y):
                    if x != 0:
                        if get_tile_coordinates_global((count_x, count_y), (new_x, self.shape_y))[0] < 0:
                            new_x = self.shape_x

            # If not colliding - change position
            if not check_collision(self.board, self.shape, (self.shape_x + x_value, self.shape_y)):
                self.shape_x = new_x

    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.
        """
        # Drop the shape down by 1 each key press
        if key == arcade.key.DOWN:
            new_y = self.shape_y + 1
            if not check_collision(self.board, self.shape, (self.shape_x, new_y)):
                self.shape_y = new_y
            self.drop()
        # Move left and right
        if key == arcade.key.LEFT:
            self.move(-1)
        if key == arcade.key.RIGHT:
            self.move(1)
        # Rotate shapes clockwise or anti-clockwise
        if key == arcade.key.Z:
            self.rotate_shape(True)
        if key == arcade.key.X:
            self.rotate_shape(False)
        # Mute
        if key == arcade.key.M:
            if not self.mute:
                self.mute = True
                self.music.stop(self.current_player)
            else:
                self.mute = False
                self.current_song_index = random.randint(0, len(MUSIC_LIST) - 1)
                self.volume = 0.25
                self.play_song()

    def advance_song(self):
        """ Advance our pointer to the next song. This does NOT start the song. """

        self.current_song_index += 1
        if self.current_song_index >= len(MUSIC_LIST):
            self.current_song_index = 0

    def play_song(self):
        """ Play the song. """
        # Stop what is currently playing.
        if self.music:
            self.music.stop(self.current_player)
        # Play the next song
        self.music = arcade.Sound(MUSIC_LIST[self.current_song_index], streaming=True)
        self.current_player = self.music.play(self.volume)
        # Quick delay to prevent accidental skipping
        time.sleep(0.03)


def main():
    """ Main Method """
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, TITLE)
    start_view = MenuView()
    window.show_view(start_view)
    start_view.setup()
    arcade.run()


if __name__ == "__main__":
    main()
