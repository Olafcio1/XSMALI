from typing import Literal

from langbase.tokens.token import TokenBase
from langbase.tokens.shortcuts import *
from langbase.classes.BaseParser import ParserError

from .Expression import ExpressionParser, Path, Parameter, Variable
from .Type import TypeParser, Type

from ..enums.ObjectSide import ObjectSide
from ..iparser import IParser

# __all__ = ("Statement", "StatementParser",)

#region Types
Statement = TokenBase
MethodBody = list[Statement]

Register = Parameter | Variable

#region Statements
class ReturnVoid(Statement):
    type: Literal["return-void"]

class ReturnObject(Statement):
    type: Literal["return-object"]
    register: Register

class DefineLocals(Statement):
    type: Literal["define-locals"]
    value: int

class DebugLine(Statement):
    type: Literal["debug-line"]
    value: int

class Invoke(Statement):
    """Invokes a method."""
    type: Literal["invoke"]
    variant: str
    providedArgs: list[str]
    methodPath: Path
    argTypes: list[Type]
    returnType: Type

class ConstString(Statement):
    """Sets a variable to a given string."""
    type: Literal["const-string"]
    name: Register
    value: str

class ConstClass(Statement):
    """Sets a variable to a given class (type) reference."""
    type: Literal["const-class"]
    name: Register
    value: Path

class NewInstance(Statement):
    type: Literal["new-instance"]
    register: Register
    path: Path

class MoveResultObject(Statement):
    type: Literal["move-result-object"]
    register: Register

class MoveObject(Statement):
    type: Literal["move-object"]
    source: Register
    destination: Register

class Move(Statement):
    type: Literal["move"]
    source: Register
    destination: Register

class Get(Statement):
    type: Literal["get"]
    register: Register
    side: ObjectSide
    path: Path

#region Parser
class StatementParser:
    @classmethod
    def parse_statement(cls, self: IParser) -> Statement:
        if self.now(Make.Literal("return-void")):
            return cls.parse_return_void(self)
        elif self.now(Make.Literal("return-object")):
            return cls.parse_return_object(self)
        elif self.now(
                Make.Operator("."),
                Make.Literal("locals")
        ):
            return cls.parse_locals(self)
        elif self.now(
                Make.Operator("."),
                Make.Literal("line")
        ):
            return cls.parse_line(self)
        elif (
                (tok := self.now({"type": "literal"}, consume=False)) and
                tok[0]['value'].startswith("invoke-")
        ):
            self.consume("literal")
            return cls.parse_invoke(self, variant=tok[0]['value'][7:])
        elif self.now(Make.Literal("const-string")):
            return cls.parse_const_string(self)
        elif self.now(Make.Literal("const-class")):
            return cls.parse_const_class(self)
        elif self.now(Make.Literal("new-instance")):
            return cls.parse_new_instance(self)
        elif self.now(Make.Literal("move-result-object")):
            return cls.parse_move_result_object(self)
        elif self.now(Make.Literal("move-object")):
            return cls.parse_move_object(self)
        elif self.now(Make.Literal("move")):
            return cls.parse_move(self)
        elif self.now(Make.Literal("sget")):
            return cls.parse_sget(self, ObjectSide.STATIC)
        # elif self.now(Make.Literal("iget")):
        #     return cls.parse_sget(self, ObjectSide.INSTANCE)
        else:
            print(self.advance())
            raise ParserError("Expected a statement")

    @classmethod
    def parse_return_void(cls, self: IParser) -> ReturnVoid:
        return ReturnVoid(
            type="return-void"
        )

    @classmethod
    def parse_return_object(cls, self: IParser) -> ReturnObject:
        return ReturnObject(
            type="return-object",
            register=cls._parse_register(self)
        )

    @classmethod
    def parse_locals(cls, self: IParser) -> DefineLocals:
        return DefineLocals(
            type="define-locals",
            value=int(self.consume("number")['value'])
        )

    @classmethod
    def parse_line(cls, self: IParser) -> DebugLine:
        return DebugLine(
            type="line",
            value=int(self.consume("number")['value'])
        )

    @classmethod
    def parse_invoke(cls, self: IParser, *, variant: str) -> Invoke:
        providedArgs = ExpressionParser.parse_list(self)
        self.consume("operator", Make.Operator(","))
        methodPath = ExpressionParser.parse_lit_path(self)
        argTypes = TypeParser.parse_type_list(self)
        returnType = TypeParser.parse_type(self)

        return Invoke(
            type="invoke",
            variant=variant,
            providedArgs=providedArgs,
            methodPath=methodPath,
            argTypes=argTypes,
            returnType=returnType
        )

    @classmethod
    def parse_const_string(cls, self: IParser) -> ConstString:
        name = cls._parse_register(self)
        self.consume("operator", Make.Operator(","))
        value = self.consume("string")['value']

        return ConstString(
            type="const-string",
            name=name,
            value=value
        )

    @classmethod
    def parse_const_class(cls, self: IParser) -> ConstClass:
        name = cls._parse_register(self)
        self.consume("operator", Make.Operator(","))
        value = ExpressionParser.parse_lit_path(self)

        return ConstClass(
            type="const-class",
            name=name,
            value=value
        )

    @classmethod
    def parse_new_instance(cls, self: IParser) -> NewInstance:
        register = cls._parse_register(self)
        self.consume("operator", Make.Operator(","))
        path = ExpressionParser.parse_lit_path(self)

        return NewInstance(
            type="new-instance",
            register=register,
            path=path
        )

    @classmethod
    def _parse_register(cls, self: IParser) -> Register:
        literal = self.consume("literal")
        value = literal['value']

        if value[0] in ('p', 'v'):
            value = value[1:]
            casted: Parameter | Variable = eval("literal")

            return casted
        else:
            raise ParserError("Expected a register")

    @classmethod
    def parse_move_result_object(cls, self: IParser) -> MoveResultObject:
        register = cls._parse_register(self)

        return MoveResultObject(
            type="move-result-object",
            register=register
        )

    @classmethod
    def parse_move_object(cls, self: IParser) -> MoveObject:
        src = cls._parse_register(self)
        dest = cls._parse_register(self)

        return MoveObject(
            type="move-object",
            source=src,
            destination=dest
        )

    @classmethod
    def parse_move(cls, self: IParser) -> Move:
        src = cls._parse_register(self)
        dest = cls._parse_register(self)

        return Move(
            type="move",
            source=src,
            destination=dest
        )

    @classmethod
    def parse_sget(cls, self: IParser, side: ObjectSide) -> Get:
        register = cls._parse_register(self)
        self.consume("operator", Make.Operator(","))
        path = ExpressionParser.parse_lit_path(self)

        return Get(
            type="get",
            register=register,
            side=side,
            path=path
        )
