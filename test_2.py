import arcade
shape = [[0, 1, 0],
         [1, 1, 1]]

# HERE FOR SAFE KEEPING
def get_rotated_tile(tile_coordinates, center_tile_coordinates, clockwise):
    """ Find the rotated coordinates of a tile relative to a center tile"""
    tile_x, tile_y = tile_coordinates
    center_tile_x, center_tile_y = center_tile_coordinates

    print("tile_x: " + str(tile_x) )
    print("tile_y: " + str(tile_y) )


    # Find the relative position of a tile to the center tile (origin)
    relative_position_x = tile_x - center_tile_x
    relative_position_y = tile_y - center_tile_y

    # Create rotation matrix depending on which way we flip
    if clockwise:
        rotation_matrix = [[1, 0],
                           [0, -1]]
    else:
        rotation_matrix = [[0, -1],
                           [1, 0]]

    # R x Vr = Vnew // Uses a rotation matrix to find the new x and y positions of our tiles
    new_postion_x = (rotation_matrix[0][0] * relative_position_x) + (rotation_matrix[0][1] * relative_position_y)
    new_postion_y = (rotation_matrix[1][0] * relative_position_x) + (rotation_matrix[0][0] * relative_position_y)
    print("new_position_x: " + str(new_postion_x) )
    print("new_position_y: " + str(new_postion_y) + "\n")

    # Put it back into it's correct place on the grid
    #new_postion_x += center_tile_x
    #new_postion_y += center_tile_y

    new_position = new_postion_x, new_postion_y
    return new_position


def get_tile_coordinates(tile_count_xy):
    """
    returns a x,y of each tile's global location on the grid
    """
    # Unpack given variables
    count_x, count_y = tile_count_xy
    # Do maths to find each tile's x and y relative to the top right hand corner of the matrix
    tile_pos_x = count_x
    tile_pos_y = count_y
    return tile_pos_x, tile_pos_y


for count_row, row in enumerate(shape):
    for count_tile, tile in enumerate(row):
        pass
        # if tile filters all the 0's
        # print("row: " + str(row))
        # print("count_y: " + str(count_row))
        # print("count_x: " + str(count_tile))
        # print("tile: " + str(tile))
        # print("tile_coordinates: " + str(get_tile_coordinates((count_row, count_tile)))+ "\n")

matrix = [[1,-1],
          [1,0],
          [0,0],
          [0,1]]
new_matrix = []

empty_matrix = [[0 for _x in range(4)] for _y in range(4)]

shape_type = 6

for row in matrix:
        empty_matrix[row[0]][row[1]] = shape_type

for count_y, row in enumerate(shape):
    for count_x, tile in enumerate(row):
        pass

center = (1,1)

shape_type = matrix[1][1]


test_index = 0
conditions = test_index < 5

while test_index < 5:
    test_index += 1


matrix = [[0, 0, 1, 0],
          [0, 1, 1, 0],
          [1, 1, 0, 0],
          [1, 1, 0, 0]]

def minus_xy_array(array_a, array_b):
    """ Function to minus array B from array A (coordinates). Will return a [x, y] list"""
    a_x_value, a_y_value = array_a[0], array_a[1]
    b_x_value, b_y_value = array_b[0], array_b[1]

    new_x_value = a_x_value - b_x_value
    new_y_value = a_y_value - b_y_value

    return new_x_value, new_y_value


print(minus_xy_array((0, -1), (0, 0)))




def offset(board, shape_matrix, old_rotation, new_rotation, clockwise):
    """ Offset tings
    ?
    /"""
    offset_val_1 = 0
    offset_val_2 = 0  # vector 2int??
    end_offset_val = 0
    cur_type = shape_matrix[1][1]
    JLSZT_OFFSET_DATA = [[[0, 0], [0, 0], [0, 0], [0, 0], [0, 0]],
                         [[0, 0], [1, 0], [1, -1], [0, 2], [1, 2]],
                         [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0]],
                         [[0, 0], [-1, 0], [-1, -1], [0, 2], [-1, 2]]]


    # Get the right offset data for each shape
    if cur_type == 6:
        cur_offset_data = O_OFFSET_DATA
    elif cur_type == 7:
        cur_offset_data = I_OFFSET_DATA
    else:
        cur_offset_data = JLSZT_OFFSET_DATA

    move_possible = False
    test_index = 0

    # Make sure we only test the amount required based on shape type
    if cur_type == 6:
        conditions = test_index == 0
    elif cur_type == 7:
        conditions = test_index < 4
    else:
        conditions = test_index < 4

    while conditions:
        # Get the end offset
        offset_val_1 = cur_offset_data[test_index][old_rotation]
        offset_val_2 = cur_offset_data[test_index][new_rotation]

        end_offset_val = minus_xy_array(offset_val_1, offset_val_2)
        print("old rotation: " + str(old_rotation))
        print("new rotation: " + str(new_rotation))
        print("offset_val_1: " + str(offset_val_1))
        print("offset_val_2: " + str(offset_val_2))
        print("end_offset_val: " + str(end_offset_val) + "\n")

        # see if the new offset collides
        if not check_collision(board, shape_matrix, end_offset_val):
            move_possible = True
            return move_possible, end_offset_val
            # Break the while loop
        else:
            test_index += 1

    if move_possible:
        pass
    else:
        return move_possible, (0, 0)
