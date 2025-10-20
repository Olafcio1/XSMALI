from enum import Enum
from typing import Any

from langbase.tokens.shortcuts import *

from .Expression import Path, ExpressionParser
from ..iparser import IParser

__all__ = ("Type", "TypeList", "SpecialType", "ObjectType", "ArrayType", "TypeParser",)

class Type:
    note: Any

    def __init__(self, value: Any = None, **fields: Any) -> None:
        self.note = value

        for k in fields:
            setattr(self, k, fields[k])

TypeList = list[Type]

class SpecialType(Type, Enum):
    INT = "I"
    LONG = "J"
    BOOLEAN = "Z"
    BYTE = "B"
    CHAR = "C"
    SHORT = "S"
    FLOAT = "F"
    DOUBLE = "D"
    VOID = "V"

class ObjectType(Type):
    path: Path

class ArrayType(Type):
    type: Type

class TypeParser:
    @classmethod
    def parse_type(cls, self: IParser) -> Type:
        # Array Type
        if self.now(Make.Operator("[")):
            return ArrayType(type=cls.parse_type(self))

        # Special Type
        for obj in SpecialType:
            ch = obj.note

            if self.now(Make.Literal(ch), {"type": "newline"}):
                return obj

        # Object Type
        value = ExpressionParser.parse_lit_path(self)
        return ObjectType(path=value)

    @classmethod
    def parse_type_list(cls, self: IParser) -> TypeList:
        self.consume("operator", Make.Operator("("))
        values = []

        while True:
            self.consume_newlines()
            if self.now(Make.Operator(")")):
                break

            self.consume_newlines()

            value = cls.parse_type(self)
            values.append(value)

        self.consume_newlines()
        return values
