import numpy as np
from pymoo.core.problem import Problem
from pymoo.algorithms.soo.nonconvex.pso import PSO
from pymoo.core.callback import Callback
from pymoo.optimize import minimize
from pymoo.termination import get_termination
from multiprocessing import Pool, cpu_count
from util.timer_decorator import time_function
import logging


class OptimizationCallback(Callback):
    """
    Callback to log progress during the optimization process.
    """

    def notify(self, algorithm):
        gen = algorithm.n_gen
        best_F = algorithm.opt[0].F[0]
        best_X = algorithm.opt[0].X
        logging.info(f"Generation {gen}: Best fitness = {best_F}, Best X = {best_X}")


class ExternalProblem(Problem):
    def __init__(self, config):
        super().__init__(n_var=2, n_obj=1, xl=config.x_min, xu=config.x_max, type_var=np.float64)
        self.config = config

    @time_function("Global optimization iteration runtime")
    def _evaluate(self, X, out, *args, **kwargs):
        # Use multiprocessing to evaluate the population in parallel
        with Pool(processes=cpu_count()) as pool:
            results = pool.starmap(
                self._evaluate_individual, 
                [(ind[0], ind[1]) for ind in X]
            )
        out["F"] = np.array(results)
        
    def _evaluate_individual(self, x, y):
        """
        Evaluate a single individual by running the external program.
        """
        from util.external_runner import run_external_program
        return run_external_program(x, y, self.config)


class GlobalOptimizer:
    def __init__(self, config):
        self.config = config

    @time_function("Global optimization total runtime")
    def optimize(self):
        # Create the problem instance
        problem = ExternalProblem(self.config)

        # Initialize the genetic algorithm with the population size
        algorithm = PSO(
            pop_size=self.config.pop_size,
            eliminate_duplicates=True
        )
        termination = get_termination("n_gen", self.config.max_generations)

        logging.info("Starting global optimization...")
        # Run the optimization using Pymoo
        result = minimize(
            problem,
            algorithm,
            termination,
            seed=self.config.seed,
            callback=OptimizationCallback(),
            verbose=False
        )
        logging.info(f"Global optimization result: fun: {result.F}, x: {result.X}")
        return result
