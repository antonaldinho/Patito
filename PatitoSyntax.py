import sys
import ply.yacc as yacc
from PatitoLex import tokens
from DirectorioProcedimientos import DirectorioProcedimientos

actualVarType = ''
actualVarId = ''
actualFunType = ''
actualFunId = ''
procedimientos = DirectorioProcedimientos()

def p_PROGRAMA(p):
    '''programa : add_main_function PROGRAM IDENTIFIER SEMICOLON DECLARACIONES FUNCIONES PRINCIPAL'''
    p[0] = "PROGRAM COMPILED"

def p_add_main_function(p):
    '''add_main_function : '''
    global actualFunId
    actualFunId = 'main'
    global actualFunType
    actualFunType = 'void'
    global procedimientos
    procedimientos.add_function(actualFunId, actualFunType, 0, [], [], 0)

def p_DECLARACIONES(p):
    '''DECLARACIONES : VAR DECLARACIONES_1
    | empty'''

def p_DECLARACIONES_1(p):
    '''DECLARACIONES_1 : TIPO_VAR DECLARACIONES_2 SEMICOLON DECLARACIONES_ADD'''

def p_DECLARACIONES_ADD(p):
    '''DECLARACIONES_ADD : DECLARACIONES_1
    | empty'''

def p_DECLARACIONES_2(p):
    '''DECLARACIONES_2 : IDENTIFIER add_var ARRAY DECLARACIONES_3'''

# def p_ARRAYDIMENSIONS(p):
#     '''ARRAYDIMENSIONS : L_SQ_BRACKET CTE_INT R_SQ_BRACKET
#     | L_SQ_BRACKET CTE_INT R_SQ_BRACKET L_SQ_BRACKET CTE_INT R_SQ_BRACKET
#     | empty'''

def p_DECLARACIONES_3(p):
    '''DECLARACIONES_3 : COMMA DECLARACIONES_2
    | empty'''

def p_ARRAY(p):
    '''ARRAY : L_SQ_BRACKET EXPRESION R_SQ_BRACKET ARRAY_2
    | empty'''

def p_ARRAY_2(p):
    '''ARRAY_2 : L_SQ_BRACKET EXPRESION R_SQ_BRACKET
    | empty'''

def p_TIPO_VAR(p):
    '''TIPO_VAR : INT save_type
    | FLOAT save_type
    | CHAR save_type'''

def p_save_type(p):
    '''save_type : '''
    global actualVarType
    actualVarType = p[-1]

def p_FUNCIONES(p):
    '''FUNCIONES : FUNCTION TIPO_FUNC IDENTIFIER save_func L_PAREN PARAMS R_PAREN DECLARACIONES BLOQUE FUNCIONES
    | empty'''

def p_save_func(p):
    '''save_func : '''
    global actualFunId
    actualFunId = p[-1]
    global procedimientos
    procedimientos.add_function(actualFunId, actualFunType, 0, [], [], 0)

def p_PARAMS(p):
    '''PARAMS : TIPO_VAR PARAMS_2
    | empty'''

def p_PARAMS_2(p):
    '''PARAMS_2 : IDENTIFIER add_var PARAMS_3'''

def p_PARAMS_3(p):
    '''PARAMS_3 : COMMA PARAMS
    | empty'''

def p_TIPO_FUNC(p):
    '''TIPO_FUNC : INT
    | FLOAT
    | CHAR
    | VOID'''
    global actualFunType
    actualFunType = p[0]

def p_ASIGNACION(p):
    '''ASIGNACION : IDENTIFIER DIMENSIONES EQUALS EXPRESION SEMICOLON'''

def p_DIMENSIONES(p):
    '''DIMENSIONES : L_SQ_BRACKET EXPRESION R_SQ_BRACKET DIMENSIONES_2
    | empty'''

def p_DIMENSIONES_2(p):
    '''DIMENSIONES_2 : L_SQ_BRACKET EXPRESION R_SQ_BRACKET
    | empty'''

def p_EXPRESION(p):
    '''EXPRESION : T_EXP EXPRESION_AUX'''

def p_EXPRESION_AUX(p):
    '''EXPRESION_AUX : OR EXPRESION
    | empty'''

def p_T_EXP(p):
    '''T_EXP : G_EXP T_EXP_AUX'''

def p_T_EXP_AUX(p):
    '''T_EXP_AUX : AND T_EXP
    | empty'''

def p_G_EXP(p):
    '''G_EXP : M_EXP
    | M_EXP COMPARADOR M_EXP'''

def p_COMPARADOR(p):
    '''COMPARADOR : LESS_THAN
    | GREATER_THAN
    | LESS_EQUAL_THAN
    | GREATER_EQUAL_THAN
    | IS_EQUAL
    | IS_DIFFERENT'''

