from smali.parser.datatypes.Class import Class

from ..iunparser import IUnparser

from ..write.Path import write_path
from ..write.enums.Visibility import write_visibility

def handle_class(self: IUnparser, tok: Class) -> None:
    write_visibility(self, tok["visibility"])

    if tok["final"]:
        self.write(" final")

    self.write(" class ")
    write_path(self, tok["path"])

    if tok["extends"] != None: # pyright: ignore[reportTypedDictNotRequiredAccess]
        self.write(" extends ")
        write_path(self, tok["extends"]) # pyright: ignore[reportTypedDictNotRequiredAccess]
