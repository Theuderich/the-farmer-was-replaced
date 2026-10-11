import warehouse
import field

active_demand = None
field.clear_field()
field.init()

while True:
	
	demand = warehouse.get_demand()
	active_demand = Entities.Pumpkin
	pumpkin_field_status = False

	field_layout = []
	field_layout_in_progress = False

	for col in range(get_world_size()):
		for row in range(get_world_size()):

			field.update_status_can_harvest(can_harvest())
			is_ready_to_harvest = can_harvest()

			if get_pos_x() == 0 and get_pos_y() == 0:
				if active_demand == Entities.Pumpkin:
					pumpkin_field_status = field.is_ready(col, row, Entities.Pumpkin)
					is_ready_to_harvest = pumpkin_field_status
					field_layout_in_progress = False

			if get_entity_type() == Entities.Pumpkin:
				is_ready_to_harvest = pumpkin_field_status
	
			if is_ready_to_harvest:
				harvest()

			if field.is_start_position() and not field_layout_in_progress:
				if warehouse.is_basics_full():
					field_layout = field.planungsmuster_basic_flex_demands()
				else:
					field_layout = field.planungsmuster_all_pumpkin()
					field_layout_in_progress = True

			# target_field = field.planungsmuster_all_pumpkin()
			# target_field = field.planungsmuster_pumpkin(col, row)
			target_field = field_layout[field._get_list_index(col, row)]
			if target_field == Entities.Pumpkin:
				field.build_pumpkin()
			elif target_field == Entities.Tree:
				field.build_tree()
			elif target_field == Entities.Carrot:
				field.build_carrot()
			elif target_field == Entities.Grass:
				field.build_grass()
				
				
			move(North)	

		move(East)