"""
04_properties_advanced.py
===========================
Demonstrates advanced property usage:
  - A computed (read-only) property derived from stored state
  - A validated property setter that rejects bad values
  - Separating the stored internal value from the presented value
  - Using __post_init__ with dataclasses for validation

Run:
    python day-02/04_properties_advanced.py
"""

from dataclasses import dataclass, field


# ══════════════════════════════════════════════════════════════════════════════
# PART 1: Computed property — derived from stored state
# ══════════════════════════════════════════════════════════════════════════════

class DataWindow:
    """A time-bounded data window. Duration is always derived from its boundaries."""

    def __init__(self, start_ts: float, end_ts: float):
        if end_ts <= start_ts:
            raise ValueError(f"end_ts must be after start_ts (got {start_ts}, {end_ts})")
        self._start = start_ts
        self._end = end_ts

    @property
    def start(self) -> float:
        return self._start

    @property
    def end(self) -> float:
        return self._end

    @property
    def duration_sec(self) -> float:
        """Computed — always consistent with start and end. No risk of stale state."""
        return self._end - self._start

    @property
    def duration_min(self) -> float:
        return self.duration_sec / 60

    def __repr__(self) -> str:
        return f"DataWindow(start={self._start}, end={self._end}, duration={self.duration_sec}s)"


def demo_computed_property():
    print("=" * 55)
    print("PART 1: Computed property")
    print("=" * 55)

    w = DataWindow(start_ts=1_000_000.0, end_ts=1_003_600.0)
    print(f"Window   : {w!r}")
    print(f"Duration : {w.duration_sec:.0f} seconds = {w.duration_min:.1f} minutes")
    print()

    # Computed property has no setter — cannot be assigned accidentally
    try:
        w.duration_sec = 100  # type: ignore
    except AttributeError as e:
        print(f"Cannot set computed property: {e}")

    print()
    print("The duration is always consistent with start and end.")
    print("There is no stored duration field that could go out of sync.")


# ══════════════════════════════════════════════════════════════════════════════
# PART 2: Validation setter — reject bad values before storing
# ══════════════════════════════════════════════════════════════════════════════

class SamplingRate:
    """Encapsulates a data sampling rate in Hz with range validation."""

    MIN_HZ = 1
    MAX_HZ = 10_000

    def __init__(self, hz: int):
        self.hz = hz  # routes through setter

    @property
    def hz(self) -> int:
        return self._hz

    @hz.setter
    def hz(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError(f"hz must be an int, got {type(value).__name__}")
        if not (self.MIN_HZ <= value <= self.MAX_HZ):
            raise ValueError(f"hz must be in [{self.MIN_HZ}, {self.MAX_HZ}], got {value}")
        self._hz = value

    @property
    def period_ms(self) -> float:
        """Computed from hz — always synchronised."""
        return 1000 / self._hz

    def __repr__(self) -> str:
        return f"SamplingRate(hz={self._hz}, period={self.period_ms:.3f} ms)"


def demo_validation_setter():
    print("\n" + "=" * 55)
    print("PART 2: Validation setter")
    print("=" * 55)

    sr = SamplingRate(100)
    print(f"Initial: {sr!r}")

    sr.hz = 1000
    print(f"After   hz=1000: {sr!r}")

    for bad in [-1, 0, 20_000, 3.5, "fast"]:
        try:
            sr.hz = bad  # type: ignore
        except (ValueError, TypeError) as e:
            print(f"  Rejected {bad!r}: {e}")


# ══════════════════════════════════════════════════════════════════════════════
# PART 3: Stored value vs. presented value
# ══════════════════════════════════════════════════════════════════════════════
#
# Internally store data in a canonical form (e.g., lowercase, stripped).
# Present it in a user-friendly form via a property.

class ColumnSpec:
    """A table column specification.

    Stores name in canonical form (lowercase, stripped).
    Presents it capitalised for display.
    """

    ALLOWED_TYPES = {"integer", "float", "string", "boolean", "timestamp"}

    def __init__(self, name: str, dtype: str, nullable: bool = True):
        self.name = name    # setter normalises
        self.dtype = dtype  # setter validates

        self.nullable = nullable

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        if not value or not value.strip():
            raise ValueError("Column name cannot be empty")
        self._name = value.strip().lower()  # canonical: lowercase

    @property
    def display_name(self) -> str:
        """Presented form — title-cased."""
        return self._name.replace("_", " ").title()

    @property
    def dtype(self) -> str:
        return self._dtype

    @dtype.setter
    def dtype(self, value: str) -> None:
        normalised = value.strip().lower()
        if normalised not in self.ALLOWED_TYPES:
            raise ValueError(f"Unknown dtype {value!r}. Allowed: {sorted(self.ALLOWED_TYPES)}")
        self._dtype = normalised

    def __repr__(self) -> str:
        nullable_str = "nullable" if self.nullable else "not null"
        return f"ColumnSpec({self._name!r}: {self._dtype}, {nullable_str})"


def demo_stored_vs_presented():
    print("\n" + "=" * 55)
    print("PART 3: Stored value vs. presented value")
    print("=" * 55)

    col = ColumnSpec("  TRIP_DISTANCE  ", "Float")  # messy input
    print(f"Stored  name : {col.name!r}")          # canonical form
    print(f"Display name : {col.display_name!r}")  # presented form
    print(f"Stored  dtype: {col.dtype!r}")         # normalised
    print(f"repr         : {col!r}")
    print()
    print("Input was normalised at set-time — consumers always get clean data.")

    try:
        col.dtype = "blob"
    except ValueError as e:
        print(f"\nRejected bad dtype: {e}")


# ══════════════════════════════════════════════════════════════════════════════
# PART 4: Properties in a dataclass via __post_init__
# ══════════════════════════════════════════════════════════════════════════════

@dataclass
class BudgetAllocation:
    """Budget split across named categories. Validates that percentages sum to 100."""
    name: str
    allocations: dict[str, float]  # category → percentage

    def __post_init__(self) -> None:
        total = sum(self.allocations.values())
        if abs(total - 100.0) > 0.01:
            raise ValueError(
                f"Allocations must sum to 100.0, got {total:.2f} for '{self.name}'"
            )

    @property
    def largest_category(self) -> str:
        return max(self.allocations, key=self.allocations.__getitem__)


def demo_post_init():
    print("\n" + "=" * 55)
    print("PART 4: __post_init__ validation in a dataclass")
    print("=" * 55)

    b = BudgetAllocation("Q1", {"compute": 45.0, "storage": 30.0, "networking": 25.0})
    print(f"Budget: {b!r}")
    print(f"Largest category: {b.largest_category}")

    try:
        BudgetAllocation("Q2", {"compute": 60.0, "storage": 20.0})
    except ValueError as e:
        print(f"Invalid budget: {e}")


def main():
    demo_computed_property()
    demo_validation_setter()
    demo_stored_vs_presented()
    demo_post_init()


if __name__ == "__main__":
    main()
