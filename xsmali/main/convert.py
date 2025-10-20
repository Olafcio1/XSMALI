from langbase.tokens.token import TokenBase

from smali import Lexer, Parser
from xsmali import Unparser

def parse_data(data: str) -> list[TokenBase]:
    lexed = Lexer(data).run()
    parsed = Parser(lexed).run()

    return parsed

def unparse_data(data: list[TokenBase]) -> str:
    unparsed = Unparser(data).run()

    return unparsed

def convert_file(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        data = f.read()

    return unparse_data(parse_data(data))
