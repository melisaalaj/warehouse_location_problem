import random
from solution import Solution
from solution import Solution
from utils import order_stores_by_demand, order_warehouses_by_cost_efficiency

def generate_initial_solution(problem, ordering_operator="random"):
    """
    Generate an initial solution that respects:
    1. The total quantity of goods taken from a warehouse cannot exceed its capacity
    2. The total quantity of goods brought to a store must be exactly equal to its request
    3. Goods can be moved only from open warehouses
    4. Two incompatible stores cannot be supplied by the same warehouse
    """
    solution = Solution(problem)
    stores = problem.get_stores()
    warehouses = problem.get_warehouses()
    supply_cost = problem.get_supply_cost()

    warehouse_stores = {wh_id: set() for wh_id in range(len(warehouses))}

    store_ids = list(range(len(stores)))
    warehouse_ids = list(range(len(warehouses)))  # Define this early

    if ordering_operator == "demand":
        store_ids = order_stores_by_demand(stores)
    elif ordering_operator == "random":
        if len(warehouse_ids) > 1:
            wh1, wh2 = random.sample(warehouse_ids, 2)
            warehouses[wh1], warehouses[wh2] = warehouses[wh2], warehouses[wh1]
    elif ordering_operator != "cost_efficiency":
        raise ValueError("Invalid ordering operator. Choose 'demand', 'cost_efficiency', or 'random'.")


    for store_id in store_ids:
        store = stores[store_id]
        demand = store.demand

        while demand > 0:
            best_wh = -1
            best_cost = float('inf')

            warehouse_ids = order_warehouses_by_cost_efficiency(warehouses)

            for wh_id in warehouse_ids:
                warehouse = warehouses[wh_id]
                remaining_capacity = warehouse.get_remaining_capacity()
                if remaining_capacity > 0:
                    incompatible = any(
                        store_id in stores[assigned_store_id].incompatible_stores
                        for assigned_store_id in warehouse_stores[wh_id]
                    )

                    if incompatible:
                        continue

                    cost = supply_cost[store_id][wh_id]

                    if not warehouse.is_open:
                        expected_usage = min(demand, remaining_capacity)
                        amortized_fixed_cost = warehouse.fixed_cost / expected_usage
                        cost += amortized_fixed_cost

                    if cost < best_cost:
                        best_cost = cost
                        best_wh = wh_id

            if best_wh != -1:
                quantity = min(demand, warehouses[best_wh].get_remaining_capacity())
                solution.add_assignment(store_id, best_wh, quantity)
                warehouse_stores[best_wh].add(store_id)
                demand -= quantity
            else:
                print(f"Warning: Could not assign all demand for store {store_id+1} due to constraints")
                break

    return solution

def generate_initial_solution_with_randomization(problem, randomization=0.3):
    """
    Generate a high-quality initial solution that balances optimization with controlled randomness.
    This uses a priority-based approach with cost-driven assignments and strategic randomization
    to produce different high-quality solutions each time.
    
    Parameters:
    - problem: The warehouse location problem instance
    - randomization: How much randomness to introduce (0.0 to 1.0)
    """
    solution = Solution(problem)
    stores = problem.get_stores()
    warehouses = problem.get_warehouses()
    supply_cost = problem.get_supply_cost()

    warehouse_stores = {wh_id: set() for wh_id in range(len(warehouses))}
    
    # Create store priorities based on both demand and cost
    store_priorities = []
    for store_id, store in enumerate(stores):
        avg_cost = sum(supply_cost[store_id]) / len(supply_cost[store_id])
        priority = store.demand * avg_cost
        store_priorities.append((store_id, priority))
    
    store_priorities.sort(key=lambda x: x[1], reverse=True)
    if randomization > 0:
        chunk_size = max(1, int(len(store_priorities) * randomization))
        for i in range(0, len(store_priorities), chunk_size):
            chunk = store_priorities[i:i+chunk_size]
            random.shuffle(chunk)
            store_priorities[i:i+chunk_size] = chunk
    
    store_ids = [s[0] for s in store_priorities]
    
    for store_id in store_ids:
        store = stores[store_id]
        demand = store.demand
        assigned_warehouses = []

        while demand > 0:
            valid_warehouses = []
            
            for wh_id in range(len(warehouses)):
                warehouse = warehouses[wh_id]
                remaining_capacity = warehouse.get_remaining_capacity()
                
                if remaining_capacity <= 0:
                    continue
                
                incompatible = any(
                    store_id in stores[assigned_store_id].incompatible_stores
                    for assigned_store_id in warehouse_stores[wh_id]
                )
                
                if incompatible:
                    continue
                
                # Calculate total cost (supply cost + fixed cost if not open)
                cost = supply_cost[store_id][wh_id]
                if not warehouse.is_open:
                    expected_usage = min(demand, remaining_capacity)
                    amortized_fixed_cost = warehouse.fixed_cost / expected_usage
                    cost += amortized_fixed_cost

                if randomization > 0:
                    variation = cost * randomization * (random.random() * 2 - 1)
                    cost += variation
                
                valid_warehouses.append((wh_id, cost, remaining_capacity))
    
            valid_warehouses.sort(key=lambda x: x[1])
            
            selection_range = max(1, int(len(valid_warehouses) * randomization))
            if selection_range > 1 and random.random() < randomization:
                selection_idx = random.randint(0, min(selection_range, len(valid_warehouses) - 1))
                wh_id, _, capacity = valid_warehouses[selection_idx]
            else:
                wh_id, _, capacity = valid_warehouses[0]
            
            if random.random() < randomization and demand > 1 and len(valid_warehouses) > 1:
                min_qty = max(1, int(demand * 0.3)) 
                max_qty = min(demand, capacity)
                
                if min_qty >= max_qty:
                    quantity = max_qty
                else:
                    quantity = random.randint(min_qty, max_qty)
            else:
                quantity = min(demand, capacity)
            
            solution.add_assignment(store_id, wh_id, quantity)
            warehouse_stores[wh_id].add(store_id)
            demand -= quantity
            
            if wh_id not in assigned_warehouses:
                assigned_warehouses.append(wh_id)
    
    return solution