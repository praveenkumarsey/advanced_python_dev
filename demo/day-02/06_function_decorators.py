"""
06_function_decorators.py
===========================
Demonstrates function decorators:
  - A minimal decorator that wraps a function
  - Timing and logging decorators
  - Why functools.wraps matters (preserving __name__ and __doc__)
  - Stacking multiple decorators
  - A decorator factory that accepts arguments

Run:
    python day-02/06_function_decorators.py
"""

import time
import functools


# ══════════════════════════════════════════════════════════════════════════════
# PART 1: Minimal decorator — the pattern made explicit
# ══════════════════════════════════════════════════════════════════════════════

def make_loud(func):
    """A decorator that announces when a function is called and returns."""

    def wrapper(*args, **kwargs):
        print(f"  → calling {func.__name__}")
        result = func(*args, **kwargs)
        print(f"  ← {func.__name__} returned {result!r}")
        return result

    return wrapper


@make_loud
def add(a: int, b: int) -> int:
    """Add two integers."""
    return a + b


def demo_minimal_decorator():
    print("=" * 55)
    print("PART 1: Minimal decorator")
    print("=" * 55)

    result = add(3, 4)
    print(f"Final result: {result}")
    print()
    print("The @make_loud syntax is equivalent to:")
    print("  add = make_loud(add)")


# ══════════════════════════════════════════════════════════════════════════════
# PART 2: functools.wraps — preserving function identity
# ══════════════════════════════════════════════════════════════════════════════

def timing_without_wraps(func):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"  [{func.__name__}] took {elapsed * 1000:.3f} ms")
        return result
    return wrapper


def timing(func):
    @functools.wraps(func)  # copies __name__, __doc__, __module__, __qualname__
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"  [{func.__name__}] took {elapsed * 1000:.3f} ms")
        return result
    return wrapper


@timing_without_wraps
def compute_without(n: int) -> int:
    """Sum integers up to n."""
    return sum(range(n))


@timing
def compute(n: int) -> int:
    """Sum integers up to n."""
    return sum(range(n))


def demo_functools_wraps():
    print("\n" + "=" * 55)
    print("PART 2: functools.wraps — preserving function identity")
    print("=" * 55)

    compute_without(100_000)
    compute(100_000)

    print()
    print(f"Without @functools.wraps:")
    print(f"  __name__ = {compute_without.__name__!r}")    # 'wrapper' — wrong
    print(f"  __doc__  = {compute_without.__doc__!r}")     # None — lost

    print()
    print(f"With @functools.wraps:")
    print(f"  __name__ = {compute.__name__!r}")            # 'compute' — correct
    print(f"  __doc__  = {compute.__doc__!r}")             # preserved


# ══════════════════════════════════════════════════════════════════════════════
# PART 3: Logging decorator
# ══════════════════════════════════════════════════════════════════════════════

def log_call(func):
    """Log function entry, exit, and any exception raised."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        arg_str = ", ".join(
            [repr(a) for a in args] + [f"{k}={v!r}" for k, v in kwargs.items()]
        )
        print(f"  CALL  {func.__name__}({arg_str})")
        try:
            result = func(*args, **kwargs)
            print(f"  OK    {func.__name__} → {result!r}")
            return result
        except Exception as e:
            print(f"  ERROR {func.__name__} raised {type(e).__name__}: {e}")
            raise

    return wrapper


@log_call
def divide(a: float, b: float) -> float:
    """Divide a by b."""
    if b == 0:
        raise ZeroDivisionError("b cannot be zero")
    return a / b


def demo_logging_decorator():
    print("\n" + "=" * 55)
    print("PART 3: Logging decorator")
    print("=" * 55)

    divide(10, 4)
    try:
        divide(10, 0)
    except ZeroDivisionError:
        pass  # already logged by decorator


# ══════════════════════════════════════════════════════════════════════════════
# PART 4: Decorator factory — decorator that accepts arguments
# ══════════════════════════════════════════════════════════════════════════════

def retry(max_attempts: int = 3, delay_sec: float = 0.0):
    """Decorator factory: retry a function up to max_attempts times on exception."""

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exc = e
                    print(f"  Attempt {attempt}/{max_attempts} failed: {e}")
                    if attempt < max_attempts and delay_sec > 0:
                        time.sleep(delay_sec)
            raise last_exc  # type: ignore

        return wrapper

    return decorator


_call_count = 0  # module-level counter to simulate flaky behaviour


@retry(max_attempts=3)
def flaky_fetch(url: str) -> str:
    """Simulates a function that fails the first two times."""
    global _call_count
    _call_count += 1
    if _call_count < 3:
        raise ConnectionError(f"Could not reach {url}")
    return f"<data from {url}>"


def demo_decorator_factory():
    print("\n" + "=" * 55)
    print("PART 4: Decorator factory with arguments")
    print("=" * 55)

    result = flaky_fetch("https://api.example.com/data")
    print(f"Final result: {result!r}")


# ══════════════════════════════════════════════════════════════════════════════
# PART 5: Stacking decorators
# ══════════════════════════════════════════════════════════════════════════════

@log_call
@timing
def process_batch(batch_id: str, size: int) -> dict:
    """Process a batch of records."""
    time.sleep(0.001)  # simulate work
    return {"batch_id": batch_id, "processed": size}


def demo_stacking():
    print("\n" + "=" * 55)
    print("PART 5: Stacking decorators")
    print("=" * 55)

    print("Decorators apply bottom-up: timing wraps process_batch first,")
    print("then log_call wraps the already-timed version.\n")
    process_batch("B-042", 500)


def main():
    demo_minimal_decorator()
    demo_functools_wraps()
    demo_logging_decorator()
    demo_decorator_factory()
    demo_stacking()


if __name__ == "__main__":
    main()
