#!/usr/bin/env python3
"""
validate_trips.py — Starter script for the Validify capstone project.

A procedural data validation script for NYC taxi trip records.
Reads a CSV, applies hardcoded checks, and produces a summary report.

As you read this script, notice:
  - Every check function returns the same (bool, str) tuple — a pattern
    that cries out for abstraction into a class hierarchy.
  - All rules are hardcoded in validate_record() — no config file.
  - check_trip_duration() crosses two fields, which doesn't fit the
    single-field function signature the other checks use.
  - The report is assembled from plain dicts — a dataclass would be cleaner.
  - Adding a new rule means editing this file in at least two places.

These observations drive the design decisions you will make in capstone/validify/.

Usage:
    python validate_trips.py <path/to/trips.csv>
    python validate_trips.py <path/to/trips.csv> --verbose
    python validate_trips.py <path/to/trips.csv> --limit 100
    python validate_trips.py <path/to/trips.csv> --output failed.csv
"""

import argparse
import csv
import sys
from datetime import datetime
from pathlib import Path


# ─────────────────────────────────────────────────────────────────────────────
# Validation functions
# Each returns (passed: bool, message: str).
# Empty message string means the check passed.
# ─────────────────────────────────────────────────────────────────────────────


def check_not_null(record: dict, field: str) -> tuple[bool, str]:
    """Fail if a field is absent, None, or whitespace-only."""
    value = record.get(field)
    if value is None or str(value).strip() == "":
        return False, f"{field}: value is null or empty"
    return True, ""


def check_range(
    record: dict, field: str, min_val: float, max_val: float
) -> tuple[bool, str]:
    """Fail if a numeric field is outside [min_val, max_val]."""
    raw = record.get(field)
    if raw is None or str(raw).strip() == "":
        return False, f"{field}: value is missing"
    try:
        value = float(raw)
    except ValueError:
        return False, f"{field}: '{raw}' is not a number"
    if not (min_val <= value <= max_val):
        return False, f"{field}: {value} is outside [{min_val}, {max_val}]"
    return True, ""


def check_allowed_values(
    record: dict, field: str, allowed: list[str]
) -> tuple[bool, str]:
    """Fail if a field's value is not in the allowed list."""
    value = str(record.get(field, "")).strip()
    if value not in allowed:
        return False, f"{field}: '{value}' is not one of {allowed}"
    return True, ""


def check_date_format(
    record: dict, field: str, fmt: str = "%Y-%m-%d %H:%M:%S"
) -> tuple[bool, str]:
    """Fail if a field cannot be parsed as a datetime in the given format."""
    raw = str(record.get(field, "")).strip()
    if not raw:
        return False, f"{field}: value is missing"
    try:
        datetime.strptime(raw, fmt)
    except ValueError:
        return False, f"{field}: '{raw}' does not match expected format '{fmt}'"
    return True, ""


def check_trip_duration(
    record: dict,
    pickup_field: str,
    dropoff_field: str,
    min_minutes: float = 1.0,
    max_minutes: float = 180.0,
    fmt: str = "%Y-%m-%d %H:%M:%S",
) -> tuple[bool, str]:
    """
    Fail if trip duration (dropoff − pickup) is outside [min_minutes, max_minutes].

    Notice: this check needs two field names, unlike every other check function
    which takes a single field. This is the design tension you will resolve on Day 3
    when you design the rule abstraction.
    """
    pickup_raw = str(record.get(pickup_field, "")).strip()
    dropoff_raw = str(record.get(dropoff_field, "")).strip()
    try:
        pickup_dt = datetime.strptime(pickup_raw, fmt)
        dropoff_dt = datetime.strptime(dropoff_raw, fmt)
    except ValueError:
        # Date-format failures are already caught by check_date_format.
        # Skip this check to avoid reporting the same row twice.
        return True, ""
    duration_minutes = (dropoff_dt - pickup_dt).total_seconds() / 60
    if duration_minutes < min_minutes:
        return (
            False,
            f"trip_duration: {duration_minutes:.1f} min is below minimum {min_minutes} min",
        )
    if duration_minutes > max_minutes:
        return (
            False,
            f"trip_duration: {duration_minutes:.1f} min exceeds maximum {max_minutes} min",
        )
    return True, ""


def check_coordinate(
    record: dict, field: str, min_val: float, max_val: float
) -> tuple[bool, str]:
    """Fail if a geographic coordinate is outside the expected bounding box."""
    raw = record.get(field)
    if raw is None or str(raw).strip() == "":
        return False, f"{field}: coordinate is missing"
    try:
        value = float(raw)
    except ValueError:
        return False, f"{field}: '{raw}' is not a valid coordinate"
    if not (min_val <= value <= max_val):
        return False, f"{field}: {value} is outside bounding box [{min_val}, {max_val}]"
    return True, ""


# ─────────────────────────────────────────────────────────────────────────────
# Single-record runner — ALL RULES ARE HARDCODED HERE
# ─────────────────────────────────────────────────────────────────────────────


