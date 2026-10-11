import warehouse
import field

active_demand = None
#field.clear_field()
field.init()

while True:
	
	demmand = warehouse.get_demand()
	
	for col in range(get_world_size()):
		for row in range(get_world_size()):
			
			is_section_ready = field.is_ready(col, row, Entities.Pumpkin)
			if is_section_ready == True:
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