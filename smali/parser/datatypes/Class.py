from typing import Literal, NotRequired

from langbase.tokens.token import Token
from langbase.tokens.shortcuts import *

from ..misc.Expression import ExpressionParser, Path
from ..enums.Visibility import Visibility, parse_visibility

from ..body.types import SectionBody
from ..iparser import IParser

__all__ = ("Class", "ClassParser",)

class Class(Token):
    type: Literal["class"]
    visibility: Visibility
    final: bool
    path: Path
    extends: NotRequired[Path | None]
    source: NotRequired[str | None]
    implements: NotRequired[Path | None]
    body: NotRequired[SectionBody]

class ClassParser:
    @classmethod
    def parse_class_header(cls, self: IParser) -> Class:
        visibility = parse_visibility(self)
        final = self.now(Make.Literal("final")) != None
        path = ExpressionParser.parse_lit_path(self)

        self.consume_newlines()

        return Class(
            type="class",
            visibility=visibility,
            final=final,
            path=path
        )

    @classmethod
    def parse_class_super(cls, self: IParser, token: Class) -> Literal[False] | None:
        if not self.now(
                Make.Operator("."),
                Make.Literal("super")
        ):
            token["extends"] = None
            return False

        token["extends"] = ExpressionParser.parse_lit_path(self)

    @classmethod
    def parse_class_source(cls, self: IParser, token: Class) -> Literal[False] | None:
        if not self.now(
                Make.Operator("."),
                Make.Literal("source")
        ):
            token["source"] = None
            return False

        token["source"] = self.consume("string")['value']

    @classmethod
    def parse_class_implements(cls, self: IParser, token: Class) -> Literal[False] | None:
        if not self.now(
                Make.Operator("."),
                Make.Literal("implements")
        ):
            token["implements"] = None
            return False

        token["implements"] = ExpressionParser.parse_lit_path(self)

    @classmethod
    def parse_class(cls, self: IParser) -> Class:
        token = cls.parse_class_header(self)
        order = [
            cls.parse_class_super,
            cls.parse_class_source,
            cls.parse_class_implements
        ]

        for func in order:
            if func(self, token) == None:
                self.consume_newlines()

        self.add_token(token)
        return token
