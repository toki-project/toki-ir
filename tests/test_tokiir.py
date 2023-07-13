import arx

def test_add():
    llvmir = arx.llvmir()
    builder = llvmir.builder()
    module = builder.module()

    hello = builder.function("hello_world")
    block = builder.make_block(hello)
    builder.position_at_entry(block)

    x, y = builder.add_function_args(
        hello,
        [builder.F64, builder.F64],
        ['a', 'b'],
    )

    adder = builder.addf(x, y, builder.F64)
    builder.ret([adder], [builder.F64])

    arx.compile(builder)
