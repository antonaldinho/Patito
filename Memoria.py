baseDirections = {
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
}

class Memoria:
    def __init__(self):
        self.createMemory()
    
    def createMemory(self):
        self.ints = []
        self.floats = []
        self.chars = []
        self.bools = []
        self.pointers = []