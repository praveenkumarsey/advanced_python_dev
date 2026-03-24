"""
03_dataclasses_field_defaults.py
==================================
Demonstrates safe default values in dataclasses:
  - Simple scalar defaults
  - Why mutable defaults (list, dict) are forbidden as plain defaults
  - field(default_factory=...) to create a fresh container per instance
  - field(default=...) for other customisation
  - frozen=True for immutable dataclasses

Run:
    python day-02/03_dataclasses_field_defaults.py
"""

from dataclasses import dataclass, field


# ══════════════════════════════════════════════════════════════════════════════
# PART 1: Scalar defaults — safe and simple
# ══════════════════════════════════════════════════════════════════════════════

@dataclass
class JobConfig:
    name: str
    parallelism: int = 4          # scalar default — safe
    timeout_sec: int = 300        # scalar default — safe
    retry_on_failure: bool = True # scalar default — safe


def demo_scalar_defaults():
    print("=" * 55)
    print("PART 1: Scalar defaults")
    print("=" * 55)

    j1 = JobConfig("ingest_job")
    j2 = JobConfig("transform_job", parallelism=8, timeout_sec=600)

    print(f"j1: {j1!r}")
    print(f"j2: {j2!r}")
    print("Scalar defaults are safe — each instance gets an independent copy.")


# ══════════════════════════════════════════════════════════════════════════════
# PART 2: Mutable default trap — why list/dict defaults are forbidden
# ══════════════════════════════════════════════════════════════════════════════
#
# @dataclass refuses `tags: list = []` and raises a TypeError to protect you.
# This is intentional — the same trap exists in regular function defaults.

class StepBad:
    """Regular class with a mutable default — classic trap."""

    def __init__(self, name: str, tags=[]):  # <-- shared list!
        self.name = name
        self.tags = tags


def demo_mutable_trap():
    print("\n" + "=" * 55)
    print("PART 2: Mutable default trap")
    print("=" * 55)

    # Show the trap with a regular class first
    s1 = StepBad("extract")
    s2 = StepBad("load")

    s1.tags.append("critical")
    print(f"s1.tags after append: {s1.tags}")
    print(f"s2.tags — untouched? : {s2.tags}")
    print("Both share the same list! Mutation through s1 is visible in s2.")
    print()

    # Show that @dataclass raises a clear error if you try the same thing
    print("Attempting: @dataclass with tags: list = []  ...")
    try:
        # Evaluated at definition time — raises ValueError
        exec(
            "from dataclasses import dataclass\n"
            "@dataclass\n"
            "class BadDC:\n"
            "    tags: list = []\n"
        )
    except ValueError as e:
        print(f"  dataclass raises ValueError: {e}")
    print("dataclass protects you by refusing mutable defaults.")


# ══════════════════════════════════════════════════════════════════════════════
# PART 3: field(default_factory=...) — the correct pattern
# ══════════════════════════════════════════════════════════════════════════════

@dataclass
class PipelineStep:
    name: str
    # default_factory=list creates a NEW list for each instance
    tags: list[str] = field(default_factory=list)
    metadata: dict[str, str] = field(default_factory=dict)
    depends_on: list[str] = field(default_factory=list)


def demo_default_factory():
    print("\n" + "=" * 55)
    print("PART 3: field(default_factory=...) — safe mutable defaults")
    print("=" * 55)

    step1 = PipelineStep("extract")
    step2 = PipelineStep("transform")

    step1.tags.append("critical")
    step1.metadata["owner"] = "team-data"

    print(f"step1.tags     : {step1.tags}")
    print(f"step2.tags     : {step2.tags}")
    print(f"step1.metadata : {step1.metadata}")
    print(f"step2.metadata : {step2.metadata}")
    print("step1 and step2 have independent lists and dicts.")
    print()

    # With initial data via constructor
    step3 = PipelineStep("load", tags=["nightly", "s3"], depends_on=["transform"])
    print(f"step3: {step3!r}")


# ══════════════════════════════════════════════════════════════════════════════
# PART 4: field() for other customisation
# ══════════════════════════════════════════════════════════════════════════════

@dataclass
class Checkpoint:
    run_id: str
    records_written: int
    # repr=False — exclude from repr (e.g. large or sensitive fields)
    raw_payload: bytes = field(default=b"", repr=False)
    # init=False — not a constructor argument; set after construction
    is_committed: bool = field(default=False, init=False)

    def commit(self) -> None:
        self.is_committed = True


def demo_field_options():
    print("\n" + "=" * 55)
    print("PART 4: field() for repr and init control")
    print("=" * 55)

    cp = Checkpoint("run-007", 45_000, raw_payload=b"\x00" * 1024)
    print(f"Before commit: {cp!r}")
    print("  raw_payload is excluded from repr (repr=False).")
    print("  is_committed is not in __init__ (init=False).")

    cp.commit()
    print(f"After commit:  {cp!r}")


# ══════════════════════════════════════════════════════════════════════════════
# PART 5: frozen=True — immutable dataclass
# ══════════════════════════════════════════════════════════════════════════════

@dataclass(frozen=True)
class SchemaVersion:
    """Immutable — once created, fields cannot be changed.

    frozen=True also generates __hash__, making instances usable in sets
    and as dictionary keys.
    """
    name: str
    version: int
    format: str


def demo_frozen():
    print("\n" + "=" * 55)
    print("PART 5: frozen=True — immutable dataclass")
    print("=" * 55)

    v1 = SchemaVersion("events", 3, "json")
    print(f"v1: {v1!r}")

    try:
        v1.version = 4  # type: ignore
    except Exception as e:
        print(f"Cannot mutate frozen dataclass: {type(e).__name__}: {e}")

    # frozen + __hash__ → usable as dict key or set member
    schema_registry = {v1: "https://schema.example.com/events/v3"}
    print(f"Used as dict key: {schema_registry[v1]}")

    v2 = SchemaVersion("events", 3, "json")
    print(f"v1 == v2: {v1 == v2}")      # True — same field values
    print(f"v1 in {{v1}}: {v1 in {v1}}")  # True — hashable


def main():
    demo_scalar_defaults()
    demo_mutable_trap()
    demo_default_factory()
    demo_field_options()
    demo_frozen()


if __name__ == "__main__":
    main()
