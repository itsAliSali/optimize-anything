from scipy.optimize import minimize
from util.timer_decorator import time_function
import logging


class LocalOptimizer:
    def __init__(self, config):
        self.config = config

    @time_function("Local optimization total runtime")
    def optimize(self):
        bounds = [(self.config.x_min, self.config.x_max), (self.config.x_min, self.config.x_max)]
        initial_guess = [self.config.x0, self.config.y0]

        @time_function("Local optimization iteration runtime")
        def objective(x):
            from util.external_runner import run_external_program
            obj_value = run_external_program(x[0], x[1], self.config)
            logging.info(f"Objective value for x: {x}, F: {obj_value}")
            return obj_value

        logging.info("Starting local optimization...")
        result = minimize(objective, initial_guess, bounds=bounds, method="nelder-mead")
        logging.info(f"Local optimization result: {result}")
        return result
