import sys
import os
import datetime
from parser import parse_file
from initial_solution import generate_initial_solution
from validator import validate_solution

if __name__ == "__main__":
    try:
        if len(sys.argv) > 1:
            file_path = sys.argv[1]
        else:
            file_path = "./PublicInstances/wlp17.dzn" 
            
        print(f"Parsing file: {file_path}")
        problem = parse_file(file_path)
        print("File parsed successfully.")
        
        print("Generating initial solution...")
        initial_solution = generate_initial_solution(problem)
        
        is_valid, message = validate_solution(problem, initial_solution)
        
        base_filename = os.path.basename(file_path).split('.')[0]
        timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        
        solution_dir = f"tmp/solution/{base_filename}/{timestamp}"
        os.makedirs(solution_dir, exist_ok=True)
        
        solution_file = f"{solution_dir}/solution.txt"
        output_file = f"{solution_dir}/output.txt"
        
        # Write the solution file in triples format
        with open(solution_file, 'w') as f:
            triples = initial_solution.to_triples_format()
            f.write(f"{{{', '.join([str(t) for t in triples])}}}")
        
        # Write the detailed output file
        with open(output_file, 'w') as f:
            def write_output(text):
                print(text)
                f.write(text + "\n")
            
            write_output(f"Warehouses: {len(problem.get_warehouses())}")
            write_output(f"Stores: {len(problem.get_stores())}")
            write_output(f"Incompatibilities: {len(problem.get_incompatibilities())}")
            
            write_output("\nWarehouse capacities:")
            for w in problem.get_warehouses():
                write_output(f"Warehouse {w.id + 1}: Capacity={w.capacity}, Fixed Cost={w.fixed_cost}")
            
            write_output("\nStore demands:")
            for s in problem.get_stores():
                write_output(f"Store {s.id + 1}: Demand={s.demand}")
            
            write_output("\nSupply costs:")
            for i, row in enumerate(problem.get_supply_cost()):
                write_output(f"Store {i + 1}: {row}")
            
            write_output("\nIncompatibilities:")
            for pair in problem.get_incompatibilities():
                write_output(f"Store {pair[0] + 1} and Store {pair[1] + 1}")
            
            write_output("\nStore incompatibilities (from store objects):")
            for s in problem.get_stores():
                if s.incompatible_stores:
                    incomp_list = [str(store_id + 1) for store_id in s.incompatible_stores]
                    write_output(f"Store {s.id + 1} is incompatible with: {', '.join(incomp_list)}")
            
            # Add solution information
            write_output("\n--- INITIAL SOLUTION ---")
            write_output(f"Solution valid: {is_valid}")
            write_output(f"Validation message: {message}")
            
            total_cost, supply_cost, opening_cost = initial_solution.get_total_cost()
            write_output(f"Total cost: {total_cost} = {supply_cost} (supply cost) + {opening_cost} (opening cost)")
            
            write_output("\nSolution in triples format:")
            triples = initial_solution.to_triples_format()
            write_output(f"{{{', '.join([str(t) for t in triples])}}}")
            
            write_output("\nStore assignments:")
            store_assignments = initial_solution.get_store_assignments()
            for store_id in range(len(problem.get_stores())):
                assignments = store_assignments.get(store_id, [])
                if assignments:
                    for wh_id, qty in assignments:
                        write_output(f"Store {store_id + 1} → Warehouse {wh_id + 1}: {qty}")
                else:
                    write_output(f"Store {store_id + 1} → Not assigned")
            
            write_output("\nWarehouse usage:")
            for wh in problem.get_warehouses():
                if wh.current_usage > 0:
                    write_output(f"Warehouse {wh.id + 1}: {wh.current_usage}/{wh.capacity} ({wh.current_usage/wh.capacity*100:.1f}%)")
            
            write_output("\nOpen warehouses:")
            open_wh = [wh.id + 1 for wh in problem.get_warehouses() if wh.is_open]
            write_output(f"{open_wh}")
        
        print(f"\nOutput saved to: {output_file}")
        print(f"Solution saved to: {solution_file}")
            
    except Exception as e:
        print(f"Error reading file: {str(e)}")
        import traceback
        traceback.print_exc() 