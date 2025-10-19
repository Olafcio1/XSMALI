"""
lightweight, simple terminal coloring library.

:project: xsmali
:author: [olafcio](https://github.com/Olafcio1)
"""

import colored
import math
from colour import Color

__all__ = ("error", "rgb", "hsl", "css", "colorize", "gradient_linear")

class error(BaseException):
    pass

def rgb(r: float, g: float, b: float) -> Color:
    """
    :param r: red (0-255)
    :param g: green (0-255)
    :param b: blue (0-255)
    """

    return Color(rgb = (
        math.floor(r) / 255,
        math.floor(g) / 255,
        math.floor(b) / 255
    ))

def hsl(h: float, s: float, l: float) -> Color:
    """
    :param h: hue (0-360)
    :param s: saturation (0-100)
    :param l: lightness (0-100)
    """

    return Color(hsl = (
        math.floor(h) / 360,
        math.floor(s) / 100,
        math.floor(l) / 100
    ))

def css(text: str) -> Color:
    functions = {
        "rgb": rgb,
        "hsl": hsl
    }

    for name, func in functions.items():
        if text.startswith(name + "("):
            a, b, c = text[4:-1].split(",")

            return func(
                float(a.strip().removesuffix("deg")),
                float(b.strip().removesuffix("%")),
                float(c.strip().removesuffix("%"))
            )
    else:
        raise error("Unsupported format")

def colorize(
        text: str,
        colors: list[Color],
        *,
        prefix: str = ""
) -> str:
    assert len(colors) == len(text)
    out = ""

    for ch in text:
        out += colored.fore_rgb(*[int(v * 255) for v in colors.pop(0).rgb])
        out += prefix
        out += ch

    return out + colored.Style.RESET

def gradient_linear(
        text: str,
        colorA: Color,
        colorB: Color,
        *,
        prefix: str = ""
) -> str:
    colors = colorA.range_to(colorB, len(text))
    return colorize(text, [*colors], prefix=prefix)
