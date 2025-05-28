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
        strategy = random.choice([
            'tweak_reassign_warehouses',
            'tweak_transfer_between_warehouses',
            'tweak_split_store_demand',
            'tweak_merge_store_assignments'
        ])
        return getattr(new_solution, strategy)()

    def tweak_reassign_warehouses(self):
        problem = self.problem
        store_id = random.randint(0, len(problem.get_stores()) - 1)
        store = problem.get_stores()[store_id]
        self.assignments = [
            (s_id, wh_id, qty) for (s_id, wh_id, qty) in self.assignments if s_id != store_id
        ]
        for warehouse in problem.get_warehouses():
            warehouse.current_usage = 0
            warehouse.is_open = False
        for s_id, wh_id, qty in self.assignments:
            problem.get_warehouses()[wh_id].add_usage(qty)
        available_warehouses = []
        demand = store.demand
        for wh_id, warehouse in enumerate(problem.get_warehouses()):
            if warehouse.get_remaining_capacity() > 0:
                incompatible = any(
                    store_id in problem.get_stores()[s_id].incompatible_stores
                    for (s_id, wid, _) in self.assignments if wid == wh_id
                )
                if not incompatible:
                    available_warehouses.append(wh_id)
        random.shuffle(available_warehouses)
        while demand > 0 and available_warehouses:
            wh_id = available_warehouses.pop(0)
            warehouse = problem.get_warehouses()[wh_id]
            if random.random() < 0.5 and len(available_warehouses) > 0:
                max_qty = min(demand, warehouse.get_remaining_capacity())
                quantity = random.randint(1, max_qty) if max_qty > 1 else max_qty
            else:
                quantity = min(demand, warehouse.get_remaining_capacity())
            if quantity > 0:
                self.add_assignment(store_id, wh_id, quantity)
                demand -= quantity
        if demand > 0:
            from utils import order_warehouses_by_cost_efficiency
            for wh_id in order_warehouses_by_cost_efficiency(problem.get_warehouses()):
                warehouse = problem.get_warehouses()[wh_id]
                if warehouse.get_remaining_capacity() == 0:
                    continue
                incompatible = any(
                    store_id in problem.get_stores()[s_id].incompatible_stores
                    for (s_id, wid, _) in self.assignments if wid == wh_id
                )
                if incompatible:
                    continue
                quantity = min(demand, warehouse.get_remaining_capacity())
                self.add_assignment(store_id, wh_id, quantity)
                demand -= quantity
                if demand == 0:
                    break
        return self

    def tweak_transfer_between_warehouses(self):
        problem = self.problem
        store_assignments = self.get_store_assignments()
        if not store_assignments:
            return self
        store_id = random.choice(list(store_assignments.keys()))
        assignments = store_assignments[store_id]
        if len(assignments) == 0:
            return self
        source_wh_id, qty = random.choice(assignments)
        for warehouse in problem.get_warehouses():
            warehouse.current_usage = 0
            warehouse.is_open = False
        for s_id, wh_id, q in self.assignments:
            problem.get_warehouses()[wh_id].add_usage(q)
        target_warehouses = []
        for wh_id, warehouse in enumerate(problem.get_warehouses()):
            if wh_id != source_wh_id and warehouse.get_remaining_capacity() > 0:
                incompatible = any(
                    store_id in problem.get_stores()[s_id].incompatible_stores
                    for (s_id, wid, _) in self.assignments if wid == wh_id
                )
                if not incompatible:
                    target_warehouses.append(wh_id)
        if not target_warehouses:
            return self
        target_wh_id = random.choice(target_warehouses)
        target_wh = problem.get_warehouses()[target_wh_id]
        transfer_amount = random.randint(1, min(qty - 1, target_wh.get_remaining_capacity())) if qty > 1 else 0
        if transfer_amount > 0:
            new_assignments = []
            for s_id, wh_id, q in self.assignments:
                if s_id == store_id and wh_id == source_wh_id:
                    new_assignments.append((s_id, wh_id, q - transfer_amount))
                else:
                    new_assignments.append((s_id, wh_id, q))
            new_assignments.append((store_id, target_wh_id, transfer_amount))
            self.assignments = new_assignments
            for warehouse in problem.get_warehouses():
                warehouse.current_usage = 0
                warehouse.is_open = False
            for s_id, wh_id, q in self.assignments:
                problem.get_warehouses()[wh_id].add_usage(q)
        return self

    def tweak_split_store_demand(self):
        problem = self.problem
        store_assignments = self.get_store_assignments()
        if not store_assignments:
            return self
        single_assigned_stores = [
            s_id for s_id, assignments in store_assignments.items()
            if len(assignments) == 1 and assignments[0][1] > 1
        ]
        if not single_assigned_stores:
            return self
        store_id = random.choice(single_assigned_stores)
        wh_id, qty = store_assignments[store_id][0]
        for warehouse in problem.get_warehouses():
            warehouse.current_usage = 0
            warehouse.is_open = False
        for s_id, w_id, q in self.assignments:
            problem.get_warehouses()[w_id].add_usage(q)
        target_warehouses = []
        for new_wh_id, warehouse in enumerate(problem.get_warehouses()):
            if new_wh_id != wh_id and warehouse.get_remaining_capacity() > 0:
                incompatible = any(
                    store_id in problem.get_stores()[s_id].incompatible_stores
                    for (s_id, w, _) in self.assignments if w == new_wh_id
                )
                if not incompatible:
                    target_warehouses.append(new_wh_id)
        if not target_warehouses:
            return self
        target_wh_id = random.choice(target_warehouses)
        target_wh = problem.get_warehouses()[target_wh_id]
        split_amount = random.randint(1, min(qty - 1, target_wh.get_remaining_capacity()))
        if split_amount > 0:
            new_assignments = []
            for s_id, w_id, q in self.assignments:
                if s_id == store_id and w_id == wh_id:
                    new_assignments.append((s_id, w_id, q - split_amount))
                else:
                    new_assignments.append((s_id, w_id, q))
            new_assignments.append((store_id, target_wh_id, split_amount))
            self.assignments = new_assignments
            for warehouse in problem.get_warehouses():
                warehouse.current_usage = 0
                warehouse.is_open = False
            for s_id, w_id, q in self.assignments:
                problem.get_warehouses()[w_id].add_usage(q)
        return self

    def tweak_merge_store_assignments(self):
        problem = self.problem
        store_assignments = self.get_store_assignments()
        if not store_assignments:
            return self
        multi_assigned_stores = [
            s_id for s_id, assignments in store_assignments.items()
            if len(assignments) > 1
        ]
        if not multi_assigned_stores:
            return self
        store_id = random.choice(multi_assigned_stores)
        assignments = store_assignments[store_id]
        indices = random.sample(range(len(assignments)), 2)
        source_wh_id, source_qty = assignments[indices[0]]
        target_wh_id, target_qty = assignments[indices[1]]
        new_assignments = []
        for s_id, wh_id, qty in self.assignments:
            if s_id == store_id and wh_id == source_wh_id:
                pass
            elif s_id == store_id and wh_id == target_wh_id:
                new_assignments.append((s_id, wh_id, qty + source_qty))
            else:
                new_assignments.append((s_id, wh_id, qty))
        self.assignments = new_assignments
        for warehouse in problem.get_warehouses():
            warehouse.current_usage = 0
            warehouse.is_open = False
        for s_id, wh_id, qty in self.assignments:
            problem.get_warehouses()[wh_id].add_usage(qty)
        return self
