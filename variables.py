from collections import deque
from quadruples import QuadrupleGenerator

class FunctionTable:
    def __init__(self):
        self.variables = VariableTable()
        self.expresiones = deque()
        self.cuadruplos = []
    
    def print_cuadruplos(self):
        for i, c in enumerate(self.cuadruplos):
            print(f"{i+1}. {c}")

    def print_expresiones(self):
        for i, c in enumerate(self.expresiones):
            print(f"{i+1}. {c}")
    
    def generate_quadruples(self):
        generator = QuadrupleGenerator()
        count = 0
        stack = []
        while self.expresiones:
            exp = self.expresiones.popleft()
            if exp == 'IF':
                self.cuadruplos.append(['gotoF', self.cuadruplos[count-1][-1], '', ''])
                stack.append(count)
                count += 1
            elif exp == 'ELSE':
                self.cuadruplos.append(['goto', '', '', ''])
                self.cuadruplos[stack.pop()][3] = str(count + 2)
                stack.append(count)
                count += 1
            elif exp == 'ENDIF':
                count += 1
                self.cuadruplos[stack.pop()][3] = str(count)
            else:
                q = generator.generate(exp)
                self.cuadruplos.extend(q)
                count += len(q)
        self.print_cuadruplos()

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
