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
pSaltos = []
cuadruplos = []
cubo = cuboSemantico()
avail = Avail()
temporales = {}
kParams = 1

#direcciones de memoria virtual para variables
virtualMemoryDirs = {
    'globalint': 1000,
    'globalfloat': 3000,
    'globalchar': 5000,
    'localint': 7000,
    'localfloat': 9000,
    'localchar': 11000,
    'tempint': 13000,
    'tempfloat': 15000,
    'tempchar': 17000,
    'tempbool': 19000,
    'constint': 21000,
    'constfloat': 23000,
    'constchar': 25000,
}

isGlobal = True

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
    procedures.add_function(actualFunId, actualFunType, 0, [], [], 0, None)

def p_add_main_function(p):
    '''add_main_function : '''
    global actualFunId
    actualFunId = 'main'
    global actualFunType
    actualFunType = 'void'
    global procedures
    procedures.add_function(actualFunId, actualFunType, 0, [], [], 0, None)

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
    '''FUNCIONES : FUNCTION TIPO_FUNC IDENTIFIER save_func L_PAREN is_local PARAMS R_PAREN DECLARACIONES add_quad_counter BLOQUE release_func FUNCIONES
    | empty'''

def p_is_local(p):
    '''is_local : '''
    global isGlobal
    isGlobal = False

def p_save_func(p):
    '''save_func : '''
    global actualFunId
    actualFunId = p[-1]
    global procedures
    procedures.add_function(actualFunId, actualFunType, 0, [], [], 0, None)

def p_add_quad_counter(p):
    '''add_quad_counter : '''
    procedures.add_quad_counter(actualFunId, len(cuadruplos))

def p_release_func(p):
    '''release_func : '''
    # Release the current VarTable (local).
    create_new_avail()
    virtualMemoryDirs['localint'] = 7000
    virtualMemoryDirs['localfloat'] = 9000
    virtualMemoryDirs['localchar'] = 11000
    virtualMemoryDirs['tempint'] = 13000
    virtualMemoryDirs['tempfloat'] = 15000
    virtualMemoryDirs['tempchar'] = 17000
    virtualMemoryDirs['tempbool'] = 19000
    procedures.delete_var_table(actualFunId)
    # Generate an action to end the function (ENDFunc).
    quad = ('ENDPROC', -1, -1, -1)
    cuadruplos.append(quad)
    # Insert into DirFunc the number of temporal vars used.

def p_PARAMS(p):
    '''PARAMS : TIPO_VAR PARAMS_2
    | empty'''

def p_PARAMS_2(p):
    '''PARAMS_2 : IDENTIFIER add_var add_param PARAMS_3'''

def p_add_param(p):
    '''add_param : '''
    # For parametric signature
    procedures.add_param(actualFunId, actualVarId, actualVarType)

def p_PARAMS_3(p):
    '''PARAMS_3 : COMMA PARAMS
    | empty'''

def p_TIPO_FUNC(p):
    '''TIPO_FUNC : INT
    | FLOAT
    | CHAR
    | VOID'''
    global actualFunType
    actualFunType = p[1]

def p_ASIGNACION(p):
    '''ASIGNACION : IDENTIFIER add_id DIMENSIONES EQUALS add_equal_operator EXPRESION generate_equal_quad SEMICOLON'''

def p_add_equal_operator(p):
    '''add_equal_operator : '''
    global pOperadores
    pOperadores.append(p[-1])
    # print('added operator: ' + str(p[-1]))

def p_generate_equal_quad(p):
    '''generate_equal_quad : '''
    global pOperadores, pOperandos, pTipos, cuadruplos
    if(len(pOperadores) > 0):
        if(pOperadores[-1] == '='):
            op = pOperadores.pop()
            operando_derecho = pOperandos.pop()
            operando_derecho_type = pTipos.pop()
            operando_izquierdo = pOperandos.pop()
            operando_izquierdo_type = pTipos.pop()
            result_type = cubo.get_tipo(operando_izquierdo_type, operando_derecho_type, op)
            if result_type != 'error':
                quad = (op, operando_izquierdo, None, operando_derecho)
                #print('cuadruplo: ' + str(quad))
                cuadruplos.append(quad)
                #create_new_avail()
            else:
                print("Type missmatch")
                sys.exit()

