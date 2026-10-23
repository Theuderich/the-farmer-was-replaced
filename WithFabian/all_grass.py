for col in range(get_world_size()):
    for row in range(get_world_size()):
        if get_ground_type() == Grounds.Soil:
            till()
        move(North)
    move(West)      