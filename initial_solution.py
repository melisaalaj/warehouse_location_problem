from solution import Solution

def generate_initial_solution(problem):
    """
    Generate an initial solution that respects ONLY warehouse capacity constraints.
    Simple greedy approach: assign each store to the cheapest warehouse that has capacity.
    """
    solution = Solution(problem)
    stores = problem.get_stores()
    warehouses = problem.get_warehouses()
    supply_cost = problem.get_supply_cost()
    
    # Sort stores by demand (descending) to place larger demands first
    store_ids = list(range(len(stores)))
    store_ids.sort(key=lambda i: stores[i].demand, reverse=True)
    
    for store_id in store_ids:
        store = stores[store_id]
        demand = store.demand
        
        # Find the cheapest warehouse with enough capacity
        while demand > 0:
            best_wh = -1
            best_cost = float('inf')
            
            for wh_id, warehouse in enumerate(warehouses):
                remaining_capacity = warehouse.capacity - solution.warehouse_usage[wh_id]
                if remaining_capacity > 0:
                    cost = supply_cost[store_id][wh_id]
                    if cost < best_cost:
                        best_cost = cost
                        best_wh = wh_id
            
            if best_wh != -1:
                # Determine how much to assign to this warehouse
                quantity = min(demand, warehouses[best_wh].capacity - solution.warehouse_usage[best_wh])
                solution.add_assignment(store_id, best_wh, quantity)
                demand -= quantity
            else:
                # No warehouse has enough capacity - this is a problem!
                print(f"Warning: Could not assign all demand for store {store_id+1} due to capacity constraints")
                break
    
    return solution 