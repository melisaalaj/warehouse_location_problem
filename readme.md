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

## License

This project is open-source and available under the [MIT License](LICENSE).
