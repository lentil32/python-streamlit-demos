import ply.yacc as yacc

from .ast import *
from .exceptions import *
from .lexer import *


class AWKParser:
    tokens = AWKLexer.tokens

    precedence = (
        ('left', 'OR'),
        ('left', 'AND'),
        ('left', 'EQ', 'NEQ'),
        ('left', 'LT', 'LTE', 'GT', 'GTE'),
        ('left', 'PLUS', 'MINUS'),
        ('left', 'TIMES', 'DIVIDE', 'MOD'),
        ('right', 'NOT'),
        ('right', 'UMINUS'),
    )

    def __init__(self) -> None:
        self.lexer = AWKLexer()
        self.lexer.build()
        self.parser = yacc.yacc(module=self, start='program')

    def parse(self, data: str) -> Program:
        return self.parser.parse(data, lexer=self.lexer.lexer)

    # Grammar rules
    def p_program(self, p):
        '''
        program : blocks
        '''
        p[0] = Program(p[1])

    def p_blocks(self, p):
        '''
        blocks : blocks block
               | block
        '''
        if len(p) == 3:
            p[0] = p[1]
            p[0].append(p[2])
        else:
            p[0] = [p[1]]

    def p_block(self, p):
        '''
        block : BEGIN LBRACE statements RBRACE
              | END LBRACE statements RBRACE
              | pattern LBRACE statements RBRACE
              | LBRACE statements RBRACE
        '''
        if p[1] == 'BEGIN' or p[1] == 'END':
            p[0] = Block(p[1], None, p[3])
        elif len(p) == 5:
            p[0] = Block('MAIN', p[1], p[3])
        else:
            # Block without pattern
            p[0] = Block('MAIN', None, p[2])

    def p_pattern(self, p):
        '''
        pattern : expression
        '''
        p[0] = p[1]

    def p_statements(self, p):
        '''
        statements : statements statement
                   | statement
        '''
        if len(p) == 3:
            p[0] = p[1]
            if p[2] is not None:
                p[0].append(p[2])
        else:
            p[0] = []
            if p[1] is not None:
                p[0].append(p[1])

    def p_statement(self, p):
        '''
        statement : print_statement
                  | assignment
                  | if_statement
                  | for_loop
                  | break_statement
                  | increment_operation
                  | block
                  | SEMICOLON
        '''
        if p[1] == ';':
            p[0] = None  # Ignore empty statements
        else:
            p[0] = p[1]

    def p_print_statement(self, p):
        '''
        print_statement : PRINT expressions
        '''
        p[0] = PrintStatement(p[2])

    def p_expressions(self, p):
        '''
        expressions : expressions COMMA expression
                    | expression
        '''
        if len(p) == 4:
            p[0] = p[1]
            p[0].append(p[3])
        else:
            p[0] = [p[1]]

    def p_assignment(self, p):
        '''
        assignment : IDENTIFIER ASSIGN expression
                   | IDENTIFIER PLUS_ASSIGN expression
                   | IDENTIFIER MINUS_ASSIGN expression
                   | IDENTIFIER TIMES_ASSIGN expression
                   | IDENTIFIER DIVIDE_ASSIGN expression
                   | IDENTIFIER MOD_ASSIGN expression
        '''
        p[0] = Assignment(p[1], p[2], p[3])

    def p_if_statement(self, p):
        '''
        if_statement : IF LPAREN expression RPAREN statement
                     | IF LPAREN expression RPAREN statement ELSE statement
        '''
        if len(p) == 6:
            p[0] = IfStatement(p[3], [p[5]], None)
        else:
            p[0] = IfStatement(p[3], [p[5]], [p[7]])

    def p_for_loop(self, p):
        '''
        for_loop : FOR LPAREN for_init SEMICOLON for_condition SEMICOLON for_increment RPAREN statement
        '''
        body = p[9]
        if isinstance(body, Block):
            p[0] = ForLoop(p[3], p[5], p[7], body.statements)
        elif body is None:
            p[0] = ForLoop(p[3], p[5], p[7], [])
        else:
            p[0] = ForLoop(p[3], p[5], p[7], [body])

    def p_for_init(self, p):
        '''
        for_init : assignment
                 | SEMICOLON
        '''
        if p[1] == ';':
            p[0] = None
        else:
            p[0] = p[1]

    def p_for_condition(self, p):
        '''
        for_condition : expression
                      | SEMICOLON
        '''
        if p[1] == ';':
            p[0] = Literal(True)  # Defaults to True
        else:
            p[0] = p[1]

    def p_for_increment(self, p):
        '''
        for_increment : assignment
                      | increment_operation
                      | SEMICOLON
        '''
        if p[1] == ';':
            p[0] = None
        else:
            p[0] = p[1]

    def p_break_statement(self, p):
        '''
        break_statement : BREAK SEMICOLON
        '''
        p[0] = BreakStatement()

    def p_increment_operation(self, p):
        '''
        increment_operation : INCREMENT IDENTIFIER
                            | DECREMENT IDENTIFIER
                            | IDENTIFIER INCREMENT
                            | IDENTIFIER DECREMENT
        '''
        if p[1] in ('++', '--'):
            p[0] = IncrementOperation(p[2], p[1], 'prefix')
        else:
            p[0] = IncrementOperation(p[1], p[2], 'postfix')

    def p_expression_binop(self, p):
        '''
        expression : expression PLUS expression
                   | expression MINUS expression
                   | expression TIMES expression
                   | expression DIVIDE expression
                   | expression MOD expression
                   | expression EQ expression
                   | expression NEQ expression
                   | expression LT expression
                   | expression LTE expression
                   | expression GT expression
                   | expression GTE expression
                   | expression AND expression
                   | expression OR expression
        '''
        p[0] = BinaryOperation(p[1], p[2], p[3])

    def p_expression_unary(self, p):
        '''
        expression : NOT expression
                   | MINUS expression %prec UMINUS
        '''
        p[0] = UnaryOperation(p[1], p[2])

    def p_expression_group(self, p):
        '''
        expression : LPAREN expression RPAREN
        '''
        p[0] = p[2]

    def p_expression_literal(self, p):
        '''
        expression : NUMBER
                   | STRING'''
        p[0] = Literal(p[1])

    def p_expression_variable(self, p):
        '''
        expression : IDENTIFIER
        '''
        p[0] = Variable(p[1])

    def p_expression_field(self, p):
        '''
        expression : DOLLAR field_index
        '''
        p[0] = FieldVariable(p[2])

    def p_field_index_number(self, p):
        '''
        field_index : NUMBER
        '''
        p[0] = Literal(p[1])

    def p_field_index_variable(self, p):
        '''
        field_index : IDENTIFIER
        '''
        p[0] = Variable(p[1])

    def p_error(self, p):
        if p:
            raise SyntaxError(
                f"Syntax error at '{p.value}' on line {p.lineno}")
        else:
            raise SyntaxError("Syntax error at EOF")
