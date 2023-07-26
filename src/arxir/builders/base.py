"""Define the public arxir API."""
from __future__ import annotations
import tempfile
from typing import Any, Protocol, Union, Callable, Dict, List, Optional

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


class ScopeNode:
    name: str
    variable: Dict[str, ast.DataType]
    parent: Optional[ScopeNode]
    default_parent: Optional[ScopeNode] = None

    def __init__(self, name: str, parent=None):
        self.variables: Dict[str, Any] = {}
        self.parent: Optional[ScopeNode] = parent or ScopeNode.default_parent
        self.name: str = name


class Scope:
    nodes: Dict[int, ScopeNode]
    current: Optional[ScopeNode]
    previous: Optional[ScopeNode]

    def __init__(self) -> None:
        self.nodes: Dict[int, ScopeNode] = {}
        self.current = None
        self.previous = None

        self.add(ScopeNode("root"))

        ScopeNode.default_parent = self.current

    def add(self, name, parent=None, change_current=True):
        node = ScopeNode(name, parent)

        # The use of id(node) as keys in the nodes dictionary is generally
        # fine, but be aware that this approach may lead to potential issues
        # if the id() of a node is reused after its destruction. It's #
        # unlikely to happen in your current code, but it's something to be aware of.
        self.nodes[id(node)] = node

        if len(self.nodes) == 1 or change_current:
            self.previous = self.current
            self.current = self.nodes[id(node)]

        return node

    def get_first(self) -> ScopeNode:
        return self.nodes[0]

    def get_last(self) -> ScopeNode:
        return self.nodes[-1]

    def destroy(self, node: ScopeNode) -> None:
        del self.nodes[id(node)]
        self.current = self.previous
        self.previous = None

    def set_default_parent(self, node: ScopeNode) -> None:
        ScopeNode.default_parent = node


class SymbolTable:
    scopes: Scope

    def __init__(self):
        self.scopes = Scope()

    def define(self, expr: ast.DataType) -> None:
        self.scopes.current.variables[expr.name] = expr

    def assign(self, expr: ast.DataType) -> None:
        self.scopes.current.variables[expr.name] = expr

    def lookup(self, name) -> ast.DataType:
        scope = self.scopes.current
        while scope is not None:
            if name in scope.variables:
                return scope.variables[name]
            scope = scope.parent
        raise NameError(f"Name '{name}' is not defined")
