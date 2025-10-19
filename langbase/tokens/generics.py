from typing import TypeVar, Generic
from .token import Token

__all__ = ("TokenWithType",)

T = TypeVar('T')
class TokenWithType(Token, Generic[T]):
    type: T
