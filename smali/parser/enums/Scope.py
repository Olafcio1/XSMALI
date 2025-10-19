from enum import StrEnum
from ..iparser import IParser

class Scope(StrEnum):
    RUNTIME = "runtime"
    SYSTEM = "system"

def parse_scope(self: IParser) -> Scope:
    value = self.consume("literal")['value']
    return Scope(value)
