from TablaVariables import TablaVariables
import getopt
import sys
class DirectorioProcedimientos(object):
    def __init__(self):
        self.list = {}
    
    def add_function(self, name, fType, numParams, typeParams, nameParams, numVars, quad):
        if(name not in self.list.keys()):
            self.list[name] = {
                'type': fType,
                'numParams': numParams,
                'typeParams': typeParams,
                'nameParams': nameParams,
                'paramLocs': [],
                'vars': TablaVariables(),
                'numVars': numVars,
                'quadNum': quad,
                'tmps': []
            }
            #print("added function: " + name)
        else:
            print("function" + name + " already declared")
    
    def add_tmp(self, name, tmp):
        self.list[name]['tmps'].append(tmp)
    
    def set_type_spaces(self, fName):
        self.list[fName]['spaces'] = {
            'localint': self.list[fName]['vars'].get_spaces('int'),
            'localfloat': self.list[fName]['vars'].get_spaces('float'),
            'localchar': self.list[fName]['vars'].get_spaces('char'),
            'tmpint':  self.get_space(fName,'int'),
            'tmpfloat': self.get_space(fName, 'float'),
            'tmpchar': self.get_space(fName, 'char'),
            'tmpbool': self.get_space(fName, 'bool'),
            'tmppointer': self.get_space(fName, 'pointer'),
        }
        # print('type spaces', fName , self.list[fName]['spaces'] )
    
    def get_space(self, fName, tipo):
        counter = 0
        for element in self.list[fName]['tmps']:
            if element == tipo:
                counter += 1
        return counter

    def search(self, name):
        return name in self.list

    def get_var_scope_type(self, fName, vName):
        if self.list[fName]['vars'].search(vName) == True and fName != 'global':
            return 'local'
        elif self.list['global']['vars'].search(vName):
            return 'global'
        else:
            print("Variable " + str(vName) + " does not exist")
            

    def search_var(self, fName, vName):
        if self.list[fName]['vars'].search(vName) == True:
            return True
        elif self.list['global']['vars'].search(vName):
            return True
        else:
            print("Variable " + str(vName) + " does not exist")
            return False

    def get_function_type(self, fName):
        return self.list[fName]['type']

    def get_var_type(self, fName, vName):
        if self.list[fName]['vars'].search(vName) == True:
            return self.list[fName]['vars'].get_type(vName)
        elif self.list['global']['vars'].search(vName) == True:
            return self.list['global']['vars'].get_type(vName)
        else:
            print("Variable " + str(vName) +" does not exist")
            sys.exit()
    
    def get_var_memory_loc(self, fName, vName):
        if self.list[fName]['vars'].search(vName) == True:
            return self.list[fName]['vars'].get_memory_loc(vName)
        elif self.list['global']['vars'].search(vName) == True:
            return self.list['global']['vars'].get_memory_loc(vName)
        else:
            print("Variable " + str(vName) +" does not exist")
            sys.exit()
    
    def get_parameter_type(self, fName, pos):
        return self.list[fName]['typeParams'][pos]

    def get_numParams(self, fName):
        return self.list[fName]['numParams']

    def get_quad_num(self, fName):
        return self.list[fName]['quadNum']
    
    def get_param_dir(self, fName, pPos):
        return self.list[fName]['paramLocs'][pPos-1]

    def add_var(self, fName, vName, vType, vMemoryLoc):
        if(self.list[fName]['vars'].search(vName) == True):
            print("Variable already exists")
            sys.exit()
        else:
            self.list[fName]['vars'].add_var(vName, vType, vMemoryLoc)
            self.list[fName]['numVars'] = self.list[fName]['numVars'] + 1
            # type = vType + 'Vars'
            # self.list[fName][type] = self.list[fName][type] +1
    
    def add_param(self, fName, vName, vType):
        self.list[fName]['numParams'] = self.list[fName]['numParams'] + 1
        self.list[fName]['nameParams'].append(vName)
        self.list[fName]['typeParams'].append(vType)
        self.list[fName]['paramLocs'].append(self.get_var_memory_loc(fName, vName))
    
    def add_quad_counter(self, fName, quad):
        self.list[fName]['quadNum'] = quad

    # Add 1 to tmp var counter by type
    def add_tmp_type(self, fName, vType):
        if vType != 'void':
            type = vType + 'Tmp'
            self.list[fName][type] = self.list[fName][type]+1

    def delete_var_table(self, fName):
        self.list[fName]['vars'] = None

    def list_vars(self, name):
        if name in self.list:
            self.list[name]['vars'].print_all_vars()
    
    def add_num_tmp(self, fName, numTmpVars):
        self.list[fName]['numTmp'] = numTmpVars

    def print_proc(self):
        for elem in self.list:
            print(elem, self.list[elem])
    
    def make_var_array(self, fName, vName):
        self.list[fName]['vars'].make_array(vName)
    
    def add_dim(self, fName, vName):
        self.list[fName]['vars'].add_dim(vName)
    
    def add_lsup(self, fName, vName, lsup):
        self.list[fName]['vars'].add_lsup(vName, lsup)

    def set_r(self, fName, vName, tipo):
        self.list[fName]['vars'].set_r(vName, tipo)

    def add_dimention(self, fName, vName):
        self.list[fName]['vars'].add_dim(vName)
    
    def set_all_nodes(self, fName, vName):
        self.list[fName]['vars'].set_all_nodes(vName)
    
    def get_array_size(self, fName, vName):
        return(self.list[fName]['vars'].get_array_size(vName))
    
    def is_dimentioned(self, fName, vName):
        if self.list[fName]['vars'].search(vName) == True:
            return(self.list[fName]['vars'].is_dimentioned(vName))
        elif self.list['global']['vars'].search(vName):
            return(self.list['global']['vars'].is_dimentioned(vName))
    
    def get_num_dims(self, fName, vName):
        if self.list[fName]['vars'].search(vName) == True:
            return(self.list[fName]['vars'].get_num_dims(vName))
        elif self.list['global']['vars'].search(vName):
            return(self.list['global']['vars'].get_num_dims(vName))
    
    def get_first_node(self, fName, vName, dim):
        if self.list[fName]['vars'].search(vName) == True:
            return(self.list[fName]['vars'].get_first_node(vName, dim))
        elif self.list['global']['vars'].search(vName):
            return(self.list['global']['vars'].get_first_node(vName, dim))
    
    def get_node(self, fName, vName, dim):
        if self.list[fName]['vars'].search(vName) == True:
            return(self.list[fName]['vars'].get_node(vName, dim))
        elif self.list['global']['vars'].search(vName):
            return(self.list['global']['vars'].get_node(vName, dim))
        
    # Print for .dout file
    def print_out_proc(self):  
        for elem in self.list:
            # print('the elem',elem)
            print(elem, str(self.list[elem]['numVars']), str(self.list[elem]['quadNum']), end=' ') 
            print(str(self.list[elem]['spaces']['localint']), str(self.list[elem]['spaces']['localfloat']), str(self.list[elem]['spaces']['localchar']), end=' ')
            print(str(self.list[elem]['spaces']['tmpint']), str(self.list[elem]['spaces']['tmpfloat']), str(self.list[elem]['spaces']['tmpchar']), str(self.list[elem]['spaces']['tmpbool']), str(self.list[elem]['spaces']['tmppointer']))


# if __name__ == "__main__":
#     print("calando tests...")
#     test = DirectorioProcedimientos()
#     test.add_function('function1', 'void', 2, ['int', 'float'], ['myInt', 'myFloat'], 0)
#     test.add_var('function1', 'x', int, 100)
#     test.add_var('function1', 'y', int, 101)
#     test.add_var('function1', 'z', int, 102)
#     test.add_var('function1', 'b', bool, 103)
#     print(test.search('function1'))
#     test.list_vars('function1')