import sys
import ply.yacc as yacc
from PatitoLex import tokens
from DirectorioProcedimientos import DirectorioProcedimientos
import queue as Queue
from cuboSemantico import cuboSemantico
from Avail import Avail

actualVarType = ''
actualVarId = ''
actualFunType = ''
actualFunId = ''
procedures = DirectorioProcedimientos()
pOperandos = []
pTipos = []
pOperadores = []
cuadruplos = Queue.Queue()
cubo = cuboSemantico()
avail = Avail()

def p_PROGRAMA(p):
    '''programa : add_global_function PROGRAM IDENTIFIER SEMICOLON DECLARACIONES FUNCIONES add_main_function PRINCIPAL'''
    p[0] = "PROGRAM COMPILED"

def p_add_global_function(p):
    '''add_global_function : '''
    global actualFunId
    actualFunId = 'global'
    global actualFunType
    actualFunType = 'void'
    global procedures
    procedures.add_function(actualFunId, actualFunType, 0, [], [], 0)

def p_add_main_function(p):
    '''add_main_function : '''
    global actualFunId
    actualFunId = 'main'
    global actualFunType
    actualFunType = 'void'
    global procedures
    procedures.add_function(actualFunId, actualFunType, 0, [], [], 0)

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
    global procedures
    procedures.add_function(actualFunId, actualFunType, 0, [], [], 0)

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
    '''M_EXP : T generate_sum_quad M_EXP_AUX'''

def p_generate_sum_quad(p):
    '''generate_sum_quad : '''
    global pOperadores
    if(len(pOperadores) > 0):
        global pOperandos
        if(pOperadores[-1] == '+' or pOperadores[-1] == '-'):
            op = pOperadores.pop()
            operando_derecho = pOperandos.pop()
            operando_derecho_type = pTipos.pop()
            operando_izquierdo = pOperandos.pop()
            operando_izquierdo_type = pTipos.pop()
            result_type = cubo.get_tipo(operando_izquierdo_type, operando_derecho_type, op)
            if(result_type != 'error'):
                result = avail.next()
                quad = (op, operando_izquierdo, operando_derecho, result)
                print('cuadruplo: ' + str(quad))
                cuadruplos.put(quad)
                pOperandos.append(result)
                pTipos.append(result_type)
            else:
                print("type mismatch")
                sys.exit()

def p_M_EXP_AUX(p):
    '''M_EXP_AUX : PLUS add_plus_minus_operator M_EXP
    | MINUS add_plus_minus_operator M_EXP
    | empty'''

def p_add_plus_minus_operator(p):
    '''add_plus_minus_operator : '''
    global pOperadores
    pOperadores.append(p[-1])
    print('added operador: ' + str(p[-1]))

def p_T(p):
    '''T : F generate_mult_quad T_AUX'''

def p_generate_mult_quad(p):
    '''generate_mult_quad : '''
    global pOperadores
    if(len(pOperadores) > 0):
        global pOperandos
        if(pOperadores[-1] == '*' or pOperadores[-1] == '/'):
            op = pOperadores.pop()
            operando_derecho = pOperandos.pop()
            operando_derecho_type = pTipos.pop()
            operando_izquierdo = pOperandos.pop()
            operando_izquierdo_type = pTipos.pop()
            result_type = cubo.get_tipo(operando_izquierdo_type, operando_derecho_type, op)
            if(result_type != 'error'):
                result = avail.next()
                quad = (op, operando_izquierdo, operando_derecho, result)
                print('cuadruplo: ' + str(quad))
                cuadruplos.put(quad)
                pOperandos.append(result)
                pTipos.append(result_type)
            else:
                print("type mismatch")
                sys.exit()



def p_T_AUX(p):
    '''T_AUX : MULTIPLICATION add_mult_div_operator T
    | DIVISION add_mult_div_operator T
    | empty'''

def p_add_mult_div_operator(p):
    '''add_mult_div_operator : '''
    global pOperadores
    pOperadores.append(p[-1])
    print('added operador: ' + str(p[-1]))


def p_F(p):
    '''F : L_PAREN l_paren_expression EXPRESION R_PAREN r_paren_expression
    | CTE_INT add_operando_cte
    | CTE_FLOAT add_operando_cte
    | CTE_CHAR add_operando_char
    | CTE_STRING add_operando_cte
    | VARIABLE
    | LLAMADA
    | IDENTIFIER MATRIZ_OP'''

def p_l_paren_expression(p):
    '''l_paren_expression : '''
    print ("left paren")

def p_r_paren_expression(p):
    '''r_paren_expression : '''
    print ("right paren")

def p_add_operando_cte(p):
    '''add_operando_cte : '''
    global pOperandos
    global pOperadores
    tipo = type(p[-1])
    pOperandos.append(p[-1])
    if tipo == int:
        pTipos.append('int')
    elif tipo == float:
        pTipos.append('float')
    print('added operando: ' + str(p[-1]))

def p_add_operando_char(p):
    '''add_operando_char : '''
    global pOperandos
    global pOperadores
    pOperandos.append(p[-1])
    pTipos.append('char')

def p_MATRIZ_OP(p):
    '''MATRIZ_OP : TRANS
    | INV
    | DET'''

def p_VARIABLE(p):
    '''VARIABLE : IDENTIFIER add_operando_var DIMENSIONES'''

def p_add_operando_var(p):
    '''add_operando_var : '''
    global pOperandos
    global pOperadores
    global actualFunId
    var_id = p[-1]
    tipo = procedures.get_var_type(var_id, actualFunId)
    if tipo != False:
        if tipo == 'int':
            pTipos.append('int')
        elif tipo == 'float':
            pTipos.append('float')
    else:
        sys.exit()
    pOperandos.append(var_id)
    
    print('added operando: ' + str(p[-1]))

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
    global procedures
    global actualVarId
    actualVarId = p[-1]
    #print(actualFunId)
    if(procedures.search(actualFunId) == True):
        procedures.add_var(actualFunId, actualVarId, actualVarType)
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