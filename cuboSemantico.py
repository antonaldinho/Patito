class cuboSemantico ():
	
	def __init__(self):
		self.Cubo = {
			'int' :
			{
				'int': { #int op int
					'+' : 'int', '-' : 'int', '*' : 'int', '/' : 'float',
					'<' : 'bool', '>' : 'bool', '<=' : 'bool', '>=' : 'bool', '==' : 'bool', '!=' : 'bool',
				},
				'float' : { #int op float
					'+' : 'float', '-' : 'float', '*' : 'float', '/' : 'float',
					'<' : 'bool', '>' : 'bool', '<=' : 'bool', '>=' : 'bool', '==' : 'bool', '!=' : 'bool',
				},
				'char' : { #int op char
					'+' : 'error', '-' : 'error', '*' : 'error', '/' : 'error',
					'<' : 'error', '>' : 'error', '<=' : 'error', '>=' : 'error', '==' : 'bool', '!=' : 'bool',
				}
			},
			
			'float' : 
			{ 
				'int': { #float op int
					'+' : 'float', '-' : 'float', '*' : 'float', '/' : 'float',
					'<' : 'bool', '>' : 'bool', '<=' : 'bool', '>=' : 'bool', '==' : 'bool', '!=' : 'bool',
				},
				'float' : { #float op float
					'+' : 'float', '-' : 'float', '*' : 'float', '/' : 'float',
					'<' : 'bool', '>' : 'bool', '<=' : 'bool', '>=' : 'bool', '==' : 'bool', '!=' : 'bool',
				},
				'char' : { #float op char
					'+' : 'float', '-' : 'float', '*' : 'float', '/' : 'float',
					'<' : 'error', '>' : 'error', '<=' : 'error', '>=' : 'error', '==' : 'bool', '!=' : 'bool',
				}
			},
			
			'char' : 
			{ 
				'int': { #char op int
					'+' : 'error', '-' : 'error', '*' : 'error', '/' : 'error',
					'<' : 'error', '>' : 'error', '<=' : 'error', '>=' : 'error', '==' : 'bool', '!=' : 'bool',
				},
				'float' : { #char op float
					'+' : 'error', '-' : 'error', '*' : 'error', '/' : 'error',
					'<' : 'error', '>' : 'error', '<=' : 'error', '>=' : 'error', '==' : 'bool', '!=' : 'bool',
				},
				'char' : { #char op char
					'+' : 'error', '-' : 'error', '*' : 'error', '/' : 'error',
					'<' : 'error', '>' : 'error', '<=' : 'error', '>=' : 'error', '==' : 'bool', '!=' : 'bool',
				}
			}
		}

	def get_tipo(self, left_op, right_op, op):
		return self.Cubo[left_op][right_op][op]

def main():
    test = cuboSemantico()
    print(test.get_tipo('char', 'float', '=='))

if __name__== "__main__":
  main()