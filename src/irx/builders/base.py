"""Define the public irx API."""

from __future__ import annotations

import os
import sys

from abc import ABC, abstractmethod
from typing import Any, Dict

from plum import dispatch

from irx import ast


class BuilderVisitor:
    """Builder translator visitor."""

    def translate(self, expr: ast.AST) -> str:
        """
        Translate an ASTx expression to string.

        Example of how it could be implemented:

            self.visit(expr)
            return str(self.result)
        """
        raise Exception("Not implemented yet.")

    @dispatch.abstract
    def visit(self, expr: ast.AST) -> None:
        """Translate an ASTx expression."""
        raise Exception("Not implemented yet.")

    @dispatch  # type: ignore[no-redef]
    def visit(self, expr: ast.FunctionCall) -> None:
        """Translate an ASTx FunctionCall expression."""
        raise Exception("Not implemented yet.")

    @dispatch  # type: ignore[no-redef]
    def visit(self, expr: ast.Function) -> None:
        """Translate an ASTx Function expression."""
        raise Exception("Not implemented yet.")

    @dispatch  # type: ignore[no-redef]
    def visit(self, expr: ast.FunctionPrototype) -> None:
        """Translate an ASTx FunctionPrototype expression."""
        raise Exception("Not implemented yet.")

    @dispatch  # type: ignore[no-redef]
    def visit(self, expr: ast.FunctionReturn) -> None:
        """Translate an ASTx FunctionReturn expression."""
        raise Exception("Not implemented yet.")

    @dispatch  # type: ignore[no-redef]
    def visit(self, expr: ast.LiteralInt32) -> None:
        """Translate an ASTx LiteralInt32 expression."""
        raise Exception("Not implemented yet.")

    @dispatch  # type: ignore[no-redef]
    def visit(self, expr: ast.ForCountLoop) -> None:
        """Translate an ASTx ForCountLoop expression."""
        raise Exception("Not implemented yet.")

    @dispatch  # type: ignore[no-redef]
    def visit(self, expr: ast.ForRangeLoop) -> None:
        """Translate an ASTx ForRangeLoop expression."""
        raise Exception("Not implemented yet.")

    @dispatch  # type: ignore[no-redef]
    def visit(self, expr: ast.If) -> None:
        """Translate an ASTx If expression."""
        raise Exception("Not implemented yet.")

    @dispatch  # type: ignore[no-redef]
    def visit(self, expr: ast.BinaryOp) -> None:
        """Translate an ASTx BinaryOp expression."""
        raise Exception("Not implemented yet.")

    @dispatch  # type: ignore[no-redef]
    def visit(self, expr: ast.UnaryOp) -> None:
        """Translate an ASTx UnaryOp expression."""
        raise Exception("Not implemented yet.")

    @dispatch  # type: ignore[no-redef]
    def visit(self, expr: ast.Block) -> None:
        """Translate an ASTx Block expression."""
        raise Exception("Not implemented yet.")

    @dispatch  # type: ignore[no-redef]
    def visit(self, expr: ast.Module) -> None:
        """Translate an ASTx Module expression."""
        raise Exception("Not implemented yet.")

    @dispatch  # type: ignore[no-redef]
    def visit(self, expr: ast.Variable) -> None:
        """Translate an ASTx Variable expression."""
        raise Exception("Not implemented yet.")

    @dispatch  # type: ignore[no-redef]
    def visit(self, expr: ast.VariableDeclaration) -> None:
        """Translate an ASTx VariableDeclaration expression."""
        raise Exception("Not implemented yet.")


class Builder(ABC):
    """ASTx Builder."""

    translator: BuilderVisitor
    tmp_path: str
    output_file: str

    sh_args: Dict[str, Any]

    def __init__(self) -> None:
        """Initialize Builder object."""
        self.translator = BuilderVisitor()
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

    def translate(self, expr: ast.AST) -> str:
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
