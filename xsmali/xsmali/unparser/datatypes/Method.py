from smali.parser.datatypes.Method import Method

from ..iunparser import IUnparser

from ..write.enums.Visibility import write_visibility
from ..write.Type import write_type

from ..misc.MethodBody import handle_method_body

def handle_method(self: IUnparser, method: Method) -> None:
    write_visibility(self, method["visibility"])

    if method["static"]:
        self.write(" static")

    if method["final"]:
        self.write(" final")

    if method["synthetic"]:
        self.write(" synthetic")

    if method["constructor"]:
        self.write(" constructor")

    self.write(" ")
    write_type(self, method["returns"])
    self.write(" ")
    self.write(method["name"])
    self.write("(")
    self.write(", ".join(method["args"]))
    self.write(") {\n")
    handle_method_body(self, method["body"]) # pyright: ignore[reportTypedDictNotRequiredAccess]
    self.write("}\n")
