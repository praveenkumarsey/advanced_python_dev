"""
05_context_managers.py
=======================
Demonstrates deterministic resource cleanup using context managers:
  - Class-based: __enter__ and __exit__
  - Function-based: contextlib.contextmanager
  - How __exit__ is called even when an exception is raised
  - Suppressing exceptions inside __exit__

Run:
    python day-02/05_context_managers.py
"""

import time
import contextlib


# ══════════════════════════════════════════════════════════════════════════════
# PART 1: Class-based context manager
# ══════════════════════════════════════════════════════════════════════════════

class ManagedConnection:
    """Simulates a database connection that must always be closed.

    __enter__ acquires the resource.
    __exit__ releases it — even if an exception occurred inside the with block.
    """

    def __init__(self, host: str, port: int = 5432):
        self.host = host
        self.port = port
        self._open = False

    def __enter__(self):
        print(f"  [open]  Connecting to {self.host}:{self.port}")
        self._open = True
        return self  # the value bound by `as`

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"  [close] Disconnecting from {self.host}:{self.port}")
        self._open = False
        # Return False (or None) to let exceptions propagate.
        # Return True to suppress them.
        return False

    def query(self, sql: str) -> list:
        if not self._open:
            raise RuntimeError("Connection is not open.")
        print(f"  [query] {sql}")
        return [{"id": 1}, {"id": 2}]  # simulated result


def demo_class_context_manager():
    print("=" * 55)
    print("PART 1: Class-based context manager")
    print("=" * 55)

    print("\n--- Normal usage ---")
    with ManagedConnection("db.example.com") as conn:
        results = conn.query("SELECT id FROM events LIMIT 2")
        print(f"  [result] {results}")
    print("Connection closed after the with block — even without explicit close().")

    print("\n--- Exception inside with block ---")
    try:
        with ManagedConnection("db.example.com") as conn:
            conn.query("SELECT * FROM events")
            raise ValueError("Downstream processing failed")
    except ValueError as e:
        print(f"  [caught] {e}")
    print("__exit__ was still called — resource was released despite the error.")


# ══════════════════════════════════════════════════════════════════════════════
# PART 2: Function-based context manager with @contextmanager
# ══════════════════════════════════════════════════════════════════════════════
#
# For simpler cases, a generator function is more compact than a class.
# Code before yield = __enter__. Code after yield = __exit__.

@contextlib.contextmanager
def managed_file_writer(path: str):
    """Open a file for writing and ensure it is closed."""
    print(f"  [open]  Opening {path} for writing")
    handle = open(path, "w")  # noqa: WPS515
    try:
        yield handle        # the value bound by `as`
    finally:
        handle.close()
        print(f"  [close] Closed {path}")


@contextlib.contextmanager
def timer(label: str):
    """Measure the elapsed time of a code block."""
    start = time.perf_counter()
    try:
        yield
    finally:
        elapsed = time.perf_counter() - start
        print(f"  [{label}] elapsed: {elapsed * 1000:.2f} ms")


def demo_function_context_manager(tmp_path: str = "/tmp/demo_output.txt"):
    print("\n" + "=" * 55)
    print("PART 2: Function-based context manager (@contextmanager)")
    print("=" * 55)

    print("\n--- File writer ---")
    with managed_file_writer(tmp_path) as f:
        f.write("record 1\n")
        f.write("record 2\n")
        print(f"  [write] Wrote 2 records to {tmp_path}")

    print("\n--- Timer ---")
    with timer("sort 1M items"):
        data = list(range(1_000_000, 0, -1))
        data.sort()
    print(f"  Sorted list length: {len(data)}")


# ══════════════════════════════════════════════════════════════════════════════
# PART 3: Suppressing exceptions inside __exit__
# ══════════════════════════════════════════════════════════════════════════════

class SuppressingContext:
    """A context manager that silently swallows a specific exception type.

    Returning True from __exit__ suppresses the exception.
    This is how contextlib.suppress() works internally.
    """

    def __init__(self, *exception_types):
        self._types = exception_types

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None and issubclass(exc_type, self._types):
            print(f"  [suppress] Swallowed {exc_type.__name__}: {exc_val}")
            return True  # suppress — execution continues after the with block
        return False      # propagate any other exception


def demo_exception_suppression():
    print("\n" + "=" * 55)
    print("PART 3: Suppressing exceptions in __exit__")
    print("=" * 55)

    print("\n--- Suppress FileNotFoundError (expected during cleanup) ---")
    with SuppressingContext(FileNotFoundError):
        raise FileNotFoundError("temp file already deleted")
    print("  Execution resumed after the with block — exception was suppressed.")

    print("\n--- Do NOT suppress ValueError (unexpected) ---")
    try:
        with SuppressingContext(FileNotFoundError):
            raise ValueError("this is a real problem")
    except ValueError as e:
        print(f"  [propagated] ValueError: {e}")

    print("\nNote: contextlib.suppress() provides this same behaviour out of the box.")
    with contextlib.suppress(FileNotFoundError):
        raise FileNotFoundError("already gone")
    print("  contextlib.suppress worked the same way.")


def main():
    demo_class_context_manager()
    demo_function_context_manager()
    demo_exception_suppression()


if __name__ == "__main__":
    main()
