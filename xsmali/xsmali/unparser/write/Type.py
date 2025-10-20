from smali.parser.misc.Type import *
from langbase.classes.BaseUnparser import UnparserError

from ..iunparser import IUnparser
from .Path import write_path

def write_type(self: IUnparser, Type: Type) -> None:
    if isinstance(Type, SpecialType):
        self.write({
            "INT": "int",
            "LONG": "long",
            "BOOELAN": "boolean",
            "BYTE": "byte",
            "CHAR": "char",
            "SHORT": "short",
            "FLOAT": "float",
            "DOUBLE": "double",
            "VOID": "void"
        }[Type.name])
    elif isinstance(Type, ArrayType):
        write_type(self, Type.type)
        self.write("[]")
    elif isinstance(Type, ObjectType):
        write_path(self, Type.path)
    else:
        raise UnparserError("Unrecognized type %r" % Type)
