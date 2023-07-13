"""Type expressions definition."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional, Union

@dataclass
class Expr:
    """Base expression class."""

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        fn_name = (
            self.function.__name__
            if not str(self.function) == 'expr'
            else self._display_name
        )

        output = '{}({})'.format(fn_name, self.args)
        return output

    @property
    def _display_name(self) -> str:
        return self.__class__.__name__

    @staticmethod
    def expr(*args, **kwargs):
        """Create an expression with the given value."""
        raise NotImplementedError('Operation not supported yet.')
