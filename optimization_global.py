import subprocess
import logging
from pymoo.core.problem import Problem
from pymoo.optimize import minimize
from pymoo.algorithms.soo.nonconvex.pso import PSO
from pymoo.core.callback import Callback
from pymoo.termination import get_termination
from multiprocessing import Pool, cpu_count
import numpy as np


# Configure logging
logging.basicConfig(
    filename='optimization_global.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def run_external_program(params):
    """
    Runs an external program with given parameters.
    
    Args:
        params (list): Parameters to pass to the external program.
        
    Returns:
        float: The result of the program execution to optimize.
    """
    try:
        # Convert parameters
        x = params[0]
        y = params[1]
        # Run the external program
        result = subprocess.run(
            f"py ./external_program.py {str(x)} {str(y)}",  # Replace './external_program' with your program path
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        # Check for errors
        if result.returncode != 0:
            logging.error(f"Program failed with error: {result.stderr}")
            return float('inf')  # Return a high value if the program fails
        # Extract the output as the objective value
        return float(result.stdout.strip())
    except Exception as e:
        logging.error(f"Exception occurred: {e}")
        return float('inf')

def evaluate_population(population):
    """
    Evaluates the entire population by calling the external program in parallel.

    Args:
        population (np.ndarray): Population array of shape (n_individuals, n_features).

    Returns:
        np.ndarray: Objective values for each individual.
    """
    with Pool(cpu_count()) as pool:
        results = pool.map(run_external_program, population)
    return np.array(results)

class ExternalProblem(Problem):
    """
    Custom problem class for optimizing the Eggholder function via an external program.
    """

    def __init__(self):
        super().__init__(n_var=2, n_obj=1, xl=-512, xu=512, type_var=np.float64)

    def _evaluate(self, X, out, *args, **kwargs):
        """
        Evaluate the problem by calling the external program for all individuals.

        Args:
            X (np.ndarray): Decision variable array of shape (n_individuals, n_features).
            out (dict): Output dictionary for storing the objective values.
        """
        out["F"] = evaluate_population(X)

class OptimizationCallback(Callback):
    """
    Callback to log progress during the optimization process.
    """

    def notify(self, algorithm):
        gen = algorithm.n_gen
        best_F = algorithm.opt[0].F[0]
        best_X = algorithm.opt[0].X
        logging.info(f"Generation {gen}: Best fitness = {best_F}, Best X = {best_X}")
        # print(f"Generation {gen}: Best fitness = {best}")

if __name__ == "__main__":
    # Configure the problem
    problem = ExternalProblem()

    # Set up the genetic algorithm
    algorithm = PSO(
        pop_size=100,  # Population size
        eliminate_duplicates=True
    )

    # Configure termination criteria
    termination = get_termination("n_gen", 10)  # Run for 100 generations

    # Run the optimization
    logging.info("Starting Genetic Algorithm optimization")
    result = minimize(
        problem,
        algorithm,
        termination,
        seed=1,
        callback=OptimizationCallback(),
        verbose=True
    )

    # Log the final result
    logging.info(f"Optimization completed. Best solution: {result.X}")
    logging.info(f"Objective value: {result.F}")
    logging.info("Optimization Completed.")
    