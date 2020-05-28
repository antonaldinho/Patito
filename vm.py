# Virtual Machine for duck ++
import sys

cuadruplos = []
constantes = {}

def create_constants(data):
    global constants
    start = data.index('---CTES---') + 1
    for i in range(start, len(data)):
        constantes[data[i][-5:]] = data[i][:-6]
    
    print(constantes)
    for i in constantes:
        print(i, constantes[i])

def make_quads(data):
    global cuadruplos
    end = data.index('---PROC---')
    for i in range(1, end):
        cuadruplos.append(data[i].split())

def clean_data(data):
    newData = []
    for i in range(len(data)):
        newData.append(data[i].rstrip('\n'))
    return newData

if __name__ == '__main__':
    if (len(sys.argv)>1):
        file = sys.argv[1]
        try:
            f = open(file, 'r')
            data = f.readlines()
            f.close()
            data = clean_data(data)
            create_constants(data)
            make_quads(data)
        except EOFError:
            print(EOFError)
    else:
        print(".dout file not found")