def validate_solution(problem, solution):
    """
    Validate if a solution respects ONLY warehouse capacity constraints.
    Returns a tuple (is_valid, error_message)
    """
    warehouses = problem.get_warehouses()
    stores = problem.get_stores()
    
    # Check warehouse capacity constraints
    for wh_id, usage in enumerate(solution.warehouse_usage):
        if usage > warehouses[wh_id].capacity:
            return False, f"Warehouse {wh_id+1} is overloaded: {usage} > {warehouses[wh_id].capacity}"
    
    # Check if all store demands are satisfied
    store_assignments = solution.get_store_assignments()
    for store_id, store in enumerate(stores):
        total_assigned = sum(qty for _, qty in store_assignments.get(store_id, []))
        if total_assigned != store.demand:
            return False, f"Store {store_id+1} demand not satisfied: {total_assigned} ≠ {store.demand}"
    
    # NOTE: Incompatibility constraints are intentionally NOT checked in this version
    # We're only focusing on capacity constraints for now
    
    return True, "Solution is valid (only checking capacity constraints)" 