from typing import Literal, TypedDict

from langbase.classes.BaseParser import ParserError

from langbase.tokens.token import TokenBase
from langbase.tokens.shortcuts import *

from ..iparser import IParser

Expression = TokenBase

class String(Expression):
    type: Literal["string"]
    value: str

class Number(Expression):
    type: Literal["number"]
    value: str

class List(Expression):
    type: Literal["list"]
    values: list[Expression]

class Path(Expression):
    type: Literal["path"]
    value: list[str]

class Parameter(Expression):
    type: Literal["parameter"]
    index: int

class Variable(Expression):
    type: Literal["variable"]
    index: int

class ExpressionParser:
    @classmethod
    def parse_expression(cls, self: IParser) -> Expression:
        if (
                (lit := self.now({"type": "literal"}, consume=False)) and
                (lit := lit[0]['value'])
        ):
            if lit[0] == "L": # Literal - Path
                return cls.parse_lit_path(self)
            elif lit[0] == "p": # Parameter - Argument provided to method
                return cls.parse_lit_parameter(self)
            elif lit[0] == "v": # Variable - Local register in the method
                return cls.parse_lit_variable(self)
            else:
                raise ParserError("Invalid literal %r" % lit)
        elif self.now({"type": "string"}, consume=False):
            return cls.parse_string(self)
        elif self.now({"type": "number"}, consume=False):
            return cls.parse_number(self)
        elif self.now(Make.Operator("{"), consume=False):
            return cls.parse_list(self)
        else:
            raise ParserError("Expected expression")

    @classmethod
    def parse_lit_path(cls, self: IParser) -> Path:
        first = True
        array = []

        while True:
            array.append(self.consume("literal")['value'][1:])

            if first:
                self.consume("operator", Make.Operator(";"))
                first = False

            if not self.now(Make.Operator("->")):
                break

        return Path(
            type="path",
            value=array
        )

    @classmethod
    def parse_lit_parameter(cls, self: IParser) -> Parameter:
        value = Parameter(
            type="parameter",
            index=int(self.consume("literal")['value'][1:])
        )

        return value

    @classmethod
    def parse_lit_variable(cls, self: IParser) -> Variable:
        value = Variable(
            type="variable",
            index=int(self.consume("literal")['value'][1:])
        )

        return value

    @classmethod
    def parse_string(cls, self: IParser) -> String:
        return String(
            type="string",
            value=self.consume("string")['value']
        )

    @classmethod
    def parse_number(cls, self: IParser) -> Number:
        return Number(
            type="number",
            value=self.consume("number")['value']
        )

    @classmethod
    def parse_list(cls, self: IParser) -> List:
        self.consume("operator", Make.Operator("{"))

        values = []
        first = True

        while True:
            self.consume_newlines()

            if self.now(Make.Operator("}")):
                break
            elif not first:
                self.consume("operator", Make.Operator(","))
                self.consume_newlines()

            value = cls.parse_expression(self)
            values.append(value)

            first = False

        self.consume_newlines()

        return List(
            type="list",
            values=values
        )
