from typing import Union

from arxir.expr import datatypes as dtypes
from arxir.expr.structures import Module
from arxir.backends.core import Backend

# numeric binary operation

BIN_OPS = {
    'add': '{} + {}',
    'truediv': '{} / {}',
    'floordiv': '{} // {}',
    'mod': '{} % {}',
    'mul': '{} * {}',
    'sub': '{} - {}',
    'pow': '{} ** {}',
    # 'eq': '{} = {}',
    'ge': '{} >= {}',
    'gt': '{} > {}',
    'le': '{} <= {}',
    'lt': '{} < {}',
    'ne': '{} <> {}',
}

FN_MAP = {}


def op_num_builder(op, tp_x, tp_y):
    dunder_op = '__{}__'.format(op)
    _tpx = (
        'i'
        if tp_x.startswith('int')
        else 'f'
        if tp_x.startswith('float')
        else None
    )
    _tpy = (
        'i'
        if tp_y.startswith('int')
        else 'f'
        if tp_y.startswith('float')
        else None
    )

    if _tpx is None:
        raise Exception('X types not recognized.')

    if _tpy is None:
        raise Exception('X types not recognized.')

    # TODO: check a way normalize the type here
    def __fn(
        x: Union[int, float], y: Union[int, float]
    ) -> str:  # type: ignore
        _dtype_x = getattr(dtypes, tp_x)
        _dtype_y = getattr(dtypes, tp_y)

        return (
            getattr(_dtype_x(x), dunder_op)(_dtype_y(y)),
            lambda: BIN_OPS[op].format(x, y),
        )  # type: ignore

    if _tpx == 'i':
        if _tpy == 'i':
            # TODO: check a way normalize the type here
            def _fn(x: int, y: int) -> str:
                return __fn(x, y)  # type: ignore

        else:
            # TODO: check a way normalize the type here
            def _fn(x: int, y: float) -> str:  # type: ignore
                return __fn(x, y)

    else:
        if _tpy == 'i':
            # TODO: check a way normalize the type here
            def _fn(x: float, y: int) -> str:  # type: ignore
                return __fn(x, y)

        else:
            # TODO: check a way normalize the type here
            def _fn(x: float, y: float) -> str:  # type: ignore
                return __fn(x, y)

    _fn.__name__ = dunder_op
    return _fn


int_types = ('int8', 'int16', 'int32', 'int64')
float_types = ('float16', 'float16', 'float64')

number_types = int_types + float_types

for tp_x in number_types:
    for tp_y in number_types:
        for op in BIN_OPS:
            FN_MAP[op] = op_num_builder(op, tp_x, tp_y)


class LLVMIR(Backend):
    # translator: BackendTranslator = TokiExampleTranslator

    def __init__(self):
        pass

    def module(self) -> Module:
        return Module()

    def compile(self, expr) -> str:
        pass

    def build(self, expr):
        request_str = self.compile(expr)
        print(request_str)
