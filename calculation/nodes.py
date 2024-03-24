class Node:
    pass


class BinaryOperation(Node):
    def __init__(self, left_operand, right_operand):
        self.left_operand = left_operand
        self.right_operand = right_operand

    def __repr__(self):
        return f"{self.__class__.__name__}({self.left_operand}, {self.right_operand})"

    def __eq__(self, other):
        return (
            type(self) == type(other)
            and self.left_operand == other.left_operand
            and self.right_operand == other.right_operand
        )


class Addition(BinaryOperation):
    pass


class Subtraction(BinaryOperation):
    pass


class Multiplication(BinaryOperation):
    pass


class Division(BinaryOperation):
    pass


class Power(BinaryOperation):
    pass


class Negation(Node):
    def __init__(self, operand):
        self.operand = operand

    def __repr__(self):
        return f"{self.__class__.__name__}({self.operand})"

    def __eq__(self, other):
        return (
            type(self) == type(other)
            and self.operand == other.operand
        )


class Value(Node):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"{self.__class__.__name__}({self.value})"

    def __eq__(self, other):
        return (
            type(self) == type(other)
            and self.value == other.value
        )
