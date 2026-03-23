"""
src/validify/main.py — CLI entry point for the validation pipeline.

─────────────────────────────────────────────────────────
DAY 1 TASK (create this file)
─────────────────────────────────────────────────────────
Create a runner that produces the same output as starter/validate_trips.py
but uses the new class hierarchy:

  1. Accept a CSV path from sys.argv[1].
  2. Open the CSV with open() + csv.DictReader (plain, no context manager yet).
  3. Instantiate rules manually:
       rules = [NullCheckRule("vendor_id"), RangeRule("passenger_count", 1, 8), ...]
  4. For each record, call each rule: result = rule(record)  # __call__
  5. Collect ValidationResult objects.
  6. Print a summary (same format as the starter script).

─────────────────────────────────────────────────────────
DAY 2 TASK (update this file)
─────────────────────────────────────────────────────────
  - Apply @timeit to the main validation function.
  - Build a Report dataclass from the results and print pass_rate from it.

─────────────────────────────────────────────────────────
DAY 3 TASK (update this file)
─────────────────────────────────────────────────────────
  - Replace the hardcoded rules list with:
      rules = RuleFactory.from_config("config/rules.yaml")
  - Wrap the CSV open() in DatasetLoader context manager (stretch).
  - Run records through normalize_record before validation.

─────────────────────────────────────────────────────────
Run with:
    python src/validify/main.py data/taxi_trips_sample.csv
─────────────────────────────────────────────────────────
"""

import csv
import sys
from pathlib import Path


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python src/validify/main.py <path/to/trips.csv>")
        sys.exit(1)

    csv_path = Path(sys.argv[1])
    if not csv_path.exists():
        print(f"Error: file not found — {csv_path}")
        sys.exit(1)

    # ---------------------------------------------------------------------------
    # YOUR CODE BELOW — follow the Day 1 steps in the docstring above
    # ---------------------------------------------------------------------------


if __name__ == "__main__":
    main()
