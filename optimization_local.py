import subprocess
import logging
from multiprocessing import Pool, cpu_count
from scipy.optimize import minimize


# Configure logging
logging.basicConfig(
    filename='optimization.log',
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

def objective_function(params):
    """
    Objective function to optimize.
    
    Args:
        params (list): Parameters for the external program.
        
    Returns:
        float: The objective fuction value.
    """
    logging.info(f"Evaluating objective function with params: {params}")
    result = run_external_program(params)
    logging.info(f"Objective value for params {params}: {result}")
    return result

def optimize_external_program(initial_guess):
    """
    Optimize the external program using scipy.optimize.minimize.
    
    Args:
        initial_guess (list): Initial parameter guess.
        
    Returns:
        OptimizeResult: The result of the optimization process.
    """
    logging.info("Starting optimization process")
    result = minimize(
        fun=objective_function,
        x0=initial_guess,
        method='Powell',  # Choose an appropriate optimization method
        options={'disp': True, 'maxiter': 5}
    )
    # logging.info(f"Optimization completed. Result: {result}")
    return result

if __name__ == "__main__":
    # Example initial guess
    initial_guess = [1.0, 2.0]  # Replace with the actual parameter guesses
    
    # Start optimization
    logging.info("Launching optimization")
    result = optimize_external_program(initial_guess)
    
    # Log final results
    logging.info(f"Final optimization result: {result}")
    logging.info("Optimization Completed.")
    