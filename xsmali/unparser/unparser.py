from langbase.classes.BaseUnparser import BaseUnparser, UnparserError
from langbase.tokens.token import TokenBase

from smali.parser.datatypes.Class import Class
from smali.parser.misc.Expression import Path

__all__ = ("Unparser",)

class Unparser(BaseUnparser[TokenBase]):
    def run(self):
        while tok := self.consume():
            if tok['type'] == "class":
                clazz: Class = eval("tok")
                self.handle_class(clazz)
            else:
                raise UnparserError("Unrecognized token %r" % tok['type'])

        return self._output

    def handle_class(self, tok: Class) -> None:
        self.write({
            "PUBLIC": "public",
            "PROTECTED": "protected",
            "PRIVATE": "private"
        }[tok["visibility"].name])

        if tok["final"]:
            self.write(" final")

        self.write(" class ")
        self.write_path(tok["path"])
        self.write(" {\n")
        self.write("}\n\n")

    def write_path(self, path: Path) -> None:
        self.write(".".join(path["value"]))
