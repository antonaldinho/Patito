import sys
import ply.yacc as yacc
from PatitoLex import tokens
from DirectorioProcedimientos import DirectorioProcedimientos
import queue as Queue
from cuboSemantico import cuboSemantico
from Avail import Avail

program_name = ''
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
cuadruplosIds = []
cubo = cuboSemantico()
avail = Avail()
temporales = {} # esto se puede implementar sin necesidad de usar esta variable.
constantes = {}
kParams = 1
tmpCounter = 0
dim = 0
pilaDim = []
node = None
numDims = 0
pilaNodos = []

theVar = [] #variable para trackear la variable que se esta llamando

actualCall = ''
actualCallType = ''

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
    'conststring': 27000,
    'temppointer': 29000
}

# Operation codes
operations = {
    '+': 1,
    '-': 2,
    '*': 3,
    '/': 4,
    '=': 5,
    '<': 6,
    '>': 7,
    '<=': 8,
    '>=': 9,
    '==': 10,
    '&&': 11,
    '||': 12,
    'print': 13,
    'goto': 14,
    'gotof': 15,
    'gosub': 16,
    'endproc': 17,
    'return': 18
}

isGlobal = True

def p_PROGRAMA(p):
    '''programa : add_global_function PROGRAM IDENTIFIER program_name SEMICOLON generate_gomain_quad make_actual_global DECLARACIONES FUNCIONES add_main_function add_main_counter PRINCIPAL'''
    p[0] = "PROGRAM COMPILED"

def p_program_name(p):
    '''program_name : '''
    global program_name
    program_name = p[-1]

def p_make_actual_global(p):
    '''make_actual_global : '''
    global actualFunId, actualFunType
    actualFunId = 'global'
    actualFunType = 'void'

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
    actualFunId = 'global'
    global actualFunType
    actualFunType = 'void'
    # global procedures
    # procedures.add_function(actualFunId, actualFunType, 0, [], [], 0, None)

def p_generate_gomain_quad(p):
    '''generate_gomain_quad : '''
    quad = ('GOMAIN', 'main', -1, None)
    cuadruplos.append(quad)
    cuadruplosIds.append(quad)

def p_add_main_counter(p):
    '''add_main_counter : '''
    procedures.add_quad_counter('global' if actualFunId == 'main' else actualFunId, len(cuadruplos))
    temp = list(cuadruplos[0])
    temp[3] = procedures.get_quad_num('global' if actualFunId == 'main' else actualFunId)
    cuadruplos[0] = tuple(temp)

    temp = list(cuadruplosIds[0])
    temp[3] = procedures.get_quad_num('global' if actualFunId == 'main' else actualFunId)
    cuadruplosIds[0] = tuple(temp)
    

def p_DECLARACIONES(p):
    '''DECLARACIONES : VAR DECLARACIONES_1
    | empty'''
    # procedures.list_vars(actualFunId)

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
    '''ARRAY : L_SQ_BRACKET make_dimentioned CTE_INT add_lsup set_r1 R_SQ_BRACKET ARRAY_2 set_all_nodes
    | empty'''

def p_ARRAY_2(p):
    '''ARRAY_2 : L_SQ_BRACKET add_dimention CTE_INT add_lsup set_r1 R_SQ_BRACKET
    | empty'''

def p_make_dimentioned(p):
    '''make_dimentioned : '''
    procedures.make_var_array(actualFunId, actualVarId)

def p_add_lsup(p):
    '''add_lsup : '''
    procedures.add_lsup(actualFunId, actualVarId, p[-1])
    
def p_set_r1(p):
    '''set_r1 : '''
    procedures.set_r(actualFunId, actualVarId, 1)

def p_add_dimention(p):
    '''add_dimention : '''
    procedures.add_dimention(actualFunId, actualVarId)

