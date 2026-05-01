"""Property functions for sortedcontainers ETNA workload.

Each property is pure, total, deterministic. Returns PropertyResult.
"""
from typing import Tuple, List

from sortedcontainers import SortedDict, SortedList, SortedSet

from ._result import PASS, DISCARD, PropertyResult, fail


# ---------------------------------------------------------------------------
# IorPreservesIdentity (variant: ior_uses_union_94b7d8f_1)
# ---------------------------------------------------------------------------
def property_ior_preserves_identity(args: Tuple[List[int], List[int]]) -> PropertyResult:
    """SortedSet.__ior__ must mutate the set in place and return self.

    Bug (94b7d8f): ``__ior__ = union`` returned a new SortedSet instead of
    updating self. ``s |= x`` rebinds ``s`` to the new object but other
    references still point to the original (un-updated) set.
    """
    initial, additions = args
    s = SortedSet(initial)
    snapshot_id = id(s)
    aliased = s
    s |= additions
    expected = sorted(set(initial) | set(additions))
    if id(s) != snapshot_id:
        return fail(
            f"ior_preserves_identity({initial!r}, {additions!r}): "
            f"|= rebound to a new object (id changed); "
            f"aliased ref now stale: aliased={list(aliased)!r}, s={list(s)!r}"
        )
    if list(aliased) != expected:
        return fail(
            f"ior_preserves_identity({initial!r}, {additions!r}): "
            f"aliased contents {list(aliased)!r} != expected {expected!r}"
        )
    return PASS


# ---------------------------------------------------------------------------
# FromkeysUsesCls (variant: fromkeys_no_cls_a0dfdd8_1)
# ---------------------------------------------------------------------------
class _SortedDictSubclass(SortedDict):
    """Dummy subclass used by property_fromkeys_uses_cls."""


def property_fromkeys_uses_cls(args: List[int]) -> PropertyResult:
    """SortedDict.fromkeys must use ``cls`` so subclasses get the right type.

    Bug (a0dfdd8): hard-coded ``SortedDict(...)`` call broke subclasses —
    ``Subclass.fromkeys(seq)`` returned a plain ``SortedDict``.
    """
    keys = args
    sub = _SortedDictSubclass.fromkeys(keys, 0)
    if type(sub) is not _SortedDictSubclass:
        return fail(
            f"fromkeys_uses_cls({keys!r}): "
            f"Subclass.fromkeys returned {type(sub).__name__}, "
            f"expected _SortedDictSubclass"
        )
    if sorted(set(keys)) != list(sub.keys()):
        return fail(
            f"fromkeys_uses_cls({keys!r}): "
            f"keys mismatch: got {list(sub.keys())!r}, "
            f"expected {sorted(set(keys))!r}"
        )
    return PASS


# ---------------------------------------------------------------------------
# CopyAliasesSet (variant: shallow_copy_aliases_set_970f93f_1)
# ---------------------------------------------------------------------------
def property_copy_does_not_alias_set(args: Tuple[List[int], int]) -> PropertyResult:
    """SortedSet.copy must produce an independent set (no shared backing storage).

    Bug (970f93f): the old ``copy`` shared ``_set`` and ``_list`` with the
    original; mutating one mutated the other.
    """
    initial, new_value = args
    s = SortedSet(initial)
    c = s.copy()
    s.add(new_value)
    # The copy must not see the new value if it was newly added to s.
    if new_value not in initial and new_value in c:
        return fail(
            f"copy_does_not_alias_set({initial!r}, {new_value!r}): "
            f"adding to original leaked into copy: c={list(c)!r}"
        )
    if list(c) != sorted(set(initial)):
        return fail(
            f"copy_does_not_alias_set({initial!r}, {new_value!r}): "
            f"copy contents {list(c)!r} != expected {sorted(set(initial))!r}"
        )
    return PASS


# ---------------------------------------------------------------------------
# CopyAliasesDict (variant: shallow_copy_aliases_dict_970f93f_1)
# ---------------------------------------------------------------------------
def property_copy_does_not_alias_dict(args: Tuple[List[int], int, int]) -> PropertyResult:
    """SortedDict.copy must produce an independent dict.

    Bug (970f93f): the old ``copy`` shared ``_dict`` and ``_list`` with the
    original; mutating one mutated the other.
    """
    initial_keys, new_key, new_value = args
    d = SortedDict({k: 0 for k in initial_keys})
    c = d.copy()
    d[new_key] = new_value
    if new_key not in initial_keys and new_key in c:
        return fail(
            f"copy_does_not_alias_dict({initial_keys!r}, {new_key!r}, {new_value!r}): "
            f"adding to original leaked into copy: c={dict(c)!r}"
        )
    if sorted(set(initial_keys)) != list(c.keys()):
        return fail(
            f"copy_does_not_alias_dict({initial_keys!r}, ...): "
            f"copy keys {list(c.keys())!r} != expected {sorted(set(initial_keys))!r}"
        )
    return PASS


# ---------------------------------------------------------------------------
# UpdateMatchesAdd (variant: update_ordering_inconsistent_7dc426c_1)
# ---------------------------------------------------------------------------
def property_update_matches_add(args: Tuple[List[int], List[int]]) -> PropertyResult:
    """SortedKeyList.update(values) must produce the same final ordering as
    repeated ``.add(v)`` calls.

    Bug (7dc426c): ``values.extend(chain.from_iterable(_lists))`` swapped the
    order of existing data and new data, so ``sorted`` (a stable sort with a
    non-injective key) put existing values *after* new values for tie keys —
    inconsistent with the element-by-element ``add`` behavior.
    """
    initial, additions = args
    # Use a non-injective key so the stable sort distinguishes orderings.
    key = lambda v: v % 10

    sl_update = SortedList(key=key)
    for v in initial:
        sl_update.add(v)
    sl_update.update(additions)

    sl_add = SortedList(key=key)
    for v in initial:
        sl_add.add(v)
    for v in additions:
        sl_add.add(v)

    if list(sl_update) != list(sl_add):
        return fail(
            f"update_matches_add({initial!r}, {additions!r}): "
            f"update={list(sl_update)!r}, add={list(sl_add)!r}"
        )
    return PASS
