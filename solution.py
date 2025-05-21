from utils import order_warehouses_by_cost_efficiency
import random
import copy

class Solution:
    def __init__(self, problem):
        self.problem = problem
        self.assignments = []  # List of (store_id, warehouse_id, quantity)
        
    def add_assignment(self, store_id, warehouse_id, quantity):
        self.assignments.append((store_id, warehouse_id, quantity))
        self.problem.get_warehouses()[warehouse_id].add_usage(quantity)
        
    def get_store_assignments(self):
        store_assignments = {}
        for store_id, wh_id, qty in self.assignments:
            if store_id not in store_assignments:
                store_assignments[store_id] = []
            store_assignments[store_id].append((wh_id, qty))
        return store_assignments

    def get_total_cost(self):
        supply_cost = 0
        opening_cost = 0
        for store_id, wh_id, quantity in self.assignments:
            supply_cost += self.problem.get_supply_cost()[store_id][wh_id] * quantity
        for warehouse in self.problem.get_warehouses():
            if warehouse.is_open:
                opening_cost += warehouse.fixed_cost
        return supply_cost + opening_cost, supply_cost, opening_cost

    def to_triples_format(self):
        triples = []
        for store_id, wh_id, quantity in self.assignments:
            triples.append((store_id + 1, wh_id + 1, quantity))
        return triples
    
    def cost(self):
        """Returns only the total cost (used by Simulated Annealing)."""
        return self.get_total_cost()[0]


    def copy_and_perturb(self):
        new_solution = copy.deepcopy(self)
        problem = self.problem

        store_id = random.randint(0, len(problem.get_stores()) - 1)
        store = problem.get_stores()[store_id]

        # Remove all assignments for the selected store
        new_solution.assignments = [
            (s_id, wh_id, qty) for (s_id, wh_id, qty) in new_solution.assignments if s_id != store_id
        ]

        # Reset warehouse usages
        for warehouse in problem.get_warehouses():
            warehouse.current_usage = 0
            warehouse.is_open = False
        for s_id, wh_id, qty in new_solution.assignments:
            problem.get_warehouses()[wh_id].add_usage(qty)

        # Reassign the store to feasible warehouses
        demand = store.demand
        warehouses = problem.get_warehouses()

        for wh_id in order_warehouses_by_cost_efficiency(warehouses):
            warehouse = warehouses[wh_id]
            if warehouse.get_remaining_capacity() == 0:
                continue

            # Check incompatibility
            incompatible = any(
                store_id in problem.get_stores()[s_id].incompatible_stores
                for (s_id, wid, _) in new_solution.assignments if wid == wh_id
            )
            if incompatible:
                continue

            quantity = min(demand, warehouse.get_remaining_capacity())
            new_solution.add_assignment(store_id, wh_id, quantity)
            demand -= quantity
            if demand == 0:
                break

        return new_solution