def p_set_all_nodes(p):
    '''set_all_nodes : '''
    procedures.set_all_nodes(actualFunId, actualVarId)

    # Set the next dir if actual var is dimentioned
    memoryType = ''
    if isGlobal:
        memoryType = 'global' + actualVarType
    else:
        memoryType = 'local' + actualVarType
    virtualMemoryDirs[memoryType] = virtualMemoryDirs[memoryType] + procedures.get_array_size(actualFunId, actualVarId) - 1

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
    # Saving a global variable with the same name as the function to store all the returns for the function
    if(actualFunType != 'void'):
        if(procedures.search(actualFunId) == True):
            memoryType = 'global' + actualFunType
            procedures.add_var('global', actualFunId, actualFunType, virtualMemoryDirs[memoryType])
            virtualMemoryDirs[memoryType] = virtualMemoryDirs[memoryType] + 1
        else:
            print("Function does not exist.")
            sys.exit()

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
    global procedures
    global tmpCounter
    # print('num tmp vars: ' + str(tmpCounter) + ' in ' + str(actualFunId))
    
    procedures.add_num_tmp(actualFunId, tmpCounter)
    tmpCounter = 0
    procedures.set_type_spaces(actualFunId)
    procedures.delete_var_table(actualFunId)
    # Generate an action to end the function (ENDFunc)
    quad = ('ENDPROC', -1, -1, -1)
    
    cuadruplos.append(quad)
    cuadruplosIds.append(quad)
    # print("cuadruplo: " + str(quad))
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
                quad = (op, operando_izquierdo['mem'], -1, operando_derecho['mem'])
                quad2 = (op, operando_izquierdo['id'], -1, operando_derecho['id'])
                # print('cuadruplo: ' + str(quad))
                cuadruplos.append(quad)
                cuadruplosIds.append(quad2)
                #create_new_avail()
            else:
                print("Type missmatch")
                sys.exit()

def p_DIMENSIONES(p):
    '''DIMENSIONES : L_SQ_BRACKET ver_dimentions EXPRESION create_dim_quad R_SQ_BRACKET DIMENSIONES_2 create_final_dim_quads
    | empty'''

def p_DIMENSIONES_2(p):
    '''DIMENSIONES_2 : L_SQ_BRACKET next_dim EXPRESION create_dim_quad R_SQ_BRACKET
    | empty'''

def p_ver_dimentions(p):
    '''ver_dimentions : '''
    operando = pOperandos.pop()
    tipo = pTipos.pop()
    global dim, pilaDim, numDims, node, pilaNodos, pOperadores
    if procedures.is_dimentioned(actualFunId, operando['id']):
        dim = 1
        pilaDim.append((operando, dim))
        node = procedures.get_node(actualFunId, operando['id'], 1)
        pOperadores.append('(') #fondo falso
        pilaNodos.append(node)
    else:
        print("Error: la variable '" + operando['id'] + "' no es dimensionada")
        sys.exit()

        
def p_create_dim_quad(p):
    '''create_dim_quad : '''
    global pOperandos, tmpCounter, procedures
    quad = ('ver', pOperandos[-1]['id'], 0, pilaNodos[-1]['lsup'])
    cuadruplosIds.append(quad)
    quad = ('ver', pOperandos[-1]['mem'], 0, pilaNodos[-1]['lsup'])
    cuadruplos.append(quad)

    if(pilaNodos[-1]['next']):
        aux = pOperandos.pop()
        result = avail.next()
        tmpCounter += 1
        procedures.add_tmp(actualFunId, 'int')
        m = pilaNodos[-1]['m']
        temporales[result] = virtualMemoryDirs['tempint']
        if(str(m) not in constantes.keys()):
            constantes[str(m)] = virtualMemoryDirs['constint']
            virtualMemoryDirs['constint'] += 1
        quad = ('*', aux['id'], m, result)
        cuadruplosIds.append(quad)
        quad = ('*', aux['mem'], constantes[str(m)], temporales[result])
        cuadruplos.append(quad)
        obj = {
            'id': result,
            'mem': temporales[result]
        }
        pOperandos.append(obj)
    if(pilaDim[-1][1] > 1):
        aux2 = pOperandos.pop()
        aux1 = pOperandos.pop()
        result = avail.next()
        tmpCounter += 1
        procedures.add_tmp(actualFunId, 'int')
        temporales[result] = virtualMemoryDirs['tempint']
        virtualMemoryDirs['tempint'] += 1
        quad = ('+', aux1['id'], aux2['id'], result)
        cuadruplosIds.append(quad)
        quad = ('+', aux1['mem'], aux2['mem'], temporales[result])
        cuadruplos.append(quad)
        obj = {
            'id': result,
            'mem': temporales[result]
        }
        pOperandos.append(obj)

