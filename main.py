from util.config_loader import Config
from optimization.local_optimizer import LocalOptimizer
from optimization.global_optimizer import GlobalOptimizer
import logging


def main():
    # Load configuration
    config = Config("sample_config.ini")
    logging.info(f"Loaded configuration: {config}")

    # Run the chosen optimization method
    if config.method == "local":
        logging.info("Running local optimization...")
        optimizer = LocalOptimizer(config)
    elif config.method == "global":
        logging.info("Running global optimization...")
        optimizer = GlobalOptimizer(config)
    else:
        raise ValueError(f"Unknown optimization method: {config.method}")
    
    result = optimizer.optimize()
    logging.info(f"End of program.")
    

if __name__ == "__main__":
    main()
