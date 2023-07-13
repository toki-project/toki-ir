"""Type expressions definition."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional, Union


from arxir.expr.base import Expr


class DataType(Expr):
    """Main data type class."""

    @property
    def value(self) -> int:
        return self.args[0]


class Boolean(DataType):
    """Boolean data type expression."""


class Number(DataType):
    """Number data type expression."""


class Integer(Number):
    """Integer number data type expression."""


class SignedInteger(Integer):
    """Signed integer number data type expression."""


class Int8(SignedInteger):
    """Int8 data type expression."""


class Int16(SignedInteger):
    """Int16 data type expression."""


class Int32(SignedInteger):
    """Int32 data type expression."""


class Int64(SignedInteger):
    """Int64 data type expression."""


class Floating(Number):
    """Floating number data type expression."""


class Float16(Floating):
    """Float16 data type expression."""


class Float32(Floating):
    """Float32 data type expression."""


class Float64(Floating):
    """Float64 data type expression."""
