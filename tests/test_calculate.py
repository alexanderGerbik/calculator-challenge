import pytest

from calculation.calculate import CalculateVisitor
from calculation.lexer import Lexer
from calculation.nodes import Value, Addition, Subtraction, Multiplication, Division, Power


@pytest.mark.parametrize("input,ast,expected", [
    ("2 + 3", Addition(Value(2), Value(3)), 5),
    ("2 - 3", Subtraction(Value(2), Value(3)), -1),
    ("2 * 3", Multiplication(Value(2), Value(3)), 6),
    ("2 / 3", Division(Value(2), Value(3)), 2 / 3),
    (" 2.7 ^ 3.5", Power(Value(2.7), Value(3.5)), 2.7 ** 3.5),
    (" 2 / ( 16 - 3 ) ", Division(Value(2), Subtraction(Value(16), Value(3))), 2 / 13),
    (" 2 + 3 * 6", Addition(Value(2), Multiplication(Value(3), Value(6))), 20),
    (" 2 + 3 ^ 2 * 6", Addition(Value(2), Multiplication(Power(Value(3), Value(2)), Value(6))), 56),
    (" 2 - 3 + 6", Addition(Subtraction(Value(2), Value(3)), Value(6)), 5),
    (" 4 / 2 * 3", Multiplication(Division(Value(4), Value(2)), Value(3)), 6),
    (" 2 ^ 3 ^ 4", Power(Value(2), Power(Value(3), Value(4))), 2 ** 81),
])
def test_calculate(input, ast, expected):
    visitor = CalculateVisitor()
    assert visitor.calculate(ast) == expected
