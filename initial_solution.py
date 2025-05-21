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

    if ordering_operator == "demand":
        store_ids = order_stores_by_demand(stores)
    elif ordering_operator == "cost_efficiency":
        store_ids = list(range(len(stores)))  
    elif ordering_operator == "random":
        warehouse_ids = list(range(len(warehouses)))
        if len(warehouse_ids) > 1:
            wh1, wh2 = random.sample(warehouse_ids, 2)
            warehouses[wh1], warehouses[wh2] = warehouses[wh2], warehouses[wh1]
    else:
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