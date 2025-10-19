from .token import TokenBase

__all__ = ("Make",)

class Make:
    @staticmethod
    def Operator(value: str) -> TokenBase:
        return {
            "type": "operator",
            "value": value
        }

    @staticmethod
    def Literal(value: str) -> TokenBase:
        return {
            "type": "literal",
            "value": value
        }
