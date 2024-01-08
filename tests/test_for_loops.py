"""Test For Loop statements."""
from typing import Type

import pytest

from arxir import ast
from arxir.builders.base import Builder
from arxir.builders.llvmliteir import LLVMLiteIR

from .conftest import check_result


@pytest.mark.parametrize(
    "action,expected_file",
    [
        ("translate", "test_for_range.ll"),
        ("build", ""),
    ],
)
@pytest.mark.parametrize(
    "builder_class",
    [
        LLVMLiteIR,
    ],
)
def test_for_range(
    action: str, expected_file: str, builder_class: Type[Builder]
) -> None:
    """Test For Range statement."""
    builder = builder_class()

    # `for` statement
    var_a = ast.Variable("a", type_=ast.Int32, value=ast.LiteralInt32(-1))
    start = ast.LiteralInt32(1)
    end = ast.LiteralInt32(10)
    step = ast.LiteralInt32(1)
    body = ast.Block()
    body.append(ast.LiteralInt32(2))
    for_loop = ast.ForRangeLoop(
        variable=var_a, start=start, end=end, step=step, body=body
    )

    # main function
    proto = ast.FunctionPrototype(name="main", args=[], return_type=ast.Int32)
    block = ast.Block()
    block.append(for_loop)
    block.append(ast.FunctionReturn(ast.LiteralInt32(0)))
    fn_main = ast.Function(prototype=proto, body=block)

    module = builder.module()
    module.block.append(fn_main)

    check_result(action, builder, module, expected_file)


@pytest.mark.parametrize(
    "action,expected_file",
    [
        ("translate", ""),
        ("build", ""),
    ],
)
@pytest.mark.parametrize(
    "builder_class",
    [
        LLVMLiteIR,
    ],
)
def test_for_count(
    action: str, expected_file: str, builder_class: Type[Builder]
) -> None:
    """Test the For Count statement."""
    builder = builder_class()

    # for
    var_a = ast.Variable("a", type_=ast.Int32, value=ast.LiteralInt32(0))
    cond = ast.BinaryOp(op_code="<", lhs=var_a, rhs=ast.LiteralInt32(10))
    update = ast.UnaryOp(op_code="++", operand=var_a)
    body = ast.Block()
    body.append(ast.LiteralInt32(2))
    for_loop = ast.ForCountLoop(
        initializer=var_a, condition=cond, update=update, body=body
    )

    # main function
    proto = ast.FunctionPrototype(name="main", args=[], return_type=ast.Int32)
    block = ast.Block()
    block.append(for_loop)
    block.append(ast.FunctionReturn(ast.LiteralInt32(0)))
    fn_main = ast.Function(prototype=proto, body=block)

    module = builder.module()
    module.block.append(fn_main)

    check_result(action, builder, module, expected_file)
