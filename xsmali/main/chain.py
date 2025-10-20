from colorium import colors, style, term
from typing import Callable

from .convert import convert_file

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
            print(term.gradient_linear(
                "  compiler error —",
                colors.css("hsl(15, 68%, 37%)"),
                colors.css("hsl(03, 68%, 36%)"),
                prefix=style.BOLD
            ) + term.gradient_linear(
                " file not found",
                colors.css("hsl(03, 68%, 36%)"),
                colors.css("hsl(15, 68%, 37%)")
            ))

    @staticmethod
    def help(*stackNames: str, _status: str | None = None) -> None:
        """
        Shows all commands available for a given target.

        :x-name: help
        """

        print(
            term.gradient_linear(
                "  xsmali",
                colors.css("hsl(23, 68%, 37%)"),
                colors.css("hsl(03, 68%, 36%)"),
                prefix=style.BOLD + style.UNDERLINE
            ) + (
                ""
                if _status == None else
                term.gradient_linear(
                    " — " + _status,
                    colors.css("hsl(03, 68%, 36%)"),
                    colors.css("hsl(23, 68%, 37%)"),
                    prefix=style.UNDERLINE
                )
            )
        )

        print(term.gradient_linear(
            "  available %scommands:" % (
                "sub" if stackNames else ""
            ),
            colors.css("hsl(23, 68%, 37%)"),
            colors.css("hsl(60, 100%, 22%)")
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

                print(term.gradient_linear(
                    "   󰘳 %s — %s" % (cmd, doc[0].rstrip()),
                    colors.css("hsl(36, 60%, 30%)"),
                    colors.css("hsl(26, 70%, 30%)")
                ))
            elif isinstance(value, type):
                print(term.gradient_linear(
                    "   󰕲 %s — %s" % (cmd, doc[0].rstrip()),
                    colors.css("hsl(36, 60%, 30%)"),
                    colors.css("hsl(26, 70%, 30%)")
                ))