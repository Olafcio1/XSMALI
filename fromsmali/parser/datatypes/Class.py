from typing import Literal, NotRequired

from langbase.tokens.token import Token
from langbase.tokens.shortcuts import *

from .Statement import MethodBody
from ..enums.Visibility import Visibility, parse_visibility
from ..iparser import IParser

__all__ = ("Class", "ClassParser",)

class Class(Token):
    type: Literal["class"]
    visibility: Visibility
    final: bool
    path: str
    extends: "NotRequired[Class | None]"
    source: NotRequired[str | None]
    implements: NotRequired[str | None]
    body: NotRequired[MethodBody]

class ClassParser:
    @classmethod
    def parse_class_header(cls, self: IParser) -> Class:
        visibility = parse_visibility(self)
        final = self.now(Make.Literal("final")) != None
        path = self.consume("literal")['value']

        self.consume("operator", Make.Operator(";"))
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

        token["extends"] = self.consume("literal")['value']
        self.consume("operator", Make.Operator(";"))

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

        token["implements"] = self.consume("literal")['value']
        self.consume("operator", Make.Operator(";"))

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
