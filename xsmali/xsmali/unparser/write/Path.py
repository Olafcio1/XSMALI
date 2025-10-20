from smali.parser.misc.Expression import Path
from ..iunparser import IUnparser

def write_path(self: IUnparser, path: Path) -> None:
    self.write(".".join(path["package"]))
    self.write("::".join(path["stack"]))
