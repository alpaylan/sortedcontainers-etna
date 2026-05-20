# sortedcontainers — Injected Bugs

Pure-Python sorted collections (SortedList, SortedDict, SortedSet) — bug fixes mined from upstream history.

Total mutations: 5

## Bug Index

| # | Variant | Name | Location | Injection | Fix Commit |
|---|---------|------|----------|-----------|------------|
| 1 | `fromkeys_no_cls_a0dfdd8_1` | `fromkeys_no_cls` | `src/sortedcontainers/sorteddict.py:319` | `patch` | `a0dfdd88ac62d4ca4629a924d522582bf9c998a7` |
| 2 | `ior_uses_union_94b7d8f_1` | `ior_uses_union` | `src/sortedcontainers/sortedset.py:659` | `patch` | `94b7d8f6e1e3514db0a315e840677c1d99f0bf98` |
| 3 | `shallow_copy_aliases_dict_970f93f_1` | `shallow_copy_aliases_dict` | `src/sortedcontainers/sorteddict.py:295` | `patch` | `970f93fbc5c98d24c0b5ace481ce91a1286ad078` |
| 4 | `shallow_copy_aliases_set_970f93f_1` | `shallow_copy_aliases_set` | `src/sortedcontainers/sortedset.py:351` | `patch` | `970f93fbc5c98d24c0b5ace481ce91a1286ad078` |
| 5 | `update_ordering_inconsistent_7dc426c_1` | `update_ordering_inconsistent` | `src/sortedcontainers/sortedlist.py:1779` | `patch` | `7dc426c95a0c329d5514e6198d92080f1ffc1e5e` |

## Property Mapping

| Variant | Property | Witness(es) |
|---------|----------|-------------|
| `fromkeys_no_cls_a0dfdd8_1` | `FromkeysUsesCls` | `witness_fromkeys_uses_cls_case_basic` |
| `ior_uses_union_94b7d8f_1` | `IorPreservesIdentity` | `witness_ior_preserves_identity_case_basic` |
| `shallow_copy_aliases_dict_970f93f_1` | `CopyDoesNotAliasDict` | `witness_copy_does_not_alias_dict_case_basic` |
| `shallow_copy_aliases_set_970f93f_1` | `CopyDoesNotAliasSet` | `witness_copy_does_not_alias_set_case_basic` |
| `update_ordering_inconsistent_7dc426c_1` | `UpdateMatchesAdd` | `witness_update_matches_add_case_basic` |

## Framework Coverage

| Property | hypothesis | crosshair |
|----------|---------:|--------:|
| `FromkeysUsesCls` | ✓ | ✓ |
| `IorPreservesIdentity` | ✓ | ✓ |
| `CopyDoesNotAliasDict` | ✓ | ✓ |
| `CopyDoesNotAliasSet` | ✓ | ✓ |
| `UpdateMatchesAdd` | ✓ | ✓ |

## Bug Details

### 1. fromkeys_no_cls

- **Variant**: `fromkeys_no_cls_a0dfdd8_1`
- **Location**: `src/sortedcontainers/sorteddict.py:319` (inside `SortedDict.fromkeys`)
- **Property**: `FromkeysUsesCls`
- **Witness(es)**:
  - `witness_fromkeys_uses_cls_case_basic` — Subclass.fromkeys returns Subclass instance
- **Source**: internal — Fix SortedDict.fromkeys to use cls
  > ``SortedDict.fromkeys`` constructed a plain ``SortedDict`` instead of using ``cls``. Subclasses calling ``Subclass.fromkeys(...)`` therefore got a ``SortedDict`` instance back, breaking subclass polymorphism.
- **Fix commit**: `a0dfdd88ac62d4ca4629a924d522582bf9c998a7` — Fix SortedDict.fromkeys to use cls
- **Invariant violated**: For any subclass ``S`` of ``SortedDict``, ``S.fromkeys(seq, value)`` returns an instance whose runtime type is exactly ``S``.
- **How the mutation triggers**: The mutation hard-codes ``SortedDict(...)`` instead of ``cls(...)`` inside the classmethod, so subclass dispatch is bypassed and the returned instance is always a plain ``SortedDict``.

### 2. ior_uses_union

- **Variant**: `ior_uses_union_94b7d8f_1`
- **Location**: `src/sortedcontainers/sortedset.py:659` (inside `SortedSet.__ior__`)
- **Property**: `IorPreservesIdentity`
- **Witness(es)**:
  - `witness_ior_preserves_identity_case_basic` — [1,2,3] |= [4,5] aliasing check
- **Source**: internal — Bug Fix: SortedSet.__ior__ should call update, not union
  > SortedSet.__ior__ was bound to ``union`` instead of ``update``. ``s |= x`` therefore returned a brand-new SortedSet, leaving any aliased reference to ``s`` pointing at the original (un-updated) set instead of mutating in place.
