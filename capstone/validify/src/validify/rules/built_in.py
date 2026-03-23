"""
rules/built_in.py — Concrete validation rules and rule factory.

─────────────────────────────────────────────────────────
DAY 1 TASK
─────────────────────────────────────────────────────────
Implement two rules as subclasses of BaseValidator.
These mirror the functions in starter/validate_trips.py:

  NullCheckRule(field: str)
    — Fails when the field is absent, None, or an empty/whitespace string.
    — Mirror of: check_not_null()

  RangeRule(field: str, min_val: float, max_val: float)
    — Fails when the field is not a number or is outside [min_val, max_val].
    — Mirror of: check_range()

Each rule stores its last checked record's result in instance state
(so that self.message can report the exact problem after validate() runs).

─────────────────────────────────────────────────────────
DAY 3 TASK — add RuleFactory
─────────────────────────────────────────────────────────
Implement RuleFactory at the bottom of this file:

    class RuleFactory:
        @staticmethod
        def from_config(path: str) -> list[BaseValidator]:
            ...

Steps inside from_config:
  1. Open and parse config/rules.yaml with yaml.safe_load().
  2. For each entry in rules[]:
       a. Look up the class: ValidatorRegistry.get(entry["type"])
       b. Instantiate it with the remaining keys as kwargs
          (field, min, max, pattern — whatever the rule needs).
       c. Catch KeyError from the registry and raise ConfigError with a clear message.
  3. Return the populated list.

─────────────────────────────────────────────────────────
DAY 5 — Git exercise
─────────────────────────────────────────────────────────
On a feature branch, add:

  RegexRule(field: str, pattern: str)
    — Fails when the field value does not match re.fullmatch(pattern, value).
    — Needed for the payment_type rule in config/rules.yaml.
    — Hint: import re; use re.fullmatch(self.pattern, value)
"""

import yaml  # noqa: F401 — needed by RuleFactory

from validify.core.base import BaseValidator  # noqa: F401
from validify.core.exceptions import ConfigError  # noqa: F401
from validify.rules.registry import ValidatorRegistry  # noqa: F401


# ---------------------------------------------------------------------------
# YOUR CODE BELOW
# ---------------------------------------------------------------------------
