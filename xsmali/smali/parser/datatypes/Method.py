from typing import Literal, NotRequired

from langbase.tokens.token import Token
from langbase.tokens.shortcuts import *

from ..misc.Statement import MethodBody, StatementParser
from ..iparser import IParser

from ..misc.Type import Type, TypeParser
from ..enums.Visibility import Visibility, parse_visibility

__all__ = ("Method", "MethodParser",)

class Method(Token):
    type: Literal["method"]
    visibility: Visibility
    static: bool
    final: bool
    synthetic: bool
    constructor: bool
    name: str
    args: list[str]
    returns: Type
    body: NotRequired[MethodBody]

class MethodParser:
    @classmethod
    def parse_method_header(cls, self: IParser) -> Method:
        visibility = parse_visibility(self)
        static = self.now(Make.Literal("static")) != None
        final = self.now(Make.Literal("final")) != None
        synthetic = self.now(Make.Literal("synthetic")) != None
        constructor = self.now(Make.Literal("constructor")) != None
        name = self.consume("literal")['value']
        args = []

        self.consume("operator", Make.Operator("("))

        while True:
            if self.now(Make.Operator(")")):
                break

            arg = TypeParser.parse_type(self)
            args.append(arg)

        returns = TypeParser.parse_type(self)
        self.consume_newlines()

        return Method(
            type="method",
            visibility=visibility,
            static=static,
            final=final,
            synthetic=synthetic,
            constructor=constructor,
            name=name,
            args=args,
            returns=returns
        )

    @classmethod
    def parse_method(cls, self: IParser) -> Method:
        method = cls.parse_method_header(self)
        body = method["body"] = []

        while True:
            if self.now(
                    Make.Operator("."),
                    Make.Literal("end"),
                    Make.Literal("method"),
                    {"type": "newline"}
            ): break

            statement = StatementParser.parse_statement(self)
            self.consume_newlines()
            body.append(statement)

        return method
