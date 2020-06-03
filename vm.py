# Virtual Machine for duck ++
import sys
from Memoria import Memoria

cuadruplos = []
memoria = {}
funciones = {}
IP = 0
pilaFunciones = []
pSaltos = []
ret_var = []
nextFun = []

memoriaGlobal = Memoria()

# Verify if dir is local
def isLocal(dir):
    dir = int(dir)
    if dir>=7000 and dir<13000: 
        return True
    else:
        return False

# Verify is dir is tmp
def isTmp(dir):
    dir = int(dir)
    if dir>=13000 and dir<21000: 
        return True
    else:
        return False

# Get var in direction by adress and actual Function
def get_var(dir):
    actualFun = pilaFunciones[-1]
    if isLocal(dir) or actualFun != 'main' and isTmp(dir):
        return convert(memoria[actualFun][dir])
    else:
        return convert(memoria[dir])

# Save result to local or global direction
def save_result(dir, result):
    actualFun = pilaFunciones[-1]
    if isLocal(dir) or actualFun != 'main' and isTmp(dir):
        memoria[actualFun][dir] = result
    else:
        memoria[dir] = result

# Verify if var is int or float
def isint(x):
    try:
        a = float(x)
        b = int(a)
    except ValueError:
        return False
    else:
        return a == b

# Convert string to float or int depending on its type
def convert(x):
    try:
        if(isint(x)):
            return int(x)
        else:
            return float(x)
    except TypeError:
        print('x', x)
        print("TypeError, failed to run")
        sys.exit()
    except ValueError:
        print("Value error, failed to run")
        sys.exit()

