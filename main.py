import sys
import colored
import colorium

from typing import Callable, NoReturn
from langbase.tokens.token import TokenBase

from smali.lexer import Lexer
from smali.parser import Parser
from xsmali.unparser import Unparser

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

args = sys.argv[1:]

class chain:
    @staticmethod
    def smali_to_xsmali(filename: str) -> None:
        """
        Converts a .smali file to a .xsmali file.

        :x-name: from
        """

        try:
            print(convert_file(filename))
        except FileNotFoundError:
            print(colorium.gradient_linear(
                "  compiler error —",
                colorium.css("hsl(15, 68%, 37%)"),
                colorium.css("hsl(03, 68%, 36%)"),
                prefix=colored.Style.BOLD
            ) + colorium.gradient_linear(
                " file not found",
                colorium.css("hsl(03, 68%, 36%)"),
                colorium.css("hsl(15, 68%, 37%)")
            ))

    @staticmethod
    def help(*stackNames: str, _status: str | None = None) -> None:
        """
        Shows all commands available for a given target.

        :x-name: help
        """

        print(
            colorium.gradient_linear(
                "  xsmali",
                colorium.css("hsl(23, 68%, 37%)"),
                colorium.css("hsl(03, 68%, 36%)"),
                prefix=colored.Style.BOLD + colored.Style.UNDERLINE
            ) + (
                ""
                if _status == None else
                colorium.gradient_linear(
                    " — " + _status,
                    colorium.css("hsl(03, 68%, 36%)"),
                    colorium.css("hsl(23, 68%, 37%)"),
                    prefix=colored.Style.UNDERLINE
                )
            )
        )

        print(colorium.gradient_linear(
            "  available %scommands:" % (
                "sub" if stackNames else ""
            ),
            colorium.css("hsl(23, 68%, 37%)"),
            colorium.css("hsl(60, 100%, 22%)")
        ))

        stack = [ chain ]
        for name in stackNames:
            stack.append(getattr(stack[-1], name))

        for cmd, value in stack[-1].__dict__.items():
            if value.__doc__ is None:
                continue

            doc: list[str] = value.__doc__.lstrip().splitlines()

            if isinstance(value, Callable):
                for line in doc:
                    line = line.strip()

                    if line.startswith(":x-name: "):
                        cmd = line[9:]
                        break
                else:
                    continue

                print(colorium.gradient_linear(
                    "   󰘳 %s — %s" % (cmd, doc[0].rstrip()),
                    colorium.css("hsl(36, 60%, 30%)"),
                    colorium.css("hsl(26, 70%, 30%)")
                ))
            elif isinstance(value, type):
                print(colorium.gradient_linear(
                    "   󰕲 %s — %s" % (cmd, doc[0].rstrip()),
                    colorium.css("hsl(36, 60%, 30%)"),
                    colorium.css("hsl(26, 70%, 30%)")
                ))

def unknownCommand(stack: list[str]) -> NoReturn:
    chain.help(*stack, _status="unknown command")
    sys.exit(1)

def invalidUsage(stack: list[str]) -> NoReturn:
    chain.help(*stack, _status="invalid usage")
    sys.exit(1)

if len(args) == 0:
    args.append("help")

target = chain
stack = []

for arg in args:
    args.pop(0)

    if arg.startswith("__"):
        unknownCommand(stack)
    else:
        name_magic = ":x-name: " + arg

        for member in target.__dict__.values():
            if not isinstance(member, Callable) or member.__doc__ is None:
                continue

            doc = member.__doc__.splitlines()

            for line in doc:
                if line.strip() == name_magic:
                    break
            else:
                continue

            break
        else:
            try:
                target = getattr(target, arg)
                if not isinstance(target, type):
                    raise BaseException("Not a group")
            except (AttributeError, BaseException):
                unknownCommand(stack)
            else:
                stack.append(arg)

            continue

        target = member
        break

if isinstance(target, Callable) and not isinstance(target, type):
    assert isinstance(target, staticmethod)

    target = target.__func__
    if target.__code__.co_argcount != len(args):
        invalidUsage(stack)
else:
    stack.insert(0, "help")
    target = chain.help

target(*args)
