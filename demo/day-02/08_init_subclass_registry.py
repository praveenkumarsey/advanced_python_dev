"""
08_init_subclass_registry.py
==============================
Demonstrates automatic plugin registration using __init_subclass__:
  - The base class maintains a registry automatically
  - Subclasses register themselves just by being defined (or imported)
  - Lookup by a string key — no manual registration needed
  - Practical use: pluggable loaders, formatters, validators

Run:
    python day-02/08_init_subclass_registry.py
"""


# ══════════════════════════════════════════════════════════════════════════════
# PART 1: Basic plugin registry with __init_subclass__
# ══════════════════════════════════════════════════════════════════════════════
#
# __init_subclass__ is called on the BASE CLASS every time a class
# inherits from it. This gives the base class a chance to register the
# subclass — without any decorator or explicit call in the subclass.

class Formatter:
    """Base class for all output formatters.

    Subclasses must:
      - Define a class attribute `format_name` (the registry key).
      - Implement the `format(rows)` method.

    Registration is automatic — define a subclass, it's in the registry.
    """

    _registry: dict[str, type["Formatter"]] = {}

    def __init_subclass__(cls, format_name: str, **kwargs):
        super().__init_subclass__(**kwargs)
        if format_name in cls._registry:
            raise ValueError(
                f"Formatter {format_name!r} is already registered by "
                f"{cls._registry[format_name].__name__}."
            )
        cls._registry[format_name] = cls
        cls.format_name = format_name
        print(f"  [registry] Registered formatter: {format_name!r} → {cls.__name__}")

    @classmethod
    def get(cls, name: str) -> "Formatter":
        """Retrieve a formatter instance by name."""
        if name not in cls._registry:
            available = sorted(cls._registry)
            raise KeyError(
                f"No formatter named {name!r}. Available: {available}"
            )
        return cls._registry[name]()

    @classmethod
    def available(cls) -> list[str]:
        return sorted(cls._registry)

    def format(self, rows: list[dict]) -> str:
        raise NotImplementedError


# ── Plugins — registered automatically when Python parses these class bodies ──

class CSVFormatter(Formatter, format_name="csv"):
    """Formats rows as CSV."""

    def format(self, rows: list[dict]) -> str:
        if not rows:
            return ""
        header = ",".join(rows[0].keys())
        lines = [header] + [",".join(str(v) for v in row.values()) for row in rows]
        return "\n".join(lines)


class JSONFormatter(Formatter, format_name="json"):
    """Formats rows as JSON."""

    def format(self, rows: list[dict]) -> str:
        import json
        return json.dumps(rows, indent=2)


class MarkdownFormatter(Formatter, format_name="markdown"):
    """Formats rows as a Markdown table."""

    def format(self, rows: list[dict]) -> str:
        if not rows:
            return ""
        keys = list(rows[0].keys())
        header = "| " + " | ".join(keys) + " |"
        sep = "| " + " | ".join("---" for _ in keys) + " |"
        body = [
            "| " + " | ".join(str(row[k]) for k in keys) + " |"
            for row in rows
        ]
        return "\n".join([header, sep] + body)


def demo_basic_registry():
    print("=" * 55)
    print("PART 1: Plugin registry with __init_subclass__")
    print("=" * 55)

    data = [
        {"product": "widget", "qty": 50, "price": 9.99},
        {"product": "gadget", "qty": 20, "price": 24.99},
    ]

    print(f"\nAvailable formatters: {Formatter.available()}")

    for name in Formatter.available():
        fmt = Formatter.get(name)
        print(f"\n--- {name.upper()} ---")
        print(fmt.format(data))


# ══════════════════════════════════════════════════════════════════════════════
# PART 2: Unknown key gives a helpful error
# ══════════════════════════════════════════════════════════════════════════════

def demo_unknown_key():
    print("\n" + "=" * 55)
    print("PART 2: Helpful error for unknown format")
    print("=" * 55)

    try:
        Formatter.get("parquet")
    except KeyError as e:
        print(f"KeyError: {e}")


# ══════════════════════════════════════════════════════════════════════════════
# PART 3: Duplicate key detection
# ══════════════════════════════════════════════════════════════════════════════

def demo_duplicate_key():
    print("\n" + "=" * 55)
    print("PART 3: Duplicate key registration raises an error")
    print("=" * 55)

    try:
        class AnotherCSVFormatter(Formatter, format_name="csv"):
            def format(self, rows):
                return ""
    except ValueError as e:
        print(f"ValueError: {e}")

    print("Duplicate keys are caught at class-definition time.")


# ══════════════════════════════════════════════════════════════════════════════
# PART 4: Adding a new plugin at runtime — no base class changes needed
# ══════════════════════════════════════════════════════════════════════════════

def demo_add_plugin_at_runtime():
    print("\n" + "=" * 55)
    print("PART 4: Adding a new plugin without changing Formatter")
    print("=" * 55)

    class TSVFormatter(Formatter, format_name="tsv"):
        """Tab-separated values. Added dynamically."""

        def format(self, rows: list[dict]) -> str:
            if not rows:
                return ""
            header = "\t".join(rows[0].keys())
            lines = [header] + [
                "\t".join(str(v) for v in row.values()) for row in rows
            ]
            return "\n".join(lines)

    data = [{"col_a": 1, "col_b": 2}]
    print(f"\nAvailable after adding TSV: {Formatter.available()}")
    print(Formatter.get("tsv").format(data))
    print()
    print("Formatter base class was never modified — it just received the registration.")


def main():
    demo_basic_registry()
    demo_unknown_key()
    demo_duplicate_key()
    demo_add_plugin_at_runtime()


if __name__ == "__main__":
    main()
