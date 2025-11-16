import multiprocessing as mp
import triton

def show():
    import triton
    print("Worker sees Triton:", triton.__version__)

print("Main sees Triton:", triton.__version__)
mp.Process(target=show).start()
