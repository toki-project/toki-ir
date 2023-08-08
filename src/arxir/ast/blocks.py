from __future__ import annotations

import copy

from astx.base import Expr
from astx.blocks import Block
from astx.blocks import Module as ModuleBase


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
        target: Target = Target(
            "e-m:e-i64:64-f80:128-n8:16:32:64-S128", "x86_64-unknown-linux-gnu"
        ),
    ):
        self.name = name
        self.target = copy.deepcopy(target)
        self.block = Block()
