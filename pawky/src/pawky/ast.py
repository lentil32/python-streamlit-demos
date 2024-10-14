from typing import Optional


class ASTNode:
    pass


class Expression(ASTNode):
    pass


class Statement(ASTNode):
    pass


class Block(ASTNode):

    def __init__(self, block_type: str, pattern: Optional[Expression],
                 statements: list[Statement]) -> None:
        self.block_type = block_type
        self.pattern = pattern
        self.statements = statements


class Program(ASTNode):

    def __init__(self, blocks: list[Block]) -> None:
        self.blocks = blocks


class PrintStatement(Statement):

    def __init__(self, expressions: list[Expression]):
        self.expressions = expressions


class Assignment(Statement):

    def __init__(self, variable: str, operator: str,
                 expression: Expression) -> None:
        self.variable = variable
        self.operator = operator
        self.expression = expression


class IfStatement(Statement):

    def __init__(self, condition: Expression, then_branch: list[Statement],
                 else_branch: Optional[list[Statement]]) -> None:
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch


class ForLoop(Statement):

    def __init__(self, init: Optional[Statement], condition: Expression,
                 increment: Optional[Statement],
                 body: list[Statement]) -> None:
        self.init = init
        self.condition = condition
        self.increment = increment
        self.body = body


class BreakStatement(Statement):
    pass


class IncrementOperation(Statement):

    def __init__(self, variable: str, operator: str, position: str) -> None:
        self.variable = variable
        self.operator = operator
        self.position = position


class BinaryOperation(Expression):

    def __init__(self, left: Expression, operator: str,
                 right: Expression) -> None:
        self.left = left
        self.operator = operator
        self.right = right


class UnaryOperation(Expression):

    def __init__(self, operator: str, operand: Expression) -> None:
        self.operator = operator
        self.operand = operand


class Literal(Expression):

    def __init__(self, value: int | float | str) -> None:
        self.value = value


class Variable(Expression):

    def __init__(self, name: str) -> None:
        self.name = name


class FieldVariable(Expression):

    def __init__(self, index: Literal | Variable) -> None:
        self.index = index
