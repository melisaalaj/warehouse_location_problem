def order_stores_by_demand(stores):
    """Sort stores by demand (highest first)."""
    store_ids = list(range(len(stores)))
    store_ids.sort(key=lambda i: stores[i].demand, reverse=True)
    return store_ids

def order_warehouses_by_cost_efficiency(warehouses):
    """Sort warehouses by cost-efficiency (lowest cost per capacity first)."""
    warehouse_ids = list(range(len(warehouses)))
    warehouse_ids.sort(key=lambda i: warehouses[i].fixed_cost / warehouses[i].capacity)
    return warehouse_ids
