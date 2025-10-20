from typing import Any, Callable

from langbase.classes.BaseUnparser import BaseUnparser, UnparserError
from langbase.tokens.token import TokenBase

from smali.parser.datatypes.Annotation import Annotation

from .datatypes.Class import handle_class
from .datatypes.Annotation import handle_annotation

from .misc.SectionBody import handle_section_body

__all__ = ("Unparser",)

class Unparser(BaseUnparser[TokenBase]):
    def run(self):
        while tok := self.consume():
            if tok['type'] == "class":
                self.handle_section(tok, handle_class)
            elif tok['type'] == "annotation":
                annotation: Annotation = eval("tok")
                handle_annotation(self, annotation)
            else:
                raise UnparserError("Unrecognized token %r" % tok['type'])

        return self._output

    def handle_section(self, tok: TokenBase, handler: Callable[["Unparser", Any], None]) -> None:
        handler(self, tok)
        handle_section_body(self, tok["body"])
