"""Public API definition."""

from arxir.builders.llvmir import LLVMIR


def builder() -> LLVMIR:
    return LLVMIR()
