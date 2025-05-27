import math
import random
import time
from initial_solution import generate_initial_solution, generate_initial_solution_with_randomization
from validator import validate_solution

def simulated_annealing(problem, T_initial=500, T_min=5, alpha=0.9, inner_limit=30, max_iterations=50000, time_limit_minutes=15):
    start_time = time.time()
    randomization = random.uniform(0.2, 0.4)
    current_solution = generate_initial_solution_with_randomization(problem, randomization=randomization)

    is_valid, message = validate_solution(problem, current_solution)
    if not is_valid:
        print(f"Warning: Initial solution is invalid: {message}")
        print("Attempting to fix initial solution...")
        # If initial solution is invalid, try a different method
        current_solution = generate_initial_solution(problem, ordering_operator="random")
        is_valid, message = validate_solution(problem, current_solution)
    
    best_solution = current_solution
    initial_cost, initial_supply_cost, initial_opening_cost = current_solution.get_total_cost()
    print(f"Initial solution cost: {initial_cost} = {initial_supply_cost} (supply cost) + {initial_opening_cost} (opening cost)")
    
    T = T_initial
    iteration = 0
    best_cost = best_solution.cost()
    
    print(f"Starting simulated annealing with max iterations: {max_iterations}")
    print(f"Annealing parameters: T_initial={T_initial}, T_min={T_min}, alpha={alpha}, inner_limit={inner_limit}")
    print(f"Time limit: {time_limit_minutes} minutes")
    print(f"Initial temperature: {T:.2f}")

    # Create a record of best solutions over time
    iteration_records = [(0, best_cost)]
    last_record_iteration = 0

    # Continue until max iterations is reached (primary condition)
    while iteration < max_iterations:
        current_time = time.time()
        elapsed_minutes = (current_time - start_time) / 60
        if elapsed_minutes >= time_limit_minutes:
            print(f"Time limit of {time_limit_minutes} minutes reached after {iteration} iterations")
            break
            
        # Reset temperature if it gets too low to continue exploring
        if T <= T_min:
            print(f"Temperature reached minimum ({T_min}), resetting to {T_initial}")
            T = T_initial
        
        improved = False
        iter_at_this_temp = 0
        
        for _ in range(inner_limit):
            iteration += 1
            iter_at_this_temp += 1
            
            if (time.time() - start_time) / 60 >= time_limit_minutes:
                print(f"Time limit of {time_limit_minutes} minutes reached during inner loop")
                break
                
            if iteration % 1000 == 0:
                elapsed_time = time.time() - start_time
                elapsed_minutes = elapsed_time / 60
                iteration_records.append((iteration, best_cost))
                print(f"Iteration {iteration} ({elapsed_minutes:.1f} min): Current temperature: {T:.2f}, Best cost: {best_cost}")
                
            if iteration >= max_iterations:
                print(f"Reached maximum iterations limit ({max_iterations})")
                break
                
            neighbor = current_solution.copy_and_perturb()
            
            is_valid, message = validate_solution(problem, neighbor)
            if not is_valid:
                # Skip invalid solutions
                continue
                
            delta = neighbor.cost() - current_solution.cost()

            # Accept the new solution if it's better or with a probability based on temperature
            if delta < 0 or random.random() < math.exp(-delta / T):
                current_solution = neighbor
                improved = True
                
                # Update best solution if this is better
                if current_solution.cost() < best_cost:
                    best_solution = neighbor
                    best_cost = best_solution.cost()
                    last_improvement_iteration = iteration
                    elapsed_time = time.time() - start_time
                    elapsed_minutes = elapsed_time / 60
                    print(f"Iteration {iteration} ({elapsed_minutes:.1f} min): Found better solution with cost {best_cost}")
        
        if (time.time() - start_time) / 60 >= time_limit_minutes:
            break
            
        # Reduce temperature
        old_T = T
        T *= alpha
        
        if iter_at_this_temp > 0 and improved:
            print(f"Temperature decreased: {old_T:.2f} -> {T:.2f} (after {iter_at_this_temp} iterations at this temperature)")
            
        if not improved and iteration > 100:
            T *= alpha 
            print(f"No improvement at temperature {old_T:.2f}, accelerating to {T:.2f}")

    total_time = time.time() - start_time
    total_minutes = total_time / 60
    
    print(f"\nSimulated annealing completed after {iteration} iterations ({total_minutes:.2f} minutes)")
    
    if total_minutes >= time_limit_minutes:
        print(f"Terminated due to reaching time limit of {time_limit_minutes} minutes")
    else:
        print(f"Completed due to reaching maximum iterations limit ({max_iterations})")
    
    final_cost, final_supply_cost, final_opening_cost = best_solution.get_total_cost()
    print(f"Final solution cost: {final_cost} = {final_supply_cost} (supply cost) + {final_opening_cost} (opening cost)")
    
    if final_cost < initial_cost:
        improvement = initial_cost - final_cost
        improvement_percent = (improvement / initial_cost) * 100
        print(f"Improvement: {improvement} ({improvement_percent:.2f}%)")
    else:
        print(f"No improvement from initial solution")
    
    print("\nImprovement over iterations:")
    for iter_num, cost in iteration_records:
        print(f"At iteration {iter_num}: Cost = {cost}")
    
    is_valid, message = validate_solution(problem, best_solution)
    if not is_valid:
        print(f"Error: Final solution is invalid: {message}")
    else:
        print("Final solution is valid.")
    
    return best_solution