from smali.parser.datatypes.Annotation import Annotation
from smali.parser.misc.Expression import Expression

from ..iunparser import IUnparser

from ..write.Path import write_path
from ..write.enums.Scope import write_scope

def handle_annotation(self: IUnparser, tok: Annotation) -> None:
    write_scope(self, tok["scope"])

    self.write(" annotation ")
    write_path(self, tok["path"])

    self.write(" {\n")
    handle_annotation_body(self, tok["fields"]) # pyright: ignore[reportTypedDictNotRequiredAccess]
    self.write("\n}")

def handle_annotation_body(self: IUnparser, tok: dict[str, Expression]) -> None:
    for key, expr in tok["fields"].items():
        self.write("%s = ..." % key)
