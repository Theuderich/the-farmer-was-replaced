import warehouse
import field
import layout_planner
import maze

HARVEST_NONE = 0
HARVEST_SIMPLE = 1
HARVEST_ALL_PUMPKINS = 2
HARVEST_SUNFLOWER = 3
HARVEST_CACTUS = 4

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
	# print(my_x)
	my_y = get_pos_y()
	# print(my_y)
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

def move_to(x, y):
	my_x = get_pos_x()
	my_y = get_pos_y()
	move_n(my_x - x, my_y - y)


def do_harvest_sunflower_mix():
	global field_layout_in_progress
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

def do_harvest_bones():
	next_x = 0
	next_y = 0
	move_to_start()
	my_x = get_pos_x()
	my_y = get_pos_y()
	change_hat(Hats.Dinosaur_Hat)
	#
	move_dir = East
	move_count = 0
	do_catch_apple = False
	do_catch_count = 0
	num_apple_harvested = 0
	world_size = get_world_size()
	while True:
		if get_entity_type() == Entities.Apple:
			next_x, next_y = measure()
			num_apple_harvested += 1
		if num_apple_harvested == 16:
			change_hat(Hats.Straw_Hat)
			return
		# Catch loop
		if next_x != 0 or next_x != world_size or next_y != 0 or next_y != world_size:
			if move_dir == East and do_catch_apple == False and (my_x == next_x or my_x == next_x - 1):
				do_catch_apple = True
				move_dir = North
				do_catch_count = 0 
			if do_catch_apple == True and do_catch_count == world_size - 2:
				move_dir = East
			elif do_catch_apple == True and do_catch_count == world_size - 1:
				move_dir = South
			elif do_catch_apple == True and do_catch_count == 2 * world_size - 1:
				move_dir = East
			elif do_catch_apple == True and do_catch_count == 2 * world_size:
				do_catch_apple = False
		# Go North
		if move_dir == East and my_x == world_size - 1:
			move_dir = North
		# Go West
		if move_dir == North and my_y == world_size - 1:
			move_dir = West
		# Go South
		if move_dir == West and my_x == 0:
			move_dir = South
		# Go East	
		if move_dir == South and my_y == 0:
			move_dir = East

		could_move = move(move_dir)
		move_count += 1
		do_catch_count += 1
		my_x = get_pos_x()
		my_y = get_pos_y()
		# move_to(next_x, next_y)

	

SCHEDULE_NOTHING = 0
SCHEDULE_BASIC_FLEX = 1
SCHEDULE_SUNFLOWER = 2
SCHEDULE_PUMPKIN = 3
SCHEDULE_CACTUS = 4
SCHEDULE_MAZE = 5
SCHEDULE_BONES = 6
SCHEDULE_WIRED_SUBSTANCE = 7

	
def schedule(crop_rotation):
	for crop in crop_rotation:
		if crop == SCHEDULE_BASIC_FLEX:
			field_layout = layout_planner.layout_basic_flex_demands()
			apply_layout(field_layout)
			do_harvest()
		elif crop == SCHEDULE_SUNFLOWER: 
			field_layout = layout_planner.layout_sunflower()
			apply_layout(field_layout)
			do_harvest_sunflower_mix()
		elif crop == SCHEDULE_PUMPKIN:
			field_layout = layout_planner.layout_all_pumpkin()
			apply_layout(field_layout)
			do_harvest_pumpkins()
		elif crop == SCHEDULE_MAZE:
			make_labyrinth(10)
			maze.search_treasure_turn_right()
			# maze.search_treasure_back_tracking()
			move_to_start()
		elif crop == SCHEDULE_CACTUS:
			field_layout = layout_planner.layout_cactus()
			apply_layout(field_layout)
			do_harvest_cactus()
			pass
		elif crop == SCHEDULE_BONES:
			do_harvest_bones()
		elif crop == SCHEDULE_WIRED_SUBSTANCE:
			field_layout = layout_planner.layout_all_grass()
			apply_layout(field_layout)
			fertalize()
			do_harvest()

def apply_layout(field_layout):
	for col in range(get_world_size()):
		for row in range(get_world_size()):
			if can_harvest():
				harvest()
			if len(field_layout) > 0:
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

change_hat(Hats.Straw_Hat)
move_to_start()

# crop_rotation_plan = [SCHEDULE_WIRED_SUBSTANCE, SCHEDULE_SUNFLOWER, SCHEDULE_CACTUS, SCHEDULE_MAZE, SCHEDULE_PUMPKIN]
crop_rotation_plan = [SCHEDULE_BONES]
while True:
	
	# demand = warehouse.get_demand()
	# active_demand = Entities.Pumpkin

	schedule(crop_rotation_plan)