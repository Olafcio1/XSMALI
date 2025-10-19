import string
from typing import ClassVar

from langbase.tokens.token import *
from langbase.classes.BaseLexer import BaseLexer

from .tokens import Tokens

__all__ = ("Lexer",)

class Lexer(BaseLexer[TokenBase]):
    literal: ClassVar[str] = \
        string.ascii_letters + string.digits + "-/$>"
    literal_open: ClassVar[str] = \
        string.ascii_letters + "<"

    operators: ClassVar[list[str]] = [
        ";",
        "->",
        "..",
        "(",
        ")",
        "{",
        "}",
        "[",
        "]",
        "$",
        ",",
        ":",
        ".",
        "=",
        "_"
    ]

    def run(self):
        while self.advance(0):
            if self.now("\n"):
                self.add_token(Tokens.NewLine(type="newline"))
            elif self.now('"', consume=False):
                self.parse_string()
            elif self.now(*string.digits, consume=False):
                self.parse_number()
            elif self.now(*self.__class__.literal_open, consume=False):
                self.parse_literal()
            elif op := self.now(*self.__class__.operators):
                self.add_token(Tokens.Operator(type="operator", value=op))
            elif self.now("#"):
                self.parse_comment()
            elif not self.now(' '):
                raise BaseException("Unexpected '%s'" % self.consume())

        return self._output

    def parse_string(self) -> None:
        assert self.consume() == '"'

        value = ""

        while ch := self.consume():
            if ch == '"':
                break
            elif ch == '\\':
                value += self.consume()
            else:
                value += ch

        self.add_token(Tokens.String(type="string", value=value))

    def parse_number(self) -> None:
        if self.now("0x"):
            allowed = string.hexdigits
            post = lambda val: int(val, 16)
        else:
            allowed = string.digits
            post = lambda val: val

        value = ""

        while ch := self.consume():
            if ch in allowed:
                value += ch
            else:
                self._index -= 1
                break

        self.add_token(Tokens.Number(type="number", value=post(value))) # pyright: ignore[reportArgumentType]

    def parse_literal(self) -> None:
        value = self.consume()

        while ch := self.consume():
            if ch in self.__class__.literal:
                value += ch
            else:
                self._index -= 1
                break

        self.add_token(Tokens.Literal(type="literal", value=value))

    def parse_comment(self) -> None:
        while self.consume() != "\n":
            pass
