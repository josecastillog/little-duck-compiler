import ply.lex as lex
import ply.yacc as yacc

# Palabras reservadas
reserved = {
   'if'        : 'IF',
   'else'      : 'ELSE',
   'program'   : 'PROGRAM',
   'main'      : 'MAIN',
   'end'       : 'END',
   'var'       : 'VAR',
   'int'       : 'INT',
   'float'     : 'FLOAT',
   'print'     : 'PRINT',
   'void'      : 'VOID',
   'while'     : 'WHILE',
   'do'        : 'DO',
   'if'        : 'IF',
   'else'      : 'ELSE',
}

# Lista de tokens
tokens = [
   'ID',
   'SEMI_COLON',
   'OPEN_PAR',
   'CLOSE_PAR',
   'DIVIDE',
   'MULTIPLY',
   'ADD',
   'SUBTRACT',
   'LESS_THAN',
   'MORE_THAN',
   'NOT_EQUAL',
   'COLON',
   'L_BRACKET',
   'R_BRACKET',
   'LEFT_CURLY',
   'RIGHT_CURLY',
   'COMMA',
   'EQUAL',
   'CTE_STRING',
   'CTE_FLOAT',
   'CTE_INT', 
] + list(reserved.values())

# Define reglas para cada token
t_SEMI_COLON = r';'
t_OPEN_PAR = r'\('
t_CLOSE_PAR = r'\)'
t_DIVIDE = r'/'
t_MULTIPLY = r'\*'
t_ADD = r'\+'
t_SUBTRACT = r'-'
t_LESS_THAN = r'<'
t_MORE_THAN = r'>'
t_NOT_EQUAL = r'!='
t_COLON = r':'
t_L_BRACKET = r'\['
t_R_BRACKET = r'\]'
t_LEFT_CURLY = r'{'
t_RIGHT_CURLY = r'}'
t_COMMA = r','
t_EQUAL = r'='

# -------------------- Funciones Expresiones Regulares --------------------
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')  # Checar palabras reservadas
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_CTE_FLOAT(t):
    r'[-+]?[0-9]*\.[0-9]+'
    t.value = float(t.value)
    return t

def t_CTE_INT(t):
    r'[0-9]+'
    t.value = int(t.value)
    return t

def t_CTE_STRING(t):
    r'"([^"]*)"'
    t.value = str(t.value)
    return t

t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# ---------------------------- Funciones parser ---------------------------

def p_programa(p):
    """programa : PROGRAM ID SEMI_COLON dec_v dec_f MAIN body END
    """

def p_vars(p):
    """vars : VAR variables COLON type SEMI_COLON mas_var
            | empty"""

def p_variables(p):
    """variables : list_ids
    """

def p_mas_var(p):
    """mas_var : variables
       | empty"""

def p_list_ids(p):
    "list_ids : ID mas_ids"

def p_mas_ids(p):
    """mas_ids : COMMA list_ids
       | empty"""
    
def p_type(p):
    """type : INT
       | FLOAT
    """

def p_dec_v(p):
    """dec_v : vars
    """

def p_dec_f(p):
    """dec_f : funcs mas_f
       | empty
    """

def p_mas_f(p):
    """mas_f : funcs mas_f
       | empty
    """

def p_body(p):
    """
    body : LEFT_CURLY mas_statement RIGHT_CURLY
    """

def p_mas_statement(p):
    """
    mas_statement : statement mas_statement
    | empty
    """

def p_statement(p):
    """
    statement : assign
    | condition
    | cycle
    | f_call
    | print
    """

def p_assign(p):
    """
    assign : ID EQUAL expresion SEMI_COLON
    """

def p_expresion(p):
    """
    expresion : exp mas_expresion
    """

def p_mas_expresion(p):
    """
    mas_expresion : MORE_THAN exp
    | LESS_THAN exp
    | NOT_EQUAL exp
    | empty
    """

def p_exp(p):
    """
    exp : termino mas_exp
    """

def p_mas_exp(p):
    """
    mas_exp : ADD termino
    | SUBTRACT termino
    | empty
    """

def p_termino(p):
    """
    termino : factor mas_termino
    """

def p_mas_termino(p):
    """
    mas_termino : MULTIPLY factor
    | DIVIDE factor
    | empty
    """

def p_factor(p):
    """
    factor : mas_factor
    """

def p_mas_factor(p):
    """
    mas_factor : OPEN_PAR expresion CLOSE_PAR
    | signo ID
    | signo cte
    | ADD cte
    | SUBTRACT cte
    """

def p_signo(p):
    """
    signo : ADD
    | SUBTRACT
    | empty
    """

def p_cte(p):
    """
    cte : CTE_STRING
    | CTE_FLOAT
    | CTE_INT
    """

def p_print(p):
    """
    print : PRINT expresion mas_print SEMI_COLON
    | PRINT CTE_STRING mas_print
    """

def p_mas_print(p):
    """
    mas_print : COMMA expresion mas_print
    | CTE_STRING mas_print
    | empty
    """

def p_cycle(p):
    """
    cycle : DO body WHILE OPEN_PAR expresion CLOSE_PAR SEMI_COLON
    """

def p_condition(p):
    """
    condition : IF OPEN_PAR expresion CLOSE_PAR body mas_condition SEMI_COLON
    """

def p_mas_condition(p):
    """
    mas_condition : ELSE body
    | empty
    """

def p_f_call(p):
    """
    f_call : ID OPEN_PAR expresion mas_f_call CLOSE_PAR SEMI_COLON
    """

def p_mas_f_call(p):
    """
    mas_f_call : COMMA expresion
    | empty
    """

def p_funcs(p):
    """
    funcs : VOID ID OPEN_PAR params CLOSE_PAR L_BRACKET vars body R_BRACKET SEMI_COLON
    """

def p_params(p):
    """
    params : ID COLON type
    params : ID COLON type mas_params
    | empty
    """

def p_mas_params(p):
    """
    mas_params : COMMA params
    """

def p_empty(p):
    'empty :'
    pass

def p_error(p):
    print("Semantic error", p)

# Constuir lexer
lexer = lex.lex()

# Archivos de input
def read_tests(file):
    with open(file, 'r') as file:
        file_contents = file.read()

    return file_contents

data = read_tests('test1.in')
lexer.input(data)

# Tokenize
while True:
    tok = lexer.token()
    if not tok:
        break
    print(tok)

# Construir parser
parser = yacc.yacc(start="programa", debug=True)
result = parser.parse(data)
print(data)
print(result)