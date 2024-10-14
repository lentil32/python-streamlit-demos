import ply.lex as lex

from .ast import *
from .exceptions import *


class AWKLexer:
    tokens = (
        'PLUS_ASSIGN',
        'MINUS_ASSIGN',
        'TIMES_ASSIGN',
        'DIVIDE_ASSIGN',
        'MOD_ASSIGN',
        'INCREMENT',
        'DECREMENT',
        'EQ',
        'NEQ',
        'LTE',
        'GTE',
        'LT',
        'GT',
        'AND',
        'OR',
        'NOT',
        'PLUS',
        'MINUS',
        'TIMES',
        'DIVIDE',
        'MOD',
        'ASSIGN',
        'LPAREN',
        'RPAREN',
        'LBRACE',
        'RBRACE',
        'SEMICOLON',
        'COMMA',
        'DOLLAR',
        'NUMBER',
        'STRING',
        'IDENTIFIER',
        'BEGIN',
        'END',
        'IF',
        'ELSE',
        'FOR',
        'PRINT',
        'BREAK',
    )

    reserved = {
        'BEGIN': 'BEGIN',
        'END': 'END',
        'if': 'IF',
        'else': 'ELSE',
        'for': 'FOR',
        'print': 'PRINT',
        'break': 'BREAK',
    }

    t_PLUS_ASSIGN = r'\+='
    t_MINUS_ASSIGN = r'-='
    t_TIMES_ASSIGN = r'\*='
    t_DIVIDE_ASSIGN = r'/='
    t_MOD_ASSIGN = r'%='
    t_INCREMENT = r'\+\+'
    t_DECREMENT = r'--'
    t_EQ = r'=='
    t_NEQ = r'!='
    t_LTE = r'<='
    t_GTE = r'>='
    t_LT = r'<'
    t_GT = r'>'
    t_AND = r'&&'
    t_OR = r'\|\|'
    t_NOT = r'!'
    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_TIMES = r'\*'
    t_DIVIDE = r'/'
    t_MOD = r'%'
    t_ASSIGN = r'='
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_LBRACE = r'\{'
    t_RBRACE = r'\}'
    t_SEMICOLON = r';'
    t_COMMA = r','
    t_DOLLAR = r'\$'

    t_ignore = ' \t'

    def t_COMMENT(self, t):
        r'\#.*'
        pass  # Ignore comments

    def t_NEWLINE(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    def t_STRING(self, t):
        r'\"([^\\\n]|(\\.))*?\"|\'([^\\\n]|(\\.))*?\''
        t.value = t.value[1:-1]  # Remove quotes
        return t

    def t_NUMBER(self, t):
        r'\d+(\.\d*)?'
        if '.' in t.value:
            t.value = float(t.value)
        else:
            t.value = int(t.value)
        return t

    def t_IDENTIFIER(self, t):
        r'[A-Za-z_][A-Za-z0-9_]*'
        t.type = self.reserved.get(t.value, 'IDENTIFIER')
        return t

    def t_error(self, t):
        raise SyntaxError(
            f'Illegal character {t.value[0]!r} at line {t.lineno}')

    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    def input(self, data):
        self.lexer.input(data)

    def token(self):
        return self.lexer.token()
