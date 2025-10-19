import sys

from fromsmali.lexer import Lexer
from fromsmali.parser import Parser

def convertData(data: str):
    lexed = Lexer(data).run()
    parsed = Parser(lexed).run()

    return parsed

def convertFile(path: str) -> ...:
    with open(path, "r", encoding="utf-8") as f:
        data = f.read()

    return convertData(data)

args = sys.argv[1:]
if len(args) != 1:
    print("Usage: xsmali [.smali filename]")
    sys.exit(0)

print(convertFile(args[0]))
