def move_to_start():
    my_x = get_pos_x()
    print(my_x)
    my_y = get_pos_y()
    print(my_y)
    move_n( my_x, my_y )

def move_n(nx, ny):
    x_dir = West
    if nx < 0:
        nx = abs(nx)
        x_dir = East
    if nx == get_world_size() - 1:
        nx = 1
        if x_dir == West:
            x_dir = East
        else:
            x_dir = West
    y_dir = South
    if ny < 0:
        ny = abs(ny)
        y_dir = North
    if ny == get_world_size() - 1:
        ny = 1
        if y_dir == North:
            y_dir = South
        else:
            y_dir = North
    for ix in range(nx):
        move(x_dir)
    for iy in range(ny):
        move(y_dir)

