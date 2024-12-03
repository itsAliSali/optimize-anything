import time
import logging

def time_function(message):
    def decorator(func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            elapsed_time = time.time() - start_time
            logging.info(f"{message}: {elapsed_time:.2f} seconds")
            return result
        return wrapper
    return decorator
