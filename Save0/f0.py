
def check_stock():
	hay_on_stock = num_items(Items.Hay)
	wood_on_stock = num_items(Items.Wood)
	carrot_on_stock = num_items(Items.Carrot)
	
def get_total_stock():
	return hay_on_stock + wood_on_stock + carrot_on_stock

def is_hay_needed():
	return hay_on_stock / get_total_stock() < 0.5
	
def is_wood_needed():
	return wood_on_stock / get_total_stock() < 0.25
	
def is_carrot_needed():
	return carrot_on_stock / get_total_stock() < 0.25
		
	