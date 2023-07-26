"""Define the public arxir API."""
import tempfile
from typing import Any, Protocol, Union, Callable, Dict, List

import sh

from arxir import ast


class BuilderTranslator(Protocol):
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


class Builder(Protocol):
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
        sh.llc(["-filetype=obj", f"{self.tmp_path}.ll", "-o", f"{self.tmp_path}.o"])
        self.output_file = output_file

    def run(self) -> None:
        sh.clang([f"{self.tmp_path}.o", "-o", self.output_file])


class SymbolTable:
    def __init__(self):
        self.stack = [{}]

    def push_scope(self):
        self.stack.append({})

    def pop_scope(self):
        if len(self.stack) > 1:
            return self.stack.pop()
        else:
            raise IndexError("Cannot pop the global scope")

    def define_variable(self, var: ast.Variable):
        self.stack[-1][var.name] = var

    def assign_variable(self, var: ast.Variable):
        for scope in reversed(self.stack):
            if name in scope:
                scope[var.name] = var
                break
        else:
            raise NameError(f"Name '{name}' is not defined")

    def lookup_variable(self, name):
        for scope in reversed(self.stack):
            if name in scope:
                return scope[name]
        raise NameError(f"Name '{name}' is not defined")
