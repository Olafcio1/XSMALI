from abc import ABCMeta
from typing import Any, Generic, TypeVar

from ..tokens.token import TokenBase

__all__ = ("T", "BaseLexer",)
T = TypeVar('T', bound=TokenBase)

class BaseLexer(Generic[T], metaclass=ABCMeta):
    _data: str
    _index: int
    _output: list[T]

    def __init__(self, data: str) -> None:
        self._data = data
        self._index = 0
        self._output = []

    def consume(self, length: int = 1) -> str:
        newIndex = self._index + length
        val = self._data[self._index:newIndex]
        self._index = newIndex

        return val

    def advance(self, after: int = 1, *, length: int = 1) -> str:
        ind = self._index + after
        return self._data[ind:ind + length]

    def now(self, *values: str, before: int = 0, consume: bool = True) -> str | None:
        for value in values:
            length = len(value)

            if self.advance(-before, length=length) == value:
                if consume:
                    self.consume(length)

                return value

        return None

    def add_token(self, value: Any) -> None:
        self._output.append(value)
