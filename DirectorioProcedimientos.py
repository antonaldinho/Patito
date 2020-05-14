from TablaVariables import TablaVariables
import getopt

class DirectorioProcedimientos(object):
    def __init__(self):
        self.list = {}
    
    def add_function(self, name, fType, numParams, typeParams, nameParams, numVars):
        if(name not in self.list.keys()):
            self.list[name] = {
                'type': fType,
                'numParams': numParams,
                'typeParams': typeParams,
                'nameParams': nameParams,
                'vars': TablaVariables(),
                'numVars': numVars
            }
            #print("added function: " + name)
        else:
            print("function" + name + " already declared")
    
    def search(self, name):
        return name in self.list

    def search_var(self, fName, vName):
        if self.list[fName]['vars'].search(vName) == True:
            return True
        elif self.list['global']['vars'].search(vName):
            return True
        else:
            print("Variable " + str(vName) + " does not exist")
            return False

    def get_var_type(self, vName, fName):
        if self.list[fName]['vars'].search(vName) == True:
            return self.list[fName]['vars'].get_type(vName)
        elif self.list['global']['vars'].search(vName) == True:
            return self.list['global']['vars'].get_type(vName)
        else:
            print("Variable " + str(vName) +" does not exist")
            return False
    
    def add_var(self, fName, vName, vType):
        if(self.list[fName]['vars'].search(vName) == True):
            print("Variable already exists")
        else:
            self.list[fName]['vars'].add_var(vName, vType)
    
    def list_vars(self, name):
        if name in self.list:
            self.list[name]['vars'].print_all_vars()

if __name__ == "__main__":
    print("calando tests...")
    test = DirectorioProcedimientos()
    test.add_function('function1', 'void', 2, ['int', 'float'], ['myInt', 'myFloat'], 0)
    test.add_var('function1', 'x', int)
    test.add_var('function1', 'y', int)
    test.add_var('function1', 'z', int)
    test.add_var('function1', 'b', bool)
    print(test.search('function1'))
    test.list_vars('function1')