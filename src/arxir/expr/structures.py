import copy

from dataclasses import dataclass
from typing import List

from arxir.expr.base import Expr


@dataclass
class Block(Expr):
    nodes: List[Expr]


@dataclass
class Target(Expr):
    datalayout: str
    triple: str


@dataclass
class Module(Block):
    target: Target
    nodes: List[Expr]

    def __init__(self, target: Target=Target("unknown", "unknown")):
        self.target = copy.deepcopy(target)