def p_next_dim(p):
    '''next_dim : '''
    global node, pilaNodos, pilaDim
    (operando, dim) = pilaDim.pop()
    dim += 1
    pilaDim.append((operando, dim))
    # Get the next node
    pilaNodos.pop()
    node = procedures.get_node(actualFunId, operando['id'], dim)
    pilaNodos.append(node)

def p_create_final_dim_quads(p):
    '''create_final_dim_quads : '''
    aux1 = pOperandos.pop()
    # aux1Type = pTipos.pop()
    result = avail.next()
    global tmpCounter
    tmpCounter += 1
    procedures.add_tmp(actualFunId, 'pointer')
    # print('vartype', actualVarType)
    # print('varid', actualVarId)
    var = pilaDim[-1][0]['id']
    temporales[result] = virtualMemoryDirs['temppointer']
    virtualMemoryDirs['temppointer'] = virtualMemoryDirs['temppointer'] + 1
    quad1 = ('sumaDir', aux1['id'], var, result)
    quad2 = ('sumaDir', aux1['mem'], procedures.get_var_memory_loc(actualFunId, var), temporales[result])
    cuadruplosIds.append(quad1)
    cuadruplos.append(quad2)
    obj = {
        'id': result,
        'mem': temporales[result]
    }
    pOperandos.append(obj)
    pOperadores.pop()
    pilaDim.pop()
    pilaNodos.pop()

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
    pOperadores.append(p[-1])

def p_r_paren_expression(p):
    '''r_paren_expression : '''
    pOperadores.pop()

def p_add_operando_cte(p):
    '''add_operando_cte : '''
    global pOperandos
    global pOperadores
    tipo = type(p[-1])
    # The constants are inserted into the const table
    if tipo == int:
        pTipos.append('int')

        if str(p[-1]) not in constantes:
            constantes[str(p[-1])] = virtualMemoryDirs['constint']
            virtualMemoryDirs['constint'] += 1
        obj = {
            'id': str(p[-1]),
            'mem': constantes[str(p[-1])]
        }
        pOperandos.append(obj)
    elif tipo == float:
        pTipos.append('float')
        if str(p[-1]) not in constantes:
            constantes[str(p[-1])] = virtualMemoryDirs['constfloat']
            virtualMemoryDirs['constfloat'] += 1
        obj = {
            'id': str(p[-1]),
            'mem': constantes[str(p[-1])]
        }
        pOperandos.append(obj)
    elif tipo == str:
        pTipos.append('string')
        string = p[-1].replace('"', '')
        if string not in constantes:
            constantes[string] = virtualMemoryDirs['conststring']
            virtualMemoryDirs['conststring'] += 1
        obj = {
            'id': string,
            'mem': constantes[string]
        }
        pOperandos.append(obj)
    # print('added operando: ' + str(p[-1]))

def p_add_operando_char(p):
    '''add_operando_char : '''
    global pOperandos
    global pOperadores
    pTipos.append('char')
    if p[-1] not in constantes:
        constantes[p[-1]] = virtualMemoryDirs['constchar']
        virtualMemoryDirs['constchar'] += 1
    obj = {            
        'id': p[-1],
        'mem': constantes[p[-1]]
    }
    pOperandos.append(obj)

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
    global actualFunId, theVar
    varId = p[-1]
    theVar.append(varId)
    if(procedures.search_var(actualFunId, varId)):
        tipo = procedures.get_var_type(actualFunId, varId)
        if tipo == 'int':
            pTipos.append('int')
        elif tipo == 'float':
            pTipos.append('float')
        elif tipo == 'char':
            pTipos.append('char')
        obj = {
            'id': varId,
            'mem': procedures.get_var_memory_loc(actualFunId, varId)
        }
        pOperandos.append(obj)
    else:
        sys.exit()
    
    # print('added operando: ' + str(p[-1]))

def p_LLAMADA(p):
    '''LLAMADA : IDENTIFIER search_func l_paren_expression L_PAREN generate_era_quad LLAMADA_AUX verify_params R_PAREN r_paren_expression generate_gosub_quad generate_temp_var'''

# Verify that function called already exits
def p_search_func(p):
    '''search_func : '''
    global actualCall, actualCallType
    actualCall = p[-1]
    if(not procedures.search(actualCall)):
        print("Procedure '", actualCall, "' not found")
        sys.exit()
    actualCallType = procedures.get_function_type(actualCall)