- **Fix commit**: `94b7d8f6e1e3514db0a315e840677c1d99f0bf98` — Bug Fix: SortedSet.__ior__ should call update, not union
- **Invariant violated**: After ``s |= x`` every reference that previously aliased ``s`` continues to refer to the same SortedSet object, and that object's contents equal the union of ``s``'s previous contents and ``x``.
- **How the mutation triggers**: The mutation re-binds ``__ior__`` to ``union``, which constructs and returns a new SortedSet. Python's ``|=`` rewrites the local name to that new object, but other references still point at the original — they observe stale contents.

### 3. shallow_copy_aliases_dict

- **Variant**: `shallow_copy_aliases_dict_970f93f_1`
- **Location**: `src/sortedcontainers/sorteddict.py:295` (inside `SortedDict.copy`)
- **Property**: `CopyDoesNotAliasDict`
- **Witness(es)**:
  - `witness_copy_does_not_alias_dict_case_basic` — add to original; copy must be unchanged
- **Source**: internal — Fix shallow copy definitions
  > ``SortedDict.copy`` aliased the original instance's ``_list`` (and the values were copied via ``dict.__setitem__`` without re-adding to ``_list``), so the copy's sorted-keys view was inconsistent with its dict contents and mutations to one dict bled into the other.
- **Fix commit**: `970f93fbc5c98d24c0b5ace481ce91a1286ad078` — Fix shallow copy definitions
- **Invariant violated**: After ``c = d.copy()``, mutating ``d`` (e.g. ``d[k] = v``) does not affect ``c``: ``c`` still equals the snapshot of ``d`` at the moment of copy.
- **How the mutation triggers**: The mutation re-binds the copy's ``_list`` to the original's, and uses raw ``dict.__setitem__`` for the values without going through SortedDict's ``__setitem__``. Mutations made later to either dict propagate to both.

### 4. shallow_copy_aliases_set

- **Variant**: `shallow_copy_aliases_set_970f93f_1`
- **Location**: `src/sortedcontainers/sortedset.py:351` (inside `SortedSet.copy`)
- **Property**: `CopyDoesNotAliasSet`
- **Witness(es)**:
  - `witness_copy_does_not_alias_set_case_basic` — add to original; copy must be unchanged
- **Source**: internal — Fix shallow copy definitions
  > ``SortedSet.copy`` aliased the underlying ``_set`` and ``_list`` attributes from the original instance, so mutating one set silently mutated its copy. Fixed by constructing a new backing ``set`` in ``copy``.
- **Fix commit**: `970f93fbc5c98d24c0b5ace481ce91a1286ad078` — Fix shallow copy definitions
- **Invariant violated**: After ``c = s.copy()``, mutating ``s`` (e.g. ``s.add(x)``) does not affect ``c``: ``c`` still equals the snapshot of ``s`` at the moment of copy.
- **How the mutation triggers**: The mutation re-binds the new SortedSet's ``_set`` and ``_list`` attributes to the originals, so subsequent additions to either object are observable through both.

### 5. update_ordering_inconsistent

- **Variant**: `update_ordering_inconsistent_7dc426c_1`
- **Location**: `src/sortedcontainers/sortedlist.py:1779` (inside `SortedKeyList.update`)
- **Property**: `UpdateMatchesAdd`
- **Witness(es)**:
  - `witness_update_matches_add_case_basic` — Modulo-10 key with tie collisions on existing and new
