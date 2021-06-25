"""
Python Tetris Game

Sources:
Created using the arcade library
Link: https://arcade.academy/index.html
"""
import arcade
import random
import PIL
import numpy


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
SCREEN_WIDTH = (WIDTH + MARGIN) * COL_COUNT + MARGIN
SCREEN_HEIGHT = (HEIGHT + MARGIN) * ROW_COUNT + MARGIN
TITLE = "My Game | Tetris"

# List of colors based on the 8 official Tetris colors - (R,B,G) format.
colors = [(0,0,0),
          (128, 0, 128),  # purple - T block
          (255, 127, 0),  # Orange - L block
          (0, 0, 255),  # blue - J block
          (0, 255, 0),  # green - S block
          (255, 0, 0),  # red - Z block
          (255, 255, 0),  # Yellow - Square
          (0, 255, 255),  # light blue (cyan) - I block    #(127, 127, 127)# Grey - background
          (255, 255, 255), # WHITE - TESTING
          (0, 0, 10)  # black
          ]

# List containing the different tetrominoes - different numbers for colouring purposes
# it is done so we know our center piece is always at for shape in shapes -> shape[1][2]
shapes = [[[0, 1, 0],
           [1, 1, 1]],

          [[0, 0, 2],
           [2, 2, 2]],

          [[3, 0, 0],
           [3, 3, 3]],

          [[0, 4, 4],
           [4, 4, 0]],

          [[5, 5, 0],
           [0, 5, 5]],

          [[0, 6, 6],
           [0, 6, 6]],

          [[0, 0, 0, 0],
           [7, 7, 7, 7]]
          ]


def create_textures():
    """ Creates a list of color boxes using width + height and color list called"""
    new_textures = []
    # loop through the color list creating a image the size of our pixel for each color
    # Uses this image to create an arcade texture and add it to the list
    for color in colors:
        # Create a box
        # noinspection PyUnresolvedReferences
        image = PIL.Image.new('RGB', (WIDTH, HEIGHT), color)
        new_textures.append(arcade.Texture(str(color), image=image))
    return new_textures


texture_list = create_textures()


def new_board():
    """ Create a grid that is X cols by Y rows filled with 0's. """
    # Board has 0's equal to the num of columns and num of rows.
    board = [[0 for _x in range(COL_COUNT)] for _y in range(ROW_COUNT)]
    # Add 1's on the bottom for easier collision checking
    board += [[1 for _x in range(COL_COUNT)]]
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
            matrix_1[count_y + offset_y - 1][count_x + offset_x] += value
    return matrix_1


def remove_row(board, row):
    """ Remove a row from the board, add a blank row on top. """
    del board[row]
    return [[0 for _ in range(COL_COUNT)]] + board

# ROTATION CALCULATION FUNCTIONS


def calculate_rotation_num(rotate_clockwise, rotation_num):
    """
    A simple loop between 0 - 3 that calculates a new rotation
    number based on a boolean of clockwise
    """
    # calculate new rotation index
    if rotate_clockwise:
        new_rotation = rotation_num + 1
    else:
        new_rotation = rotation_num - 1
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

    # Find the relative position of a tile to the center tile (origin)
    relative_position_x = tile_x - center_tile_x
    relative_position_y = tile_y - center_tile_y

    # Create rotation matrix depending on which way we flip
    if clockwise:
        rotation_matrix = [[0, 1],
                           [-1, 0]]
    else:
        rotation_matrix = [[0, -1],
                           [1, 0]]

    # R x Vr = Vnew // Uses a rotation matrix to find the new x and y positions of our tiles
    new_postion_x = (rotation_matrix[0][0] * relative_position_x) + (rotation_matrix[0][1] * relative_position_y)
    new_postion_y = (rotation_matrix[1][0] * relative_position_x) + (rotation_matrix[0][0] * relative_position_y)

    print("rotation_matrix: "+ "\n" + str(rotation_matrix[0]) + "\n" + str(rotation_matrix[1]))

    # Put it back into it's correct place on the grid
    new_postion_x += center_tile_x
    new_postion_y += center_tile_y
    print("new_postion_x: " + str(new_postion_x))
    print("new_postion_y: " + str(new_postion_y))

    new_position = new_postion_x, new_postion_y
    return new_position


