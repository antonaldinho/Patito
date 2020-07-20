# Virtual Machine for duck ++
import sys
from Memoria import Memoria

cuadruplos = []
memoria = {}
funciones = {}
instructionPointer = 0

memorias = []
constantes = {}

memoriaGlobal = Memoria()

pilaParams = []
pilaEjecucion = []

# Obtener el valor que se encuentra en direction
def get_value(direction):
    #print('getting value', direction)
    if int(direction) in range(21000, 28999): # constant value
        if int(direction) < 23000:
            # print('the constante',constantes[direction])
            return int(float(constantes[direction]))
        if int(direction) < 25000:
            return float(constantes[direction])
        return (constantes[direction])
    elif int(direction) in range(1000, 6999): # globals
        if int(direction) < 3000:
            return int(memoriaGlobal.get_value(direction))
        if int(direction) < 5000:v
            return float(memoriaGlobal.get_value(direction))
        if int(direction) < 7000:
            return memoriaGlobal.get_value(direction)
    elif int(direction) in range(7000, 12999): # locals
        if int(direction) < 9000:
            return int(memorias[-1].get_value(direction))
        if int(direction) < 11000:
            return float(memorias[-1].get_value(direction))
        if int(direction) < 13000:
            return memorias[-1].get_value(direction)
    elif int(direction) in range(13000, 20999): # temporals
        if int(direction) < 15000:
            return int(memorias[-1].get_value(direction))
        if int(direction) < 17000:
            return float(memorias[-1].get_value(direction))
        if int(direction) < 19000:
            return memorias[-1].get_value(direction)
        if int(direction) < 21000:
            return bool(memorias[-1].get_value(direction))
    elif int(direction) >= 29000 and int(direction) < 31000:
        return get_value(memoriaGlobal.get_value(direction))
    elif int(direction) >= 31000:
        return get_value(memorias[-1].get_value(direction))

# Guardar value en direction
def set_value(direction, value):
    if int(direction) in range(1000, 6999): # globals
        memoriaGlobal.set_value(direction, value)
        #print('setted', value, ' in', direction, ' in global')
    elif int(direction) in range(7000, 20999):
        memorias[-1].set_value(direction, value)
        #print('setted', value, ' in', direction, ' in local')
    elif int(direction) >= 29000 and int(direction) < 31000:
        pointer = memoriaGlobal.get_value(direction)
        memoriaGlobal.set_value(pointer, value)
    elif int(direction) >= 31000:
        pointer = memorias[-1].get_value(direction)
        memorias[-1].set_value(pointer, value)

def save_pointer(direction, pointer):
    if(int(direction) < 31000):
        memoriaGlobal.set_value(direction, pointer)
    else:
        memorias[-1].set_value(direction, pointer)
    
def calculate(operation, value1, value2):
    if operation == '+':
        return value1 + value2
    elif operation == '-':
        return value1 - value2
    elif operation == '*':
        return value1 * value2
    elif operation == '/':
        return value1 / value2
    elif operation == '<':
        return value1 < value2
    elif operation == '>':
        return value1 > value2
    elif operation == '<=':
        return value1 <= value2
    elif operation == '>=':
        return value1 >= value2
    elif operation == '&&':
        return value1 and value2
    elif operation == '||':
        return value1 or value2
    elif operation == '!=':
        return value1 != value2
    elif operation == '==':
        return value1 == value2

