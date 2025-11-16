python - <<'PY'
import pkgutil, importlib, sys
for finder, name, ispkg in pkgutil.iter_modules():
    if name.startswith("triton"):
        print("module:", name, "->", finder)
import triton, triton.compiler
print("triton.__file__:", getattr(triton, "__file__", None))
try:
    import inspect
    print("compiler module file:", inspect.getsourcefile(triton.compiler.compiler))
except Exception as e:
    print("inspect failed:", e)
PY

