import warehouse
import movement
import field
import layout_planner
import harvest
import maze

active_demand = None
field_layout_in_progress = False
schedule_harvest_type = HARVEST_SIMPLE
field_layout = []
pumpkin_field_status = False

# field.clear_field()

field.init()
maze.init()


    
def schedule():
    global schedule_harvest_type
    field_layout = []
        if warehouse.is_basics_full() and num_items(Items.Pumpkin) < 100000:
            field_layout = layout_planner.layout_all_pumpkin()
            field_layout_in_progress = True
            schedule_harvest_type = HARVEST_ALL_PUMPKINS
        elif warehouse.is_energy_available(): 
            field_layout = layout_planner.layout_sunflower()
            field_layout_in_progress = True
            schedule_harvest_type = HARVEST_SUNFLOWER
        elif num_items(Items.Cactus) < 10000:
            field_layout = layout_planner.layout_cactus()
            schedule_harvest_type = HARVEST_CACTUS
        else:
            field_layout = layout_planner.layout_basic_flex_demands()
            schedule_harvest_type = HARVEST_SIMPLE
    return field_layout
    

def apply_layout(field_layout):
    for col in range(get_world_size()):
        for row in range(get_world_size()):
            if can_harvest():
                harvest()
            target_field = field_layout[field._get_list_index(col, row)]
            field.build_field(target_field)
            move(North) 
        move(East)

def fertalize():
    for col in range(get_world_size()):
        for row in range(get_world_size()):
            use_item(Items.Fertilizer)
            move(North) 
        move(East)

def make_labyrinth(size):
    field.clear_field()
    plant(Entities.Bush)
    use_item(Items.Weird_Substance, size)



movement.move_to_start()

fertalize()
do_harvest()
    
field_layout = layout_planner.layout_sunflower()
apply_layout(field_layout)
do_harvest_sunflower_mix(3)



while True:
    
    demand = warehouse.get_demand()
    active_demand = Entities.Pumpkin


    make_labyrinth(10)
    maze.search_treasure_turn_right()
    # maze.search_treasure_back_tracking()
    movement.move_to_start()

    # while True:
    #   if get_entity_type() == Entities.Treasure:
    #       harvest()
    #       break
    #   else:
    #       tx, ty = measure()

    # apply_layout(layout_planner.layout_cactus())
    # do_harvest_cactus()
    # fertalize()
    # do_harvest()
    
    # field_layout = schedule()
    # apply_layout(field_layout)
    # # schedule_harvest_type = HAVEST_ALL_PUMPKINS
    # if schedule_harvest_type == HARVEST_SIMPLE:
    #   do_harvest()
    # elif schedule_harvest_type == HARVEST_ALL_PUMPKINS:
    #   do_harvest_pumpkins()
    # elif schedule_harvest_type == HARVEST_SUNFLOWER:
    #   do_harvest_sunflower_mix(3)
    # elif schedule_harvest_type == HARVEST_CACTUS:
    #   do_harvest_cactus()

    # field_layout = layout_planner.layout_sunflower()
    # apply_layout(field_layout)
    # do_harvest_sunflower_mix(3)
