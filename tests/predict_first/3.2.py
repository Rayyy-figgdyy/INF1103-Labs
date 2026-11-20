"""Predict: an unknown factory type and an uncaught exception."""
import subprocess
import sys
import traceback

from _support import ROOT, supplier
from ProductFactory import ProductFactory


def main():
    try:
        ProductFactory.create("service", "S001", "Installation", 30, 5, supplier())
    except ValueError as error:
        frame = traceback.extract_tb(error.__traceback__)[-1]
        assert frame.name == "create"
        assert str(error) == "Unknown product type: service"
        print(f"Caught {type(error).__name__}: {error}")
        print(f"Raised at {frame.filename}:{frame.lineno}: {frame.line}")
    else:
        raise AssertionError("Expected ValueError")

    code = (
        f"import sys; sys.path.insert(0, {str(ROOT)!r}); "
        "from ProductFactory import ProductFactory; "
        "from Supplier import Supplier; "
        "ProductFactory.create('service', 'S001', 'Installation', 30, 5, "
        "Supplier('S001', 'Supplier', 'test@example.com')); "
        "print('CREATION COMPLETED')"
    )
    result = subprocess.run([sys.executable, "-B", "-c", code], capture_output=True, text=True)
    assert result.returncode != 0
    assert "ValueError: Unknown product type: service" in result.stderr
    assert "CREATION COMPLETED" not in result.stdout
    print("\nUncaught exception in a separate process:")
    print(result.stderr.rstrip())
    print(f"Process exit code: {result.returncode}; execution stopped before the next print.")


if __name__ == "__main__":
    main()
