"""Hypothesis strategies for the sortedcontainers ETNA workload.

CrossHair-compatible: only ``st.integers``, ``st.text``, ``st.lists``,
``st.tuples``, ``st.booleans``. No custom ``@composite`` strategies.
"""
from hypothesis import strategies as st


_INT = st.integers(min_value=-100, max_value=100)


def strategy_ior_preserves_identity():
    return st.tuples(
        st.lists(_INT, max_size=8),
        st.lists(_INT, max_size=8),
    )


def strategy_fromkeys_uses_cls():
    return st.lists(_INT, max_size=8)


def strategy_copy_does_not_alias_set():
    return st.tuples(
        st.lists(_INT, max_size=8),
        _INT,
    )


def strategy_copy_does_not_alias_dict():
    return st.tuples(
        st.lists(_INT, max_size=8),
        _INT,
        _INT,
    )


def strategy_update_matches_add():
    return st.tuples(
        st.lists(_INT, max_size=8),
        st.lists(_INT, max_size=8),
    )
