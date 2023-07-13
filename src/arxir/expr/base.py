"""Type expressions definition."""
from __future__ import annotations

from typing import Any, Callable, Dict, List

from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional, Union

@dataclass
class Expr:
    """Base expression class."""

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return self.__class__.__name__

    @staticmethod
    def expr(*args, **kwargs):
        """Create an expression with the given value."""
        raise NotImplementedError('Operation not supported yet.')
