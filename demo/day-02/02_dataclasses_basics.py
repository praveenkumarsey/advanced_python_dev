"""
02_dataclasses_basics.py
=========================
Demonstrates the @dataclass decorator:
  - A regular class written by hand vs the same class as a dataclass
  - Auto-generated __init__, __repr__, and __eq__
  - How dataclasses reduce boilerplate without hiding behaviour

Run:
    python day-02/02_dataclasses_basics.py
"""

from dataclasses import dataclass


# ══════════════════════════════════════════════════════════════════════════════
# PART 1: Regular class — written by hand
# ══════════════════════════════════════════════════════════════════════════════

class PipelineConfigManual:
    """Manually written data class. All boilerplate, no logic."""

    def __init__(self, name: str, source: str, destination: str, parallelism: int = 4):
        self.name = name
        self.source = source
        self.destination = destination
        self.parallelism = parallelism

    def __repr__(self) -> str:
        return (
            f"PipelineConfigManual("
            f"name={self.name!r}, "
            f"source={self.source!r}, "
            f"destination={self.destination!r}, "
            f"parallelism={self.parallelism})"
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, PipelineConfigManual):
            return NotImplemented
        return (
            self.name == other.name
            and self.source == other.source
            and self.destination == other.destination
            and self.parallelism == other.parallelism
        )


# ══════════════════════════════════════════════════════════════════════════════
# PART 2: Same class as a dataclass
# ══════════════════════════════════════════════════════════════════════════════
#
# @dataclass generates __init__, __repr__, and __eq__ automatically.
# The class definition expresses WHAT the data is, not HOW to manage it.

@dataclass
class PipelineConfig:
    """Dataclass version — identical behaviour, far less code."""
    name: str
    source: str
    destination: str
    parallelism: int = 4   # default value, just like a parameter default


# ══════════════════════════════════════════════════════════════════════════════
# PART 3: A slightly richer dataclass
# ══════════════════════════════════════════════════════════════════════════════

@dataclass
class DatasetMeta:
    """Metadata about a dataset used in a pipeline."""
    name: str
    format: str          # e.g. "parquet", "csv", "json"
    row_count: int
    size_mb: float
    is_partitioned: bool = False

    def summary(self) -> str:
        partitioned = "partitioned" if self.is_partitioned else "flat"
        return (
            f"{self.name} [{self.format.upper()}] "
            f"— {self.row_count:,} rows, {self.size_mb:.1f} MB, {partitioned}"
        )


def demo_manual_vs_dataclass():
    print("=" * 55)
    print("PART 1 & 2: Manual class vs @dataclass")
    print("=" * 55)

    manual = PipelineConfigManual("etl_daily", "s3://raw/", "s3://clean/")
    auto = PipelineConfig("etl_daily", "s3://raw/", "s3://clean/")

    print(f"Manual   repr : {manual!r}")
    print(f"Dataclass repr: {auto!r}")
    print()

    # Both support equality by value
    manual2 = PipelineConfigManual("etl_daily", "s3://raw/", "s3://clean/")
    auto2 = PipelineConfig("etl_daily", "s3://raw/", "s3://clean/")

    print(f"manual == manual2 : {manual == manual2}")
    print(f"auto   == auto2   : {auto == auto2}")
    print()
    print("Same behaviour — but the dataclass required far less code.")


def demo_dataclass_features():
    print("\n" + "=" * 55)
    print("PART 3: Dataclass with methods and defaults")
    print("=" * 55)

    ds1 = DatasetMeta("taxi_trips", "parquet", 1_200_000, 340.5, is_partitioned=True)
    ds2 = DatasetMeta("user_events", "json", 85_000, 12.3)
    ds3 = DatasetMeta("taxi_trips", "parquet", 1_200_000, 340.5, is_partitioned=True)

    print(ds1.summary())
    print(ds2.summary())
    print()

    # Generated __repr__
    print(f"repr: {ds1!r}")
    print()

    # Generated __eq__
    print(f"ds1 == ds3 (same data): {ds1 == ds3}")
    print(f"ds1 == ds2 (diff data): {ds1 == ds2}")


def demo_dataclass_inspection():
    print("\n" + "=" * 55)
    print("PART 4: What @dataclass generates")
    print("=" * 55)

    import inspect
    # Show the generated __init__ signature
    sig = inspect.signature(PipelineConfig.__init__)
    print(f"Generated __init__ signature: {sig}")
    print()
    print("@dataclass generates:")
    print("  __init__  — positional + keyword args from the field definitions")
    print("  __repr__  — class name + all fields")
    print("  __eq__    — field-by-field comparison")
    print()
    print("It does NOT generate __hash__ by default when __eq__ is defined.")
    print("Add frozen=True or eq=False to control hash behaviour.")


def main():
    demo_manual_vs_dataclass()
    demo_dataclass_features()
    demo_dataclass_inspection()


if __name__ == "__main__":
    main()
