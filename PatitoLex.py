import ply.lex as lex

keywords = {
    'program': 'PROGRAM',
    'var': 'VAR',
    'int': 'INT',
    'float': 'FLOAT',
    'char': 'CHAR',
    'main': 'MAIN',
    'function': 'FUNCTION',
    'void': 'VOID',
    'if': 'IF',
    'else': 'ELSE',
    'print': 'PRINT',
    'read': 'READ',
    'while': 'WHILE',
    'do': 'DO',
    'from': 'FROM',
    'until': 'UNTIL',
    'return': 'RETURN'
}

tokens = [
    'CTE_INT',
    'CTE_FLOAT',
    'CTE_CHAR',
    'CTE_STRING',
    'IDENTIFIER',
    'PLUS',
    'MINUS',
    'MULTIPLICATION',
    'DIVISION',
    'L_PAREN',
    'R_PAREN',
    'L_BRACKET',
    'R_BRACKET',
    'R_SQ_BRACKET',
    'L_SQ_BRACKET',
    # 'COLON',
    'SEMICOLON',
    'EQUALS',
    'LESS_THAN',
    'GREATER_THAN',
    'LESS_EQUAL_THAN',
    'GREATER_EQUAL_THAN',
    'IS_DIFFERENT',
    'IS_EQUAL',
    'AND',
    'OR',
    'COMMA',
    # 'COMMENT'
    'TRANS',
    'INV',
    'DET'
] + list(keywords.values())

t_CTE_STRING = r'".*."'
t_PLUS = r'\+'
t_MINUS = r'-'
t_MULTIPLICATION = r'\*'
t_DIVISION = r'/'
t_L_PAREN = r'\('
t_R_PAREN = r'\)'
t_L_BRACKET = r'{'
t_R_BRACKET = r'}'
t_R_SQ_BRACKET = r'\]'
t_L_SQ_BRACKET = r'\['
# t_COLON = r'\:'
t_SEMICOLON = r';'
t_EQUALS = r'='
t_LESS_THAN = r'<'
t_GREATER_THAN = r'>'
t_LESS_EQUAL_THAN = r'<='
t_GREATER_EQUAL_THAN = r'>='
t_IS_DIFFERENT = r'!='
t_IS_EQUAL = r'=='
t_AND = r'&&'
t_OR = r'\|\|'
t_COMMA = r'\,'
# t_COMMENT = r'%%.*'
# t_CTE_INT = r'[0-9][0-9]*'
# t_CTE_FLOAT = r'(\+|-)?[0-9]*.[0-9][0-9]*?f'
t_TRANS = r'%'
t_DET = r'\$'
t_INV = r'\?'

def t_CTE_FLOAT(t):
    # r'\[-+]?\d+|(\.\d+|\d+\.\d+)([eE][-+]?\d+)?'
    r'[-+]?[0-9]+[.][0-9]+'
    t.value = float(t.value)
    return t
    
def t_CTE_INT(t):
    r'[-+]?[0-9]+'
    t.value = int(t.value)
    return t

def t_CTE_CHAR(t):
    r'\'[A-Za-z]\''
    t.value = t.value[1]
    return t


def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = keywords.get(t.value, 'IDENTIFIER')
    return t


# Ignore whitespace
t_ignore = " \t"


def t_new_line(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    print("Illegal character '{}' at: {}".format(t.value[0], t.lexer.lineno))
    t.lexer.skip(1)
	
lexer = lex.lex()