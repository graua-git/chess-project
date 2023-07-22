# This file is strictly for optimization testing purposes

import time

num_runs = 0
total_time = 0

def timer(func):
    """
    Maintenance function to time other functions
    """
    def wrapper(*args, **kwargs):
        global total_time, num_runs
        t1 = time.time()
        result = func(*args, **kwargs)
        t2 = time.time()
        total_time += t2 - t1
        num_runs += 1
        print("Avg time: {}".format(total_time / num_runs), ", Num runs: {}".format(num_runs))
        return result
    return wrapper