"""
07_class_decorators.py
=======================
Demonstrates class decorators:
  - A class decorator that adds metadata to a class
  - A class decorator that adds a method to a class
  - When class decorators are useful vs. when inheritance is better
  - The difference between a class decorator and a metaclass (brief note)

Run:
    python day-02/07_class_decorators.py
"""


# ══════════════════════════════════════════════════════════════════════════════
# PART 1: Class decorator that adds metadata
# ══════════════════════════════════════════════════════════════════════════════
#
# A class decorator is a callable that receives a class and returns a class.
# It can add attributes, wrap methods, or register the class — without
# requiring the class to inherit from anything.

def register_component(kind: str):
    """Decorator factory: stamps a class with a component kind label."""

    def decorator(cls):
        cls.component_kind = kind
        cls.component_name = cls.__name__
        return cls

    return decorator


@register_component(kind="extractor")
class S3Extractor:
    """Reads data from S3."""

    def run(self, path: str) -> list:
        print(f"  Extracting from {path}")
        return [{"id": 1}, {"id": 2}]


@register_component(kind="transformer")
class DropNullsTransformer:
    """Removes rows with null values."""

    def run(self, rows: list) -> list:
        return [r for r in rows if all(v is not None for v in r.values())]


@register_component(kind="loader")
class BigQueryLoader:
    """Loads data into BigQuery."""

    def run(self, rows: list, table: str) -> None:
        print(f"  Loading {len(rows)} rows into {table}")


def demo_metadata_decorator():
    print("=" * 55)
    print("PART 1: Class decorator adding metadata")
    print("=" * 55)

    for cls in (S3Extractor, DropNullsTransformer, BigQueryLoader):
        print(f"{cls.__name__:30s} kind={cls.component_kind!r}")

    print()
    print("Each class carries its component_kind without inheriting from a base.")
    print("Useful when classes come from different hierarchies but share a label.")


# ══════════════════════════════════════════════════════════════════════════════
# PART 2: Class decorator that adds a method
# ══════════════════════════════════════════════════════════════════════════════

def add_describe(cls):
    """Add a describe() method to any class that has a __dataclass_fields__ dict
    or explicit fields listed in _describe_fields.
    Works as a post-hoc enhancement — no inheritance required.
    """

    def describe(self) -> str:
        parts = [f"{cls.__name__}:"]
        for attr, val in vars(self).items():
            if not attr.startswith("_"):
                parts.append(f"  {attr} = {val!r}")
        return "\n".join(parts)

    cls.describe = describe
    return cls


@add_describe
class RunSummary:
    def __init__(self, job: str, records: int, duration_sec: float):
        self.job = job
        self.records = records
        self.duration_sec = duration_sec


def demo_add_method():
    print("\n" + "=" * 55)
    print("PART 2: Class decorator adding a method")
    print("=" * 55)

    summary = RunSummary("etl_daily", 45_000, 12.4)
    print(summary.describe())
    print()
    print("describe() was injected by the decorator — RunSummary did not inherit it.")


# ══════════════════════════════════════════════════════════════════════════════
# PART 3: Class decorator that enforces a convention
# ══════════════════════════════════════════════════════════════════════════════

def require_docstring(cls):
    """Raise an error at class definition time if the class has no docstring.

    Useful for enforcing documentation standards in large teams.
    Runs at import time (definition time) — not at instantiation.
    """
    if not cls.__doc__ or not cls.__doc__.strip():
        raise TypeError(
            f"Class {cls.__name__!r} is missing a docstring. "
            f"All pipeline components must be documented."
        )
    return cls


@require_docstring
class ValidatedStep:
    """A pipeline step that has passed the documentation requirement."""

    def run(self) -> None:
        print("  Running validated step")


def demo_convention_enforcement():
    print("\n" + "=" * 55)
    print("PART 3: Class decorator enforcing a convention")
    print("=" * 55)

    step = ValidatedStep()
    step.run()

    print("\nAttempting to define a class without a docstring:")
    try:
        @require_docstring
        class UndocumentedStep:
            pass
    except TypeError as e:
        print(f"  Error at class definition: {e}")

    print()
    print("The error fired at class-definition time, not at instantiation.")
    print("This catches the problem as early as possible (during import).")


# ══════════════════════════════════════════════════════════════════════════════
# PART 4: When to use a class decorator vs. inheritance
# ══════════════════════════════════════════════════════════════════════════════

def demo_when_to_use():
    print("\n" + "=" * 55)
    print("PART 4: Class decorator vs. inheritance")
    print("=" * 55)
    print("""
  Use a class decorator when:
  ─────────────────────────────────────────────────────
  • You want to add metadata, a method, or a label
    to classes that don't share a common base.
  • You want to apply a cross-cutting concern
    (logging, registration, validation) without coupling.
  • The added behaviour is orthogonal to the class's
    domain responsibility.

  Use inheritance when:
  ─────────────────────────────────────────────────────
  • The classes share a genuine IS-A relationship.
  • Subclasses need to override behaviour, not just
    receive it.
  • You want the base class to enforce an interface
    (combine with ABC for that).

  A class decorator modifies a class from the outside.
  Inheritance builds a new type from the inside.
    """)


def main():
    demo_metadata_decorator()
    demo_add_method()
    demo_convention_enforcement()
    demo_when_to_use()


if __name__ == "__main__":
    main()
