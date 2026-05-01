"""Concrete witnesses for the sortedcontainers ETNA workload.

Each ``witness_<snake>_case_<tag>`` is a no-arg function that calls
``property_<snake>`` with frozen inputs. On the base tree every witness
returns PASS; with the corresponding patch reverse-applied, the witness
returns fail(...).
"""
from ._result import PropertyResult
from . import properties


def witness_ior_preserves_identity_case_basic() -> PropertyResult:
    return properties.property_ior_preserves_identity(([1, 2, 3], [4, 5]))


def witness_fromkeys_uses_cls_case_basic() -> PropertyResult:
    return properties.property_fromkeys_uses_cls([1, 2, 3])


def witness_copy_does_not_alias_set_case_basic() -> PropertyResult:
    return properties.property_copy_does_not_alias_set(([1, 2, 3], 99))


def witness_copy_does_not_alias_dict_case_basic() -> PropertyResult:
    return properties.property_copy_does_not_alias_dict(([1, 2, 3], 99, 1))


def witness_update_matches_add_case_basic() -> PropertyResult:
    # Tie-key collision: both keys map to (val % 10) == 1.
    return properties.property_update_matches_add(([11, 21], [1, 31]))
