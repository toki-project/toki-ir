from __future__ import annotations

import copy

from enum import Enum
from typing import List
from astx.base import Expr
from astx.blocks import (
    Block, Module as ModuleBase
)

class Target(Expr):
    datalayout: str
    triple: str

    def __init__(self, datalayout: str, triple: str) -> None:
        self.datalayout = datalayout
        self.triple = triple


class Module(ModuleBase):
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