def p_DIMENSIONES(p):
    '''DIMENSIONES : L_SQ_BRACKET EXPRESION R_SQ_BRACKET DIMENSIONES_2
    | empty'''

def p_DIMENSIONES_2(p):
    '''DIMENSIONES_2 : L_SQ_BRACKET EXPRESION R_SQ_BRACKET
    | empty'''

def p_EXPRESION(p):
    '''EXPRESION : T_EXP generate_or_quad EXPRESION_AUX'''

def p_generate_or_quad(p):
    '''generate_or_quad : '''
    global pOperadores
    if(len(pOperadores) > 0):
        if(pOperadores[-1] == '||'):
            quad_generator_4args()

def p_EXPRESION_AUX(p):
    '''EXPRESION_AUX : OR add_or_operator EXPRESION
    | empty'''

def p_add_or_operator(p):
	'''add_or_operator : '''
	global pOperadores
	pOperadores.append(p[-1])
	# print('added operador: ' + str(p[-1]))

def p_T_EXP(p):
    '''T_EXP : G_EXP generate_and_quad T_EXP_AUX'''

def p_generate_and_quad(p):
    '''generate_and_quad : '''
    global pOperadores
    if(len(pOperadores) > 0):
        if(pOperadores[-1] == '&&'):
            quad_generator_4args()

def p_T_EXP_AUX(p):
    '''T_EXP_AUX : AND add_and_operator T_EXP
    | empty'''

def p_add_and_operator(p):
    '''add_and_operator : '''
    global pOperadores
    pOperadores.append(p[-1])
    # print('added operator: ' + str(p[-1]))

def p_G_EXP(p):
    '''G_EXP : M_EXP generate_comparator_quad
    | M_EXP COMPARADOR M_EXP generate_comparator_quad'''

def p_generate_comparator_quad(p):
    '''generate_comparator_quad : '''
    global pOperadores
    if(len(pOperadores) > 0):
        if(pOperadores[-1] == '<' or pOperadores[-1] == '>' 
        or pOperadores[-1] == '<=' or pOperadores[-1] == '>='
        or pOperadores[-1] == '==' or pOperadores[-1] == '!='):
            quad_generator_4args()

def p_COMPARADOR(p):
    '''COMPARADOR : LESS_THAN add_comparator
    | GREATER_THAN add_comparator
    | LESS_EQUAL_THAN add_comparator
    | GREATER_EQUAL_THAN add_comparator
    | IS_EQUAL add_comparator
    | IS_DIFFERENT add_comparator'''

def p_add_comparator(p):
    '''add_comparator : '''
    global pOperadores
    pOperadores.append(p[-1])
    # print('added operador: ' + str(p[-1]))

def p_M_EXP(p):
    '''M_EXP : T generate_sum_quad M_EXP_AUX'''

def p_generate_sum_quad(p):
    '''generate_sum_quad : '''
    global pOperadores
    if(len(pOperadores) > 0):
        if(pOperadores[-1] == '+' or pOperadores[-1] == '-'):
            quad_generator_4args()

def p_M_EXP_AUX(p):
    '''M_EXP_AUX : PLUS add_plus_minus_operator M_EXP
    | MINUS add_plus_minus_operator M_EXP
    | empty'''

def p_add_plus_minus_operator(p):
    '''add_plus_minus_operator : '''
    global pOperadores
    pOperadores.append(p[-1])
    # print('added operador: ' + str(p[-1]))

def p_T(p):
    '''T : F generate_mult_quad T_AUX'''

def p_generate_mult_quad(p):
    '''generate_mult_quad : '''
    global pOperadores
    if(len(pOperadores) > 0):
        if(pOperadores[-1] == '*' or pOperadores[-1] == '/'):
            quad_generator_4args()

def p_T_AUX(p):
    '''T_AUX : MULTIPLICATION add_mult_div_operator T
    | DIVISION add_mult_div_operator T
    | empty'''

