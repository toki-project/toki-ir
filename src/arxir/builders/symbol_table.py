from public import public

from astx.symbol_table import (
    SymbolTable as SymbolTableBase,
    ScopeNodeBase,
    Scope as ScopeBase,
)


@public
class ScopeNode(ScopeNodeBase):
    ...


@public
class Scope(ScopeBase):
    ...


@public
class SymbolTable(SymbolTableBase):
    def __init__(self):
        self.scopes = Scope()
