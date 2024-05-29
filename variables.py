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
        
    def starts_with_non_num_or_at(self, s):
        reserved = ['=', '+', '-', '*', '/', 'IF', 'ELSE', 
                    'ENDIF', 'DO', 'WHILE', 'ENDPRINT', 'gotoF', 'VAR_PRINT',
                    'gotoV', 'goto', 'CTE_STRING', 'PRINT', '<', '>', '%']
        if s in reserved or not s or s[0] == '"':
            return False
        first_char = s[0]
        return not (first_char.isdigit())
    
    def translate_to_address(self):
        for i, c in enumerate(self.cuadruplos):
            for j, s in enumerate(c):
                if self.starts_with_non_num_or_at(s) and s[0] != '-':
                    self.cuadruplos[i][j] = self.variables.get_variable_address(s)

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
                self.cuadruplos[stack.pop()][3] = str(count + 1)
            elif exp == 'DO':
                stack.append(count+1)
            elif exp == 'WHILE':
                self.cuadruplos.append(['gotoV', self.cuadruplos[count-1][-1], '', str(stack.pop())])
                count += 1
            elif exp == 'ENDPRINT':
                self.cuadruplos.append(['PRINT', '', '', str(self.cuadruplos[count-1][-1])])
                count += 1
            elif exp.startswith('"'):
                name = exp.strip('"')
                self.cuadruplos.append(['CTE_STRING', '', '', '"{}"'.format(name)])
                count += 1
            elif exp in self.variables.symbols_map:
                self.cuadruplos.append(['VAR_PRINT', '', '', str(exp)])
                count += 1
            else:
                q = generator.generate(exp)
                self.cuadruplos.extend(q)
                count += len(q)
        self.translate_to_address()
        self.print_cuadruplos()

class VariableTable:
    def __init__(self):
        self.symbols = {}
        self.symbols_map = {}
        self.global_int_count = 0
        self.global_float_count = 0
        self.temp_count = 0
    
    def print_expresiones(self):
        for i, c in self.symbols.items():
            print(f"{i+1}. {c}")

    def add_variable(self, name, data_type):
        if name in self.symbols:
            raise ValueError(f"Variable '{name}' is already declared in this scope")
        if data_type == 'int':
            self.symbols_map[name] = 1000+self.global_int_count
            self.symbols[1000+self.global_int_count] = None
            self.global_int_count += 1
        elif data_type == 'float':
            self.symbols_map[name] = 2000+self.global_float_count
            self.symbols[2000+self.global_float_count] = None
            self.global_float_count += 1

    def get_variable_address(self, name):
        if name in self.symbols_map:
            return self.symbols_map[name]
        elif name[0] == '@':
            self.symbols_map[name] = 3000+self.temp_count
            self.symbols[3000+self.temp_count] = None
            self.temp_count += 1
            return 3000+self.temp_count-1
        else:
            raise KeyError(f"Variable '{name}' not found in symbol table")