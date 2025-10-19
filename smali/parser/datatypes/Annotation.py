from typing import Literal, NotRequired

from langbase.tokens.token import Token
from langbase.tokens.shortcuts import *

from ..enums.Scope import Scope, parse_scope
from ..misc.Expression import Expression, ExpressionParser

from ..iparser import IParser

__all__ = ("Annotation", "AnnotationParser",)

class Annotation(Token):
    type: Literal["annotation"]
    scope: Scope
    path: str
    fields: NotRequired[dict[str, Expression]]

class AnnotationParser:
    @classmethod
    def parse_annotation_header(cls, self: IParser) -> Annotation:
        scope = parse_scope(self)
        path = self.consume("literal")['value']

        self.consume("operator", Make.Operator(";"))
        self.consume_newlines()

        return Annotation(
            type="annotation",
            scope=scope,
            path=path
        )

    @classmethod
    def parse_annotation(cls, self: IParser) -> Annotation:
        annotation = cls.parse_annotation_header(self)
        body = annotation["fields"] = {}

        while True:
            if self.now(
                    Make.Operator("."),
                    Make.Literal("end"),
                    Make.Literal("annotation"),
                    {"type": "newline"}
            ): break

            name = self.consume("literal")['value']
            self.consume("operator", Make.Operator("="))
            value = ExpressionParser.parse_expression(self)

            body[name] = value

            self.consume_newlines()

        return annotation
