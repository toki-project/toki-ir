from arxir.builders.llvmir import LLVMIR
from arxir.expr import structures as sts
from arxir.expr import datatypes as dts

def test_module():
    builder = LLVMIR()

    module = builder.module()

    var_a = dts.VariableType(name="a", typ=dts.Int32)
    var_b = dts.VariableType(name="b", typ=dts.Int32)

    proto = sts.FunctionPrototype(
        name="add",
        args=[var_a, var_b],
        return_type=dts.Int32
    )
    block = sts.Block()
    var_sum = var_a + var_b
    block.append(var_sum)
    fn = sts.Function(prototype=proto, body=block)
    module.block.append(fn)

    print(builder.compile(module))
    assert False
