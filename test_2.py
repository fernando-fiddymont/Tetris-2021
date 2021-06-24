
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

print(shape_type)






