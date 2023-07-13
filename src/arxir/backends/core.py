"""Define the public arxir API."""
from typing import Any, Protocol, Union

import arxir
from arxir.expr.base import Expr

class Backend(Protocol):
    """Backend protocol."""

    def compile(self, expr: Expr) -> Union[str, Any]:
        """
        Compile a arxir expression.

        Parameters
        ----------
        expr : Expr

        Returns
        -------
        Union[str, Any]
        """

    def build(
        self, expr: Expr
    ) -> Union[str, int, float, bool, Any]:
        """
        Execute a arxir expression.

        Parameters
        ----------
        expr : Expr

        Returns
        -------
        Union[pd.DataFrame, str, int, float, bool, Any]
        """


class BackendTranslator(Protocol):
    """Backend translator protocol."""

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
