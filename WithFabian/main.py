import warehouse
import field
import layout_planner

HARVEST_SIMPLE = 0
HARVEST_ALL_PUMPKINS = 1


active_demand = None
field_layout_in_progress = False
schedule_harvest_type = HARVEST_SIMPLE
field_layout = []
pumpkin_field_status = False

field.clear_field()
field.init()

def move_n(nx, ny):
	for ix in range(nx):
		move(West)
	for iy in range(ny):
		move(South)


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
	n_fields_spoiled = field.get_n_not_harvest()
	for i in range(n_fields_spoiled):
		field.update_status_can_harvest(can_harvest())
		my_x = get_pos_x()
		my_y = get_pos_y()
		x,y = field.get_next_not_harvest()
		move_n(my_x - x, my_y - y)
		field.build_field(Entities.Pumpkin)
	return
	

def schedule():
	global field_layout_in_progress
	global schedule_harvest_type
	field_layout = []
	if not field_layout_in_progress:
		if warehouse.is_basics_full():
			field_layout = layout_planner.layout_all_pumpkin()
			field_layout_in_progress = True
			schedule_harvest_type = HARVEST_ALL_PUMPKINS
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


while True:
	
	demand = warehouse.get_demand()
	active_demand = Entities.Pumpkin

	field_layout = schedule()
	apply_layout(field_layout)
	if schedule_harvest_type == HARVEST_SIMPLE:
		do_harvest()
	elif schedule_harvest_type == HARVEST_ALL_PUMPKINS:
		do_harvest_pumpkins()