class QuadrupleGenerator:
    def __init__(self): 
        self.temp_count = 0

    def new_temp(self):
        self.temp_count += 1
        return f't{self.temp_count}'

    def generate(self, expr):
        expr = expr.replace(" ", "")
        quadruples = []
        self.parse_assignment(expr, quadruples)
        return quadruples

    def parse_assignment(self, expr, quadruples):
        if '=' in expr:
            var, expr = expr.split('=')
            result = self.parse_expression(expr, quadruples)
            quadruples.append(['=', result, '', var])
        else:
            return self.parse_expression(expr, quadruples)

    def parse_expression(self, expr, quadruples):
        if '(' in expr:
            return self.parse_parentheses(expr, quadruples)

        for operators in ['><', '+-', '*/']:
            result = self.split_at_operator(expr, operators)
            if result:
                left, op, right = result
                left_result = self.parse_expression(left, quadruples)
                right_result = self.parse_expression(right, quadruples)
                temp_var = self.new_temp()
                quadruples.append([op, left_result, right_result, temp_var])
                return temp_var
        return expr

    def parse_parentheses(self, expr, quadruples):
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
                    temp_var = self.parse_expression(sub_expr, quadruples)
                    new_expr = expr[:start] + temp_var + expr[i + 1:]
                    return self.parse_expression(new_expr, quadruples)
        return self.parse_expression(expr, quadruples)

    def split_at_operator(self, expr, operators):
        depth = 0
        for i in range(len(expr) - 1, -1, -1):
            if expr[i] == ')':
                depth += 1
            elif expr[i] == '(':
                depth -= 1
            elif depth == 0 and expr[i] in operators:
                return expr[:i], expr[i], expr[i+1:]
        return None