# Execute quads
def execute():
    global IP
    last_quad = len(cuadruplos)-1
    x = 0 # TODO: Eliminar variable de control para evitar ciclos infinitos
    while (IP != last_quad and x<1000):
        cod_op = cuadruplos[IP][0]
        quad = cuadruplos[IP]
        print(IP, cod_op, quad)
        if cod_op == '+':
            op_izq = get_var(quad[1])
            op_der = get_var(quad[2])
            # print('+',op_izq, op_der)
            result = op_izq + op_der
            save_result (quad[3], result)
            IP += 1
        elif cod_op == '-':
            op_izq = get_var(quad[1])
            op_der = get_var(quad[2])
            result = op_izq - op_der
            save_result (quad[3], result)
            IP += 1
        elif cod_op == '*':
            op_izq = get_var(quad[1])
            op_der = get_var(quad[2])
            result = op_izq * op_der
            save_result (quad[3], result)
            IP += 1
        elif cod_op == '/':
            op_izq = get_var(quad[1])
            op_der = get_var(quad[2])
            result = op_izq / op_der
            save_result (quad[3], result)
            IP += 1
        elif cod_op == '=':
            actualFun = pilaFunciones[-1]
            dir_op_izq = quad[1]
            dir_op_der = quad[3]
            if isLocal(dir_op_izq) or actualFun != 'main' and isTmp(dir_op_izq):
                if isLocal(dir_op_der) or actualFun != 'main' and isTmp(dir_op_der):
                    memoria[actualFun][dir_op_izq] = memoria[actualFun][dir_op_der]
                else:
                    memoria[actualFun][dir_op_izq] = memoria[dir_op_der]
            else:
                memoria[dir_op_izq] = memoria[dir_op_der]
            IP += 1
        elif cod_op == 'print':
            actualFun = pilaFunciones[-1]
            dir_op = quad[3]
            if isLocal(dir_op) or actualFun != 'main' and isTmp(dir_op):
                toPrint = memoria[actualFun][dir_op]
            else:
                toPrint = memoria[dir_op]
            print(toPrint)
            IP += 1
        # elif cod_op == 'read': # TODO Solo funciona por el momento para leer numeros
        #     toRead = input()
        #     memoria[cuadruplos[IP][3]] = convert(toRead)
        #     IP += 1
        elif cod_op == '<':
            op_izq = get_var(quad[1])
            op_der = get_var(quad[2])
            result = op_izq < op_der
            save_result (quad[3], result)
            IP += 1
        elif cod_op == '>':
            op_izq = get_var(quad[1])
            op_der = get_var(quad[2])
            result = op_izq > op_der
            save_result (quad[3], result)
            IP += 1
        elif cod_op == '<=':
            op_izq = get_var(quad[1])
            op_der = get_var(quad[2])
            result = op_izq <= op_der
            save_result (quad[3], result)
            IP += 1
        elif cod_op == '>=':
            op_izq = get_var(quad[1])
            op_der = get_var(quad[2])
            result = op_izq >= op_der
            save_result (quad[3], result)
            IP += 1
        elif cod_op == '&&':
            actualFun = pilaFunciones[-1]
            if actualFun == 'main':
                op_izq = memoria[quad[1]]
                op_der = memoria[quad[2]]
                result = op_izq and op_der
                memoria[quad[3]] = result
            else:
                op_izq = memoria[actualFun][quad[1]]
                op_der = memoria[actualFun][quad[2]]
                result = op_izq and op_der
                memoria[actualFun][quad[3]] = result
            IP += 1
        elif cod_op == '||':
            actualFun = pilaFunciones[-1]
            if actualFun == 'main':
                op_izq = memoria[quad[1]]
                op_der = memoria[quad[2]]
                result = op_izq and op_der
                memoria[quad[3]] = result
            else:
                op_izq = memoria[actualFun][quad[1]]
                op_der = memoria[actualFun][quad[2]]
                result = op_izq or op_der
                memoria[actualFun][quad[3]] = result
            IP += 1
        elif cod_op == '!=':
            op_izq = get_var(quad[1])
            op_der = get_var(quad[2])
            result = op_izq != op_der
            save_result (quad[3], result)
            IP += 1
        elif cod_op == '==':
            op_izq = get_var(quad[1])
            op_der = get_var(quad[2])
            result = op_izq == op_der
            save_result (quad[3], result)
            IP += 1
        elif cod_op == 'GOTO':
            IP = int(cuadruplos[IP][3])
        elif cod_op == 'GOTOF':
            dir = quad[1]
            actualFun = pilaFunciones[-1]
            if isLocal(dir) or actualFun != 'main' and isTmp(dir):
                flag =  memoria[actualFun][dir]
            else:
                flag = memoria[dir]

            if flag == False:
                IP = int(quad[3])
            else:
                IP += 1
        elif cod_op == 'GOTOV':
            dir = quad[1]
            actualFun = pilaFunciones[-1]
            if isLocal(dir) or actualFun != 'main' and isTmp(dir):
                flag = memoria[actualFun][dir]
            else:
                flag = memoria[dir]
            
            if flag == True:
                IP = int(quad[3])
            else:
                IP += 1
        elif cod_op == 'ERA':
            funName = quad[3]
            fun = funName + str(len(pilaFunciones))
            # pilaFunciones.append(fun)
            nextFun.append(fun)
            memoria[fun] = {}

            # Create function local vars
            vars = int(funciones[funName]['intVars'])
            if (vars>0):
                for i in range(7000, 7000+vars):
                    memoria[fun][str(i)] = None
            vars = int(funciones[funName]['floatVars'])
            if (vars>0):
                for i in range(9000, 9000+vars):
                    memoria[fun][str(i)] = None
            vars = int(funciones[funName]['charVars'])
            if(vars>0):
                for i in range(11000, 11000+vars):
                    memoria[fun][str(i)] = None 
            
            # Create Local Tmp vars
            varsFun = int(funciones[funName]['intTmp'])
            if (varsFun>0):
                for i in range(13000, 13000+varsFun):
                    memoria[fun][str(i)] = None
            varsFun = int(funciones[funName]['floatTmp'])
            if (varsFun>0):
                for i in range(15000, 15000+varsFun):
                    memoria[fun][str(i)] = None
            varsFun = int(funciones[funName]['charTmp'])
            if(varsFun>0):
                for i in range(17000, 17000+varsFun):
                    memoria[fun][str(i)] = None 
            varsFun = int(funciones[funName]['boolTmp'])
            if(varsFun>0):
                for i in range(19000, 19000+varsFun):
                    memoria[fun][str(i)] = None
            # print(memoria[fun])
            IP += 1
        elif cod_op == 'PARAMETER':
            actualFun = pilaFunciones[-1]
            nextF = nextFun.pop()
            # print('parameter', nextF, actualFun)
            if actualFun == 'main':
                memoria[nextF][quad[3]] = memoria[quad[1]]
            else:
                memoria[nextF][quad[3]] = memoria[actualFun][quad[1]]
            IP += 1
        elif cod_op == 'GOSUB': 
            fun = funName + str(len(pilaFunciones))
            pilaFunciones.append(fun)
            pSaltos.append(IP+1)
            IP = int(quad[3])
        elif cod_op == 'RETURN':
            ret_var.append(get_var(quad[3]))
            IP += 1
        elif cod_op == 'ENDPROC':
            actualFun = pilaFunciones.pop()
            del memoria[actualFun]
            IP = pSaltos.pop()
        elif cod_op == 'RET':
            actualFun = pilaFunciones[-1]
            # print('ret', actualFun)
            if actualFun == 'main':
                memoria[quad[1]] = ret_var.pop()
            else:
                memoria[actualFun][quad[1]] = ret_var.pop()
            IP += 1
        elif cod_op == 'GOMAIN':
            IP = int(quad[3])
        else:
            IP += 1 # TODO No Olvidar quitarlo
        x += 1
        print('pilaFunciones', pilaFunciones, memoria)
        print('pila retornos', ret_var)
        print()
        # print('memoria', IP, cod_op)

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
            'boolTmp' : newData[9]
        }
    # Create global chunk of memory
    varsGlobal = int(funciones['global']['intVars'])
    if (varsGlobal>0):
        for i in range(1000, 1000+varsGlobal):
            memoria[str(i)] = None
    varsGlobal = int(funciones['global']['floatVars'])
    if (varsGlobal>0):
        for i in range(3000, 3000+varsGlobal):
            memoria[str(i)] = None
    varsGlobal = int(funciones['global']['charVars'])
    if(varsGlobal>0):
        for i in range(5000, 5000+varsGlobal):
            memoria[str(i)] = None 
    
    # Create main chunk of memory
    varsMain = int(funciones['main']['intTmp'])
    if (varsMain>0):
        for i in range(13000, 13000+varsMain):
            memoria[str(i)] = None
    varsMain = int(funciones['main']['floatTmp'])
    if (varsMain>0):
        for i in range(15000, 15000+varsMain):
            memoria[str(i)] = None
    varsMain = int(funciones['main']['charTmp'])
    if(varsMain>0):
        for i in range(17000, 17000+varsMain):
            memoria[str(i)] = None 
    varsMain = int(funciones['main']['boolTmp'])
    if(varsMain>0):
        for i in range(19000, 19000+varsMain):
            memoria[str(i)] = None 
    pilaFunciones.append('main')

# Extract constants data from .dout
def create_constants(data):
    global constants
    start = data.index('---CTES---') + 1
    for i in range(start, len(data)):
        memoria[data[i][-5:]] = data[i][:-6]

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
            log()
        except EOFError:
            print(EOFError)
    else:
        print(".dout file not found")