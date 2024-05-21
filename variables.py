from quadruples import QuadrupleGenerator

class FunctionTable:
    def __init__(self):
        self.variables = VariableTable()
        self.quadruples = QuadrupleGenerator()

class VariableTable:
    def __init__(self):
        self.symbols = {}

    def add_variable(self, name, data_type):
        if name in self.symbols:
            raise ValueError(f"Variable '{name}' is already declared in this scope")
        self.symbols[name] = {'type': data_type, 'value': None}

    def set_variable_value(self, name, value):
        if name in self.symbols:
            self.symbols[name]['value'] = value
        else:
            raise KeyError(f"Variable '{name}' not found in symbol table")

    def get_variable_value(self, name):
        if name in self.symbols:
            return self.symbols[name]['value']
        else:
            raise KeyError(f"Variable '{name}' not found in symbol table")


# # Create a symbol table instance
# symbol_table = SymbolTable()

# # Add variables to the symbol table
# symbol_table.add_variable('x', 'int')
# symbol_table.add_variable('y', 'float')

# # Assign values to variables
# symbol_table.set_variable_value('x', 10)
# symbol_table.set_variable_value('y', 3.14)

# # Retrieve values of variables
# x_value = symbol_table.get_variable_value('x')  # Retrieves 10
# y_value = symbol_table.get_variable_value('y')  # Retrieves 3.14