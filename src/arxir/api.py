"""Public API definition."""
from typing import Union

from arxir.expr import datatypes as dts
from arxir.expr import stmts
from arxir.expr import structures as st
from arxir import operations as ops
from arxir import rules as rls


from arxir.builders.llvmir import LLVMIR


def builder() -> LLVMIR:
    return LLVMIR()