# Generate ERA quad 
def p_generate_era_quad(p):
    '''generate_era_quad : '''
    global kParams, actualCall
    quad = ('ERA', -1, -1, actualCall)
    
    cuadruplos.append(quad)
    cuadruplosIds.append(quad)
    kParams = 1

# Verify kParams matches the actual # of parameters defined 
def p_verify_params(p):
    '''verify_params : '''
    global kParams, actualCall
    if (kParams != procedures.get_numParams(actualCall)):
        print("Error in parameters, function calling:", actualCall)
        sys.exit()

# Generate GOSUB quad
def p_generate_gosub_quad(p):
    '''generate_gosub_quad : '''
    global actualCall
    quad = ('GOSUB', actualCall, -1, procedures.get_quad_num(actualCall))
    
    cuadruplos.append(quad)
    cuadruplosIds.append(quad)

def p_generate_temp_var(p):
    '''generate_temp_var : '''
    # Every time we call a function we need to store the value it returns in a tmp variable and append it to the operands list.
    # print('theactualfuntype', actualCallType)
    if(actualCallType != 'void'):
        global pOperandos, pTipos
        result = avail.next()
        global tmpCounter
        tmpCounter += 1
        procedures.add_tmp(actualFunId, actualCallType)
        if actualCallType == 'int':
            temporales[result] = virtualMemoryDirs['tempint']
            virtualMemoryDirs['tempint'] = virtualMemoryDirs['tempint'] + 1
        elif actualCallType == 'float':
            temporales[result] = virtualMemoryDirs['tempfloat']
            virtualMemoryDirs['tempfloat'] = virtualMemoryDirs['tempfloat'] + 1
        elif actualCallType == 'char':
            temporales[result] = virtualMemoryDirs['tempfloat']
            virtualMemoryDirs['tempchar'] = virtualMemoryDirs['tempchar'] + 1
        quad = ('RET', temporales[result], -1, procedures.get_var_memory_loc('global', actualCall))
        quad2 = ('RET', result, -1,  actualCall)
        
        cuadruplos.append(quad)
        cuadruplosIds.append(quad2)
        obj = {
            'id': result,
            'mem': temporales[result]
        }
        pOperandos.append(obj)
        pTipos.append(actualCallType)

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
    if (kParams <= procedures.get_numParams(actualCall)):
        '''TODO: Checar este pedo en el actualFunId o actualCall'''
        argumentType = procedures.get_parameter_type(actualCall, kParams-1)
        if (currentArgType != argumentType):
            print("Parameter type mismatch, calling function:", actualCall)
            sys.exit()
        dirDest = procedures.get_param_dir(actualCall, kParams)
        quad = ('PARAMETER', currentArg['mem'], -1, dirDest)
        quad2 = ('PARAMETER', currentArg['id'], -1, kParams)
        
        cuadruplos.append(quad)
        cuadruplosIds.append(quad2)
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
    quad = ('GOTO', -1, -1, jump)
    
    cuadruplos.append(quad)
    cuadruplosIds.append(quad)
    fill_quad(end)

def p_DESDE(p):
    '''DESDE : FROM L_PAREN ASIGNACION_DESDE R_PAREN UNTIL add_while_from_cond L_PAREN EXPRESION add_from_exp R_PAREN DO BLOQUE add_end_while_from'''

def p_add_from_exp(p):
    '''add_from_exp : '''
    add_if_while_from('GOTOV')

def p_ASIGNACION_DESDE(p):
    '''ASIGNACION_DESDE : IDENTIFIER add_id DIMENSIONES EQUALS add_equal_operator EXPRESION generate_equal_quad'''

def p_PRINCIPAL(p):
    '''PRINCIPAL : MAIN L_PAREN R_PAREN BLOQUE release_func'''

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
    quad = ('GOTO', -1, -1, -1)
    
    cuadruplos.append(quad)
    cuadruplosIds.append(quad)
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
            # print('the actual fun id direction var',procedures.get_var_memory_loc('global', actualFunId))
            
            op = pOperadores.pop()
            resultado = pOperandos.pop()
            resultado_type = pTipos.pop()
            if resultado_type == actualFunType:
                quad = (op, -1, procedures.get_var_memory_loc('global', actualFunId), resultado['mem'])
                # print("cuadruplo: " + str(quad))
                
                cuadruplos.append(quad)
                quad2 = (op, -1, -1, resultado['id'])
                cuadruplosIds.append(quad2)
            else:
                print("Type missmatch")
                sys.exit()

