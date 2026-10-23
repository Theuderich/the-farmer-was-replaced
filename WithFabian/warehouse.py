
warehouse_targets = {Items.Hay:20000, Items.Wood:10000, Items.Carrot:3000, Items.Pumpkin:10000, Items.Power:500}

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

def get_demand_ratio(item):
    item_num = num_items(item)
    if item_num > warehouse_targets[item]:
        return 0
    return ( item_num / warehouse_targets[item] - 1 ) * -1

def is_basics_full():
    hay_demand = get_demand_ratio(Items.Hay)
    wood_demand = get_demand_ratio(Items.Wood)
    carrot_demand = get_demand_ratio(Items.Carrot)
    average_demand = hay_demand + wood_demand + carrot_demand
    return average_demand == 0

def is_energy_available():
    return get_demand_ratio(Items.Power) > warehouse_targets[Items.Power]