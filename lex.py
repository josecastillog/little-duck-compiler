import ply.lex as lex
import ply.yacc as yacc
from variables import VariableTable
from variables import FunctionTable
from quadruples import QuadrupleGenerator
from maquina_virtual import MaquinaVirtual

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
    # print('TOP', p[7])
    functionTable['global'].expresiones.extend(p[7])


def p_vars(p):
    """vars : VAR variables COLON type SEMI_COLON mas_var
            | empty"""

def p_variables(p):
    """variables : list_ids
    """

def p_mas_var(p):
    """mas_var : variables COLON type SEMI_COLON mas_var
       | empty"""

def p_list_ids(p):
    "list_ids : ID mas_ids"
    variableStack.append(p[1])

def p_mas_ids(p):
    """mas_ids : COMMA list_ids
       | empty"""
    
def p_type(p):
    """type : INT
       | FLOAT
    """
    global currType
    currType = p[1]
    if variableStack and currScope == 'global':
        for i in variableStack:
            functionTable[currScope].variables.add_variable(i, p[1])
        variableStack.clear()

def p_dec_v(p):
    """dec_v : vars
    """
    global currScope
    currScope = ''

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
    p[0] = p[2]

# Esta es la logica mas importante hasta ahora
def p_mas_statement(p):
    """
    mas_statement : statement mas_statement
    | empty
    """
    if len(p) > 2:
        # If mas_statement is non-empty, combine statement and mas_statement
        if type(p[1]) != list:
            p[0] = [p[1]] + p[2]
        else:
            p[0] = p[1] + p[2]
    else:
        # If mas_statement is empty, initialize p[0] to an empty list
        p[0] = []

def p_statement(p):
    """
    statement : assign
    | condition
    | cycle
    | f_call
    | print
    """
    if p[1]:
        p[0] = p[1]

def p_assign(p):
    """
    assign : ID EQUAL expresion SEMI_COLON
    """
    p[0] = f"{p[1]} {p[2]} {p[3]}"


def p_expresion(p):
    """
    expresion : exp mas_expresion
    """
    p[0] = p[1] + (p[2] if p[2] else "")

def p_mas_expresion(p):
    """
    mas_expresion : MORE_THAN exp
    | LESS_THAN exp
    | NOT_EQUAL exp
    | empty
    """
    if p[1] == '!=':
        p[0] = '%' + p[2] if len(p) > 2 else ""
    else:
        p[0] = p[1] + p[2] if len(p) > 2 else ""

def p_exp(p):
    """
    exp : termino mas_exp
    """
    p[0] = p[1] + (p[2] if p[2] else "")

def p_mas_exp(p):
    """
    mas_exp : ADD termino
    | SUBTRACT termino
    | empty
    """
    p[0] = p[1] + p[2] if len(p) > 2 else ""

def p_termino(p):
    """
    termino : factor mas_termino
    """
    p[0] = p[1] + (p[2] if p[2] else "")

def p_mas_termino(p):
    """
    mas_termino : MULTIPLY factor
    | DIVIDE factor
    | empty
    """
    p[0] = p[1] + p[2] if len(p) > 2 else ""

def p_factor(p):
    """
    factor : mas_factor
    """
    p[0] = p[1]

def p_mas_factor(p):
    """
    mas_factor : OPEN_PAR expresion CLOSE_PAR
    | signo ID
    | signo cte
    | ADD cte
    | SUBTRACT cte
    """
    if len(p) == 4:
        p[0] = f"({p[2]})"
    else:
        p[0] = p[1] + str(p[2]) if len(p) > 2 else p[1]

def p_signo(p):
    """
    signo : ADD
    | SUBTRACT
    | empty
    """
    p[0] = p[1] if p[1] else ""

def p_cte(p):
    """
    cte : CTE_STRING
    | CTE_FLOAT
    | CTE_INT
    """
    p[0] = str(p[1])

def p_print(p):
    """
    print : PRINT OPEN_PAR expresion mas_print CLOSE_PAR SEMI_COLON
    | PRINT OPEN_PAR CTE_STRING mas_print CLOSE_PAR SEMI_COLON
    """
    if p[4]:
        p[0] = ["PRINT"] + [p[3]] + ["ENDPRINT"] + p[4]
    else:
        p[0] = ["PRINT"] + [p[3]] + ["ENDPRINT"]

def p_mas_print(p):
    """
    mas_print : COMMA expresion mas_print
    | CTE_STRING mas_print
    | empty
    """
    if len(p) > 2:
        if p[3]:
            p[0] = ["PRINT"] + [p[2]] + ["ENDPRINT"] + p[3]
        else:
            p[0] = ["PRINT"] + [p[2]] + ["ENDPRINT"]
    elif len(p) < 2:
        p[0] = ["PRINT"] + [p[1]] + ["ENDPRINT"] + p[2]

def p_cycle(p):
    """
    cycle : DO body WHILE OPEN_PAR expresion CLOSE_PAR SEMI_COLON
    """
    p[0] = ["DO"] + p[2] + [p[5]] + ["WHILE"]

def p_condition(p):
    """
    condition : IF OPEN_PAR expresion CLOSE_PAR body mas_condition SEMI_COLON
    """
    if p[6]:
        p[0] = [p[3]] + ["IF"] + p[5] + ["ELSE"] + p[6] + ["ENDIF"]
    else:
        p[0] = [p[3]] + ["IF"] + p[5] + ["ENDIF"]

def p_mas_condition(p):
    """
    mas_condition : ELSE body
    | empty
    """
    if len(p) > 2:
        p[0] = p[2]

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
    currScope = p[2]
    functionTable[currScope] = FunctionTable()
    for i in variableStack:
            functionTable[currScope].variables.add_variable(i, currType)
    variableStack.clear()

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
    raise KeyError(f"Semantic error '{p}'")

# --------------------- Estructuras Auxiliares ---------------------

# variableTable = VariableTable()
variableStack = []

currScope = 'global'
currType = ''
functionTable = {}
functionTable[currScope] = FunctionTable()

quadrupleG = QuadrupleGenerator()

def printFuncVariables():
    for i, v in functionTable.items():
        print('Function name:', i)
        for n, t in v.variables.symbols.items():
            print(n, t)
        print()

# Archivos de input
def read_tests(file):
    with open(file, 'r') as file:
        file_contents = file.read()

    return file_contents

# ----------------------------- Driver -----------------------------

def run(code):


    # Constuir lexer
    lexer = lex.lex()
    lexer.input(code)

    # Tokenize
    # while True:
    #     tok = lexer.token()
    #     if not tok:
    #         break
    #     print(tok)

    # Construir parser
    parser = yacc.yacc(start="programa", debug=True)
    result = parser.parse(code, tracking=True)

    # Generar cuadruplos de main
    functionTable['global'].generate_quadruples()
    # functionTable['global'].print_cuadruplos()

    # Correr maquina virtual
    m = MaquinaVirtual(functionTable['global'].cuadruplos, functionTable['global'].variables.symbols)
    m.main()

    return m.output

if __name__ == "__main__":
    data = read_tests('test11.in')
    run(data)