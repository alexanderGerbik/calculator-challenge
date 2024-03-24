from calculation.nodes import Addition, Subtraction, Multiplication, Division, Power, Value, Negation


class CalculateVisitor:
    def calculate(self, ast):
        return self._visit(ast)

    def _visit(self, node):
        """Visit a node."""
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method)
        return visitor(node)

    def visit_Addition(self, node: Addition):
        return self._visit(node.left_operand) + self._visit(node.right_operand)

    def visit_Subtraction(self, node: Subtraction):
        return self._visit(node.left_operand) - self._visit(node.right_operand)

    def visit_Multiplication(self, node: Multiplication):
        return self._visit(node.left_operand) * self._visit(node.right_operand)

    def visit_Division(self, node: Division):
        return self._visit(node.left_operand) / self._visit(node.right_operand)

    def visit_Power(self, node: Power):
        return self._visit(node.left_operand) ** self._visit(node.right_operand)

    def visit_Value(self, node: Value):
        return node.value

    def visit_Negation(self, node: Negation):
        return -self._visit(node.operand)
