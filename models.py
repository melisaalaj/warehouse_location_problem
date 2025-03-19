class Warehouse:
    def __init__(self, id, capacity, fixed_cost):
        self.id = id
        self.capacity = capacity
        self.fixed_cost = fixed_cost

class Store:
    def __init__(self, id, demand):
        self.id = id
        self.demand = demand
        self.incompatible_stores = []
    
    def add_incompatible_store(self, store_id):
        if store_id not in self.incompatible_stores:
            self.incompatible_stores.append(store_id)
    
    def is_incompatible_with(self, store_id):
        return store_id in self.incompatible_stores

class WarehouseLocationProblem:
    def __init__(self, warehouses, stores, supply_cost, incompatibilities):
        self.warehouses = warehouses
        self.stores = stores
        self.supply_cost = supply_cost
        self.incompatibilities = incompatibilities
        
        for pair in incompatibilities:
            store1_id, store2_id = pair
            self.stores[store1_id].add_incompatible_store(store2_id)
            self.stores[store2_id].add_incompatible_store(store1_id)

    def get_warehouses(self):
        return self.warehouses

    def get_stores(self):
        return self.stores

    def get_supply_cost(self):
        return self.supply_cost

    def get_incompatibilities(self):
        return self.incompatibilities 