"""
02_functions_and_exceptions.py
================================
Demonstrates function parameters, default values, return values,
local scope, and exception handling with try/except/else/finally.

Run:
    python day-01/02_functions_and_exceptions.py
"""


# ── Parameters and return values ────────────────────────────────────────────

def calculate_discount(price, discount_pct=10):
    """Return price after applying a percentage discount.

    discount_pct defaults to 10 if not provided.
    """
    if not (0 <= discount_pct <= 100):
        raise ValueError(f"discount_pct must be 0–100, got {discount_pct}")
    reduction = price * (discount_pct / 100)
    return price - reduction


def demo_parameters():
    print("=" * 50)
    print("SECTION 1: Parameters and default values")
    print("=" * 50)

    print(calculate_discount(200))           # uses default 10%
    print(calculate_discount(200, 25))       # explicit 25%
    print(calculate_discount(200, discount_pct=50))  # keyword argument


# ── Local scope ─────────────────────────────────────────────────────────────

def demo_scope():
    print("\n" + "=" * 50)
    print("SECTION 2: Local scope")
    print("=" * 50)

    rate = 0.05  # this is a local variable — it shadows nothing here

    def apply_rate(amount):
        # rate here is read from the enclosing scope (closure)
        return amount * (1 + rate)

    print(f"apply_rate(1000) = {apply_rate(1000)}")
    print(f"rate in outer scope is still: {rate}")

    # Local reassignment inside a function does not affect the outer name
    outer = "original"

    def modify():
        outer = "local copy"  # noqa: F841 — creates a new local, outer unchanged
        return outer

    modify()
    print(f"\nouter after modify() = '{outer}'")
    print("Reassignment inside modify() created a new local — outer is unchanged.")


# ── Exception handling ───────────────────────────────────────────────────────

def parse_sensor_reading(raw_value):
    """Convert a string sensor reading to float. Raises ValueError on bad input."""
    value = float(raw_value)  # raises ValueError if raw_value is not numeric
    if value < 0:
        raise ValueError(f"Sensor reading cannot be negative: {value}")
    return value


def demo_exceptions():
    print("\n" + "=" * 50)
    print("SECTION 3: try / except / else / finally")
    print("=" * 50)

    test_cases = ["23.7", "-5.1", "bad_data", "0.0"]

    for raw in test_cases:
        print(f"\n  Processing raw value: {raw!r}")
        try:
            reading = parse_sensor_reading(raw)
        except ValueError as e:
            # Runs only when an exception is raised in the try block
            print(f"  [except]  Invalid reading — {e}")
        else:
            # Runs only when NO exception was raised
            print(f"  [else]    Valid reading: {reading}")
        finally:
            # Always runs — good for cleanup (closing files, releasing locks, etc.)
            print(f"  [finally] Finished processing {raw!r}")


# ── Raising and re-raising ───────────────────────────────────────────────────

def load_pipeline_config(config: dict):
    """Extract required keys from a configuration dictionary."""
    required_keys = ["source", "destination", "format"]
    missing = [k for k in required_keys if k not in config]
    if missing:
        raise KeyError(f"Missing required config keys: {missing}")
    return config


def demo_raising():
    print("\n" + "=" * 50)
    print("SECTION 4: Raising exceptions with context")
    print("=" * 50)

    valid_config = {"source": "s3://bucket/raw", "destination": "s3://bucket/clean", "format": "parquet"}
    incomplete_config = {"source": "s3://bucket/raw"}

    try:
        cfg = load_pipeline_config(valid_config)
        print(f"Loaded config: {cfg}")
    except KeyError as e:
        print(f"Config error: {e}")

    try:
        load_pipeline_config(incomplete_config)
    except KeyError as e:
        print(f"Config error: {e}")


def main():
    demo_parameters()
    demo_scope()
    demo_exceptions()
    demo_raising()


if __name__ == "__main__":
    main()
