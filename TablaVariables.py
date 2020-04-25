class TablaVariables(object):
    def __init__(self):
        self.list = {}
    
    def add_var(self, name, type):
        self.list[name] = {
            'type': type
        }
        print("added var: " + str(name) + " with type " + str(type))
    
    def search(self, name):
        return name in self.list.keys()
    
    def print_all_vars(self):
        print(self.list.items())
        