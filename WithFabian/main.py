import warehouse
import field
import layout_planner


active_demand = None
field_layout_in_progress = False
field_layout = []
pumpkin_field_status = False

field.clear_field()
field.init()


def apply_layout(layout):
	if target_field == Entities.Pumpkin:
		field.build_pumpkin()
	elif target_field == Entities.Tree:
		field.build_tree()
	elif target_field == Entities.Carrot:
		field.build_carrot()
	elif target_field == Entities.Grass:
		field.build_grass()


def do_harvest():
	global field_layout_in_progress
	global pumpkin_field_status

	is_ready_to_harvest = can_harvest()

	if get_pos_x() == 0 and get_pos_y() == 0:
		if active_demand == Entities.Pumpkin:
			is_ready_to_harvest = pumpkin_field_status
			field_layout_in_progress = False
			pumpkin_field_status = field.is_ready(col, row, Entities.Pumpkin)

	if get_entity_type() == Entities.Pumpkin:
		is_ready_to_harvest = pumpkin_field_status

	if is_ready_to_harvest:
		harvest()

	
while True:
	
	demand = warehouse.get_demand()
	active_demand = Entities.Pumpkin


	for col in range(get_world_size()):
		for row in range(get_world_size()):

			field.update_status_can_harvest(can_harvest())
			do_harvest()

			if field.is_start_position() and not field_layout_in_progress:
				if warehouse.is_basics_full():
					field_layout = layout_planner.layout_all_pumpkin()
					field_layout_in_progress = True
				else:
					field_layout = layout_planner.layout_basic_flex_demands()
					
			target_field = field_layout[field._get_list_index(col, row)]
			apply_layout(target_field)
				
			move(North)	

		move(East)