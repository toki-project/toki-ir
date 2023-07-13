from __future__ import annotations

import copy

from enum import Enum
from typing import List

from arxir.expr.base import Expr
from arxir.expr.modifiers import ScopeKind, VisibilityKind


class Block(Expr):
    nodes: List[Expr]
    position: int = 0

    def __init__(self):
        self.nodes: List[Expr] = []
        self.position: int = 0

    def append(self, value: Expr):
        self.nodes.append(value)

    def __iter__(self) -> Block:
        return self

    def __next__(self) -> Expr:
        if self.position >= len(self.nodes):
            raise StopIteration()

        i = self.position
        self.position += 1
        return self.nodes[i]


class Target(Expr):
    datalayout: str
    triple: str

    def __init__(self, datalayout: str, triple: str) -> None:
        self.datalayout = datalayout
        self.triple = triple


class Module(Expr):
    name: str
    block: Block
    target: Target

    def __init__(
        self,
        name: str = "main",
        target: Target = Target("unknown", "unknown"),
    ):
        self.name = name
        self.target = copy.deepcopy(target)
        self.block = Block()


class FunctionPrototype(Expr):
    name: str
    args: List[dts.DataType]
    return_type: Type[dts.DataType]
    scope: ScopeKind
    visibility: VisibilityKind

    def __init__(
        self,
        name: str,
        args: List[Expr],
        return_type: str,
        scope: ScopeKind = ScopeKind.global_,
        visibility: VisibilityKind = VisibilityKind.public,
    ) -> None:
        self.name = name
        self.args = args
        self.return_type = return_type
        self.scope = scope
        self.visibility = visibility


class Function(Expr):
    prototype: FunctionPrototype
    body: Block

    def __init__(self, prototype: FunctionPrototype, body: Block) -> None:
        self.prototype = prototype
        self.body = body
