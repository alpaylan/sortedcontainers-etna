"""Pytest collector that runs every witness on the base tree."""
import inspect

import pytest

from etna_runner import witnesses


def _all_witness_fns():
    return sorted(
        (name, fn)
        for name, fn in inspect.getmembers(witnesses, inspect.isfunction)
        if name.startswith("witness_")
    )


@pytest.mark.parametrize("name,fn", _all_witness_fns())
def test_witness(name: str, fn) -> None:
    r = fn()
    assert r.kind == "pass", f"{name}: {r.message}"