def p_add_mult_div_operator(p):
    '''add_mult_div_operator : '''
    global pOperadores
    pOperadores.append(p[-1])
    # print('added operador: ' + str(p[-1]))


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

def p_r_paren_expression(p):
    '''r_paren_expression : '''

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
    elif tipo == str:
        pTipos.append('string')
    # print('added operando: ' + str(p[-1]))

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
    varId = p[-1]
    if(procedures.search_var(actualFunId, varId)):
        tipo = procedures.get_var_type(actualFunId, varId)
        if tipo == 'int':
            pTipos.append('int')
        elif tipo == 'float':
            pTipos.append('float')
        elif tipo == 'char':
            pTipos.append('char')
        pOperandos.append(procedures.get_var_memory_loc(actualFunId, varId))
    
    # print('added operando: ' + str(p[-1]))

def p_LLAMADA(p):
    '''LLAMADA : IDENTIFIER search_func L_PAREN generate_era_quad LLAMADA_AUX verify_params R_PAREN SEMICOLON generate_gosub_quad'''

# Verify that function called already exits
def p_search_func(p):
    '''search_func : '''
    global actualVarId, actualVarType
    actualVarId = p[-1]
    if(not procedures.search(actualVarId)):
        print("Procedure '", actualVarId, "' not found")
        sys.exit()
    actualVarType = procedures.get_function_type(actualVarId)

# Generate ERA quad 
def p_generate_era_quad(p):
    '''generate_era_quad : '''
    global kParams, actualVarId
    quad = ('ERA', None, None, actualVarId)
    cuadruplos.append(quad)
    kParams = 1

# Verify kParams matches the actual # of parameters defined 
def p_verify_params(p):
    '''verify_params : '''
    global kParams, actualVarId
    if (kParams != procedures.get_numParams(actualVarId)):
        print("Error in parameters, function calling:", actualVarId)
        sys.exit()

# Generate GOSUB quad
def p_generate_gosub_quad(p):
    '''generate_gosub_quad : '''
    global actualVarId
    quad = ('GOSUB', actualVarId, None, procedures.get_quad_num(actualVarId))
    cuadruplos.append(quad)

def p_LLAMDA_AUX(p):
    '''LLAMADA_AUX : EXPRESION generate_quad_parameter LLAMADA_AUX_2
    | empty set_k_cero'''

# Expression receives 0 arguments
def p_set_k_cero(p):
    '''set_k_cero : '''
    global kParams
    kParams = 0

# Generate quad for parameters
def p_add_paramater(p):
    '''generate_quad_parameter : '''
    global pOperandos, pTipos, kParams
    currentArg = pOperandos.pop()
    currentArgType = pTipos.pop()
    # Verify if kParams hasn't passed the number of parameters defined
    if (kParams <= procedures.get_numParams(actualVarId)):
        argumentType = procedures.get_parameter_type(actualVarId, kParams-1)
        if (currentArgType != argumentType):
            print("Parameter type mismatch, calling function:", actualVarId)
            sys.exit()
        quad = ('PARAMETER', currentArg, None, kParams)
        cuadruplos.append(quad)
    else:
        print("Error in parameters, calling function:", actualVarId)
        sys.exit()

def p_LLAMADA_AUX_2(p):
    '''LLAMADA_AUX_2 : sum_kParams COMMA LLAMADA_AUX
    | empty'''

# kParams + 1 when receives more parameters
def p_add_kParams(p):
    '''sum_kParams : '''
    global kParams
    kParams = kParams + 1

def p_MIENTRAS(p):
    '''MIENTRAS : WHILE add_while_from_cond L_PAREN EXPRESION add_while_exp R_PAREN DO BLOQUE add_end_while_from'''

def p_add_while_from_cond(p):
    '''add_while_from_cond : '''
    pSaltos.append(len(cuadruplos))

def p_add_while_exp(p):
    '''add_while_exp : '''
    add_if_while_from('GOTOF')

def p_add_end_while_from(p):
    '''add_end_while_from : '''
    global pSaltos, cuadruplos
    end = pSaltos.pop()
    jump = pSaltos.pop()
    quad = ('GOTO', None, None, jump)
    cuadruplos.append(quad)
    fill_quad(end)

