"""

"""

import os
import psutil
from time import sleep

def get_mem_usage(precision: int = 2) -> float:
    """Returns current process' memory usage in MB."""
    process = psutil.Process(os.getpid())
    return round(process.memory_info().rss / 1000000, precision)