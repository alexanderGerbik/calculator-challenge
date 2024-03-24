import pytest

from calculation.lexer import Lexer
from calculation.nodes import Value, Addition, Subtraction, Multiplication, Division, Power


@pytest.mark.parametrize("input,expected", [
    ("2 + 3", Addition(Value(2), Value(3))),
    ("2 - 3", Subtraction(Value(2), Value(3))),
    ("2 * 3", Multiplication(Value(2), Value(3))),
    ("2 / 3", Division(Value(2), Value(3))),
    (" 2.7 ^ 3.5", Power(Value(2.7), Value(3.5))),
    (" 2 / ( 16 - 3 ) ", Division(Value(2), Subtraction(Value(16), Value(3)))),
    (" 2 + 3 * 6", Addition(Value(2), Multiplication(Value(3), Value(6)))),
    (" 2 + 3 ^ 2 * 6", Addition(Value(2), Multiplication(Power(Value(3), Value(2)), Value(6)))),
    (" 2 - 3 + 6", Addition(Subtraction(Value(2), Value(3)), Value(6))),
    (" 4 / 2 * 3", Multiplication(Division(Value(4), Value(2)), Value(3))),
    (" 2 ^ 3 ^ 4", Power(Value(2), Power(Value(3), Value(4)))),
])
def test_lexer(input, expected):
    lexer = Lexer(input)
    assert lexer.get_ast() == expected


def test_extra_tokens__raise_error():
    with pytest.raises(Exception) as e_info:
        Lexer("3 * (4 + 5) 15").get_ast()
    assert e_info.value.args[0] == "Invalid expression: unexpected characters after parsed expression"


def test_no_matching_closing_parenthesis__raise_error():
    with pytest.raises(Exception) as e_info:
        Lexer("3 * (4 + 5").get_ast()
    assert e_info.value.args[0] == "Invalid expression: no matching closing parenthesis"


def test_no_matching_opening_parenthesis__raise_error():
    with pytest.raises(Exception) as e_info:
        Lexer("3 * 4 + 5)").get_ast()
    assert e_info.value.args[0] == "Invalid expression: unexpected characters after parsed expression"


def test_unexpected_operation__raise_error():
    with pytest.raises(Exception) as e_info:
        Lexer("3 * ( + 5)").get_ast()
    assert e_info.value.args[0] == "Invalid expression: expected number at pos 6"
