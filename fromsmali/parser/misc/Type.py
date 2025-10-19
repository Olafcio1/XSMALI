from enum import Enum

from langbase.tokens.token import Token
from langbase.tokens.shortcuts import *

from .Expression import Path, ExpressionParser
from ..iparser import IParser

__all__ = ("Type", "TypeList", "SpecialType", "ObjectType", "ArrayType", "TypeParser",)

class Type(Token): pass
TypeList = list[Type]

class SpecialType(Enum):
    INT = ("I", Type())
    LONG = ("J", Type())
    BOOLEAN = ("Z", Type())
    BYTE = ("B", Type())
    CHAR = ("C", Type())
    SHORT = ("S", Type())
    FLOAT = ("F", Type())
    DOUBLE = ("D", Type())
    VOID = ("V", Type())

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
        for specialType in SpecialType:
            ch, obj = specialType.value

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
