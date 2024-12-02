"""Tests for the Module AST."""

from typing import Type

import astx
import pytest

from irx.builders.base import Builder
from irx.builders.llvmliteir import LLVMLiteIR

from .conftest import check_result


@pytest.fixture
def fn_add() -> astx.AST:
    """Create a fixture for a function `add`."""
    var_a = astx.Argument(
        name="a", type_=astx.Int32(), default=astx.LiteralInt32(1)
    )
    var_b = astx.Argument(
        name="b", type_=astx.Int32(), default=astx.LiteralInt32(2)
    )

    proto = astx.FunctionPrototype(
        name="add", args=astx.Arguments(var_a, var_b), return_type=astx.Int32()
    )
    block = astx.Block()
    var_sum = var_a + var_b
    block.append(astx.FunctionReturn(var_sum))
    return astx.Function(prototype=proto, body=block)


@pytest.mark.parametrize(
    "action,expected_file",
    [
        # ("translate", "test_module_fn_main.ll"),
        ("build", ""),
    ],
)
@pytest.mark.parametrize(
    "builder_class",
    [
        LLVMLiteIR,
    ],
)
def test_module_fn_main(
    action: str,
    expected_file: str,
    fn_add: astx.AST,
    builder_class: Type[Builder],
) -> None:
    """Test ASTx Module with a main function and a function called add."""
    builder = builder_class()

    module = builder.module()
    module.block.append(fn_add)

    main_proto = astx.FunctionPrototype(
        name="main", args=astx.Arguments(), return_type=astx.Int32()
    )
    main_block = astx.Block()
    main_block.append(astx.FunctionReturn(astx.LiteralInt32(0)))
    main_fn = astx.Function(prototype=main_proto, body=main_block)

    module.block.append(main_fn)

    check_result(action, builder, module, expected_file)
