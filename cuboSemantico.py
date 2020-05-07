class cuboSemantico ():
	
	def __init__(self):
		self.Cubo = {
			'int' :
			{
				'int': { #int op int
					'+' : 'int', '-' : 'int', '*' : 'int', '/' : 'float',
					'<' : 'bool', '>' : 'bool', '<=' : 'bool', '>=' : 'bool', '==' : 'bool', '!=' : 'bool',
					'||' : 'error', '&&': 'error',
				},
				'float' : { #int op float
					'+' : 'float', '-' : 'float', '*' : 'float', '/' : 'float',
					'<' : 'bool', '>' : 'bool', '<=' : 'bool', '>=' : 'bool', '==' : 'bool', '!=' : 'bool',
					'||' : 'error', '&&': 'error',
				},
				'char' : { #int op char
					'+' : 'error', '-' : 'error', '*' : 'error', '/' : 'error',
					'<' : 'error', '>' : 'error', '<=' : 'error', '>=' : 'error', '==' : 'bool', '!=' : 'bool',
					'||' : 'error', '&&': 'error',
				},
				'bool' : { #int op bool
					'+' : 'error', '-' : 'error', '*' : 'error', '/' : 'error',
					'<' : 'error', '>' : 'error', '<=' : 'error', '>=' : 'error', '==' : 'error', '!=' : 'error',
					'||' : 'error', '&&': 'error',
				},
			},
			
			'float' : 
			{ 
				'int': { #float op int
					'+' : 'float', '-' : 'float', '*' : 'float', '/' : 'float',
					'<' : 'bool', '>' : 'bool', '<=' : 'bool', '>=' : 'bool', '==' : 'bool', '!=' : 'bool',
					'||' : 'error', '&&': 'error',
				},
				'float' : { #float op float
					'+' : 'float', '-' : 'float', '*' : 'float', '/' : 'float',
					'<' : 'bool', '>' : 'bool', '<=' : 'bool', '>=' : 'bool', '==' : 'bool', '!=' : 'bool',
					'||' : 'error', '&&': 'error',
				},
				'char' : { #float op char
					'+' : 'float', '-' : 'float', '*' : 'float', '/' : 'float',
					'<' : 'error', '>' : 'error', '<=' : 'error', '>=' : 'error', '==' : 'bool', '!=' : 'bool',
					'||' : 'error', '&&': 'error',
				},
				'bool' : { #float op bool
					'+' : 'error', '-' : 'error', '*' : 'error', '/' : 'error',
					'<' : 'error', '>' : 'error', '<=' : 'error', '>=' : 'error', '==' : 'error', '!=' : 'error',
					'||' : 'error', '&&': 'error',
				},
			},
			
			'char' : 
			{ 
				'int': { #char op int
					'+' : 'error', '-' : 'error', '*' : 'error', '/' : 'error',
					'<' : 'error', '>' : 'error', '<=' : 'error', '>=' : 'error', '==' : 'bool', '!=' : 'bool',
					'||' : 'error', '&&': 'error',
				},
				'float' : { #char op float
					'+' : 'error', '-' : 'error', '*' : 'error', '/' : 'error',
					'<' : 'error', '>' : 'error', '<=' : 'error', '>=' : 'error', '==' : 'bool', '!=' : 'bool',
					'||' : 'error', '&&': 'error',
				},
				'char' : { #char op char
					'+' : 'error', '-' : 'error', '*' : 'error', '/' : 'error',
					'<' : 'error', '>' : 'error', '<=' : 'error', '>=' : 'error', '==' : 'bool', '!=' : 'bool',
					'||' : 'error', '&&': 'error',
				},
				'bool' : { #char op bool
					'+' : 'error', '-' : 'error', '*' : 'error', '/' : 'error',
					'<' : 'error', '>' : 'error', '<=' : 'error', '>=' : 'error', '==' : 'error', '!=' : 'error',
					'||' : 'error', '&&': 'error',
				},
			},

			'bool' : 
			{ 
				'int': { #bool op int
					'+' : 'error', '-' : 'error', '*' : 'error', '/' : 'error',
					'<' : 'error', '>' : 'error', '<=' : 'error', '>=' : 'error', '==' : 'error', '!=' : 'error',
					'||' : 'error', '&&': 'error',
				},
				'float' : { #bool op float
					'+' : 'error', '-' : 'error', '*' : 'error', '/' : 'error',
					'<' : 'error', '>' : 'error', '<=' : 'error', '>=' : 'error', '==' : 'error', '!=' : 'error',
					'||' : 'error', '&&': 'error',
				},
				'char' : { #bool op char
					'+' : 'error', '-' : 'error', '*' : 'error', '/' : 'error',
					'<' : 'error', '>' : 'error', '<=' : 'error', '>=' : 'error', '==' : 'error', '!=' : 'error',
					'||' : 'error', '&&': 'error',
				},
				'bool' : { #bool op bool
					'+' : 'error', '-' : 'error', '*' : 'error', '/' : 'error',
					'<' : 'error', '>' : 'error', '<=' : 'error', '>=' : 'error', '==' : 'error', '!=' : 'error',
					'||' : 'bool', '&&': 'bool',
				},
			},
		}

	def get_tipo(self, left_op, right_op, op):
		return self.Cubo[left_op][right_op][op]

def main():
    test = cuboSemantico()
    print(test.get_tipo('bool', 'bool', '||'))

if __name__== "__main__":
  main()