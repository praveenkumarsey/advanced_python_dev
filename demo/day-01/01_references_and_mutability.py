"""
01_references_and_mutability.py
================================
Demonstrates how Python names work as references to objects,
what aliasing means, how mutation through one name is visible
through another, and how reassignment differs from mutation.

Run:
    python day-01/01_references_and_mutability.py
"""


def demo_names_and_references():
    print("=" * 50)
    print("SECTION 1: Names are references, not containers")
    print("=" * 50)

    x = 42
    y = x  # y points to the same object as x

    print(f"x = {x}, y = {y}")
    print(f"Same object? {x is y}")  # True — both point to int 42

    # Reassign x — this does not affect y
    x = 100
    print(f"\nAfter x = 100:")
    print(f"x = {x}, y = {y}")
    print(f"y is unchanged — reassignment rebinds x to a new object, y still points to 42")


def demo_aliasing_mutable():
    print("\n" + "=" * 50)
    print("SECTION 2: Aliasing — two names, one mutable object")
    print("=" * 50)

    pipeline_a = ["extract", "transform"]
    pipeline_b = pipeline_a  # Both names point to the same list

    print(f"pipeline_a: {pipeline_a}")
    print(f"pipeline_b: {pipeline_b}")
    print(f"Same object? {pipeline_a is pipeline_b}")

    # Mutate through pipeline_b
    pipeline_b.append("load")

    print(f"\nAfter pipeline_b.append('load'):")
    print(f"pipeline_a: {pipeline_a}")  # Also changed!
    print(f"pipeline_b: {pipeline_b}")
    print("Both names reflect the change — they share the same list object.")


def demo_copy_to_break_aliasing():
    print("\n" + "=" * 50)
    print("SECTION 3: Breaking aliasing with a copy")
    print("=" * 50)

    original = ["step1", "step2"]
    independent = original.copy()  # A new list with the same contents

    independent.append("step3")

    print(f"original:    {original}")
    print(f"independent: {independent}")
    print("original is unaffected — independent has its own list object.")


def demo_immutable_reassignment():
    print("\n" + "=" * 50)
    print("SECTION 4: Immutable objects — reassignment creates a new object")
    print("=" * 50)

    status = "pending"
    print(f"status = '{status}', id = {id(status)}")

    status = "complete"
    print(f"status = '{status}', id = {id(status)}")
    print("Strings are immutable — 'status = ...' always creates a new string object.")

    print()
    count = 0
    original_id = id(count)
    count += 1
    print(f"count after += 1: {count}, same object? {id(count) == original_id}")
    print("Integers are immutable too — += creates a new int object and rebinds the name.")


def demo_mutable_default_warning():
    print("\n" + "=" * 50)
    print("SECTION 5: Mutable default argument — a common mistake")
    print("=" * 50)

    # BAD: the default list is created once and shared across all calls
    def add_item_bad(item, collection=[]):
        collection.append(item)
        return collection

    r1 = add_item_bad("alpha")
    r2 = add_item_bad("beta")
    print(f"BAD — call 1 result: {r1}")
    print(f"BAD — call 2 result: {r2}")
    print("Both calls share the same list — this is almost never what you want.")

    # GOOD: use None as sentinel, create a fresh list each call
    def add_item_good(item, collection=None):
        if collection is None:
            collection = []
        collection.append(item)
        return collection

    r3 = add_item_good("alpha")
    r4 = add_item_good("beta")
    print(f"\nGOOD — call 1 result: {r3}")
    print(f"GOOD — call 2 result: {r4}")
    print("Each call gets its own list.")


def main():
    demo_names_and_references()
    demo_aliasing_mutable()
    demo_copy_to_break_aliasing()
    demo_immutable_reassignment()
    demo_mutable_default_warning()


if __name__ == "__main__":
    main()
