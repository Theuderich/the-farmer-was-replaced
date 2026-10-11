def plant_hay():
	if get_ground_type() == Grounds.Soil:
		till()
	plant(Entities.Grass)

def plant_bush():
	if get_ground_type() == Grounds.Soil:
		till()
	plant(Entities.Bush)

def plant_tree():
	if get_ground_type() == Grounds.Soil:
		till()
	plant(Entities.Tree)
	
def plant_carrot():
	if get_ground_type() != Grounds.Soil:
		till()
	if num_items(Items.Carrot_Seed) < 1:
		trade(Items.Carrot_Seed,10)
	plant(Entities.Carrots)	

def plant_sunflower():
	if get_ground_type() != Grounds.Soil:
		till()
	if num_items(Items.Sunflower_Seed) < 1: 
		trade(Items.Sunflower_Seed, 10)
	plant(Entities.Sunflower)	
		
def plant_pumpkin():
	if get_ground_type() != Grounds.Soil:
		till()
	
	plant(Entities.Pumpkin)	
		
def repair_ground():
	plant_hay()