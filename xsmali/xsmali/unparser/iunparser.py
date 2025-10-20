from typing import Any, Literal, Protocol, overload

from langbase.classes.BaseUnparser import EOFReaction
from langbase.tokens.token import *

__all__ = ("T", "TArg", "IUnparser",)

T = TokenBase
TArg = Any

class IUnparser(Protocol):
    @overload
    def consume(self, /, fields: dict[str, Any] = {}, *, allowEOF: Literal[False]) -> T: ...
    @overload
    def consume(self, /, fields: dict[str, Any] = {}, *, allowEOF: Literal[True] = True) -> T | None: ...
    def consume(self, /, fields: dict[str, Any] = {}, *, allowEOF: bool = True) -> T | None: ...

    def advance(self, after: int = 0) -> T | None: ...
    def now(
                self,
                *tokens: TArg,
                before: int = 0,
                consume: bool = True,
                eof: EOFReaction = EOFReaction.RAISE
    ) -> list[T] | None: ...

    def tab(self, inc: int) -> None: ...
    def write(self, value: str) -> None: ...
    def unwrite(self, length: int) -> None: ...
