from arxir.builders.llvmir import LLVMIR
from arxir import ast

def test_module():
    builder = LLVMIR()

    module = builder.module()

    var_a = ast.Variable(name="a", type_=ast.Int32)
    var_b = ast.Variable(name="b", type_=ast.Int32)

    proto = ast.FunctionPrototype(
        name="add",
        args=[var_a, var_b],
        return_type=ast.Int32
    )
    block = ast.Block()
    # var_sum = var_a + var_b
    # block.append(var_sum)
    fn = ast.Function(prototype=proto, body=block)
    module.block.append(fn)

    print(builder.compile(module))
    assert False
