"""Tests for the Module AST."""
import pytest

from arxir import ast
from arxir.builders.llvmir import LLVMIR

from .conftest import check_result


@pytest.fixture
def fn_add() -> ast.AST:
    """Create a fixture for a function `add`."""
    var_a = ast.Variable(name="a", type_=ast.Int32, value=ast.Int32Literal(1))
    var_b = ast.Variable(name="b", type_=ast.Int32, value=ast.Int32Literal(2))

    proto = ast.FunctionPrototype(
        name="add", args=[var_a, var_b], return_type=ast.Int32
    )
    block = ast.Block()
    var_sum = var_a + var_b
    block.append(ast.Return(var_sum))
    return ast.Function(prototype=proto, body=block)


@pytest.mark.parametrize(
    "action,expected_file",
    [
        ("translate", "test_module_fn_add.ll"),
    ],
)
def test_module_fn_add(
    action: str, expected_file: str, fn_add: ast.AST
) -> None:
    """Test ASTx Module with a function called add."""
    builder = LLVMIR()

    module = builder.module()
    module.block.append(fn_add)

    check_result(action, builder, module, expected_file)


@pytest.mark.parametrize(
    "action,expected_file",
    [
        ("translate", "test_module_fn_main.ll"),
        ("build", ""),
    ],
)
def test_module_fn_main(
    action: str, expected_file: str, fn_add: ast.AST
) -> None:
    """Test ASTx Module with a main function and a function called add."""
    builder = LLVMIR()

    module = builder.module()
    module.block.append(fn_add)

    main_proto = ast.FunctionPrototype(
        name="main", args=[], return_type=ast.Int32
    )
    main_block = ast.Block()
    main_block.append(ast.Return(ast.Int32Literal(0)))
    main_fn = ast.Function(prototype=main_proto, body=main_block)

    module.block.append(main_fn)

    check_result(action, builder, module, expected_file)
