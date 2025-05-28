# Warehouse Location Problem with Store Incompatibilities

This project solves the **Warehouse Location Problem with Store Incompatibilities**, originally proposed as part of the **MESS-2020+1 Competition**.
You can find problem specifications here: https://www.ants-lab.it/mess2020/wp-content/uploads/2021/competition/MESS-CompetitionSpecs.pdf.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/warehouse_location_problem.git
   cd warehouse_location_problem
   ```

## Usage

1. Define the input file path in `main.py`:

   ```python
   file_path = "./PublicInstances/toy.dzn"
   ```

2. Run the program:

   ```bash
   python3 main.py
   ```

3. Check the `tmp/solution` folder for the saved solution and output files.

## Input Format

The input file should be in `.dzn` format and include:

- **Warehouse capacities**
- **Fixed opening costs**
- **Store demands**
- **Supply costs** (matrix format)
- **Incompatible store pairs**

### Example

```minizinc
Warehouses = 3;
Stores = 4;
Capacity = [100, 200, 150];
FixedCosts = [500, 700, 600];
Goods = [50, 60, 70, 80];
SupplyCost = [
  [10, 20, 30],
  [15, 25, 35],
  [20, 30, 40],
  [25, 35, 45]
];
IncompatiblePairs = [(1, 2), (3, 4)];
```

## Output Format

The program generates two files:

1. **Solution File (`solution.txt`)**  
   Contains the solution in triples format.  
   Example:
   ```text
   {(Store 1, Warehouse 2, Quantity 50), ...}
   ```

2. **Output File (`output.txt`)**  
   Includes detailed results such as:
   - Warehouse capacities and usage
   - Store demands and assignments
   - Total costs (supply + opening)
   - Violations (if any)

## Examples

### Example Run

1. Set the input file path in `main.py`:

   ```python
   file_path = "./PublicInstances/toy.dzn"
   ```

2. Run the program:

   ```bash
   python3 main.py
   ```

3. Output:

   ```yaml
    Parsing file: ./PublicInstances/toy.dzn
    File parsed successfully.
    Generating initial solution...
    Warehouses: 4
    Stores: 10
    Incompatibilities: 3
    
    Warehouse capacities:
    Warehouse 1: Capacity=100, Fixed Cost=860
    Warehouse 2: Capacity=40, Fixed Cost=350
    Warehouse 3: Capacity=60, Fixed Cost=440
    Warehouse 4: Capacity=60, Fixed Cost=580
    
    Store demands:
    Store 1: Demand=12
    Store 2: Demand=17
    Store 3: Demand=5
    Store 4: Demand=13
    Store 5: Demand=20
    Store 6: Demand=20
    Store 7: Demand=17
    Store 8: Demand=19
    Store 9: Demand=11
    Store 10: Demand=20
    
    Supply costs:
    Store 1: [27, 66, 44, 55]
    Store 2: [53, 89, 68, 46]
    Store 3: [17, 40, 18, 61]
    Store 4: [20, 68, 44, 78]
    Store 5: [42, 89, 65, 78]
    Store 6: [57, 55, 49, 31]
    Store 7: [89, 101, 90, 16]
    Store 8: [37, 31, 23, 55]
    Store 9: [76, 60, 63, 44]
    Store 10: [82, 107, 91, 31]
    
    Incompatibilities:
    Store 1 and Store 10
    Store 2 and Store 7
    Store 8 and Store 9
    
    Store incompatibilities (from store objects):
    Store 1 is incompatible with: 10
    Store 2 is incompatible with: 7
    Store 7 is incompatible with: 2
    Store 8 is incompatible with: 9
    Store 9 is incompatible with: 8
    Store 10 is incompatible with: 1
    
    --- INITIAL SOLUTION ---
    Solution valid: True
    Validation message: Solution is valid
    Total cost: 8695 = 6905 (supply cost) + 1790 (opening cost)
    
    Solution in triples format:
    {(5, 1, 20), (6, 1, 20), (10, 4, 20), (8, 1, 19), (2, 4, 17), (7, 1, 17), (4, 1, 13), (1, 1, 11), (1, 2, 1), (9, 4, 11), (3, 2, 5)}
    
    Store assignments:
    Store 1 → Warehouse 1: 11
    Store 1 → Warehouse 2: 1
    Store 2 → Warehouse 4: 17
    Store 3 → Warehouse 2: 5
    Store 4 → Warehouse 1: 13
    Store 5 → Warehouse 1: 20
    Store 6 → Warehouse 1: 20
    Store 7 → Warehouse 1: 17
    Store 8 → Warehouse 1: 19
    Store 9 → Warehouse 4: 11
    Store 10 → Warehouse 4: 20
    
    Warehouse usage:
    Warehouse 1: 100/100 (100.0%)
    Warehouse 2: 6/40 (15.0%)
    Warehouse 4: 48/60 (80.0%)
    
    Open warehouses:
    [1, 2, 4]
    
    Output saved to: tmp/solution/toy/20250416-182000/output.txt
    Solution saved to: tmp/solution/toy/20250416-182000/solution.txt
   ```

## Initial Solution Strategies

Two initial solution generators are implemented:

### `generate_initial_solution(problem, ordering_operator="random")`

- **Deterministic heuristic** (greedy or demand-based)
- Ensures:
  - Total goods taken from any warehouse ≤ its capacity
  - Each store’s demand is fully satisfied
  - No warehouse supplies incompatible stores

### `generate_initial_solution_with_randomization(problem, randomization=0.3)`

- Adds **controlled randomness** to increase solution diversity
- Stores are prioritized using:  
  `priority = store.demand × average_supply_cost`
- Warehouses are selected from the **top-K cheapest** using random perturbation
- Randomness applies to:
  - Warehouse selection
  - Quantity assignment  
- Produces varied, high-quality initial solutions

---

## Neighborhood Moves (Tweaks)

The `Solution.copy_and_perturb()` method applies a **random local change** to explore the solution space. One of the following strategies is selected:

### `Reassign`
- Completely reassign a store’s demand from scratch
- Useful for diversifying assignments heavily

### `Transfer`
- Move a portion of a store’s demand from one warehouse to another
- Helps explore small incremental cost improvements

### `Split`
- Divide a store’s demand across multiple warehouses
- Can help balance load and improve cost

### `Merge`
- Combine multiple warehouse assignments for a store into one
- Reduces warehouse usage and may lower fixed costs

> **All tweaks respect:**
> - Capacity constraints  
> - Demand satisfaction  
> - Store incompatibility rules

## Simulated Annealing

This project uses **Simulated Annealing (SA)** as a metaheuristic to iteratively improve the warehouse-location solution by exploring the solution space intelligently.
<img width="548" alt="image" src="https://github.com/user-attachments/assets/178a55cb-ebe2-473d-88ec-69f406ba5718" />

### Why Simulated Annealing?

Simulated Annealing balances **exploration** and **exploitation**:

- Accepts **worse solutions** early on to escape local minima.
- Gradually becomes **more selective** as the temperature decreases.
- Suitable for complex combinatorial optimization problems like this one.

### Algorithm Overview

1. **Initial Solution**  
   Begins with a feasible solution generated using:
   - `generate_initial_solution` or  
   - `generate_initial_solution_with_randomization`

2. **Temperature Schedule**
   - Starts at `T_initial`
   - Gradually cools down with factor `alpha`
   - Stops when reaching `T_min` or time/iteration limits

3. **Inner Loop**
   For each temperature:
   - Generate a **neighbor solution** using `Solution.copy_and_perturb()`
   - Validate the new solution
   - Accept if:
     - It has **lower cost**
     - Or, with probability `exp(-Δcost / T)` if it’s worse

4. **Update Best Solution**
   - Tracks and updates the best valid solution found
   - Records cost progression over time

<img width="600" alt="image" src="https://github.com/user-attachments/assets/b3f62582-6af4-4176-a73b-292742dea47f" />


### Parameters

| Parameter       | Description                                      |
|----------------|--------------------------------------------------|
| `T_initial`     | Initial temperature (default: 500)               |
| `T_min`         | Minimum temperature to reset from (default: 5)   |
| `alpha`         | Cooling rate (e.g., 0.9 for 10% reduction)       |
| `inner_limit`   | Number of iterations per temperature level       |
| `max_iterations`| Overall iteration limit (default: 50,000)        |
| `time_limit_minutes` | Execution time cap (default: 15 mins)       |

Listed here are the results of 3 runs: https://docs.google.com/spreadsheets/d/1851_3L6803wNDPyTEpld6INGKz5fg8dPto6rfVb8tOc/edit?usp=sharing

## License

This project is open-source and available under the [MIT License](LICENSE).
