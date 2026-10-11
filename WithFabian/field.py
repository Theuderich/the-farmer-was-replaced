import warehouse

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

def planungsmuster_all_pumpkin():
	field_list = []
	for x in range(get_world_size()):
		for y in range(get_world_size()):
			field_list.append(Entities.Pumpkin)
	return field_list

def planungsmuster_pumpkin(col, row):
	if ( col < pumpkin_field_size and row < pumpkin_field_size ):
		return Entities.Pumpkin
	nr = get_field_index()
	if nr % 2 == 0:
		return Entities.Tree
	if col <= 5:
		return Entities.Carrot
	else:
		return Entities.Grass
										
def planungsmuster_basic_flex_demands():
	n_fields = get_n_fields()
	wood_demand = warehouse.get_demand_ratio(Items.Wood)
	n_fields_tree = n_fields / 2 * wood_demand
	carrot_demand = warehouse.get_demand_ratio(Items.Carrot)
	n_fields_carrot = n_fields - n_fields_tree
	field_list = []
	for x in range(get_world_size()):
		for y in range(get_world_size()):
			field_appended = False
			nr = y + ( y * get_world_size() )
			nr = nr + ( x % 2 )
			if nr % 2 == 0:
				if n_fields_tree > 0:
					n_fields_tree -= 1
					field_list.append(Entities.Tree)
					field_appended = True
				else:
					n_fields_carrot += 1
			if not field_appended and n_fields_carrot > 0:
				n_fields_carrot -= 1
				field_list.append(Entities.Carrot)
				field_appended = True
			if not field_appended:
				field_list.append(Entities.Grass)

	return field_list
				

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

																					