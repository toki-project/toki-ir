"""Tests for the Module AST."""
from typing import Type

import pytest

from irx import ast
from irx.builders.base import Builder
from irx.builders.llvmliteir import LLVMLiteIR

from .conftest import check_result


@pytest.mark.parametrize(
    "action,expected_file",
    [
        ("translate", "test_binary_op_basic.ll"),
        ("build", ""),
    ],
)
@pytest.mark.parametrize(
    "builder_class",
    [
        LLVMLiteIR,
    ],
)
def test_binary_op_basic(
    action: str, expected_file: str, builder_class: Type[Builder]
) -> None:
    """Test ASTx Module with a function called add."""
    builder = builder_class()
    module = builder.module()

    a = ast.Variable(name="a", type_=ast.Int32, value=ast.LiteralInt32(1))
    b = ast.Variable(name="b", type_=ast.Int32, value=ast.LiteralInt32(2))
    c = ast.Variable(name="c", type_=ast.Int32, value=ast.LiteralInt32(4))

    lit_1 = ast.LiteralInt32(1)

    basic_op = lit_1 + b - a * c / a + (b - a + c / a)

    main_proto = ast.FunctionPrototype(
        name="main", args=[], return_type=ast.Int32
    )
    main_block = ast.Block()
    main_block.append(ast.FunctionReturn(basic_op))
    main_fn = ast.Function(prototype=main_proto, body=main_block)

    module.block.append(main_fn)
    check_result(action, builder, module, expected_file)
