import functools
import logging

logging.basicConfig(level=logging.INFO)

def log_method_call(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logging.info(f"Calling: {func.__name__}")
        result = func(*args, **kwargs)
        logging.info(f"Finished: {func.__name__}")
        return result
    return wrapper
