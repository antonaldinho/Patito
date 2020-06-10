import sys

class Memoria:
    def __init__(self):
        self.values = {}

    # Guardar value en address
    def set_value(self, address, value):
        self.values[address] = value

    # Obtener valor que se encuentra en address
    def get_value(self, address):
        if address not in self.values:
            print("Error. La direccion no se encuentra en este ambiente")
            sys.exit()
        return self.values[address]