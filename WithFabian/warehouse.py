def get_demand():
	demand = [Entities.Pumpkin]
	if num_items(Items.Wood) < 1000:
		demand.insert(0, Items.wood)
	else:
		demand.append(Items.wood)
	if num_items(Items.Carrot) < 1000:
		demand.insert(0, Items.Carrot)
	else:
		demand.append(Items.Carrot)
	if num_items(Items.Pumpkin) < 1000:
		demand.insert(0, Items.Pumpkin)
	else:
		demand.append(Items.Pumpkin)
					