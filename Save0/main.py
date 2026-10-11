hay_on_stock=0
wood_on_stock=0
carrot_on_stock=0

pumpkin_ready = 0
pumpkin_harvest = True
def is_tree_cell( ):
	col = get_pos_x()
	row = get_pos_y()
	return (col % 2) != (row % 2)

while True:
	world_size = get_world_size()

	
	check_stock()
	
	if(get_pos_x() == 0) and (get_pos_y() == 0):
		pumpkin_harvest = False
		if pumpkin_ready > 47:
			pumpkin_harvest = True
		pumpkin_ready = 0
		
			
							
	if can_harvest():
		if get_entity_type() == Entities.Pumpkin:

			if pumpkin_harvest:
				harvest()
			else:
				pumpkin_ready+=1				
		else:
			harvest()
	# elif get_entity_type() == None:
	# 	repair_ground()

	#if (row == 1) and (col == 1):
	#	plant_sunflower()
					
	if num_items(Items.Hay) < 1500:
		plant_hay()
	
	elif num_items(Items.Wood) < 1500:
		if is_tree_cell():
			plant_tree()
		else:
			plant_bush()
	
	elif num_items(Items.Carrot) < 2100:
		plant_carrot()
			
	else:
		if num_items(Items.Pumpkin_Seed) < 10: 
				trade(Items.Pumpkin_Seed, 50)		
		if num_items(Items.Carrot) < 2120:
			plant_carrot()
		else:
			plant_pumpkin()
			
	if get_pos_y() == get_world_size()-1:						
		move(East)
	move(North)
