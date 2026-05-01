# sortedcontainers — ETNA Tasks

Total tasks: 20

## Task Index

| Task | Variant | Framework | Property | Witness |
|------|---------|-----------|----------|---------|
| 001 | `fromkeys_no_cls_a0dfdd8_1` | proptest | `FromkeysUsesCls` | `witness_fromkeys_uses_cls_case_basic` |
| 002 | `fromkeys_no_cls_a0dfdd8_1` | quickcheck | `FromkeysUsesCls` | `witness_fromkeys_uses_cls_case_basic` |
| 003 | `fromkeys_no_cls_a0dfdd8_1` | crabcheck | `FromkeysUsesCls` | `witness_fromkeys_uses_cls_case_basic` |
| 004 | `fromkeys_no_cls_a0dfdd8_1` | hegel | `FromkeysUsesCls` | `witness_fromkeys_uses_cls_case_basic` |
| 005 | `ior_uses_union_94b7d8f_1` | proptest | `IorPreservesIdentity` | `witness_ior_preserves_identity_case_basic` |
| 006 | `ior_uses_union_94b7d8f_1` | quickcheck | `IorPreservesIdentity` | `witness_ior_preserves_identity_case_basic` |
| 007 | `ior_uses_union_94b7d8f_1` | crabcheck | `IorPreservesIdentity` | `witness_ior_preserves_identity_case_basic` |
| 008 | `ior_uses_union_94b7d8f_1` | hegel | `IorPreservesIdentity` | `witness_ior_preserves_identity_case_basic` |
| 009 | `shallow_copy_aliases_dict_970f93f_1` | proptest | `CopyDoesNotAliasDict` | `witness_copy_does_not_alias_dict_case_basic` |
| 010 | `shallow_copy_aliases_dict_970f93f_1` | quickcheck | `CopyDoesNotAliasDict` | `witness_copy_does_not_alias_dict_case_basic` |
| 011 | `shallow_copy_aliases_dict_970f93f_1` | crabcheck | `CopyDoesNotAliasDict` | `witness_copy_does_not_alias_dict_case_basic` |
| 012 | `shallow_copy_aliases_dict_970f93f_1` | hegel | `CopyDoesNotAliasDict` | `witness_copy_does_not_alias_dict_case_basic` |
| 013 | `shallow_copy_aliases_set_970f93f_1` | proptest | `CopyDoesNotAliasSet` | `witness_copy_does_not_alias_set_case_basic` |
| 014 | `shallow_copy_aliases_set_970f93f_1` | quickcheck | `CopyDoesNotAliasSet` | `witness_copy_does_not_alias_set_case_basic` |
| 015 | `shallow_copy_aliases_set_970f93f_1` | crabcheck | `CopyDoesNotAliasSet` | `witness_copy_does_not_alias_set_case_basic` |
| 016 | `shallow_copy_aliases_set_970f93f_1` | hegel | `CopyDoesNotAliasSet` | `witness_copy_does_not_alias_set_case_basic` |
| 017 | `update_ordering_inconsistent_7dc426c_1` | proptest | `UpdateMatchesAdd` | `witness_update_matches_add_case_basic` |
| 018 | `update_ordering_inconsistent_7dc426c_1` | quickcheck | `UpdateMatchesAdd` | `witness_update_matches_add_case_basic` |
| 019 | `update_ordering_inconsistent_7dc426c_1` | crabcheck | `UpdateMatchesAdd` | `witness_update_matches_add_case_basic` |
| 020 | `update_ordering_inconsistent_7dc426c_1` | hegel | `UpdateMatchesAdd` | `witness_update_matches_add_case_basic` |

## Witness Catalog

- `witness_fromkeys_uses_cls_case_basic` — Subclass.fromkeys returns Subclass instance
- `witness_ior_preserves_identity_case_basic` — [1,2,3] |= [4,5] aliasing check
- `witness_copy_does_not_alias_dict_case_basic` — add to original; copy must be unchanged
- `witness_copy_does_not_alias_set_case_basic` — add to original; copy must be unchanged
- `witness_update_matches_add_case_basic` — Modulo-10 key with tie collisions on existing and new