- **Source**: [#159](https://github.com/grantjenks/python-sortedcontainers/pull/159) — Fix update() ordering to be more consistent with add() ordering (#159)
  > When the bulk-update path was taken, ``SortedKeyList.update`` extended the freshly-sorted *new* values with the existing values, which placed new values *before* existing values for tie-keys. The subsequent stable sort therefore produced an order that disagreed with calling ``add`` element-by-element.
- **Fix commit**: `7dc426c95a0c329d5514e6198d92080f1ffc1e5e` — Fix update() ordering to be more consistent with add() ordering (#159)
- **Invariant violated**: For any starting ``SortedKeyList`` ``A`` and iterable ``vs``, ``A.update(vs)`` produces the same final ordering as calling ``A.add(v)`` for each ``v`` in ``vs`` in turn.
- **How the mutation triggers**: The mutation reverts the bulk-update branch to ``values.extend(chain.from_iterable(_lists))``, which prepends new data to existing data instead of appending it. Because the subsequent ``values.sort(key=...)`` is stable, tie-key elements end up in the wrong order.

## Dropped Candidates

- `8100a8f` (Fix bug in SortedSet.setitem when ValueError occurs) — surface removed: SortedSet no longer defines __setitem__
- `501d4a9` (Fix SortedList.__setitem__ to support slices with stop less than start and step equal one) — surface removed: SortedList.__setitem__ raises NotImplementedError in v2
- `bc44999` (fix setitem to support slices that alias itself) — surface removed: SortedList.__setitem__ raises NotImplementedError in v2
- `367c64a` (Bug fix: setitem must update _maxes) — surface removed: SortedList.__setitem__ raises NotImplementedError in v2
- `1d91579` (Apply aliasing fix to SortedListWithKey.__setitem__) — surface removed: SortedKeyList.__setitem__ raises NotImplementedError in v2
- `780e50b` (Fix sortedlist when setting slice with empty iterable) — surface removed: SortedList.__setitem__ raises NotImplementedError in v2
- `53ab610` (Test and bug fix for SortedList.extend with empty iterable) — surface removed: SortedList.extend raises NotImplementedError in v2; SortedList.update handles empty iterables natively
- `1c6a43a` (Fix sortedset setitem and improve tests) — surface removed: SortedSet no longer defines __setitem__
- `be06d8d` (Pickle fix for SortedSet on py27) — Python 2 only — bug not reachable on Python 3
- `fe780f5` (Fixes for Python 2.6, 3.2, 3.3, and 3.4) — Python 2 / legacy Python 3 only — not reachable on supported toolchains
- `9ba1980` (Fix relative import for python 3 in sortedlistwithkey) — Python 2/3 import-style fix; surface removed (sortedlistwithkey module deleted)
- `3367ea5` (Make iteritems, iterkeys, itervalues, viewitems, viewkeys, viewvalues raise AttributeError) — Python 2 cleanup — modern Python does not expose these names; behavior is now provided by inherited dict semantics
- `2b03703` (Fix for issue #147 -- Stop caching dict methods using super) — memory/GC pause regression; not expressible as a pure functional invariant
- `a04f4a6` (Fix bug in SortedDict comparison (possible KeyError)) — surface changed: SortedDict in v2 inherits from dict and uses dict.__eq__/__ne__, so the buggy iteration path no longer exists
- `4ce5210` (Fix SortedDict.update to accept dict type) — surface changed: modern SortedDict.update accepts dict types via inherited dict.update path
- `0962877` (Fix lte/gte to le/ge for sortedset) — no observable public invariant: SortedSet inherits __le__/__ge__ from MutableSet via collections.abc, so renaming the SortedSet-defined methods to nonsense names still yields correct subset/superset comparisons through inheritance
- `b3cae10` (Fix index check when child exceeds length) — internal-only: bug is in SortedList._check (an O(n) invariant validator that user code typically never calls); the public API never observes the assertion failure
- `a37f243` (Fix comment on SortedList.index) — comment-only change — no behavioral effect
- `9b2d38c` (Correct SortedValuesView docstring) — docstring-only change — no behavioral effect
- `15b8165` (Fix typo in doc for SortedList comparison methods) — docstring-only change — no behavioral effect
- `9ff3270` (change the documentation of SortedValuesViews) — docs-only change — no behavioral effect
- `ff966d1` (Fix import formatting) — code-formatting only — no behavioral effect
- `a13ac31` (Add support for Python 3.11 and 3.12) — compatibility / packaging change — not a bug fix to library logic
- `ca44935` (Add Cython and GitHub actions workflow for integration) — feature/build-config addition — not a bug fix
- `2678a78` (Implement SortedDict methods: __or__, __ror__, and __ior__) — feature addition — not a bug fix
- `66c39a1` (Bump version to 0.9.1) — version bump — no behavioral effect
- `dcba212` (Bump version to 0.8.1 after SortedDict comparison fix) — version bump — no behavioral effect
- `dc9cf97` (Revert "Fix SortedListWithKey w/ incomparable values on Python 3") — revert commit; underlying surface (sortedlistwithkey module) removed in v2
- `59a358c` (Fix SortedListWithKey w/ incomparable values on Python 3) — subsequently reverted by dc9cf97; surface (sortedlistwithkey module) removed in v2
- `9e81697` (Improve coverage for sorteddict and fix bugs) — vague catch-all commit; the underlying SortedDict (MutableMapping-based) was rewritten in v2 to inherit from dict, so the specific defects addressed here no longer exist on the modern surface
- `4887276` (Coverage, stress, and bug fixes.) — primarily test/coverage churn against an obsolete SortedList implementation that was rewritten in v2
- `1fa4168` (Fix self._dict reference in ValuesView.count) — surface changed: SortedDict in v2 uses SortedValuesView (subclass of collections.abc.ValuesView) which inherits .count from Sequence; the buggy custom .count method no longer exists
