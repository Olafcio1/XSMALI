from smali.parser.body.types import SectionBody
from ..iunparser import IUnparser

from smali.parser.datatypes.Class import Class
from smali.parser.datatypes.Method import Method
from smali.parser.datatypes.Annotation import Annotation

from ..datatypes.Class import handle_class
from ..datatypes.Method import handle_method
from ..datatypes.Annotation import handle_annotation

def handle_section_body(self: IUnparser, body: SectionBody) -> None:
    self.write(" {\n")
    self.tab(1)

    for member in body:
        if member['type'] == "method":
            method: Method = eval("member")
            handle_method(self, method)
        elif member['type'] == "class":
            clazz: Class = eval("member")
            handle_class(self, clazz)
            handle_section_body(self, clazz["body"]) # pyright: ignore[reportTypedDictNotRequiredAccess]
        elif member["type"] == "annotation":
            annotation: Annotation = eval("member")
            handle_annotation(self, annotation)

    self.tab(-1)
    self.write("}\n\n")
