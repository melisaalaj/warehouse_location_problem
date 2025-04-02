from solution import Solution

def generate_initial_solution(problem):
    """
    Generate an initial solution that respects:
    1. The total quantity of goods taken from a warehouse cannot exceed its capacity
    2. The total quantity of goods brought to a store must be exactly equal to its request
    3. Goods can be moved only from open warehouses
    
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
                remaining_capacity = warehouse.get_remaining_capacity()
                if remaining_capacity > 0:
                    cost = supply_cost[store_id][wh_id]
                    # Include fixed cost if warehouse is not yet open
                    if not warehouse.is_open:
                        # Amortize the fixed cost over the expected usage
                        # This is a heuristic to decide when to open a new warehouse
                        expected_usage = min(demand, remaining_capacity)
                        amortized_fixed_cost = warehouse.fixed_cost / expected_usage
                        cost += amortized_fixed_cost
                    
                    if cost < best_cost:
                        best_cost = cost
                        best_wh = wh_id
            
            if best_wh != -1:
                # Determine how much to assign to this warehouse
                quantity = min(demand, warehouses[best_wh].get_remaining_capacity())
                solution.add_assignment(store_id, best_wh, quantity)
                demand -= quantity
            else:
                # No warehouse has enough capacity - this is a problem!
                print(f"Warning: Could not assign all demand for store {store_id+1} due to capacity constraints")
                break
    
    return solution