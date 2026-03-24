"""
09_combined_modeling_demo.py
==============================
Combines the techniques from Day 2 into one cohesive, compact example:
  - @dataclass for a data-centric type
  - @property for computed values and validation
  - Context manager for resource lifecycle
  - Function decorator for timing
  - __init_subclass__ for automatic plugin registration

Domain: a small pipeline execution framework where data sources are
pluggable, jobs track timing automatically, and resources ensure cleanup.

Run:
    python day-02/09_combined_modeling_demo.py
"""

import time
import functools
import contextlib
from dataclasses import dataclass, field


# ══════════════════════════════════════════════════════════════════════════════
# 1. DECORATOR — time any function automatically
# ══════════════════════════════════════════════════════════════════════════════

def timed(func):
    """Record wall-clock time of a function call on the instance's timing_log."""

    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        start = time.perf_counter()
        result = func(self, *args, **kwargs)
        elapsed_ms = (time.perf_counter() - start) * 1000
        # Only log if the instance has a timing_log attribute (duck typing)
        if hasattr(self, "timing_log"):
            self.timing_log[func.__name__] = round(elapsed_ms, 3)
        return result

    return wrapper


# ══════════════════════════════════════════════════════════════════════════════
# 2. DATACLASS — a job result carrying computed properties
# ══════════════════════════════════════════════════════════════════════════════

@dataclass
class JobResult:
    """Immutable summary of a completed pipeline run."""
    source: str
    records_in: int
    records_out: int
    timing_log: dict[str, float] = field(default_factory=dict)

    @property
    def drop_rate(self) -> float:
        """Fraction of records dropped (0.0 – 1.0)."""
        if self.records_in == 0:
            return 0.0
        return (self.records_in - self.records_out) / self.records_in

    @property
    def drop_pct(self) -> str:
        return f"{self.drop_rate * 100:.1f}%"

    def summary(self) -> str:
        timing_str = ", ".join(f"{k}={v} ms" for k, v in self.timing_log.items())
        return (
            f"JobResult | source={self.source!r} "
            f"in={self.records_in:,} out={self.records_out:,} "
            f"drop={self.drop_pct} | {timing_str}"
        )


# ══════════════════════════════════════════════════════════════════════════════
# 3. PLUGIN REGISTRY — pluggable data sources via __init_subclass__
# ══════════════════════════════════════════════════════════════════════════════

class DataSource:
    """Base class for pluggable data sources.

    Subclasses register themselves automatically.
    Implement: fetch(self) -> list[dict]
    """

    _registry: dict[str, type["DataSource"]] = {}

    def __init_subclass__(cls, source_type: str, **kwargs):
        super().__init_subclass__(**kwargs)
        DataSource._registry[source_type] = cls
        cls.source_type = source_type

    @classmethod
    def create(cls, source_type: str, **kwargs) -> "DataSource":
        if source_type not in cls._registry:
            raise KeyError(f"Unknown source type {source_type!r}. Available: {sorted(cls._registry)}")
        return cls._registry[source_type](**kwargs)

    def fetch(self) -> list[dict]:
        raise NotImplementedError


class InMemorySource(DataSource, source_type="memory"):
    """A pre-loaded in-memory source — useful for testing."""

    def __init__(self, rows: list[dict]):
        self._rows = rows

    def fetch(self) -> list[dict]:
        time.sleep(0.002)  # simulate I/O
        return list(self._rows)


class GeneratedSource(DataSource, source_type="generated"):
    """Generates synthetic rows on demand."""

    def __init__(self, count: int = 10):
        self._count = count

    def fetch(self) -> list[dict]:
        time.sleep(0.001)
        return [{"id": i, "value": i * 1.5} for i in range(self._count)]


# ══════════════════════════════════════════════════════════════════════════════
# 4. CONTEXT MANAGER — pipeline session lifecycle
# ══════════════════════════════════════════════════════════════════════════════

class PipelineSession:
    """Manages the lifecycle of a pipeline run.

    Attributes collected here are available to all steps within the session.
    Ensures resource cleanup even if a step raises.
    """

    def __init__(self, name: str):
        self.name = name
        self.timing_log: dict[str, float] = {}
        self._active = False

    def __enter__(self) -> "PipelineSession":
        print(f"  [session] Starting '{self.name}'")
        self._active = True
        self._start = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        total_ms = (time.perf_counter() - self._start) * 1000
        self.timing_log["total"] = round(total_ms, 3)
        self._active = False
        if exc_type:
            print(f"  [session] '{self.name}' ended with error: {exc_type.__name__}: {exc_val}")
        else:
            print(f"  [session] '{self.name}' completed in {total_ms:.1f} ms")
        return False  # let exceptions propagate


# ══════════════════════════════════════════════════════════════════════════════
# 5. JOB — ties everything together
# ══════════════════════════════════════════════════════════════════════════════

class FilterJob:
    """A simple filter + transform job decorated for timing."""

    def __init__(self, session: PipelineSession):
        self.session = session
        self.timing_log = session.timing_log  # share the log

    @timed
    def fetch(self, source: DataSource) -> list[dict]:
        return source.fetch()

    @timed
    def filter_rows(self, rows: list[dict], min_value: float) -> list[dict]:
        return [r for r in rows if r.get("value", 0) >= min_value]

    def run(self, source: DataSource, min_value: float = 5.0) -> JobResult:
        raw = self.fetch(source)
        filtered = self.filter_rows(raw, min_value)
        return JobResult(
            source=source.source_type,
            records_in=len(raw),
            records_out=len(filtered),
            timing_log=dict(self.timing_log),
        )


# ══════════════════════════════════════════════════════════════════════════════
# DEMO
# ══════════════════════════════════════════════════════════════════════════════

def demo_combined():
    print("=" * 55)
    print("COMBINED DEMO: All Day-2 techniques in one example")
    print("=" * 55)

    print("\n--- Registered data sources ---")
    print(f"  {sorted(DataSource._registry)}")

    print("\n--- Run with 'generated' source ---")
    source = DataSource.create("generated", count=20)
    with PipelineSession("etl_demo") as session:
        job = FilterJob(session)
        result = job.run(source, min_value=7.5)

    print(f"\n  {result.summary()}")

    print("\n--- Run with 'memory' source ---")
    fixed_data = [{"id": i, "value": float(i)} for i in range(5)]
    mem_source = DataSource.create("memory", rows=fixed_data)
    with PipelineSession("memory_run") as session:
        job = FilterJob(session)
        result2 = job.run(mem_source, min_value=2.0)

    print(f"\n  {result2.summary()}")

    print("\n--- Error handling inside session ---")
    try:
        with PipelineSession("failing_run") as session:
            raise RuntimeError("simulated downstream failure")
    except RuntimeError:
        pass  # already reported by __exit__


def demo_technique_map():
    print("\n" + "=" * 55)
    print("TECHNIQUE MAP")
    print("=" * 55)
    print("""
  Technique               Where it appears in this demo
  ──────────────────────  ──────────────────────────────────────────
  @dataclass              JobResult — data-centric type, no boilerplate
  @property               drop_rate, drop_pct — computed from stored fields
  Context manager         PipelineSession — __enter__ / __exit__ lifecycle
  Function decorator      @timed — wraps fetch() and filter_rows() on FilterJob
  __init_subclass__       DataSource — InMemorySource & GeneratedSource auto-register
    """)


def main():
    demo_combined()
    demo_technique_map()


if __name__ == "__main__":
    main()
