field_can_harvest = []
pumpkin_path_forward = True

# pumpkin_field_size = get_world_size()
pumpkin_field_size = 7

def get_n_fields():
	return get_world_size() * get_world_size()

def is_start_position():
	return get_pos_x() == 0 and get_pos_y() == 0

def init():
	n_fields = get_n_fields()
	for x in range(n_fields):
			field_can_harvest.append(None)

def _get_list_index(x, y):
	return y + (x * get_world_size())

def get_coordinates(list_index):
	x = list_index // get_world_size()
	y = list_index % get_world_size()
	return x, y

def get_n_not_harvest():
	global field_can_harvest
	n = 0
	for i in range(get_n_fields()):
		if field_can_harvest[i] != True:
			n += 1
	return n

def check_fiels_limits(list_iterator):
	global pumpkin_path_forward
	n_fields = get_n_fields()
	if list_iterator < 0:
		list_iterator = 1
		pumpkin_path_forward = True
	if list_iterator > n_fields:
		list_iterator = n_fields - 1
		pumpkin_path_forward = False
	return list_iterator

def get_next_not_harvest():
	global field_can_harvest
	global pumpkin_path_forward
	my_x = get_pos_x()
	my_y = get_pos_y()
	my_list_index = _get_list_index(my_x, my_y)
	n_fields = get_n_fields()
	# my_harvest_status = field_can_harvest[my_list_index]
	# if my_harvest_status == False:
	# 	return my_x, my_y
	# else:
	if pumpkin_path_forward:
		list_iterator = my_list_index + 1
	else:
		list_iterator = my_list_index - 1
	list_iterator = check_fiels_limits(list_iterator)
		
	while list_iterator < n_fields and list_iterator >= 0:
		if field_can_harvest[list_iterator] != True:
			return get_coordinates(list_iterator)
		if pumpkin_path_forward:
			list_iterator += 1
		else:
			list_iterator -= 1
		list_iterator = check_fiels_limits(list_iterator)
	return 0,0

def update_status_can_harvest(status_can_harvest):
	field_can_harvest[_get_list_index(get_pos_x(), get_pos_y())] = status_can_harvest
	
def is_sector_ready(x, x_, y, y_):
	for ix in range(x_-x):
		for iy in range(y_-y):
			if field_can_harvest[_get_list_index(x + ix, y + iy)] != True:
				return False
	return True
	
def is_pumpkin_field_ready():
	return is_sector_ready(0, pumpkin_field_size, 0, pumpkin_field_size)

def check_harvest_pumpkin(col, row):
	if col < pumpkin_field_size and row < pumpkin_field_size:
		field_can_harvest[_get_list_index(col, row)] = can_harvest()
		return is_pumpkin_field_ready()
	return can_harvest()
			

def is_ready(col, row, planungsmuster):
	if planungsmuster == Entities.Pumpkin:
		return check_harvest_pumpkin(col, row)

def get_field_index():
	nr = get_pos_y() + ( get_pos_y() * get_world_size() )
	nr = nr + ( get_pos_x() % 2 )
	return nr
	
def planungsmuster_wood(col, row):
	field_type = Entities.Grass
	nr = col * row
	if nr % 2 == 0:
		field_tyoe = Entities.Tree

def get_type(col, row, demand):
	field_type = Entities.Grass
	nr = col * row
	if nr % 2 == 0:
		field_tyoe = Entities.Tree

def clear_field():
	clear()

def build_pumpkin():
	if get_entity_type() == Entities.Pumpkin and can_harvest() == True:
		return
	field_can_harvest[_get_list_index(get_pos_x(), get_pos_y())] = False
	if get_ground_type() == Grounds.Grassland:
		till()
	plant(Entities.Pumpkin)

def build_tree():
	if get_ground_type() == Grounds.Soil:
		till()
	plant(Entities.Tree)

def build_carrot():
	if get_ground_type() == Grounds.Grassland:
		till()
	plant(Entities.Carrot)

def build_grass():
	if get_ground_type() == Grounds.Soil:
		till()

def build_field(target_field):
	if target_field == Entities.Pumpkin:
		build_pumpkin()
	elif target_field == Entities.Tree:
		build_tree()
	elif target_field == Entities.Carrot:
		build_carrot()
	elif target_field == Entities.Grass:
		build_grass()

																				