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
        print(self.expresiones)
        while self.expresiones:
            exp = self.expresiones.popleft()
            # print(exp)
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
            elif exp == 'DO':
                stack.append(count)
            elif exp == 'WHILE':
                self.cuadruplos.append(['gotoV', self.cuadruplos[count-2][-1], '', str(stack.pop())])
                count += 1
            elif exp == 'ENDPRINT':
                self.cuadruplos.append(['PRINT', '', '', str(self.cuadruplos[count-1][-1])])
                count += 1
            elif exp.startswith('"'):
                name = exp.strip('"')
                self.cuadruplos.append(['CTE_STRING', '', '', name])
                count += 1
            else:
                # pass
                q = generator.generate(exp)
                self.cuadruplos.extend(q)
                count += len(q)
        print(self.variables.symbols)
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
