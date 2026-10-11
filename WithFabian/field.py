field_can_harvest = []

pumpkin_field_size = 6

def init():
	n_fields = get_world_size() * get_world_size()
	for x in range(n_fields):
			field_can_harvest.append(None)

def _get_list_index(x, y):
	return y + (x * get_world_size())

def is_sector_ready(x, x_, y, y_):
	all_ready = True
	for ix in range(x_-x):
		for iy in range(y_-y):
			if field_can_harvest[_get_list_index(x + ix, y + iy)] != True:
				all_ready = False
	return all_ready
	
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



def planungsmuster_wood(col, row):
	field_type = Entities.Grass
	nr = col * row
	if nr % 2 == 0:
		field_tyoe = Entities.Tree

def planungsmuster_pumpkin(col, row):
	if ( col < pumpkin_field_size and row < pumpkin_field_size ):
		return Entities.Pumpkin
	nr = row + ( row * get_world_size() )
	nr = nr + ( col % 2 )
	if nr % 2 == 0:
		return Entities.Tree
	if col <= 5:
		return Entities.Carrot
	else:
		return Entities.Grass
										

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

																					