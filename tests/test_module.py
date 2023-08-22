import pytest

from arxir import ast
from arxir.builders.llvmir import LLVMIR


@pytest.fixture
def fn_add() -> ast.AST:
    var_a = ast.Variable(name="a", type_=ast.Int32, value=ast.Int32Literal(1))
    var_b = ast.Variable(name="b", type_=ast.Int32, value=ast.Int32Literal(2))

    proto = ast.FunctionPrototype(
        name="add", args=[var_a, var_b], return_type=ast.Int32
    )
    block = ast.Block()
    var_sum = var_a + var_b
    block.append(ast.Return(var_sum))
    return ast.Function(prototype=proto, body=block)


@pytest.fixture
def fn_main() -> ast.AST:
    proto = ast.FunctionPrototype(name="main", args=[], return_type=ast.Int32)
    block = ast.Block()
    block.append(ast.Return(ast.Int32Literal(0)))
    return ast.Function(prototype=proto, body=block)


def test_module_compile(fn_main: ast.AST, fn_add: ast.AST):
    builder = LLVMIR()

    module = builder.module()
    module.block.append(fn_add)

    ir_result = builder.compile(module)
    print(ir_result)
    assert ir_result


def test_module_build(fn_main: ast.AST, fn_add: ast.AST):
    builder = LLVMIR()

    module = builder.module()
    module.block.append(fn_add)
    module.block.append(fn_main)

    # TODO: after the first compiling, the next ones
    #       doesn't work properly. it needs to be fixed
    # ir_result = builder.compile(module)
    # print(ir_result)
    # assert ir_result

    builder.build(module, "/tmp/sum.exe")
