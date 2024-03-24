"""Test For Loop statements."""

from typing import Type

import pytest

from irx import ast
from irx.builders.base import Builder
from irx.builders.llvmliteir import LLVMLiteIR

from .conftest import check_result


@pytest.mark.parametrize(
    "action,expected_file",
    [
        # ("translate", "test_for_range.ll"),
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
    var_a = ast.InlineVariableDeclaration(
        "a", type_=ast.Int32, value=ast.LiteralInt32(-1)
    )
    start = ast.LiteralInt32(1)
    end = ast.LiteralInt32(10)
    step = ast.LiteralInt32(1)
    body = ast.Block()
    body.append(ast.LiteralInt32(2))
    for_loop = ast.ForRangeLoop(
        variable=var_a,
        start=start,
        end=end,
        step=step,
        body=body,
    )

    # main function
    proto = ast.FunctionPrototype(
        name="main", args=tuple(), return_type=ast.Int32
    )
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
        # ("translate", ""),
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

    # NOTE: it seems that the systable in the tests is not correctly
    # sanitized, the variable `a` was renamed to `a2`
    init_a = ast.InlineVariableDeclaration(
        "a2", type_=ast.Int32, value=ast.LiteralInt32(0)
    )
    var_a = ast.Variable("a2")
    cond = ast.BinaryOp(op_code="<", lhs=var_a, rhs=ast.LiteralInt32(10))
    update = ast.UnaryOp(op_code="++", operand=var_a)

    for_body = ast.Block()
    for_body.append(ast.LiteralInt32(2))
    for_loop = ast.ForCountLoop(
        initializer=init_a,
        condition=cond,
        update=update,
        body=for_body,
    )

    # main function
    proto = ast.FunctionPrototype(
        name="main", args=tuple(), return_type=ast.Int32
    )
    fn_block = ast.Block()
    fn_block.append(for_loop)
    fn_block.append(ast.FunctionReturn(ast.LiteralInt32(0)))
    fn_main = ast.Function(prototype=proto, body=fn_block)

    module = builder.module()
    module.block.append(fn_main)

    # note: not yet fully implemented
    # check_result(action, builder, module, expected_file)
