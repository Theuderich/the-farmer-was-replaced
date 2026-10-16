import field
import warehouse

def layout_all_pumpkin():
	field_list = []
	for x in range(field.get_n_fields()):
		field_list.append(Entities.Pumpkin)
	return field_list


def layout_pumpkin_sizeable(pumpkin_size):
	field_list = []
	for col in range(get_world_size()):
		for row in range(get_world_size()):
			if ( col < pumpkin_size and row < pumpkin_size ):
				field_list.append(Entities.Pumpkin)
			else:
				nr = field.get_field_index()
				if nr % 2 == 0:
					field_list.append(Entities.Tree)
				if col <= get_world_size() / 2:
					field_list.append(Entities.Carrot)
				else:
					field_list.append(Entities.Grass)
	return field_list

	
def layout_basic_flex_demands():
	n_fields = field.get_n_fields()
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
									