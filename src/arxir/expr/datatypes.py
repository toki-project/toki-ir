"""Type expressions definition."""
from __future__ import annotations

from typing import Any, Callable, Dict, List, Optional, Union

from arxir.expr.modifiers import ScopeKind


from arxir.expr.base import Expr


class DataType(Expr):
    """Main data type class."""


class Boolean(DataType):
    """Boolean data type expression."""

    value: bool

    def __init__(self, value: bool):
        self.value = value


class Number(DataType):
    """Number data type expression."""


class Integer(Number):
    """Integer number data type expression."""

    value: int

    def __init__(self, value: int):
        self.value = value

    @classmethod
    @property
    def name(cls) -> str:
        return cls.__name__.lower()


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

    value: float

    def __init__(self, value: float):
        self.value = value


class Float16(Floating):
    """Float16 data type expression."""


class Float32(Floating):
    """Float32 data type expression."""


class Float64(Floating):
    """Float64 data type expression."""


class VariableType(Expr):
    """A variable."""

    typ: Type[DataType]
    name: str
    scope: Scope

    def __init__(
        self,
        name: str,
        typ: Type[DataType],
        scope: ScopeKind = ScopeKind.local,
    ) -> None:
        self.name = name
        self.scope = scope
        self.typ = typ
