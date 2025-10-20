def _format(text: str) -> str:
    return "\x1b[" + text + "m"

RESET = _format("0")
BOLD = _format("1")
UNDERLINE = _format("4")

def fore(r: int, g: int, b: int) -> str:
    return _format(f"38;2;{r};{g};{b}")
