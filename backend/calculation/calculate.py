from calculation.nodes import Addition, Subtraction, Multiplication, Division, Power, Value, Negation


class CalculateVisitor:
    def calculate(self, ast):
        return ast.calculate()
