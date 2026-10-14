field_can_harvest = []

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
	if get_ground_type() == Grounds.Grassland:
		till()
	plant(Entities.Pumpkin)
	field_can_harvest[_get_list_index(get_pos_x(), get_pos_y())] = False

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

																					