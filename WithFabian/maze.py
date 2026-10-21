n_edge = get_world_size()
n_fields = get_world_size() * get_world_size()

list_dirs = [North, East, South, West]
mem_maze_cell_status = []


def init():
	for field_index in range(n_fields):
		mem_maze_cell_status.append(None)

def get_list_index(x, y):
	return y + (x * n_edge)

def where_am_i():
	return get_pos_x(), get_pos_y()

def set_my_cell_status(status):
	x, y = where_am_i()
	mem_maze_cell_status[get_list_index(x, y)] = status

def coordinate_move(dir):
	x, y = where_am_i()
	if dir == North:
		y += 1
	elif dir == East:
		x += 1
	elif dir == South:
		y -= 1
	elif dir == West:
		x -= 1
	return x, y

def get_dir_status(dir):
	dir_x, dir_y = coordinate_move(dir)
	dir_list_index = get_list_index(dir_x, dir_y)
	return mem_maze_cell_status[dir_list_index]

def is_dir_known(dir):
	return get_dir_status(dir) == None

def is_dir_status_smaller(dir, compare):
	return get_dir_status(dir) < compare
	
def count_movements():
	directions = [North, East, South, West]
	count = 0
	for dir in directions:
		if can_move(dir):
			count += 1
	return count


def is_corner():
	return count_movements() > 2


def search_treasurt():
	step_count = 1
	back_tracking_active = False
	back_tracking_last_status = n_fields
	while True:
		if get_entity_type() == Entities.Treasure:
			harvest()
			return
		if not back_tracking_active:
			set_my_cell_status(step_count)
			have_moved = False
			for dir in list_dirs:
				if not have_moved and can_move(dir) and is_dir_known(dir):
					move(dir)
					have_moved = True
			if have_moved:
				step_count += 1
			else:
				back_tracking_active = True
				back_tracking_last_status = step_count
				change_hat(Hats.Purple_Hat)
		else:
			have_moved = False
			for dir in list_dirs:
				if not have_moved and can_move(dir) and is_dir_status_smaller(dir, back_tracking_last_status):
					move(dir)
					have_moved = True
					back_tracking_last_status = get_dir_status(dir)
			if have_moved:
				if is_corner():
					change_hat(Hats.Straw_Hat)
					back_tracking_active = False
			
			# harvest()
			# return
			


			