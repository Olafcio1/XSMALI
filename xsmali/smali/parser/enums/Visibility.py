from enum import StrEnum
from langbase.classes.BaseLexer import BaseLexer

from ..iparser import IParser

class Visibility(StrEnum):
    PUBLIC = "public"
    PROTECTED = "protected"
    PRIVATE = "private"

def parse_visibility(self: IParser) -> Visibility:
    value = self.consume("literal")['value']
    return Visibility(value)
