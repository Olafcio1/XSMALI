import math

from error import error
from colour import Color

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
