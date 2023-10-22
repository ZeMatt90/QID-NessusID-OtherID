import math
import time
import urllib.request
import matplotlib.pyplot as plt

from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor



def multithreading(func, args, workers):
    with ThreadPoolExecutor(workers) as ex:
        res = ex.map(func, args)
    return list(res)


def multiprocessing(func, args, workers):
    with ProcessPoolExecutor(workers) as ex:
        res = ex.map(func, args)
    return list(res)




#più veloce con più thread
def io_intensive():
    write_count = 50
    with urllib.request.urlopen(addrs[x], timeout=20) as conn:
        page = conn.read()
        for _ in range(write_count):
            with open('output.txt', 'w') as output:
                output.write(str(page))

#più veloce con più processi
def compute_intensive(x):
    foo = 0
    for i in range(10**7):
        foo += foo * math.cos(i*math.pi)


def test_compute_intensive():
    times = []
    num_tasks = 2
    time_init = time.time()
    for i in range(num_tasks):
        compute_intensive(i)
    time_end = time.time()
    times.append(float(time_end - time_init))
    print(f'Serial execution took {time_end - time_init}s.')
    n_threads = num_tasks
    time_init = time.time()
    multithreading(compute_intensive, range(num_tasks), n_threads)
    time_end = time.time()
    times.append(float(time_end - time_init))
    print(f'Multithreading with {n_threads} threads took {time_end - time_init}s.')
    n_procs = num_tasks
    time_init = time.time()
    multiprocessing(compute_intensive, range(num_tasks), n_procs)
    time_end = time.time()
    times.append(float(time_end - time_init))
    print(f'Multiprocessing with {n_procs} processes took {time_end - time_init}s.')
    return times

print("start")
start = time.time()
test_compute_intensive()
#io_intensive()
end = time.time()
print(end - start) # Time in seconds, e.g. 5.38091952400282
