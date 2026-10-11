import warehouse
import field

active_demand = None
field.clear_field()
field.init()

while True:
	
	demand = warehouse.get_demand()
	active_demand = Entities.Pumpkin

	for col in range(get_world_size()):
		for row in range(get_world_size()):
			
			is_ready_to_harvest = can_harvest()
			if get_pos_x() == 0 and get_pos_y() == 0:
				if active_demand == Entities.Pumpkin:
					is_ready_to_harvest = field.is_ready(col, row, Entities.Pumpkin)
			if is_ready_to_harvest:
				harvest()

			target_field = field.planungsmuster_pumpkin(col, row)
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