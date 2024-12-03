from util.config_loader import Config
from optimization.local_optimizer import LocalOptimizer
from optimization.global_optimizer import GlobalOptimizer
import logging

def main():
    # Load configuration
    config = Config("config.ini")
    logging.info(f"Loaded configuration: {config}")

    # Run the chosen optimization method
    if config.method == "local":
        logging.info("Running local optimization...")
        optimizer = LocalOptimizer(config)
        # result = optimizer.optimize()
    elif config.method == "global":
        logging.info("Running global optimization...")
        optimizer = GlobalOptimizer(config)
        # result = optimizer.optimize()
    else:
        raise ValueError(f"Unknown optimization method: {config.method}")
    
    result = optimizer.optimize()
    

if __name__ == "__main__":
    main()
