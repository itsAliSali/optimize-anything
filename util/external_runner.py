import subprocess
import logging


def run_external_program(x, y, config):
    """
    Runs an external program to compute the Eggholder function value with a timeout.

    Args:
        x (float): First parameter.
        y (float): Second parameter.
        config (Config): Configuration from the config file.

    Returns:
        float: The result of the program execution to optimize, or a high penalty if the process fails or times out.
    """

    config.setup_logging()
    
    try:
        # Run the external program with the given timeout
        result = subprocess.run(
            ["python", "external_program.py", str(x), str(y)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=config.timeout
        )
        if result.returncode != 0:
            logging.error(f"External program failed with error: {result.stderr}")
            return float('inf')  # High penalty for failure

        # Extract and return the objective value
        return float(result.stdout.strip())

    except subprocess.TimeoutExpired:
        logging.error(f"External program timed out after {config.timeout} seconds for input ({x}, {y}).")
        return float('inf')  # High penalty for timeout

    except Exception as e:
        logging.error(f"Error while running external program: {e}")
        return float('inf')
