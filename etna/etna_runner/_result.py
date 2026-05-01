from dataclasses import dataclass


@dataclass(frozen=True)
class PropertyResult:
    kind: str  # "pass" | "fail" | "discard"
    message: str = ""


PASS = PropertyResult("pass")
DISCARD = PropertyResult("discard")


def fail(msg: str) -> PropertyResult:
    return PropertyResult("fail", msg)