def p_DESDE(p):
    '''DESDE : FROM L_PAREN ASIGNACION_DESDE R_PAREN UNTIL add_while_from_cond L_PAREN EXPRESION add_from_exp R_PAREN DO BLOQUE add_end_while_from'''

def p_add_from_exp(p):
    '''add_from_exp : '''
    add_if_while_from('GOTOV')

def p_ASIGNACION_DESDE(p):
    '''ASIGNACION_DESDE : IDENTIFIER add_id DIMENSIONES EQUALS add_equal_operator EXPRESION generate_equal_quad'''

def p_PRINCIPAL(p):
    '''PRINCIPAL : MAIN L_PAREN R_PAREN BLOQUE'''

def p_BLOQUE(p):
    '''BLOQUE : L_BRACKET BLOQUE_AUX R_BRACKET'''

def p_BLOQUE_AUX(p):
    '''BLOQUE_AUX : ESTATUTO BLOQUE_AUX
    | empty'''

def p_CONDICION(p):
    '''CONDICION : IF L_PAREN EXPRESION R_PAREN add_if BLOQUE CONDICION_AUX add_end_if'''

def p_add_if(p):
    '''add_if : '''
    add_if_while_from('GOTOF')

def p_add_end_if(p):
    '''add_end_if : '''
    global pSaltos, cuadruplos
    end = pSaltos.pop()
    fill_quad(end)

def p_CONDICION_AUX(p):
    '''CONDICION_AUX : ELSE add_else BLOQUE
    | empty'''

def p_add_else(p):
    '''add_else : '''
    global pSaltos, cuadruplos
    quad = ('GOTO', None, None, -1)
    cuadruplos.append(quad)
    jump = pSaltos.pop()
    pSaltos.append(len(cuadruplos)-1)
    fill_quad(jump)

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
    '''REGRESO : RETURN add_return_op EXPRESION add_return_quad SEMICOLON'''

def p_add_return_op(p):
    '''add_return_op : '''
    global pOperadores
    pOperadores.append('RETURN')

def p_add_return_quad(p):
    '''add_return_quad : '''
    global pOperadores, pOperandos, pTipos, cuadruplos, actualFunId
    if(len(pOperadores) > 0):
        if(pOperadores[-1] == 'RETURN'):
            op = pOperadores.pop()
            resultado = pOperandos.pop()
            resultado_type = pTipos.pop()
            if resultado_type == actualFunType:
                quad = (op, -1, -1, resultado)
                cuadruplos.append(quad)
            else:
                print("Type missmatch")
                sys.exit()

def p_ESCRITURA(p):
    'ESCRITURA : PRINT L_PAREN ESCRITURA_AUX R_PAREN SEMICOLON'

def p_ESCRITURA_AUX(p):
    'ESCRITURA_AUX : add_print_operator EXPRESION generate_print_quad ESCRITURA_AUX_2'

def p_add_print_operator(p):
	'''add_print_operator : '''
	global pOperadores
	if(p[-1] == ','):
		pOperadores.append('print')
	else:
		pOperadores.append(p[-2])
	# print('added operator: ' + pOperadores[-1])

def p_generate_print_quad(p):
	'''generate_print_quad : '''
	global pOperadores
	if(len(pOperadores) > 0):
		if(pOperadores[-1] == 'print'):
			quad_generator_2args()

def p_ESCRITURA_AUX_2(p):
    '''ESCRITURA_AUX_2 : COMMA ESCRITURA_AUX
    | empty'''

def p_LECTURA(p):
    'LECTURA : READ L_PAREN LECTURA_AUX R_PAREN SEMICOLON'

def p_LECTURA_AUX(p):
    'LECTURA_AUX : add_read_operator IDENTIFIER add_id DIMENSIONES generate_read_quad LECTURA_AUX_2'

def p_add_id(p):
    '''add_id : '''
    global actualVarId, procedures
    actualVarId = p[-1]
    if procedures.search_var(actualFunId, actualVarId):
        pOperandos.append(procedures.get_var_memory_loc(actualFunId, actualVarId))
        pTipos.append(procedures.get_var_type(actualFunId, actualVarId))
        # print("added operando: " + str(p[-1]))
    else:
        sys.exit()

