from smali.parser.enums.Visibility import Visibility
from ...iunparser import IUnparser

def write_visibility(self: IUnparser, visibility: Visibility) -> None:
    self.write({
        "PUBLIC": "public",
        "PROTECTED": "protected",
        "PRIVATE": "private"
    }[visibility.name])
