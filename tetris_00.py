"""
Python Tetris Game

Sources:
Created using the arcade library
Link: https://arcade.academy/index.html
"""
import arcade
import random
import PIL

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
print(SCREEN_WIDTH,SCREEN_HEIGHT)
# List of colors based on the 8 official Tetris colors - (R,B,G) format.
colors = [(0, 255, 255), (255, 255, 0), (128, 0, 128),
          (0, 255, 0), (255, 0, 0), (0, 0, 255),
          (255, 127, 0), (127, 127, 127)
          ]

shapes = []


def create_textures():
    """ Creates a list of color boxes using width + height and color list called"""
    new_textures = []
    # loop through the color list creating a image the size of our pixel for each color
    # Uses this image to create an arcade texture and add it to the list
    for color in colors:
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


class Tetris():
    box_size = 100
    gird_width = 10
    grid_height = 40

    def get_width(self):
        return self.gird_width

    def get_height(self):
        return self.grid_height

    def get_box_size(self):
        return self.box_size


class Game(arcade.Window):
    """
    Main Application class for game
    Has multiple in-built functions from arcade library
    """

    def __init__(self, width, height, title):
        """ Initializer class. Code to be ran on launch """
        super().__init__(width, height, title)

        arcade.set_background_color(arcade.color.AMARANTH_PINK)

        # Put all sprite lists here = to "None"
        self.board = None
        self.board_sprite_list = None

    def setup(self):
        """ Set up the game variables. Call to re-start the game. """
        # Create sprites and sprite lists here
        # Create a list containing the board (bunch of 0's with some 1's)
        self.board = new_board()

        # For each row, and each column in that row, create a sprite and append textures and positions
        self.board_sprite_list = arcade.SpriteList()
        for row in range(len(self.board)):
            for column in range(len(self.board[0])):
                sprite = arcade.Sprite()
                for texture in texture_list:
                    sprite.append_texture(texture)
                sprite.set_texture(0)
                sprite.center_x = (MARGIN + WIDTH) * column + MARGIN + WIDTH // 2
                sprite.center_y = SCREEN_HEIGHT - (MARGIN + HEIGHT) * row + MARGIN + HEIGHT // 2
                self.board_sprite_list.append(sprite)

    def on_draw(self):
        """ Render the screen """
        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        arcade.start_render()
        # Call draw() on all your sprite lists below
        self.board_sprite_list.draw()

    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that need it.
        """
        pass

    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.

        For a full list of keys, see:
        http://arcade.academy/arcade.key.html
        """
        pass


def main():
    """ Main Method """
    game = Game(SCREEN_WIDTH, SCREEN_HEIGHT, TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
