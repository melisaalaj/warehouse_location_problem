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
        """
        Create a perturbed copy of the current solution.
        This introduces randomness to explore different solutions.
        """
        new_solution = copy.deepcopy(self)
        problem = self.problem
        
        strategy = random.choice(['reassign', 'transfer', 'split', 'merge'])
        
        if strategy == 'reassign':
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
            
            # Get all available warehouses (with capacity and no incompatibilities)
            available_warehouses = []
            demand = store.demand
            
            for wh_id, warehouse in enumerate(problem.get_warehouses()):
                if warehouse.get_remaining_capacity() > 0:
                    # Check incompatibility
                    incompatible = any(
                        store_id in problem.get_stores()[s_id].incompatible_stores
                        for (s_id, wid, _) in new_solution.assignments if wid == wh_id
                    )
                    if not incompatible:
                        available_warehouses.append(wh_id)
            
            # Shuffle available warehouses to introduce randomness
            random.shuffle(available_warehouses)
            
            # Assign to random warehouses
            while demand > 0 and available_warehouses:
                wh_id = available_warehouses.pop(0)
                warehouse = problem.get_warehouses()[wh_id]
                
                # Assign a random portion or all of the remaining demand
                if random.random() < 0.5 and len(available_warehouses) > 0:
                    # Split the demand
                    max_qty = min(demand, warehouse.get_remaining_capacity())
                    quantity = random.randint(1, max_qty) if max_qty > 1 else max_qty
                else:
                    # Assign all remaining demand
                    quantity = min(demand, warehouse.get_remaining_capacity())
                
                if quantity > 0:
                    new_solution.add_assignment(store_id, wh_id, quantity)
                    demand -= quantity
            
            # If we couldn't assign all demand, revert to greedy approach
            if demand > 0:
                for wh_id in order_warehouses_by_cost_efficiency(problem.get_warehouses()):
                    warehouse = problem.get_warehouses()[wh_id]
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
            
        elif strategy == 'transfer':
            # Transfer some demand from one warehouse to another
            # Get all current assignments
            store_assignments = new_solution.get_store_assignments()
            if not store_assignments:
                return new_solution
            
            # Pick a random store that has assignments
            store_id = random.choice(list(store_assignments.keys()))
            assignments = store_assignments[store_id]
            
            if len(assignments) == 0:
                return new_solution
            
            # Pick a source warehouse
            source_wh_id, qty = random.choice(assignments)
            
            # Reset warehouse usages
            for warehouse in problem.get_warehouses():
                warehouse.current_usage = 0
                warehouse.is_open = False
            for s_id, wh_id, q in new_solution.assignments:
                problem.get_warehouses()[wh_id].add_usage(q)
            
            # Find potential target warehouses
            target_warehouses = []
            for wh_id, warehouse in enumerate(problem.get_warehouses()):
                if wh_id != source_wh_id and warehouse.get_remaining_capacity() > 0:
                    # Check incompatibility
                    incompatible = any(
                        store_id in problem.get_stores()[s_id].incompatible_stores
                        for (s_id, wid, _) in new_solution.assignments if wid == wh_id
                    )
                    if not incompatible:
                        target_warehouses.append(wh_id)
            
            if not target_warehouses:
                return new_solution
            
            # Select a random target warehouse
            target_wh_id = random.choice(target_warehouses)
            target_wh = problem.get_warehouses()[target_wh_id]
            
            # Determine transfer amount
            transfer_amount = random.randint(1, min(qty - 1, target_wh.get_remaining_capacity())) if qty > 1 else 0
            
            if transfer_amount > 0:
                # Update assignments
                new_assignments = []
                for s_id, wh_id, q in new_solution.assignments:
                    if s_id == store_id and wh_id == source_wh_id:
                        new_assignments.append((s_id, wh_id, q - transfer_amount))
                    else:
                        new_assignments.append((s_id, wh_id, q))
                
                # Add the new assignment
                new_assignments.append((store_id, target_wh_id, transfer_amount))
                
                # Replace assignments
                new_solution.assignments = new_assignments
                
                # Reset warehouse usages again
                for warehouse in problem.get_warehouses():
                    warehouse.current_usage = 0
                    warehouse.is_open = False
                for s_id, wh_id, q in new_solution.assignments:
                    problem.get_warehouses()[wh_id].add_usage(q)
            
        elif strategy == 'split':
            # Split a store's demand across more warehouses
            store_assignments = new_solution.get_store_assignments()
            if not store_assignments:
                return new_solution
            
            # Find stores with single warehouse assignment
            single_assigned_stores = [
                s_id for s_id, assignments in store_assignments.items()
                if len(assignments) == 1 and assignments[0][1] > 1  # Quantity > 1
            ]
            
            if not single_assigned_stores:
                return new_solution
            
            # Pick a random store
            store_id = random.choice(single_assigned_stores)
            wh_id, qty = store_assignments[store_id][0]
            
            # Reset warehouse usages
            for warehouse in problem.get_warehouses():
                warehouse.current_usage = 0
                warehouse.is_open = False
            for s_id, w_id, q in new_solution.assignments:
                problem.get_warehouses()[w_id].add_usage(q)
            
            # Find potential target warehouses for splitting
            target_warehouses = []
            for new_wh_id, warehouse in enumerate(problem.get_warehouses()):
                if new_wh_id != wh_id and warehouse.get_remaining_capacity() > 0:
                    # Check incompatibility
                    incompatible = any(
                        store_id in problem.get_stores()[s_id].incompatible_stores
                        for (s_id, w, _) in new_solution.assignments if w == new_wh_id
                    )
                    if not incompatible:
                        target_warehouses.append(new_wh_id)
            
            if not target_warehouses:
                return new_solution
            
            # Select a random target warehouse
            target_wh_id = random.choice(target_warehouses)
            target_wh = problem.get_warehouses()[target_wh_id]
            
            # Determine split amount
            split_amount = random.randint(1, min(qty - 1, target_wh.get_remaining_capacity()))
            
            if split_amount > 0:
                # Update assignments
                new_assignments = []
                for s_id, w_id, q in new_solution.assignments:
                    if s_id == store_id and w_id == wh_id:
                        new_assignments.append((s_id, w_id, q - split_amount))
                    else:
                        new_assignments.append((s_id, w_id, q))
                
                # Add the new assignment
                new_assignments.append((store_id, target_wh_id, split_amount))
                
                # Replace assignments
                new_solution.assignments = new_assignments
                
                # Reset warehouse usages again
                for warehouse in problem.get_warehouses():
                    warehouse.current_usage = 0
                    warehouse.is_open = False
                for s_id, w_id, q in new_solution.assignments:
                    problem.get_warehouses()[w_id].add_usage(q)
        
        elif strategy == 'merge':
            # Merge assignments from multiple warehouses into one
            store_assignments = new_solution.get_store_assignments()
            if not store_assignments:
                return new_solution
            
            # Find stores with multiple warehouse assignments
            multi_assigned_stores = [
                s_id for s_id, assignments in store_assignments.items()
                if len(assignments) > 1
            ]
            
            if not multi_assigned_stores:
                return new_solution
            
            # Pick a random store
            store_id = random.choice(multi_assigned_stores)
            assignments = store_assignments[store_id]
            
            # Pick random source and target warehouses from its assignments
            indices = random.sample(range(len(assignments)), 2)
            source_wh_id, source_qty = assignments[indices[0]]
            target_wh_id, target_qty = assignments[indices[1]]
            
            # Update assignments
            new_assignments = []
            for s_id, wh_id, qty in new_solution.assignments:
                if s_id == store_id and wh_id == source_wh_id:
                    # Skip this assignment, we'll merge it
                    pass
                elif s_id == store_id and wh_id == target_wh_id:
                    # Merge the quantities
                    new_assignments.append((s_id, wh_id, qty + source_qty))
                else:
                    new_assignments.append((s_id, wh_id, qty))
            
            # Replace assignments
            new_solution.assignments = new_assignments
            
            # Reset warehouse usages
            for warehouse in problem.get_warehouses():
                warehouse.current_usage = 0
                warehouse.is_open = False
            for s_id, wh_id, qty in new_solution.assignments:
                problem.get_warehouses()[wh_id].add_usage(qty)
        
        return new_solution