def validate_record(record: dict) -> list[str]:
    """
    Run all validation checks against one record.
    Returns a list of error messages; empty list means the record is valid.

    Design problems to notice (you will fix these during Days 1–3):
      - Rules are a hardcoded flat list — no YAML config, no factory.
      - Changing a threshold (e.g. max fare) means editing this function.
      - No concept of "rule priority" or "stop on first failure".
      - check_trip_duration does not fit the single-field call pattern.
    """
    errors: list[str] = []

    checks = [
        check_not_null(record, "vendor_id"),
        check_not_null(record, "pickup_datetime"),
        check_not_null(record, "dropoff_datetime"),
        check_date_format(record, "pickup_datetime"),
        check_date_format(record, "dropoff_datetime"),
        check_trip_duration(record, "pickup_datetime", "dropoff_datetime"),
        check_range(record, "passenger_count", 1, 8),
        check_range(record, "trip_distance", 0.1, 200.0),
        check_coordinate(record, "pickup_lon", -75.0, -72.0),
        check_coordinate(record, "pickup_lat", 40.0, 42.0),
        check_coordinate(record, "dropoff_lon", -75.0, -72.0),
        check_coordinate(record, "dropoff_lat", 40.0, 42.0),
        check_range(record, "fare_amount", 0.01, 500.0),
        check_range(record, "total_amount", 0.01, 600.0),
        check_allowed_values(
            record, "payment_type", ["Credit", "Cash", "No Charge", "Dispute"]
        ),
    ]

    for passed, message in checks:
        if not passed:
            errors.append(message)

    return errors


# ─────────────────────────────────────────────────────────────────────────────
# Reporting helpers
# ─────────────────────────────────────────────────────────────────────────────


def aggregate_by_field(error_details: list[dict]) -> dict[str, int]:
    """
    Count failures per field across all failed records.
    Returns a dict sorted by failure count descending.
    """
    counts: dict[str, int] = {}
    for item in error_details:
        for msg in item["messages"]:
            field_name = msg.split(":")[0].strip()
            counts[field_name] = counts.get(field_name, 0) + 1
    return dict(sorted(counts.items(), key=lambda x: x[1], reverse=True))


def print_report(
    total: int,
    passed: int,
    failed: int,
    error_details: list[dict],
    verbose: bool = False,
) -> None:
    line = "=" * 60
    print(f"\n{line}")
    print("VALIDATION REPORT")
    print(line)
    print(f"  Total records : {total}")
    print(f"  Passed        : {passed}")
    print(f"  Failed        : {failed}")
    print(f"  Pass rate     : {passed / total * 100:.1f}%")

    if error_details:
        field_counts = aggregate_by_field(error_details)
        print("\n  Top failing fields:")
        for field, count in list(field_counts.items())[:5]:
            pct = count / total * 100
            print(f"    {field:<28} {count:>4} failures  ({pct:.1f}%)")

        rows_to_show = error_details if verbose else error_details[:10]
        label = "\nAll failed rows:" if verbose else "\nFailed rows (first 10):"
        print(label)
        for item in rows_to_show:
            messages = "; ".join(item["messages"])
            print(f"  Row {item['row']:>4} | {messages}")
        if not verbose and len(error_details) > 10:
            print(f"  ... and {len(error_details) - 10} more. Use --verbose to see all.")

    print(line)


def write_failed_records(
    output_path: str,
    error_details: list[dict],
    all_records: list[dict],
) -> None:
    """Write failed records plus an error_messages column to a new CSV file."""
    if not error_details:
        print("No failed records to write.")
        return

    row_errors: dict[int, list[str]] = {
        item["row"]: item["messages"] for item in error_details
    }
    failed_rows = [r for r in all_records if r["_row"] in row_errors]
    if not failed_rows:
        return

    fieldnames = [k for k in failed_rows[0] if k != "_row"] + ["error_messages"]
    with open(output_path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        for row in failed_rows:
            row_num = row["_row"]
            out = {k: v for k, v in row.items() if k != "_row"}
            out["error_messages"] = " | ".join(row_errors[row_num])
            writer.writerow(out)

    print(f"\nFailed records written to: {output_path}")


# ─────────────────────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────────────────────


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate NYC taxi trip records from a CSV file.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "examples:\n"
            "  python validate_trips.py taxi_trips_sample.csv\n"
            "  python validate_trips.py taxi_trips_sample.csv --verbose\n"
            "  python validate_trips.py taxi_trips_sample.csv --limit 50\n"
            "  python validate_trips.py taxi_trips_sample.csv --output failed.csv\n"
        ),
    )
    parser.add_argument("csv_file", help="Path to the CSV file to validate")
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        metavar="N",
        help="Only validate the first N records",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show all failed rows in the report (default: first 10 only)",
    )
    parser.add_argument(
        "--output",
        metavar="FILE",
        default=None,
        help="Write failed records to this CSV file",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    csv_path = Path(args.csv_file)
    if not csv_path.exists():
        print(f"Error: file not found — {csv_path}", file=sys.stderr)
        sys.exit(1)

    total = 0
    passed = 0
    failed = 0
    error_details: list[dict] = []
    all_records: list[dict] = []

    with open(csv_path, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for row_num, record in enumerate(reader, start=2):
            if args.limit is not None and total >= args.limit:
                break
            total += 1
            if args.output:
                snapshot = dict(record)
                snapshot["_row"] = row_num
                all_records.append(snapshot)
            errors = validate_record(record)
            if errors:
                failed += 1
                error_details.append({"row": row_num, "messages": errors})
            else:
                passed += 1

    if total == 0:
        print("No records found in the file.", file=sys.stderr)
        sys.exit(1)

    print_report(total, passed, failed, error_details, verbose=args.verbose)

    if args.output:
        write_failed_records(args.output, error_details, all_records)


if __name__ == "__main__":
    main()
