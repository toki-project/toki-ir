"""
Operation expressions.

Note
----

For base operations, that operations that is not used directly,
use the suffix name "Op" (e.g. BinaryOp).

"""
from __future__ import annotations

from typing import Type

from arxir.ast.base import Expr
from arxir.ast import datatypes as dts


class OperationExpr(Expr):
    """Operation expression."""

    result_type: Type[dts.DataType] = dts.DataType

    @property
    def _display_name(self) -> str:
        return '{}[{}]'.format(
            super()._display_name, self.result_type.__name__
        )


class UnaryOp(OperationExpr):
    """Unary base operation."""

    @property
    def argument(self) -> dts.DataType:
        return self.args[0]


class BinaryOp(OperationExpr):
    """Binary base operation."""

    @property
    def left(self) -> dts.DataType:
        return self.args[0]

    @property
    def right(self) -> dts.DataType:
        return self.args[1]

    @classmethod
    def expr(  # type: ignore
        cls, left: dts.DataType, right: dts.DataType
    ) -> dts.DataType:
        """Create an BinaryOp expression for the given parameters."""

        def _expr(
            source: Type[BinaryOp], left: dts.DataType, right: dts.DataType
        ):
            ...

        _expr.__annotations__['return'] = cls.result_type


        return _expr(cls, left, right)


class NumericBinaryOp(BinaryOp):
    """Base numeric binary operation."""

    result_type: Type = dts.Number


class Add(NumericBinaryOp):
    """Addition operation."""


class Subtract(NumericBinaryOp):
    """Subtraction operation."""


class Multiply(NumericBinaryOp):
    """Multiplication operation."""


class Divide(NumericBinaryOp):
    """Division operation."""


class FloorDivide(NumericBinaryOp):
    """Floor division operation."""


class Power(NumericBinaryOp):
    """Power operation."""


class Modulus(NumericBinaryOp):
    """Division operation."""


class ComparisonOp(BinaryOp):
    """Comparison base operation"""

    result_type: Type = dts.Boolean


class Equals(ComparisonOp):
    """Equals operation"""


class NotEquals(ComparisonOp):
    """NotEquals operation"""


class GreaterEqual(ComparisonOp):
    """GreaterEqual operation"""


class GreaterThan(ComparisonOp):
    """GreaterThan operation"""


class LessEqual(ComparisonOp):
    """LessEqual operation"""


class LessThan(ComparisonOp):
    """LessThan operation"""


class IdenticalTo(ComparisonOp):
    """IdenticalTo operation"""


class LogicalBinaryOp(BinaryOp):
    """LogicalBinary base operation."""

    result_type: Type = dts.Boolean


class And(LogicalBinaryOp):
    """AND logical operation."""


class Or(LogicalBinaryOp):
    """AND logical operation."""


class Xor(LogicalBinaryOp):
    """AND logical operation."""


class Not(UnaryOp):
    """Not logical operation."""