def p_add_read_operator(p):
	'''add_read_operator : '''
	global pOperadores
	if(p[-1] == ','):
		pOperadores.append('read')
	else:
		pOperadores.append(p[-2])
	# print('added operator: ' + pOperadores[-1])
	
def p_generate_read_quad(p):
	'''generate_read_quad : '''
	global pOperadores, pOperandos
	if(len(pOperadores) > 0):
		if(pOperadores[-1] == 'read'):
			quad_generator_2args()

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
    global virtualMemoryDirs
    actualVarId = p[-1]
    #print(actualFunId)
    # print(virtualMemoryDirs['globalint'])
    if(procedures.search(actualFunId) == True):
        memoryType = ''
        if isGlobal:
            memoryType = 'global' + actualVarType
        else:
            memoryType = 'local' + actualVarType
        procedures.add_var(actualFunId, actualVarId, actualVarType, virtualMemoryDirs[memoryType])
        virtualMemoryDirs[memoryType] = virtualMemoryDirs[memoryType] + 1
    else:
        print("Function does not exist.")
        sys.exit()

def quad_generator_4args():
    global pOperadores, pOperandos, pTipos, cuadruplos
    op = pOperadores.pop()
    operando_derecho = pOperandos.pop()
    operando_derecho_type = pTipos.pop()
    operando_izquierdo = pOperandos.pop()
    operando_izquierdo_type = pTipos.pop()
    result_type = cubo.get_tipo(operando_izquierdo_type, operando_derecho_type, op)
    if(result_type != 'error'):
        result = avail.next()
        if result_type == 'int':
            temporales[result] = virtualMemoryDirs['tempint']
            virtualMemoryDirs['tempint'] = virtualMemoryDirs['tempint'] + 1
        elif result_type == 'float':
            temporales[result] = virtualMemoryDirs['tempfloat']
            virtualMemoryDirs['tempfloat'] = virtualMemoryDirs['tempfloat'] + 1
        elif result_type == 'char':
            temporales[result] = virtualMemoryDirs['tempfloat']
            virtualMemoryDirs['tempchar'] = virtualMemoryDirs['tempchar'] + 1
        elif result_type == 'bool':
            temporales[result] = virtualMemoryDirs['tempbool']
            virtualMemoryDirs['tempbool'] = virtualMemoryDirs['tempbool'] + 1
        quad = (op, operando_izquierdo, operando_derecho, temporales[result])
        #print('cuadruplo: ' + str(quad))
        cuadruplos.append(quad)
        pOperandos.append(temporales[result])
        pTipos.append(result_type)
    else:
        print("type mismatch")
        sys.exit()
	
def quad_generator_2args():
    global pOperadores, pOperandos, pTipos, cuadruplos
    op = pOperadores.pop()
    operando = pOperandos.pop()
    operando_type = pTipos.pop()
    quad = (op, None, None, operando)
    #print('cuadruplo: ' + str(quad))
    cuadruplos.append(quad)
    pOperandos.append(operando)
    pTipos.append(operando_type)
    #create_new_avail()

def add_if_while_from(goto):
    global pTipos, pSaltos, cuadruplos
    exp_type = pTipos.pop()
    if exp_type == 'bool':
        result = pOperandos.pop()
        quad = (goto, result, None, -1)
        cuadruplos.append(quad)
        pSaltos.append(len(cuadruplos)-1)
        #print('cuadruplo: ' + str(quad))
    else: 
        print("type mismatch")
        sys.exit()
    
def fill_quad(i):
    global cuadruplos
    temp = list(cuadruplos[i])
    temp[3] = len(cuadruplos)
    cuadruplos[i] = tuple(temp)
    #print('cuadruplo: ' + str(cuadruplos[i]))

def printCuadruplos():
    for (i, elem) in enumerate(cuadruplos):
        print(i, elem)
    #procedures.print_proc() 

# Function for resetting the avail
def create_new_avail():
    global avail
    avail = Avail()

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
				printCuadruplos()

		except EOFError:
	   		print(EOFError)
	else:
		print('File missing')