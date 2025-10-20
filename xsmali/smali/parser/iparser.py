from typing import Any, Literal, Protocol, overload

from langbase.classes.BaseParser import EOFReaction
from langbase.tokens.token import *

__all__ = ("T", "TArg", "IParser",)

T = TokenBase
TArg = Any

class IParser(Protocol):
    @overload
    def consume(self, /, type: str, fields: dict[str, Any] = {}, *, allowEOF: Literal[False] = False) -> T: ...

    @overload
    def consume(self, /, type: str, fields: dict[str, Any] = {}, *, allowEOF: Literal[True]) -> T | None: ...

    def consume(self, /, type: str, fields: dict[str, Any] = {}, *, allowEOF: bool = False) -> T | None: ...

    def advance(self, after: int = 0) -> T | None: ...
    def now(
                self,
                *tokens: TArg,
                before: int = 0,
                consume: bool = True,
                eof: EOFReaction = EOFReaction.RAISE
    ) -> list[T] | None: ...
    def add_token(self, value: TArg) -> None: ...

    def consume_newlines(self) -> None: ...
