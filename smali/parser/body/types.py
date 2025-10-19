from typing import Generic, Literal, TypeVar
from langbase.tokens.generics import TokenWithType

__all__ = ("Section", "Member", "SectionBody",)

Section = TokenWithType[Literal['class']]
Member = Section | TokenWithType[Literal['method', 'annotation']]
SectionBody = list[Member]
