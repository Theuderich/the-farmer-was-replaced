import warehouse
import field
import layout_planner
import maze

HARVEST_SIMPLE = 0
HARVEST_ALL_PUMPKINS = 1
HARVEST_SUNFLOWER = 2
HARVEST_CACTUS = 3

active_demand = None
field_layout_in_progress = False
schedule_harvest_type = HARVEST_SIMPLE
field_layout = []
pumpkin_field_status = False

# field.clear_field()

field.init()
maze.init()


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


def do_harvest_sunflower_mix(loops):
	global field_layout_in_progress
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
			move_n(my_x - x, my_y - y)
			harvest()
			field.build_field(field_entity)
			field_layout_in_progress = False
		move_to_start()
	return
	


def do_harvest():
	global field_layout_in_progress

	pumpkin_field_status = False
	for col in range(get_world_size()):
		for row in range(get_world_size()):

			field_entity = get_entity_type()
			field.update_status_can_harvest(can_harvest())
			
			is_ready_to_harvest = can_harvest()
			if get_pos_x() == 0 and get_pos_y() == 0:
				if active_demand == Entities.Pumpkin:
					field_layout_in_progress = False
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
	global field_layout_in_progress
	while True:
		n_fields_spoiled = field.get_n_not_harvest()
		if n_fields_spoiled == 0:
			break
		for i in range(n_fields_spoiled):
			field.update_status_can_harvest(can_harvest())
			my_x = get_pos_x()
			my_y = get_pos_y()
			x,y = field.get_next_not_harvest()
			move_n(my_x - x, my_y - y)
			field.build_field(Entities.Pumpkin)
	harvest()
	field_layout_in_progress = False
	return
	
def do_harvest_cactus():
	global field_layout_in_progress
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
	move_to_start()
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
	# Sort field
	# while True:
	# 	my_x = get_pos_x()
	# 	my_y = get_pos_y()

	# 	move_n(my_x - x, my_y - y)
	# 	swap()
	# 	field.build_field(field_entity)
	# 	field_layout_in_progress = False
	move_to_start()
	move(South)
	move(West)
	change_hat(Hats.Pumpkin_Hat)
	harvest()
	return
	
def schedule():
	global field_layout_in_progress
	global schedule_harvest_type
	field_layout = []
	if not field_layout_in_progress:
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

def count_movements():
	directions = [North, East, South, West]
	count = 0
	for dir in directions:
		if can_move(dir):
			count += 1
	return count


def is_corner():
	return count_movements() > 2



move_to_start()
while True:
	
	demand = warehouse.get_demand()
	active_demand = Entities.Pumpkin


	make_labyrinth(5)
	maze.search_treasurt()
	move_to_start()

	# while True:
	# 	if get_entity_type() == Entities.Treasure:
	# 		harvest()
	# 		break
	# 	else:
	# 		tx, ty = measure()

	# apply_layout(layout_planner.layout_cactus())
	# do_harvest_cactus()
	# fertalize()
	# do_harvest()
	
	# field_layout = schedule()
	# apply_layout(field_layout)
	# # schedule_harvest_type = HAVEST_ALL_PUMPKINS
	# if schedule_harvest_type == HARVEST_SIMPLE:
	# 	do_harvest()
	# elif schedule_harvest_type == HARVEST_ALL_PUMPKINS:
	# 	do_harvest_pumpkins()
	# elif schedule_harvest_type == HARVEST_SUNFLOWER:
	# 	do_harvest_sunflower_mix(3)
	# elif schedule_harvest_type == HARVEST_CACTUS:
	# 	do_harvest_cactus()

	# field_layout = layout_planner.layout_sunflower()
	# apply_layout(field_layout)
	# do_harvest_sunflower_mix(3)