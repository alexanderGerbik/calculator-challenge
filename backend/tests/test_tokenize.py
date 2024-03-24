import pytest

from calculation.tokens import Plus, Number, Caret, Slash, LeftPar, RightPar, Minus, Asterisk
from calculation.tokenize import Tokenizer


@pytest.mark.parametrize("input,expected", [
    ("2 + 3", [Number(2), Plus(), Number(3)]),
    ("2 - 3", [Number(2), Minus(), Number(3)]),
    ("2 * 3", [Number(2), Asterisk(), Number(3)]),
    ("2 / 3", [Number(2), Slash(), Number(3)]),
    (" 2.7 ^ 3.5", [Number(2.7), Caret(), Number(3.5)]),
    (" 2 / ( 16 - 3 ) ", [Number(2), Slash(), LeftPar(), Number(16), Minus(), Number(3), RightPar()]),
    ("2 + 3.17 - 5", [Number(2), Plus(), Number(3.17), Minus(), Number(5)]),
    ("14.15", [Number(14.15)]),
    ("14.", [Number(14.)]),
    (".15", [Number(.15)]),
])
def test_tokenize(input, expected):
    assert list(Tokenizer(input)) == expected


def test_improper_float__raise_error():
    with pytest.raises(ValueError) as e_info:
        list(Tokenizer("."))
    assert e_info.value.args[0] == "No sole '.' is allowed. Number should contain either integer or fractional part"


def test_unknown_character__raise_error():
    with pytest.raises(ValueError) as e_info:
        list(Tokenizer("3 - 5 % 7"))
    assert e_info.value.args[0] == f"Unexpected character: '%'."


def test_tokenize_lookahead():
    tokenizer = Tokenizer("2 - 3")

    assert tokenizer.get_next_token() == Number(2)
    assert tokenizer.peek() == Minus()
    assert tokenizer.get_next_token() == Minus()
    assert tokenizer.get_next_token() == Number(3)
    assert tokenizer.is_empty
