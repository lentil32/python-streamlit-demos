from typing import Any

from .ast import *
from .exceptions import *
from .lexer import *
from .parser import *


class AWKInterpreter:

    def __init__(self, script: str) -> None:
        self.parser = AWKParser()
        self.ast: Program = self.parser.parse(script)
        self.variables: dict[str, Any] = {}
        self.builtins: dict[str, Any] = {
            'FS': ' ',
            'OFS': ' ',
            'RS': '\n',
            'ORS': '\n',
            'NF': 0,
            'NR': 0,
        }
        self.input_data = ""
        self.begin_blocks: list[Block] = []
        self.main_blocks: list[Block] = []
        self.end_blocks: list[Block] = []

    def set_input(self, input_data: str) -> None:
        self.input_data = input_data

    def run(self) -> None:
        # Separate blocks
        for block in self.ast.blocks:
            if block.block_type == 'BEGIN':
                self.begin_blocks.append(block)
            elif block.block_type == 'END':
                self.end_blocks.append(block)
            else:
                self.main_blocks.append(block)

        # Execute BEGIN blocks
        for block in self.begin_blocks:
            self.execute_statements(block.statements)

        # Split input_data into records based on RS
        records = self.input_data.split(self.builtins['RS'])

        # Process each record
        for record in records:
            # Skip empty records
            if not record.strip():
                continue
            self.builtins['NR'] += 1
            self.line = record
            self.fields = self.line.split(self.builtins['FS'])
            self.builtins['NF'] = len(self.fields)
            # Execute MAIN blocks
            for block in self.main_blocks:
                if block.pattern:
                    condition = self.evaluate_expression(block.pattern)
                    if not condition:
                        continue
                self.execute_statements(block.statements)

        # Execute END blocks
        for block in self.end_blocks:
            self.execute_statements(block.statements)

    def execute_statements(self, statements: list[Statement]) -> None:
        for stmt in statements:
            self.execute_statement(stmt)

    def execute_statement(self, stmt: Statement) -> None:
        if isinstance(stmt, PrintStatement):
            self.execute_print(stmt)
        elif isinstance(stmt, Assignment):
            self.execute_assignment(stmt)
        elif isinstance(stmt, IfStatement):
            self.execute_if(stmt)
        elif isinstance(stmt, ForLoop):
            self.execute_for(stmt)
        elif isinstance(stmt, BreakStatement):
            raise BreakException()
        elif isinstance(stmt, IncrementOperation):
            self.execute_increment(stmt)
        elif isinstance(stmt, Block):
            self.execute_statements(stmt.statements)
        else:
            raise NotImplementedError(f"Unknown statement type: {type(stmt)}")

    def execute_print(self, stmt: PrintStatement) -> None:
        output = []
        for expr in stmt.expressions:
            value = self.evaluate_expression(expr)
            output.append(str(value))
        ofs = self.builtins['OFS']
        ors = self.builtins['ORS']
        print(ofs.join(output), end=ors)

    def execute_assignment(self, stmt: Assignment) -> None:
        var_name = stmt.variable
        operator = stmt.operator
        value = self.evaluate_expression(stmt.expression)
        _, var_storage = self.get_variable_storage(var_name)

        if operator == '=':
            var_storage[var_name] = value
        else:
            if var_name not in var_storage:
                var_storage[var_name] = 0
            current = var_storage[var_name]
            if operator == '+=':
                var_storage[var_name] = current + value
            elif operator == '-=':
                var_storage[var_name] = current - value
            elif operator == '*=':
                var_storage[var_name] = current * value
            elif operator == '/=':
                var_storage[var_name] = current / value
            elif operator == '%=':
                var_storage[var_name] = current % value
            else:
                raise SyntaxError(f"Unknown assignment operator: {operator}")

    def execute_if(self, stmt: IfStatement) -> None:
        condition = self.evaluate_expression(stmt.condition)
        if condition:
            self.execute_statements(stmt.then_branch)
        elif stmt.else_branch:
            self.execute_statements(stmt.else_branch)

    def execute_for(self, stmt: ForLoop) -> None:
        try:
            if stmt.init:
                self.execute_statement(stmt.init)
            while self.evaluate_expression(stmt.condition):
                try:
                    self.execute_statements(stmt.body)
                except BreakException:
                    break
                if stmt.increment:
                    self.execute_statement(stmt.increment)
        except BreakException:
            pass

    def execute_increment(self, stmt: IncrementOperation) -> None:
        var_name = stmt.variable
        operator = stmt.operator  # `++` or `--`
        _, var_storage = self.get_variable_storage(var_name)

        if var_name in var_storage:
            if not isinstance(var_storage[var_name], (int, float)):
                raise TypeError(
                    f"Variable '{var_name}' must be a number for increment/decrement operations."
                )
            if operator == '++':
                var_storage[var_name] += 1
            elif operator == '--':
                var_storage[var_name] -= 1
        else:
            var_storage[var_name] = 1 if operator == '++' else -1

    def get_variable_storage(
        self, var_name: str
    ) -> tuple[str, dict[str, Any]]:  # TODO Use TypeGuard to narrow typing
        if var_name in self.builtins:
            return 'builtins', self.builtins
        else:
            return 'variables', self.variables

    def evaluate_expression(self, expr: Expression) -> Any:
        if isinstance(expr, Literal):
            return expr.value
        elif isinstance(expr, Variable):
            return self.get_variable(expr.name)
        elif isinstance(expr, FieldVariable):
            return self.get_field(expr.index)
        elif isinstance(expr, BinaryOperation):
            left = self.evaluate_expression(expr.left)
            right = self.evaluate_expression(expr.right)
            return self.apply_binary_operator(expr.operator, left, right)
        elif isinstance(expr, UnaryOperation):
            operand = self.evaluate_expression(expr.operand)
            return self.apply_unary_operator(expr.operator, operand)
        else:
            raise NotImplementedError(f"Unknown expression type: {type(expr)}")

    def get_variable(self, name: str) -> int | float | str:
        if name in self.variables:
            return self.variables[name]
        elif name in self.builtins:
            return self.builtins[name]
        else:
            return 0  # Undefined variables default to 0

    def get_field(self, index_expr: Literal | Variable) -> int | float | str:
        index = self.evaluate_expression(index_expr)
        if isinstance(index, str):
            if index.isdigit():
                index = int(index)
            else:
                return ""
        if index == 0:
            return self.line
        elif 1 <= index <= len(self.fields):
            field = self.fields[index - 1]
            # Attempt to convert the field to int or float
            try:
                if '.' in field:
                    return float(field)
                else:
                    return int(field)
            except ValueError:
                return field  # Return as string if not a number
        else:
            return ""

    def apply_binary_operator(self, operator: str, left: Any,
                              right: Any) -> Any:
        try:
            if operator == '+':
                return left + right
            elif operator == '-':
                return left - right
            elif operator == '*':
                return left * right
            elif operator == '/':
                return left / right
            elif operator == '%':
                return left % right
            elif operator == '==':
                return left == right
            elif operator == '!=':
                return left != right
            elif operator == '<':
                return left < right
            elif operator == '<=':
                return left <= right
            elif operator == '>':
                return left > right
            elif operator == '>=':
                return left >= right
            elif operator == '&&':
                return left and right
            elif operator == '||':
                return left or right
            else:
                raise SyntaxError(f"Unknown binary operator: {operator}")
        except Exception as e:
            raise Exception(f"Error applying operator '{operator}': {e}")

    def apply_unary_operator(self, operator: str, operand: Any) -> Any:
        try:
            if operator == '-':
                return -operand
            elif operator == '!':
                return not operand
            else:
                raise SyntaxError(f"Unknown unary operator: {operator}")
        except Exception as e:
            raise Exception(f"Error applying unary operator '{operator}': {e}")
