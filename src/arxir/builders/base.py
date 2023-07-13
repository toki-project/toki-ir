"""Define the public arxir API."""
from typing import Any, Protocol, Union, Callable, Dict, List

from arxir.expr.base import Expr
from arxir.expr import structures as sts


class BuilderTranslator(Protocol):
    """Builder translator visitor."""

    def translate(self, expr: Expr) -> Union[str, Any]:
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

    def module(self) -> sts.Module:
        return sts.Module()

    def compile(self, expr: str) -> str:
        return self.translator.translate(expr)

    def build(self, expr: str) -> None:
        request_str = self.compile(expr)
        print(request_str)
