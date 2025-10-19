from langbase.classes.BaseParser import BaseParser, EOFReaction

from langbase.tokens.token import TokenBase
from langbase.tokens.shortcuts import *

from .body.parser import BodyParser
from .tokens import *

class Parser(BaseParser[TokenBase]):
    def run(self):
        while self.advance():
            token = BodyParser.parse_section(self)
            self.add_token(token)

        return self._output

    def consume_newlines(self) -> None:
        while self.now({"type": "newline"}, eof=EOFReaction.NON_MATCH):
            pass
