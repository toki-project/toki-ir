"""ASTx Blocks extensions."""
from __future__ import annotations

import copy

from typing import cast

from astx.base import Expr, ReprStruct
from astx.blocks import Block
from astx.blocks import Module as ModuleBase
from public import public

__all__ = ["Block"]


@public
class Target(Expr):
    datalayout: str
    triple: str

    def __init__(self, datalayout: str, triple: str) -> None:
        self.datalayout = datalayout
        self.triple = triple

    def get_struct(self) -> ReprStruct:
        """Return a simple structure that represents the object."""
        struct = {"TARGET": f"{self.triple}: {self.datalayout}"}
        return cast(ReprStruct, struct)


@public
class Module(ModuleBase):
    name: str
    target: Target

    def __init__(
        self,
        name: str = "main",
        target: Target = Target(
            "e-m:e-i64:64-f80:128-n8:16:32:64-S128", "x86_64-unknown-linux-gnu"
        ),
    ):
        super().__init__(name=name)
        self.target = copy.deepcopy(target)
