from typing import Any

from langbase.tokens.shortcuts import *
from langbase.classes.BaseParser import ParserError, EOFReaction

from ..datatypes.Class import ClassParser
from ..datatypes.Method import MethodParser
from ..datatypes.Statement import MethodBody
from ..datatypes.Annotation import AnnotationParser

from ..tokens import Token
from ..iparser import IParser

__all__ = ("BodyParser",)

class BodyParser:
    @classmethod
    def parse_body(cls, self: IParser, keyword: str) -> MethodBody:
        output = []

        while True:
            if self.now(
                    Make.Operator("."),
                    Make.Literal("end"),
                    Make.Literal(keyword),
                    {"type": "newline"},
                    eof=EOFReaction.EOF_TOKEN
            ): break

            output.append(cls.parse_member(self))

        return output

    @classmethod
    def parse_section(cls, self: IParser) -> Token:
        token: Any
        allowed = {
            "class": lambda: ClassParser.parse_class(self)
        }

        self.consume("operator", Make.Operator("."))

        for keyword, func in allowed.items():
            if self.now(Make.Literal(keyword)):
                token = func()
                token["body"] = cls.parse_body(self, keyword)

                break
        else:
            raise ParserError("Expected a section")

        return token

    @classmethod
    def parse_member(cls, self: IParser) -> Token:
        token: Any

        self.consume("operator", Make.Operator("."))
        if self.now(Make.Literal("method")):
            token = MethodParser.parse_method(self)
        elif self.now(Make.Literal("annotation")):
            token = AnnotationParser.parse_annotation(self)
        else:
            raise ParserError("Expected a member")

        self.consume_newlines()
        return token
