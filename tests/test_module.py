import pytest

from arxir.builders.llvmir import LLVMIR
from arxir import ast


@pytest.fixture
def fn_expr() -> ast.AST:
    var_a = ast.Variable(name="a", type_=ast.Int32, value=ast.Int32Literal(1))
    var_b = ast.Variable(name="b", type_=ast.Int32, value=ast.Int32Literal(2))

    proto = ast.FunctionPrototype(
        name="add", args=[var_a, var_b], return_type=ast.Int32
    )
    # add_op = ast.BinaryOp(
    #     op_code="+", lhs=var_a, rhs=var_b
    # )
    block = ast.Block()
    var_sum = var_a + var_b
    block.append(var_sum)
    block.append(ast.Return(var_sum))
    return ast.Function(prototype=proto, body=block)


def test_module_compile(fn_expr: ast.Expr):
    builder = LLVMIR()

    module = builder.module()
    module.block.append(fn_expr)

    ir_result = builder.compile(module)
    print(ir_result)
    assert ir_result
    assert False


def test_module_build(fn_expr: ast.Expr):
    builder = LLVMIR()

    module = builder.module()
    module.block.append(fn_expr)

    builder.build(module, "/tmp/sum.exe")
    builder.run()
