def move_n(nx, ny):
    for ix in range(nx):
        move(West)
    for iy in range(ny):
        move(South)

my_x = get_pos_x()
print(my_x)
my_y = get_pos_y()
print(my_y)
move_n( my_x, my_y )