# Execute quads and read operation code
def execute():
    global instructionPointer, memorias, pilaParams, pilaEjecucion
    last_quad = len(cuadruplos)-1
    memoriaInicial = Memoria()
    memorias.append(memoriaInicial)
    while (instructionPointer != last_quad):
        operationCode = cuadruplos[instructionPointer][0]
        quad = cuadruplos[instructionPointer]
        if operationCode in ('+', '-', '*', '/', '<', '>', '<=', '>=', '&&', '||', '==', '!='):
            izquierdo = get_value(quad[1])
            derecho = get_value(quad[2])
            result = calculate(operationCode, izquierdo, derecho)
            set_value(quad[3], result)
            #print('completed quad', instructionPointer)
            instructionPointer += 1
        elif operationCode == '=':
            derecho = get_value(quad[3])
            set_value(quad[1], derecho)
            #print('completed quad', instructionPointer)
            instructionPointer += 1
        elif operationCode == 'print':
            # print(memorias[-1])
            value = get_value(quad[3])
            print(value)
            instructionPointer += 1
        elif operationCode in ('GOTO', 'GOMAIN'):
            instructionPointer = int(cuadruplos[instructionPointer][3])
        elif operationCode == 'GOTOF':
            value = get_value(quad[1])
            if(not value):
                instructionPointer = int(cuadruplos[instructionPointer][3])
            else:
                instructionPointer += 1
        elif operationCode == 'GOTOV':
            value = get_value(quad[1])
            if(value):
                instructionPointer = int(cuadruplos[instructionPointer][3])
            else:
                instructionPointer += 1
        elif operationCode == 'ERA':
            #memorias.append(Memoria())
            instructionPointer += 1
        elif operationCode == 'PARAMETER':
            parameter = get_value(quad[1])
            direction = quad[3]
            pilaParams.append((parameter, direction))
            instructionPointer += 1
        elif operationCode == 'GOSUB':
            newFunc = Memoria()
            memorias.append(newFunc)
            for param in pilaParams:
                value = param[0]
                direction = param[1]
                set_value(direction, value)
            pilaParams = []
            pilaEjecucion.append(instructionPointer + 1)
            instructionPointer = int(quad[3])
        elif operationCode == 'RET':
            value = get_value(quad[3])
            set_value(quad[1], value)
            instructionPointer += 1
        elif operationCode == 'RETURN':
            derecho = get_value(quad[3])
            # print('the quad', quad)
            # print('the return', quad[2], derecho)
            set_value(quad[2], derecho)
            instructionPointer += 1
        elif operationCode == 'ENDPROC':
            memorias.pop()
            instructionPointer = pilaEjecucion.pop()
        elif operationCode == 'sumaDir':
            val1 = get_value(quad[1])
            address = int(quad[2])
            result = val1 + address
            save_pointer(quad[3], result)
            instructionPointer += 1
        elif operationCode == 'ver':
            verificando = get_value(quad[1])
            linf = int(quad[2])
            lsup = int(quad[3])
            # print('the verificando', verificando, linf, lsup)
            # print(type(verificando), type(linf), type(lsup))
            if verificando in range(linf, lsup + 1):
                instructionPointer += 1
            else:
                print("Index out of range")
                sys.exit()
        elif operationCode == 'read':
            theInput = input()
            theInput = int(theInput)
            set_value(quad[3], theInput)
            instructionPointer += 1
            

# Extract functions data from .dout
def create_functions(data):
    start = data.index("---PROC---") + 1
    end = data.index("---CTES---")
    for i in range(start, end):
        newData = data[i].split()
        funciones[newData[0]] = {
            'numVars' : newData[1],
            'quadNum': newData[2],
            'intVars' : newData[3],
            'floatVars' : newData[4],
            'charVars' : newData[5],
            'intTmp' : newData[6],
            'floatTmp' : newData[7],
            'charTmp' : newData[8],
            'boolTmp' : newData[9],
            'tmppointer': newData[10]
        }

# Extract constants data from .dout
def create_constants(data):
    global constantes
    start = data.index('---CTES---') + 1
    for i in range(start, len(data)):
        constantes[data[i][-5:]] = data[i][:-6]

# Extract quads data from .dout
def create_quads(data):
    global cuadruplos
    end = data.index('---PROC---')
    for i in range(1, end):
        cuadruplos.append(data[i].split())

# Clean data from .dout
def clean_data(data):
    newData = []
    for i in range(len(data)):
        newData.append(data[i].rstrip('\n'))
    return newData

def create(data):
    create_functions(data)
    create_constants(data)
    create_quads(data)

# Logs
def log():
    for i in cuadruplos:
        print(i)
    
    for i in memoria:
        print(type(i), i, memoria[i])
    
    for i in funciones:
        print(i, funciones[i])

if __name__ == '__main__':
    if (len(sys.argv)>1):
        file = sys.argv[1]
        try:
            f = open(file, 'r')
            data = f.readlines()
            f.close()
            data = clean_data(data)
            create(data)
            execute()
            # log()
        except EOFError:
            print(EOFError)
    else:
        print(".dout file not found")