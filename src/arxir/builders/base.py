"""Define the public arxir API."""
from __future__ import annotations
import tempfile
from typing import Any, Union

import sh

from arxir import ast


class BuilderTranslator:
    """Builder translator visitor."""

    def translate(self, expr: ast.Expr) -> Union[str, Any]:
        """
        Translate a arxir expression.

        Parameters
        ----------
        expr : Expr

        Returns
        -------
        Union[str, Any]
        """


class Builder:
    """Backend protocol."""

    translator: BuilderTranslator
    tmp_path: str
    output_file: str

    def __init__(self) -> None:
        self.translator = BuilderTranslator()
        self.tmp_path = ""
        self.output_file = ""

    def module(self) -> ast.Module:
        return ast.Module()

    def compile(self, expr: ast.Expr) -> str:
        return self.translator.translate(expr)

    def build(self, expr: ast.Expr, output_file: str) -> None:
        result = self.compile(expr)

        with tempfile.NamedTemporaryFile(suffix="", delete=False) as temp_file:
            self.tmp_path = temp_file.name

        with open(f"{self.tmp_path}.ll", "w") as f:
            f.write(result)

        # llc -filetype=obj hello-world.ll -o hello-world.o
        sh.llc(
            [
                "-filetype=obj",
                f"{self.tmp_path}.ll",
                "-o",
                f"{self.tmp_path}.o",
            ]
        )
        self.output_file = output_file

    def run(self) -> None:
        sh.clang([f"{self.tmp_path}.o", "-o", self.output_file])