def p_M_EXP(p):
    '''M_EXP : T M_EXP_AUX'''

def p_M_EXP_AUX(p):
    '''M_EXP_AUX : PLUS M_EXP
    | MINUS M_EXP
    | empty'''

def p_T(p):
    '''T : F T_AUX'''

def p_T_AUX(p):
    '''T_AUX : MULTIPLICATION T
    | DIVISION T
    | empty'''

def p_F(p):
    '''F : L_PAREN EXPRESION R_PAREN
    | CTE_INT
    | CTE_FLOAT
    | CTE_CHAR
    | CTE_STRING
    | VARIABLE
    | LLAMADA
    | IDENTIFIER MATRIZ_OP'''

def p_MATRIZ_OP(p):
    '''MATRIZ_OP : TRANS
    | INV
    | DET'''

def p_VARIABLE(p):
    '''VARIABLE : IDENTIFIER DIMENSIONES'''

def p_LLAMADA(p):
    '''LLAMADA : IDENTIFIER L_PAREN LLAMADA_AUX R_PAREN SEMICOLON'''

def p_LLAMDA_AUX(p):
    '''LLAMADA_AUX : EXPRESION LLAMADA_AUX_2
    | empty'''

def p_LLAMADA_AUX_2(p):
    '''LLAMADA_AUX_2 : COMMA LLAMADA_AUX
    | empty'''

def p_MIENTRAS(p):
    '''MIENTRAS : WHILE L_PAREN EXPRESION R_PAREN DO BLOQUE'''

def p_DESDE(p):
    '''DESDE : FROM IDENTIFIER DIMENSIONES UNTIL EXPRESION DO BLOQUE'''

def p_PRINCIPAL(p):
    '''PRINCIPAL : MAIN L_PAREN R_PAREN BLOQUE'''

def p_BLOQUE(p):
    '''BLOQUE : L_BRACKET BLOQUE_AUX R_BRACKET'''

def p_BLOQUE_AUX(p):
    '''BLOQUE_AUX : ESTATUTO BLOQUE_AUX
    | empty'''

def p_CONDICION(p):
    '''CONDICION : IF L_PAREN EXPRESION R_PAREN BLOQUE CONDICION_AUX'''

def p_CONDICION_AUX(p):
    '''CONDICION_AUX : ELSE BLOQUE
    | empty'''

def p_ESTATUTO(p):
    '''ESTATUTO : ASIGNACION
    | CONDICION
    | ESCRITURA
    | LECTURA
    | LLAMADA
    | MIENTRAS
    | DESDE
    | REGRESO'''

def p_REGRESO(p):
    '''REGRESO : RETURN EXPRESION SEMICOLON'''

def p_ESCRITURA(p):
    'ESCRITURA : PRINT L_PAREN ESCRITURA_AUX R_PAREN SEMICOLON'

def p_ESCRITURA_AUX(p):
    'ESCRITURA_AUX : EXPRESION ESCRITURA_AUX_2'

def p_ESCRITURA_AUX_2(p):
    '''ESCRITURA_AUX_2 : COMMA ESCRITURA_AUX
    | empty'''

def p_LECTURA(p):
    'LECTURA : READ L_PAREN LECTURA_AUX R_PAREN SEMICOLON'

def p_LECTURA_AUX(p):
    'LECTURA_AUX : IDENTIFIER DIMENSIONES LECTURA_AUX_2'

def p_LECTURA_AUX_2(p):
    '''LECTURA_AUX_2 : COMMA LECTURA_AUX
    | empty'''

def p_empty(p):
    '''empty :'''

def p_error(token):
    if token is not None:
        print ("Line %s, illegal token %s" % (token.lineno, token.value))
        parser.errok() # Para que no se meta en un loop infinito al encontrar un error.
    else:
        print('Unexpected end of input')

def p_add_var(p):
    '''add_var : '''
    global procedimientos
    global actualVarId
    actualVarId = p[-1]
    print(actualFunId)
    if(procedimientos.search(actualFunId) == True):
        procedimientos.add_var(actualFunId, actualVarId, actualVarType)
    else:
        print("Function does not exist.")

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULTIPLICATION', 'DIVISION'),
    ('right', 'EQUALS'),
    ('left', 'AND', 'OR'),
)

parser = yacc.yacc()


if __name__ == '__main__':
	if (len(sys.argv) > 1):
		file = sys.argv[1]
		try:
			f = open(file,'r')
			data = f.read()
			f.close()
			if (yacc.parse(data, tracking=True) == 'PROGRAM COMPILED'):
				print ("Finished compiling")

		except EOFError:
	   		print(EOFError)
	else:
		print('File missing')