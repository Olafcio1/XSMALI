import style
from colour import Color

def colorize(
        text: str,
        colors: list[Color],
        *,
        prefix: str = ""
) -> str:
    assert len(colors) == len(text)
    out = ""

    for ch in text:
        out += style.fore(*[int(v * 255) for v in colors.pop(0).rgb])
        out += prefix
        out += ch

    return out + style.RESET

def gradient_linear(
        text: str,
        colorA: Color,
        colorB: Color,
        *,
        prefix: str = ""
) -> str:
    colors = colorA.range_to(colorB, len(text))
    return colorize(text, [*colors], prefix=prefix)
