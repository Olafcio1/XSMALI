from typing import TypedDict, Literal

class Token(TypedDict):
    type: str

class Tokens:
    class NewLine(Token):
        type: Literal["newline"]

    class String(Token):
        type: Literal["string"]
        value: str

    class Number(Token):
        type: Literal["number"]
        value: str

    class Literal(Token):
        type: Literal["literal"]
        value: str

    class Operator(Token):
        type: Literal["operator"]
        value: str
