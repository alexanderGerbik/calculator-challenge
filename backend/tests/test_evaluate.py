import pytest

from calculation import evaluate


@pytest.mark.parametrize("expression,expected", [
    ("13 % 4", 1),
    ("2 + 13 % 2 ^ 2", 3),
    ("(3 + 4) % (2 + 2)", 3),
    ("2 + 3", 5),
    ("2 - 3", -1),
    ("2 * 3", 6),
    ("2 / 3", 2 / 3),
    (" 2.7 ^ 3.5", 2.7 ** 3.5),
    (" 2 / ( 16 - 3 ) ", 2 / 13),
    (" 2 + 3 * 6", 20),
    (" 2 + 3 ^ 2 * 6", 56),
    (" 2 - 3 + 6", 5),
    (" 4 / 2 * 3", 6),
    (" 2 ^ 3 ^ 4", 2 ** 81),
])
def test_evaluate(expression, expected):
    assert evaluate(expression) == expected
