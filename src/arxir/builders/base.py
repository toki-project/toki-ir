"""Define the public arxir API."""
from __future__ import annotations

import os
import sys

from abc import ABC, abstractmethod
from typing import Any, Dict, Union

from arxir import ast


class BuilderTranslator:
    """Builder translator visitor."""

    def translate(self, expr: ast.AST) -> Union[str, Any]:
        """
        Translate a arxir expression.

        Parameters
        ----------
        expr : Expr

        Returns
        -------
        Union[str, Any]
        """


class Builder(ABC):
    """ASTx Builder."""

    translator: BuilderTranslator
    tmp_path: str
    output_file: str

    sh_args: Dict[str, Any]

    def __init__(self) -> None:
        """Initialize Builder object."""
        self.translator = BuilderTranslator()
        self.tmp_path = ""
        self.output_file = ""
        self.sh_args: Dict[str, Any] = dict(
            _in=sys.stdin,
            _out=sys.stdout,
            _err=sys.stderr,
            _env=os.environ,
            # _new_session=True,
        )

    def module(self) -> ast.Module:
        """Create a new ASTx Module."""
        return ast.Module()

    def compile(self, expr: ast.AST) -> str:
        """Transpile ASTx to LLVM-IR."""
        return self.translator.translate(expr)

    @abstractmethod
    def build(
        self,
        expr: ast.AST,
        output_file: str,  # noqa: F841, RUF100
    ) -> None:
        """Transpile ASTx to LLVM-IR and build an executable file."""
        ...

    @abstractmethod
    def run(self) -> None:
        """Run the generated executable."""
        ...