# def p_generate_endproc(p):
#     '''generate_endproc : '''
#     global cuadruplos
#     quad = ('ENDPROC', -1, -1, -1)
#     cuadruplos.append(quad)

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
    global actualVarId, procedures, actualVarType, theVar
    actualVarId = p[-1]
    theVar.append(actualVarId)
    if procedures.search_var(actualFunId, actualVarId):
        # pOperandos.append(procedures.get_var_memory_loc(actualFunId, actualVarId))
        obj = {
            'id': actualVarId,
            'mem': procedures.get_var_memory_loc(actualFunId, actualVarId)
        }
        pOperandos.append(obj)
        pTipos.append(procedures.get_var_type(actualFunId, actualVarId))
        actualVarType = procedures.get_var_type(actualFunId, actualVarId)
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
        sys.exit()
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
        
        # print(actualFunId, actualVarId, actualVarType, virtualMemoryDirs[memoryType])
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
        global tmpCounter
        tmpCounter += 1
        procedures.add_tmp(actualFunId, result_type)
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
        quad = (op, operando_izquierdo['mem'], operando_derecho['mem'], temporales[result])
        quad2 = (op, operando_izquierdo['id'], operando_derecho['id'], result)
        # print('cuadruplo: ' + str(quad))
        
        cuadruplos.append(quad)
        cuadruplosIds.append(quad2)
        obj = {
            'id': result,
            'mem': temporales[result]
        }
        pOperandos.append(obj)
        # pOperandos.append(temporales[result])
        pTipos.append(result_type)
    else:
        print("type mismatch")
        sys.exit()
	
def quad_generator_2args():
    global pOperadores, pOperandos, pTipos, cuadruplos
    op = pOperadores.pop()
    operando = pOperandos.pop()
    operando_type = pTipos.pop()
    quad = (op, -1, -1, operando['mem'])
    quad2 = (op, -1, -1, operando['id'])
    # print('cuadruplo: ' + str(quad))
    
    cuadruplos.append(quad)
    cuadruplosIds.append(quad2)
    pOperandos.append(operando)
    pTipos.append(operando_type)
    #create_new_avail()

def add_if_while_from(goto):
    global pTipos, pSaltos, cuadruplos
    exp_type = pTipos.pop()
    if exp_type == 'bool':
        result = pOperandos.pop()
        quad = (goto, result['mem'], -1, -1)
        quad2 = (goto, result['id'], -1, -1)
        
        cuadruplos.append(quad)
        cuadruplosIds.append(quad2)
        pSaltos.append(len(cuadruplos)-1)
        # print('cuadruplo: ' + str(quad))
    else: 
        print("type mismatch")
        sys.exit()
    
def fill_quad(i):
    global cuadruplos
    temp = list(cuadruplos[i])
    temp[3] = len(cuadruplos)
    # print(temp, temp[3])
    cuadruplos[i] = tuple(temp)
    '''Para los ids'''
    temp = list(cuadruplosIds[i])
    temp[3] = len(cuadruplosIds)
    cuadruplosIds[i] = tuple(temp)
    # print('cuadruplo: ' + str(cuadruplos[i]))

def printCuadruplos():
    for (i, elem) in enumerate(cuadruplosIds):
        print (i, elem)
    
    for (i, elem) in enumerate(cuadruplos):
        print(i, elem)
    procedures.print_proc()
    print(constantes)

# Function for resetting the avail
def create_new_avail():
    global avail
    avail = Avail()

# Function to create output file for VM
def createDout():
    global program_name
    orig_stdout = sys.stdout
    filename = str(program_name + ".dout")
    print(filename)
    file = open(filename, "w")
    sys.stdout = file

    print("---QUADS---")
    for quad in cuadruplos:
        for elem in quad:
            print(str(elem), end = ' ')
        print()
    print("---PROC---")
    procedures.print_out_proc()
    print("---CTES---")
    for cte in constantes:
        print(cte, constantes[cte])

    sys.stdout = orig_stdout
    file.close()

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
                # printCuadruplos()
                createDout()

        except EOFError:
            print(EOFError)
    else:
        print('File missing')