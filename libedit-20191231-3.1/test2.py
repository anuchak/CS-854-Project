# save as check_triton.py and run with the same python you use for vllm
import multiprocessing as mp
import importlib, inspect, sys

def inspect_triton(prefix="Worker"):
    m = importlib.import_module("triton.compiler.compiler")
    print(f"{prefix} module __file__:", getattr(m, "__file__", None))
    print(f"{prefix} module dir contains 'triton_key':", "triton_key" in dir(m))
    try:
        print(f"{prefix} source head:\n", "\n".join(inspect.getsource(m).splitlines()[:40]))
    except (OSError, TypeError):  # compiled module or not accessible
        print(f"{prefix} (no python source available; probably compiled extension)")

print("Main (before spawn):")
inspect_triton("Main")
p = mp.Process(target=inspect_triton, args=("Worker",))
p.start()
p.join()
