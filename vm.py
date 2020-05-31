# Virtual Machine for duck ++
import sys

cuadruplos = []
memoria = {}
funciones = {}
IP = 0

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
        print("Failed to run")
        sys.exit()

# Execute quads
def execute():
    global IP
    last_quad = len(cuadruplos)-1
    while (IP != last_quad):
        cod_op = cuadruplos[IP][0]
        # print(cod_op)
        if cod_op == '+':
            op_izq = convert(memoria[cuadruplos[IP][1]])
            op_der = convert(memoria[cuadruplos[IP][2]])
            result = op_izq + op_der
            memoria[cuadruplos[IP][3]] = result
            IP = IP + 1
        elif cod_op == '-':
            op_izq = convert(memoria[cuadruplos[IP][1]])
            op_der = convert(memoria[cuadruplos[IP][2]])
            result = op_izq - op_der
            memoria[cuadruplos[IP][3]] = result
            IP = IP + 1
        elif cod_op == '*':
            op_izq = convert(memoria[cuadruplos[IP][1]])
            op_der = convert(memoria[cuadruplos[IP][2]])
            result = op_izq * op_der
            memoria[cuadruplos[IP][3]] = result
            IP = IP + 1
        elif cod_op == '/':
            op_izq = convert(memoria[cuadruplos[IP][1]])
            op_der = convert(memoria[cuadruplos[IP][2]])
            result = op_izq / op_der
            memoria[cuadruplos[IP][3]] = result
            IP = IP + 1
        elif cod_op == '=':
            memoria[cuadruplos[IP][1]] = memoria[cuadruplos[IP][3]]
            IP = IP + 1
        elif cod_op == 'print':
            toPrint = memoria[cuadruplos[IP][3]]
            print(toPrint)
            IP = IP + 1
        elif cod_op == 'GOSUB': 
            IP = int(cuadruplos[IP][3])
        else:
            IP = IP + 1

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
    vars = int(funciones['global']['intVars'])
    if (vars>0):
        for i in range(1000, 1000+vars):
            memoria[str(i)] = None
    vars = int(funciones['global']['floatVars'])
    if (vars>0):
        for i in range(3000, 3000+vars):
            memoria[str(i)] = None
    vars = int(funciones['global']['charVars'])
    if(vars>0):
        for i in range(5000, 5000+vars):
            memoria[str(i)] = None  

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
            # log()
        except EOFError:
            print(EOFError)
    else:
        print(".dout file not found")