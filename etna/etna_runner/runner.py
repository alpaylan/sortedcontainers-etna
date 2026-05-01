"""ETNA runner for the sortedcontainers Python workload.

Dispatches ``<tool> <property>`` programmatically. Emits a single JSON line
on stdout per invocation; always exits 0 except on argv-parse errors.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from typing import Optional

from hypothesis import HealthCheck, given, settings
from hypothesis.errors import HypothesisException

from . import properties, strategies, witnesses

ALL_PROPERTIES = [
    "IorPreservesIdentity",
    "FromkeysUsesCls",
    "CopyDoesNotAliasSet",
    "CopyDoesNotAliasDict",
    "UpdateMatchesAdd",
]


def _emit(
    tool: str,
    prop: str,
    status: str,
    tests: int,
    time_us: int,
    counterexample: Optional[str] = None,
    error: Optional[str] = None,
) -> None:
    sys.stdout.write(
        json.dumps(
            {
                "status": status,
                "tests": tests,
                "discards": 0,
                "time": f"{time_us}us",
                "counterexample": counterexample,
                "error": error,
                "tool": tool,
                "property": prop,
            }
        )
        + "\n"
    )
    sys.stdout.flush()


def _pascal_to_snake(s: str) -> str:
    out = []
    for i, c in enumerate(s):
        if c.isupper() and i and not s[i - 1].isupper():
            out.append("_")
        out.append(c.lower())
    return "".join(out)


def _run_witness(prop: str) -> tuple[str, int, Optional[str]]:
    """Tool=etna: replay every witness for ``prop`` once."""
    snake = _pascal_to_snake(prop)
    fns = [
        getattr(witnesses, n)
        for n in dir(witnesses)
        if n.startswith(f"witness_{snake}_case_") and callable(getattr(witnesses, n))
    ]
    if not fns:
        return ("aborted", 0, f"no witnesses for {prop}")
    n_run = 0
    for fn in fns:
        n_run += 1
        try:
            r = fn()
        except Exception as e:  # noqa: BLE001 — surface library panic as failure
            return ("failed", n_run, f"{type(e).__name__}: {e}")
        if r.kind == "fail":
            return ("failed", n_run, r.message)
    return ("passed", n_run, None)


def _run_hypothesis(
    prop: str, backend: str, max_examples: int
) -> tuple[str, int, Optional[str], Optional[str]]:
    snake = _pascal_to_snake(prop)
    strat = getattr(strategies, f"strategy_{snake}")()
    prop_fn = getattr(properties, f"property_{snake}")

    counter = {"n": 0}
    counterexample: list[Optional[str]] = [None]
    fail_message: list[Optional[str]] = [None]

    def _wrapped(args):
        counter["n"] += 1
        try:
            r = prop_fn(args)
        except Exception as e:  # library panic
            counterexample[0] = repr(args)
            fail_message[0] = f"{type(e).__name__}: {e}"
            raise AssertionError(fail_message[0])
        if r.kind == "fail":
            counterexample[0] = repr(args)
            fail_message[0] = r.message
            raise AssertionError(r.message)
        # PASS or DISCARD: just return None (no error in hypothesis terms)

    test = given(strat)(_wrapped)
    test = settings(
        backend=backend,
        max_examples=max_examples,
        deadline=None,
        derandomize=False,
        suppress_health_check=list(HealthCheck),
        database=None,
    )(test)

    try:
        test()
        return ("passed", counter["n"], None, None)
    except AssertionError:
        return (
            "failed",
            counter["n"],
            counterexample[0] or "<unknown>",
            None,
        )
    except HypothesisException as e:
        # Hypothesis-level failure (e.g. unsatisfied assumption, MultipleFailures).
        # If we recorded a counterexample, surface it; else surface the exception.
        return (
            "failed",
            counter["n"],
            counterexample[0] or "<unknown>",
            f"{type(e).__name__}: {e}",
        )
    except Exception as e:  # noqa: BLE001 — surface unexpected runner errors
        return (
            "aborted",
            counter["n"],
            None,
            f"{type(e).__name__}: {e}",
        )


def main(argv: Optional[list[str]] = None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("tool", choices=["etna", "hypothesis", "crosshair"])
    p.add_argument("property")
    p.add_argument("--max-examples", type=int, default=200)
    args = p.parse_args(argv)

    targets = ALL_PROPERTIES if args.property == "All" else [args.property]
    t0 = time.perf_counter()

    for prop in targets:
        if prop not in ALL_PROPERTIES:
            _emit(args.tool, prop, "aborted", 0, 0, None, f"unknown property: {prop}")
            continue
        if args.tool == "etna":
            status, tests, err = _run_witness(prop)
            cex = err if status == "failed" else None
            _emit(
                args.tool,
                prop,
                status,
                tests,
                int((time.perf_counter() - t0) * 1e6),
                cex,
                None,
            )
        else:
            backend = "crosshair" if args.tool == "crosshair" else "hypothesis"
            try:
                status, tests, cex, err = _run_hypothesis(
                    prop, backend, args.max_examples
                )
            except Exception as e:  # noqa: BLE001 — defensive last resort
                status, tests, cex, err = (
                    "aborted",
                    0,
                    None,
                    f"{type(e).__name__}: {e}",
                )
            _emit(
                args.tool,
                prop,
                status,
                tests,
                int((time.perf_counter() - t0) * 1e6),
                cex,
                err,
            )

    return 0


if __name__ == "__main__":
    sys.exit(main())
