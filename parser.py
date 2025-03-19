import re
from models import Warehouse, Store, WarehouseLocationProblem

def parse_file(file_path):
    warehouses = []
    stores = []
    supply_cost = []
    incompatibilities = []

    with open(file_path, 'r') as file:
        content = file.read()
        
        capacities = [int(x.strip()) for x in re.search(r'Capacity\s*=\s*\[(.*?)\];', content).group(1).split(',')]
        fixed_costs = [int(x.strip()) for x in re.search(r'FixedCost\s*=\s*\[(.*?)\];', content).group(1).split(',')]
        demands = [int(x.strip()) for x in re.search(r'Goods\s*=\s*\[(.*?)\];', content).group(1).split(',')]
        
        warehouses = [Warehouse(i, cap, cost) for i, (cap, cost) in enumerate(zip(capacities, fixed_costs))]
        stores = [Store(i, demand) for i, demand in enumerate(demands)]
        

        supply_cost_match = re.search(r'SupplyCost\s*=\s*\[(.*?)\];', content, re.DOTALL)
        if supply_cost_match:
            matrix_str = supply_cost_match.group(1)

            rows = matrix_str.strip().split('\n')
            for row in rows:
                row = row.strip()
                if row and '|' in row:
                    row = row.replace('|', '').strip()
                    values = [int(x.strip()) for x in row.split(',') if x.strip()]
                    if values:
                        supply_cost.append(values)
        
        num_incompatibilities = 0
        incomp_count_match = re.search(r'Incompatibilities\s*=\s*(\d+);', content)
        if incomp_count_match:
            num_incompatibilities = int(incomp_count_match.group(1))
        
        if num_incompatibilities > 0:
            incomp_pairs_match = re.search(r'IncompatiblePairs\s*=\s*\[(.*?)\];', content, re.DOTALL)
            if incomp_pairs_match:
                pairs_str = incomp_pairs_match.group(1)
                pairs = re.findall(r'\|\s*(\d+)\s*,\s*(\d+)\s*', pairs_str)
                for pair in pairs:
                    incompatibilities.append([int(pair[0]) - 1, int(pair[1]) - 1])

    return WarehouseLocationProblem(warehouses, stores, supply_cost, incompatibilities) 