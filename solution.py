class Solution:
    def __init__(self, problem):
        self.problem = problem
        # Store assignments as a list of triples (store_id, warehouse_id, quantity)
        self.assignments = []
        
    def add_assignment(self, store_id, warehouse_id, quantity):
        """Add an assignment of a store to a warehouse with a specific quantity"""
        self.assignments.append((store_id, warehouse_id, quantity))
        self.problem.get_warehouses()[warehouse_id].add_usage(quantity)
        
    def get_store_assignments(self):
        """Get a dictionary mapping store_id to list of (warehouse_id, quantity) tuples"""
        store_assignments = {}
        for store_id, wh_id, qty in self.assignments:
            if store_id not in store_assignments:
                store_assignments[store_id] = []
            store_assignments[store_id].append((wh_id, qty))
        return store_assignments
    
    def get_total_cost(self):
        supply_cost = 0
        opening_cost = 0
        
        # Calculate supply costs
        for store_id, wh_id, quantity in self.assignments:
            supply_cost += self.problem.get_supply_cost()[store_id][wh_id] * quantity
                
        # Add fixed costs for open warehouses
        for warehouse in self.problem.get_warehouses():
            if warehouse.is_open:
                opening_cost += warehouse.fixed_cost
        
        return supply_cost + opening_cost, supply_cost, opening_cost
    
    def to_triples_format(self):
        """Convert solution to the triples format (1-indexed)"""
        triples = []
        for store_id, wh_id, quantity in self.assignments:
            triples.append((store_id + 1, wh_id + 1, quantity))
        return triples
    