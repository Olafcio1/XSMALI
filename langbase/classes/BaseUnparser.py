from abc import ABCMeta
from enum import Enum
from typing import Any, Generic, Literal, TypeVar, overload

from ..tokens.token import *

__all__ = ("T", "TArg", "BaseUnparser", "UnparserError", "EOFReaction",)

T = TypeVar('T', bound=TokenBase)
TArg = Any # it's really dict[str, Any] / TypedDict, but i can't merge them

class UnparserError(BaseException):
    pass

class EOFReaction(Enum):
    RAISE = 0
    NON_MATCH = 1
    EOF_TOKEN = 2

class BaseUnparser(Generic[T], metaclass=ABCMeta):
    _data: list[T]
    _index: int
    _output: str

    def __init__(self, data: list[T]) -> None:
        self._data = data
        self._index = 0
        self._output = ""

    @overload
    def consume(self, /, fields: dict[str, Any] = {}, *, allowEOF: Literal[False]) -> T: ...

    @overload
    def consume(self, /, fields: dict[str, Any] = {}, *, allowEOF: Literal[True] = True) -> T | None: ...

    def consume(self, /, fields: dict[str, Any] = {}, *, allowEOF: bool = True) -> T | None:
        try:
            val = self._data[self._index]
            self._index += 1

            for key in fields:
                if val[key] != fields[key]:
                    raise UnparserError("Unsatisfied fields")
        except IndexError:
            if allowEOF:
                return None
            else:
                raise EOFError("No more data left")
        else:
            return val

    def advance(self, after: int = 0) -> T | None:
        try:
            return self._data[self._index + after]
        except IndexError:
            return None

    def now(
                self,
                *tokens: TArg,
                before: int = 0,
                consume: bool = True,
                eof: EOFReaction = EOFReaction.RAISE
    ) -> list[T] | None:
        index = -before
        output = []

        for fields in tokens:
            have = self.advance(index)
            index += 1

            if have == None:
                if eof == EOFReaction.NON_MATCH:
                    return None
                elif eof == EOFReaction.EOF_TOKEN:
                    return eval('''[
                        TokenBase(
                            type="eof"
                        )
                    ]''')
                else:
                    raise EOFError("Missing token")

            for k in fields:
                if have[k] != fields[k]:
                    return None

            output.append(have)

        if consume:
            self._index += index

        return output

    def write(self, value: str) -> None:
        self._output += value
