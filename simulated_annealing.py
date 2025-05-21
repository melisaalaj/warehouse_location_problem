import math
import random
from initial_solution import generate_initial_solution

def simulated_annealing(problem, T_initial=1000, T_min=1, alpha=0.95, inner_limit=50):
    current_solution = generate_initial_solution(problem, ordering_operator="demand")
    best_solution = current_solution
    T = T_initial

    while T > T_min:
        for _ in range(inner_limit):
            neighbor = current_solution.copy_and_perturb()

            delta = neighbor.cost() - current_solution.cost()

            if delta < 0 or random.random() < math.exp(-delta / T):
                current_solution = neighbor
                if current_solution.cost() < best_solution.cost():
                    best_solution = neighbor

        T *= alpha

    return best_solution
