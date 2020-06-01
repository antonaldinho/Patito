class TablaVariables(object):
    def __init__(self):
        self.list = {}
    
    def add_var(self, name, type, memoryLocation):
        self.list[name] = {
            'type': type,
            'memory_location': memoryLocation,
            'is_dimentioned': False,
            'num_dimentions': 0,
            'dim': None,
            'r': None,
            'k': None
        }
        #print("added var: " + str(name) + " with type " + str(type))
    
    def search(self, name):
        return name in self.list.keys()
    
    def get_type(self, name):
        return self.list[name]['type']
    
    def get_memory_loc(self, name):
        return self.list[name]['memory_location']
    
    def make_array(self, name):
        self.list[name]['is_dimentioned'] = True
        self.list[name]['num_dimentions'] = 1
        self.list[name]['dim'] = 1
        self.list[name]['r'] = 1
        self.list[name]['lsup'] = []
        self.list[name]['m'] = []
    
    def add_dim(self, name):
        self.list[name]['num_dimentions'] = self.list[name]['num_dimentions'] + 1
        self.list[name]['dim'] = self.list[name]['dim'] + 1
    
    def add_lsup(self, name, lsup):
        self.list[name]['lsup'].append(lsup)
    
    def set_r(self, name, tipo):
        if(tipo == 1):
            self.list[name]['r'] = (self.list[name]['lsup'][self.list[name]['dim']-1]) * self.list[name]['r']
            
        elif(tipo == 2):
            self.list[name]['r'] = self.list[name]['m'][self.list[name]['dim']-1]
    
    def set_all_nodes(self, name):
        self.list[name]['dim'] = 1
        self.list[name]['size'] = self.list[name]['r']
        while(self.list[name]['dim'] - 1 < self.list[name]['num_dimentions']):
            m = self.list[name]['r'] / (self.list[name]['lsup'][self.list[name]['dim']-1])
            self.list[name]['m'].append(m)
            self.list[name]['r'] = m
            self.list[name]['dim']+=1
        self.list[name]['k'] = 0

    def get_array_size(self, name):
        return(self.list[name]['size'])
    
    def is_dimentioned(self, name):
        return(self.list[name]['is_dimentioned'])
    
    def get_num_dims(self, name):
        return(self.list[name]['num_dimentions'])
    
    def get_first_node(self, name, dim):
        if dim == 1:
            return(
                {
                    'lsup': self.list[name]['lsup'][0],
                    'm': self.list[name]['m'][0],
                }
            )
        elif dim == 2:
            return(
                {
                    'lsup': self.list[name]['lsup'][1],
                    'm': self.list[name]['m'][1],
                }
            )

    def print_all_vars(self):
        print(self.list.items())
        