class Game(arcade.Window):
    """
    Main Application class for game
    Has multiple in-built functions from arcade library
    """
    def __init__(self, width, height, title):
        """ Initializer class. Code to be ran on launch """
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)
        # Put all sprite lists here = to "None"
        self.board = None
        self.board_sprite_list = None

        self.shape = None
        self.shape_x = 0
        self.shape_y = 0

        self.frame_count = 0

        self.level = 0
        self.rotation = 0

    def setup(self):
        """ Set up the game variables. Call to re-start the game. """
        # Create sprites and sprite lists here
        # Create a list containing the board (bunch of 0's with some 1's)
        self.board = new_board()

        # For each row, and each column in that row, create a sprite and append simple and positions
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

        self.level = 1

        self.new_shape()
        self.update_board()

    def new_shape(self):
        """ Randomly select new shape - create at top of screen - TO DO: add collision for game over soon"""
        self.shape = random.choice(shapes)
        # Work out the x value - take it from the middle of columns rounded to the left
        self.shape_x = int(COL_COUNT / 2 - len(self.shape[0]) + 1)
        self.shape_y = 0

        # ADD COLLISON CHECKING FOR GAME OVER

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
                    color = colors[shape_matrix[row][column]]

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
        # Call draw() on all your sprite lists below
        self.board_sprite_list.draw()
        self.draw_shapes(self.shape, self.shape_x, self.shape_y)

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
        # Drop shape down by 1
        #self.shape_y += 1
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
                        break
                else:
                    break

            self.update_board()
            self.new_shape()

    def rotate_shape(self, clockwise, should_offset):
        """
        Rotate the shape and re-draw it
        This is done by creating a new matrix, rotating each individual tile relative to a
        center block, putting them back into the matrix and redrawing it on the board
        """
        # Create an empty matrix to load our rotated tiles into
        new_shape_matrix = [[0, 0, 0, 0],
                            [0, 0, 0, 0],
                            [0, 0, 0, 0],
                            [0, 0, 0, 0]]

        # Remember current rotation
        old_rotation = self.rotation
        # find the new rotation - between 0 and 3
        new_rotation = calculate_rotation_num(clockwise, self.rotation)

        # The center tile always exists at shape[1][1]
        center_tile_coordinates = get_tile_coordinates_global((1, 1), (self.shape_x, self.shape_y))
        # Get shape type from center so we can re-color our new shape
        shape_type = self.shape[1][1]

        # Count_x, count_y is the xy coordinates in the matrix
        # For each tile in the shape
        for count_y, row in enumerate(self.shape):
            for count_x, tile in enumerate(row):
                # Filter out any 0's to get each tile
                if tile:
                    # Find the new x and y coordinates of each tile
                    new_x, new_y = get_rotated_tile((count_x, count_y), (1, 1), clockwise)

                    # Add newly rotated tile to our matrix as the shape type.
                    new_shape_matrix[new_y][new_x] = shape_type
        # Set the shape to the new matrix and update the board
        self.shape = new_shape_matrix

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
        Will contain different times for different levels later on
        """
        self.frame_count += 1

        if self.level == 1:
            if self.frame_count % 60 == 0:
                self.drop()
        elif self.level == 2:
            if self.frame_count % 30 == 0:
                self.drop()
        elif self.level == 3:
            if self.frame_count % 20 == 0:
                self.drop()
        elif self.level == 4:
            if self.frame_count % 10 == 0:
                self.drop()

    def move(self, x_value):
        """
        :param x_value: delta x - the amount to move the shape across by
        :return: changes self.shape.x to the new_x value
        """
        # Set the new x value to current + amount to change
        new_x = self.shape_x + x_value
        # If it exceeds either boundary - set to boundary
        if new_x < 0:
            new_x = 0
        if new_x > COL_COUNT - len(self.shape[0]):
            new_x = COL_COUNT - len(self.shape[0])
        # If not colliding - change position
        if not check_collision(self.board, self.shape, (self.shape_x + x_value, self.shape_y)):
            self.shape_x = new_x

    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.
        """
        # Drop the shape down by 1 each key press
        if key == arcade.key.DOWN:
            self.shape_y += 1
            self.drop()
        # Move left and right
        if key == arcade.key.LEFT:
            self.move(-1)
        if key == arcade.key.RIGHT:
            self.move(1)
        if key == arcade.key.Z:
            self.rotate_shape(False, True)
        if key == arcade.key.X:
            self.rotate_shape(True, True)


def main():
    """ Main Method """
    game = Game(SCREEN_WIDTH, SCREEN_HEIGHT, TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
