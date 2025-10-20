import sys
import importlib

sys.path.insert(0, "/".join(__file__.replace("\\", "/").split("/")[:-2]))
importlib.import_module("main")
