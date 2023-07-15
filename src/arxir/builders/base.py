"""Define the public arxir API."""
from typing import Any, Protocol, Union, Callable, Dict, List

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

    def __init__(self) -> None:
        self.translator = BuilderTranslator()

    def module(self) -> ast.Module:
        return ast.Module()

    def compile(self, expr: str) -> str:
        return self.translator.translate(expr)

    def build(self, expr: str) -> None:
        request_str = self.compile(expr)
        print(request_str)
