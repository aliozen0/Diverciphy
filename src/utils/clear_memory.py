import functools
import gc

def clear_memory(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        finally:
            
            gc.collect()
    return wrapper