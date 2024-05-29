class MaquinaVirtual:
    def __init__(self, cuadruplos, memoria) -> None:
        self.cuadruplos = cuadruplos
        self.memoria = memoria
        self.output = []
    
    def fix_type(self, address):
        if address in range(1000, 2000):
            self.memoria[address] = int(self.memoria[address])
    
    def main(self):
        i = 0
        while i < len(self.cuadruplos):
            op, v1, v2, r = self.cuadruplos[i]
            if op == '=':
                if type(v1) == int:
                    self.memoria[r] = self.memoria[v1]
                else:
                    self.memoria[r] = float(v1)
                i += 1
                self.fix_type(r)
            elif op == '+':
                if type(v1) == int and type(v2) == str:
                    self.memoria[r] = self.memoria[v1] + float(v2)
                elif type(v1) == str and type(v2) == int:
                    self.memoria[r] = float(v1) + self.memoria[v2]
                elif type(v1) == int and type(v2) == int:
                    self.memoria[r] = self.memoria[v1] + self.memoria[v2]
                elif type(v1) == str and type(v2) == str:
                    self.memoria[r] = float(v1) + float(v2)
                i += 1
            elif op == '-':
                if type(v1) == int and type(v2) == str:
                    self.memoria[r] = self.memoria[v1] - float(v2)
                elif type(v1) == str and type(v2) == int:
                    self.memoria[r] = float(v1) - self.memoria[v2]
                elif type(v1) == int and type(v2) == int:
                    self.memoria[r] = self.memoria[v1] - self.memoria[v2]
                elif type(v1) == str and type(v2) == str:
                    self.memoria[r] = float(v1) - float(v2)
                i += 1
            elif op == '*':
                if type(v1) == int and type(v2) == str:
                    self.memoria[r] = self.memoria[v1] * float(v2)
                elif type(v1) == str and type(v2) == int:
                    self.memoria[r] = float(v1) * self.memoria[v2]
                elif type(v1) == int and type(v2) == int:
                    self.memoria[r] = self.memoria[v1] * self.memoria[v2]
                elif type(v1) == str and type(v2) == str:
                    self.memoria[r] = float(v1) * float(v2)
                i += 1
            elif op == '/':
                if type(v1) == int and type(v2) == str:
                    self.memoria[r] = self.memoria[v1] / float(v2)
                elif type(v1) == str and type(v2) == int:
                    self.memoria[r] = float(v1) / self.memoria[v2]
                elif type(v1) == int and type(v2) == int:
                    self.memoria[r] = self.memoria[v1] / self.memoria[v2]
                elif type(v1) == str and type(v2) == str:
                    self.memoria[r] = float(v1) / float(v2)
                i += 1
            elif op == 'PRINT':
                if type(r) == int:
                    print(self.memoria[r])
                    self.output.append(self.memoria[r])
                else:
                    print(r.strip('"'))
                    self.output.append(r.strip('"'))
                i += 1
            elif op == '<':
                if type(v1) == int and type(v2) == str:
                    self.memoria[r] = self.memoria[v1] < float(v2)
                elif type(v1) == str and type(v2) == int:
                    self.memoria[r] = float(v1) < self.memoria[v2]
                elif type(v1) == int and type(v2) == int:
                    self.memoria[r] = self.memoria[v1] < self.memoria[v2]
                elif type(v1) == str and type(v2) == str:
                    self.memoria[r] = float(v1) < float(v2)
                i += 1
            elif op == '>':
                if type(v1) == int and type(v2) == str:
                    self.memoria[r] = self.memoria[v1] > float(v2)
                elif type(v1) == str and type(v2) == int:
                    self.memoria[r] = float(v1) > self.memoria[v2]
                elif type(v1) == int and type(v2) == int:
                    self.memoria[r] = self.memoria[v1] > self.memoria[v2]
                elif type(v1) == str and type(v2) == str:
                    self.memoria[r] = float(v1) > float(v2)
                i += 1
            elif op == '%':
                if type(v1) == int and type(v2) == str:
                    self.memoria[r] = self.memoria[v1] != float(v2)
                elif type(v1) == str and type(v2) == int:
                    self.memoria[r] = float(v1) != self.memoria[v2]
                elif type(v1) == int and type(v2) == int:
                    self.memoria[r] = self.memoria[v1] != self.memoria[v2]
                elif type(v1) == str and type(v2) == str:
                    self.memoria[r] = float(v1) != float(v2)
                i += 1
            elif op == 'gotoV':
                if self.memoria[v1]:
                    i = int(r)-1
                    continue
                i += 1
            elif op == 'gotoF':
                if not self.memoria[v1]:
                    i = int(r)-1
                    continue
                i += 1
            elif op == 'goto':
                i = int(r)-1
            elif op == 'CTE_STRING' or 'VAR_PRINT':
                i += 1