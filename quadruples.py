class QuadrupleGenerator:
    def __init__(self): 
        self.quadruples = []
        self.temp_count = 0

    def new_temp(self):
        self.temp_count += 1
        return f't{self.temp_count}'

    def generate(self, expr):
        expr = expr.replace(" ", "")
        return self.parse_assignment(expr)

    def parse_assignment(self, expr):
        if '=' in expr:
            var, expr = expr.split('=')
            result = self.parse_expression(expr)
            self.quadruples.append(['=', result, '', var])
        else:
            return self.parse_expression(expr)

    def parse_expression(self, expr):
        if '(' in expr:
            return self.parse_parentheses(expr)
        else:
            return self.parse_simple_expr(expr)

    def parse_parentheses(self, expr):
        stack = []
        start = None
        for i, char in enumerate(expr):
            if char == '(':
                stack.append(i)
                if start is None:
                    start = i
            elif char == ')':
                start = stack.pop()
                if not stack:
                    sub_expr = expr[start + 1:i]
                    temp_var = self.parse_expression(sub_expr)
                    new_expr = expr[:start] + temp_var + expr[i + 1:]
                    return self.parse_expression(new_expr)
        return self.parse_simple_expr(expr)

    def parse_simple_expr(self, expr):
        operators = ['+', '-', '*', '/', '>', '<']
        for op in operators[::-1]:  # Start from the lowest precedence
            if op in expr:
                left, right = expr.split(op, 1)
                left_result = self.parse_expression(left)
                right_result = self.parse_expression(right)
                temp_var = self.new_temp()
                self.quadruples.append([op, left_result, right_result, temp_var])
                return temp_var
        return expr

# Example usage
expression = "x = (A+B)*(C-D) > E"
generator = QuadrupleGenerator()
generator.generate(expression)
for quad in generator.quadruples:
    print(quad)
