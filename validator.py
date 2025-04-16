def validate_solution(problem, solution):
    """
    Validate if a solution respects:
    1. The total quantity of goods taken from a warehouse cannot exceed its capacity
    2. The total quantity of goods brought to a store must be exactly equal to its request
    3. Goods can be moved only from open warehouses
    4. Two incompatible stores cannot be supplied by the same warehouse
    
    Returns a tuple (is_valid, error_message)
    """
    warehouses = problem.get_warehouses()
    stores = problem.get_stores()
    
    # Check warehouse capacity constraints
    for wh in warehouses:
        if wh.current_usage > wh.capacity:
            return False, f"Warehouse {wh.id+1} is overloaded: {wh.current_usage} > {wh.capacity}"
    
    # Check if all store demands are satisfied exactly
    store_assignments = solution.get_store_assignments()
    for store_id, store in enumerate(stores):
        total_assigned = sum(qty for _, qty in store_assignments.get(store_id, []))
        if total_assigned != store.demand:
            return False, f"Store {store_id+1} demand not satisfied: {total_assigned} ≠ {store.demand}"
    
    # Check that goods are only moved from open warehouses
    for store_id, wh_id, quantity in solution.assignments:
        if not warehouses[wh_id].is_open:
            return False, f"Goods are moved from closed warehouse {wh_id+1} to store {store_id+1}"
    
    # Check incompatibility constraints
    # Group stores by warehouse
    warehouse_stores = {}
    for store_id, wh_id, _ in solution.assignments:
        if wh_id not in warehouse_stores:
            warehouse_stores[wh_id] = set()
        warehouse_stores[wh_id].add(store_id)
    
    # Check for incompatible stores assigned to the same warehouse
    for wh_id, store_set in warehouse_stores.items():
        for store_id in store_set:
            store = stores[store_id]
            for incomp_store_id in store.incompatible_stores:
                if incomp_store_id in store_set:
                    return False, f"Incompatible stores {store_id+1} and {incomp_store_id+1} are assigned to the same warehouse {wh_id+1}"
    
    return True, "Solution is valid"