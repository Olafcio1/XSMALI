import sys
import colorama

from typing import Callable, NoReturn
from colorium import *

from .chain import chain

def unknown_command(stack: list[str]) -> NoReturn:
    chain.help(*stack, _status="unknown command")
    sys.exit(1)

def invalid_usage(stack: list[str]) -> NoReturn:
    chain.help(*stack, _status="invalid usage")
    sys.exit(1)

def main():
    colorama.just_fix_windows_console()

    args = sys.argv[1:]
    if len(args) == 0:
        args.append("help")

    target = chain
    stack = []

    for arg in args:
        args.pop(0)

        if arg.startswith("__"):
            unknown_command(stack)
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
                    unknown_command(stack)
                else:
                    stack.append(arg)

                continue

            target = member
            break

    if isinstance(target, Callable) and not isinstance(target, type):
        assert isinstance(target, staticmethod)

        target = target.__func__
        if target.__code__.co_argcount != len(args):
            invalid_usage(stack)
    else:
        stack.insert(0, "help")
        target = chain.help

    target(*args)

main()
