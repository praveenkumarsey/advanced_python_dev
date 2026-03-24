"""
01_repr_and_eq.py
==================
Demonstrates Python's data model for object representation and equality:
  - The default (useless) repr and equality behaviour
  - Implementing __repr__ for readable output
  - Implementing __str__ for user-facing strings
  - Implementing __eq__ for value-based equality

Run:
    python day-02/01_repr_and_eq.py
"""


# ══════════════════════════════════════════════════════════════════════════════
# PART 1: Default repr and equality are often not useful
# ══════════════════════════════════════════════════════════════════════════════

class JobRunDefault:
    """No dunder methods defined — Python falls back to its defaults."""

    def __init__(self, job_id: str, status: str, records: int):
        self.job_id = job_id
        self.status = status
        self.records = records


def demo_default_behaviour():
    print("=" * 55)
    print("PART 1: Default repr and equality")
    print("=" * 55)

    run1 = JobRunDefault("job-101", "success", 4500)
    run2 = JobRunDefault("job-101", "success", 4500)

    print(f"run1 repr  : {run1!r}")       # e.g. <__main__.JobRunDefault object at 0x...>
    print(f"run1 str   : {run1}")         # same as repr by default
    print(f"run1 == run2: {run1 == run2}") # False — compares identity (memory address)
    print(f"run1 is run2: {run1 is run2}") # False — different objects
    print()
    print("Two objects with identical data are not considered equal.")
    print("The repr tells us nothing useful about their state.")


# ══════════════════════════════════════════════════════════════════════════════
# PART 2: __repr__ and __str__
# ══════════════════════════════════════════════════════════════════════════════
#
# __repr__  — aimed at developers: unambiguous, ideally eval()-able
# __str__   — aimed at end users: readable, can omit internal details
# If only __repr__ is defined, str() falls back to it.

class JobRun:
    """A pipeline job run result with repr and str."""

    def __init__(self, job_id: str, status: str, records: int):
        self.job_id = job_id
        self.status = status
        self.records = records

    def __repr__(self) -> str:
        # Convention: class name + enough info to reconstruct the object
        return (
            f"JobRun(job_id={self.job_id!r}, "
            f"status={self.status!r}, "
            f"records={self.records})"
        )

    def __str__(self) -> str:
        # Human-readable summary, used by print()
        return f"[{self.status.upper()}] Job {self.job_id} — {self.records:,} records processed"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, JobRun):
            return NotImplemented
        return self.job_id == other.job_id and self.status == other.status and self.records == other.records


def demo_repr_and_str():
    print("\n" + "=" * 55)
    print("PART 2: __repr__ and __str__")
    print("=" * 55)

    run = JobRun("job-202", "success", 12_450)

    print(f"repr : {run!r}")   # uses __repr__
    print(f"str  : {run}")     # uses __str__ (falls back to __repr__ if not defined)
    print(f"list : {[run]}")   # repr is used inside containers


# ══════════════════════════════════════════════════════════════════════════════
# PART 3: __eq__ for value-based equality
# ══════════════════════════════════════════════════════════════════════════════

class MetricPoint:
    """A timestamped measurement. Two points are equal if all fields match."""

    def __init__(self, metric: str, value: float, timestamp: str):
        self.metric = metric
        self.value = value
        self.timestamp = timestamp

    def __repr__(self) -> str:
        return f"MetricPoint({self.metric!r}, {self.value}, {self.timestamp!r})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, MetricPoint):
            return NotImplemented  # let Python try the other side
        return (
            self.metric == other.metric
            and self.value == other.value
            and self.timestamp == other.timestamp
        )


def demo_eq():
    print("\n" + "=" * 55)
    print("PART 3: __eq__ for value-based equality")
    print("=" * 55)

    a = MetricPoint("cpu_pct", 72.5, "2026-03-01T10:00:00")
    b = MetricPoint("cpu_pct", 72.5, "2026-03-01T10:00:00")
    c = MetricPoint("cpu_pct", 90.0, "2026-03-01T10:00:00")

    print(f"a = {a!r}")
    print(f"b = {b!r}")
    print(f"c = {c!r}")
    print()
    print(f"a == b  (same data)      : {a == b}")   # True
    print(f"a == c  (different value): {a == c}")   # False
    print(f"a is b  (same object?)   : {a is b}")   # False — different objects
    print()

    # Equality enables use in sets and as dict keys (with __hash__ too)
    # Without __eq__, deduplication based on value would fail
    readings = [a, b, c]
    unique = []
    seen = []
    for r in readings:
        if r not in seen:
            seen.append(r)
            unique.append(r)
    print(f"De-duplicated readings: {unique}")
    print("a and b are collapsed into one because they are equal by value.")


# ══════════════════════════════════════════════════════════════════════════════
# PART 4: Quick comparison — before and after
# ══════════════════════════════════════════════════════════════════════════════

def demo_before_after():
    print("\n" + "=" * 55)
    print("PART 4: Before / After summary")
    print("=" * 55)

    # Before
    bad = JobRunDefault("job-303", "failed", 0)
    print(f"Before __repr__/__eq__:")
    print(f"  repr : {bad!r}")
    print(f"  equal to itself by value? {bad == JobRunDefault('job-303', 'failed', 0)}")

    # After
    good = JobRun("job-303", "failed", 0)
    print(f"\nAfter __repr__/__eq__:")
    print(f"  repr : {good!r}")
    print(f"  str  : {good}")
    print(f"  equal to itself by value? {good == JobRun('job-303', 'failed', 0)}")


def main():
    demo_default_behaviour()
    demo_repr_and_str()
    demo_eq()
    demo_before_after()


if __name__ == "__main__":
    main()
