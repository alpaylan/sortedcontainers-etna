# sortedcontainers — ETNA Tasks

Total tasks: 10

## Task Index

| Task | Variant | Framework | Property | Witness |
|------|---------|-----------|----------|---------|
| 001 | `fromkeys_no_cls_a0dfdd8_1` | hypothesis | `FromkeysUsesCls` | `witness_fromkeys_uses_cls_case_basic` |
| 002 | `fromkeys_no_cls_a0dfdd8_1` | crosshair | `FromkeysUsesCls` | `witness_fromkeys_uses_cls_case_basic` |
| 003 | `ior_uses_union_94b7d8f_1` | hypothesis | `IorPreservesIdentity` | `witness_ior_preserves_identity_case_basic` |
| 004 | `ior_uses_union_94b7d8f_1` | crosshair | `IorPreservesIdentity` | `witness_ior_preserves_identity_case_basic` |
| 005 | `shallow_copy_aliases_dict_970f93f_1` | hypothesis | `CopyDoesNotAliasDict` | `witness_copy_does_not_alias_dict_case_basic` |
| 006 | `shallow_copy_aliases_dict_970f93f_1` | crosshair | `CopyDoesNotAliasDict` | `witness_copy_does_not_alias_dict_case_basic` |
| 007 | `shallow_copy_aliases_set_970f93f_1` | hypothesis | `CopyDoesNotAliasSet` | `witness_copy_does_not_alias_set_case_basic` |
| 008 | `shallow_copy_aliases_set_970f93f_1` | crosshair | `CopyDoesNotAliasSet` | `witness_copy_does_not_alias_set_case_basic` |
| 009 | `update_ordering_inconsistent_7dc426c_1` | hypothesis | `UpdateMatchesAdd` | `witness_update_matches_add_case_basic` |
| 010 | `update_ordering_inconsistent_7dc426c_1` | crosshair | `UpdateMatchesAdd` | `witness_update_matches_add_case_basic` |

## Witness Catalog

- `witness_fromkeys_uses_cls_case_basic` — Subclass.fromkeys returns Subclass instance
- `witness_ior_preserves_identity_case_basic` — [1,2,3] |= [4,5] aliasing check
- `witness_copy_does_not_alias_dict_case_basic` — add to original; copy must be unchanged
- `witness_copy_does_not_alias_set_case_basic` — add to original; copy must be unchanged
- `witness_update_matches_add_case_basic` — Modulo-10 key with tie collisions on existing and new
