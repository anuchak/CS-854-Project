# inspect_triton.py
import multiprocessing as mp, importlib, inspect, sys

def inspect_triton(prefix="Worker"):
    try:
        m = importlib.import_module("triton.compiler.compiler")
        print(f"{prefix} __file__:", getattr(m, "__file__", None))
        print(f"{prefix} has triton_key?:", "triton_key" in dir(m))
        # show the first 80 lines of the file (if readable)
        try:
            src = inspect.getsource(m)
            print(f"{prefix} source head:\\n", "\\n".join(src.splitlines()[:80]))
        except Exception as e:
            print(f"{prefix} (no python source available or compiled .so): {e}")
    except Exception as e:
        print(f"{prefix} import failed:", e)

print("Main:")
inspect_triton("Main")
p = mp.Process(target=inspect_triton, args=("Worker",))
p.start()
p.join()

