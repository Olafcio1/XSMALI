"""
lightweight, simple terminal coloring library.

:project: xsmali
:author: [olafcio](https://github.com/Olafcio1)
"""

import sys
sys.path.insert(0, "/".join(__file__.replace("\\", "/").split("/")[:-1]))

import colors
import error
import style
import term

__all__ = ("error", "colors", "style", "term",)
