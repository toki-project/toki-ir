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

    decl_a = ast.VariableDeclaration(
        name="a", type_=ast.Int32, value=ast.LiteralInt32(1)
    )
    decl_b = ast.VariableDeclaration(
        name="b", type_=ast.Int32, value=ast.LiteralInt32(2)
    )
    decl_c = ast.VariableDeclaration(
        name="c", type_=ast.Int32, value=ast.LiteralInt32(4)
    )

    a = ast.Variable("a")
    b = ast.Variable("b")
    c = ast.Variable("c")

    lit_1 = ast.LiteralInt32(1)

    basic_op = lit_1 + b - a * c / a + (b - a + c / a)

    main_proto = ast.FunctionPrototype(
        name="main", args=tuple(), return_type=ast.Int32
    )
    main_block = ast.Block()
    main_block.append(decl_a)
    main_block.append(decl_b)
    main_block.append(decl_c)
    main_block.append(ast.FunctionReturn(basic_op))
    main_fn = ast.Function(prototype=main_proto, body=main_block)

    module.block.append(main_fn)
    check_result(action, builder, module, expected_file)
