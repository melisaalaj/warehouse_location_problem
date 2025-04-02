def validate_solution(problem, solution):
    """
    Validate if a solution respects:
    1. The total quantity of goods taken from a warehouse cannot exceed its capacity
    2. The total quantity of goods brought to a store must be exactly equal to its request
    3. Goods can be moved only from open warehouses
    
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
    
    # NOTE: Incompatibility constraints are intentionally NOT checked in this version
    # We're only focusing on capacity and demand constraints for now
    
    return True, "Solution is valid (only checking capacity and demand constraints)"