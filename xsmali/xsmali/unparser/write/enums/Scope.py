from smali.parser.enums.Scope import Scope
from ...iunparser import IUnparser

def write_scope(self: IUnparser, scope: Scope) -> None:
    self.write({
        "RUNTIME": "runtime",
        "SYSTEM": "system"
    }[scope.name])
