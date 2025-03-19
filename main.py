import sys
import os
import datetime
from parser import parse_file

if __name__ == "__main__":
    try:
        if len(sys.argv) > 1:
            file_path = sys.argv[1]
        else:
            file_path = "./PublicInstances/toy.dzn" 
            
        print(f"Parsing file: {file_path}")
        problem = parse_file(file_path)
        print("File parsed successfully.")
        
        os.makedirs("tmp", exist_ok=True)
        
        base_filename = os.path.basename(file_path).split('.')[0]
        timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        output_file = f"tmp/{base_filename}-{timestamp}.txt"
        
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
        
        print(f"\nOutput saved to: {output_file}")
            
    except Exception as e:
        print(f"Error reading file: {str(e)}")
        import traceback
        traceback.print_exc() 