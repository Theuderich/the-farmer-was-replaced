HARVEST_SIMPLE = 0
HARVEST_ALL_PUMPKINS = 1
HARVEST_SUNFLOWER = 2
HARVEST_CACTUS = 3

def do_harvest_sunflower_mix(loops):
    for cycle in range(loops):
        for col in range(get_world_size()):
            for row in range(get_world_size()):
                field.update_status_can_harvest(can_harvest())
                field.update_my_measure()
                field_entity = get_entity_type()
                if field_entity != Entities.Sunflower:
                    harvest()
                    field.build_field(field_entity)
                move(North) 
            move(East)

        for field_nr in range(field.get_n_fields()/2):
            my_x = get_pos_x()
            my_y = get_pos_y()
            x,y = field.get_coordinates_best_sunflower()
            movement.move_n(my_x - x, my_y - y)
            harvest()
            field.build_field(field_entity)
        movement.move_to_start()
    return
    


def do_harvest():
    pumpkin_field_status = False
    for col in range(get_world_size()):
        for row in range(get_world_size()):

            field_entity = get_entity_type()
            field.update_status_can_harvest(can_harvest())
            
            is_ready_to_harvest = can_harvest()
            if get_pos_x() == 0 and get_pos_y() == 0:
                if active_demand == Entities.Pumpkin:
                    pumpkin_field_status = field.is_ready(col, row, Entities.Pumpkin)
                    is_ready_to_harvest = pumpkin_field_status

            if get_entity_type() == Entities.Pumpkin:
                is_ready_to_harvest = pumpkin_field_status

            if is_ready_to_harvest:
                harvest()
                field.build_field(field_entity)

            move(North) 
        move(East)

def do_harvest_pumpkins():
    while True:
        n_fields_spoiled = field.get_n_not_harvest()
        if n_fields_spoiled == 0:
            break
        for i in range(n_fields_spoiled):
            field.update_status_can_harvest(can_harvest())
            my_x = get_pos_x()
            my_y = get_pos_y()
            x,y = field.get_next_not_harvest()
            field.move_n(my_x - x, my_y - y)
            field.build_field(Entities.Pumpkin)
    harvest()
    return
    
def do_harvest_cactus():
    # Scan size and status first
    for outer_index in range(get_world_size()):
        for col in range(get_world_size()):
            is_swapped = False
            for row in range(get_world_size()):
                if get_pos_y() < get_world_size() - 1:
                    if measure() > measure(North):
                        swap(North)
                        is_swapped = True
                move(North) 
            if not is_swapped:
                break
            move(North)
        move(East)
    movement.move_to_start()
    for outer_index in range(get_world_size()):
        for col in range(get_world_size()):
            is_swapped = False
            for row in range(get_world_size()):
                if get_pos_x() < get_world_size() - 1:
                    if measure() > measure(East):
                        swap(East)
                        is_swapped = True
                move(East)  
            if not is_swapped:
                break
            move(East)
        move(North)
    movement.move_to_start()
    move(South)
    move(West)
    change_hat(Hats.Pumpkin_Hat)
    harvest()
    return

