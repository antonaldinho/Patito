class TablaVariables(object):
    def __init__(self):
        self.list = {}
    
    def add_var(self, name, type, memoryLocation):
        self.list[name] = {
            'type': type,
            'memory_location': memoryLocation
        }
        #print("added var: " + str(name) + " with type " + str(type))
    
    def search(self, name):
        return name in self.list.keys()
    
    def get_type(self, name):
        return self.list[name]['type']
    
    def get_memory_loc(self, name):
        return self.list[name]['memory_location']

    def print_all_vars(self):
        print(self.list.items())
        