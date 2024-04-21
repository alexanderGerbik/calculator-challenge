import pytest

from parse_json import parse_json
from parse_json.exceptions import ParseError
from parse_json.tokens import (
    Number,
    LeftBracket,
    RightBracket,
    LeftBrace,
    RightBrace,
    String,
    Colon,
    Comma,
    BoolTrue,
    BoolFalse,
    Null,
)
from parse_json.tokenize import Tokenizer


@pytest.mark.parametrize("input,expected", [
    ("""{"qwe": [true, false, 13], "asd": null}""", {"qwe": [True, False, 13], "asd": None}),
    ("""[true, false, [true, false, 13]]""", [True, False, [True, False, 13]]),
    ("""[true, false,]""", [True, False]),
    ("""{"qwe": true, "asd": null,}""", {"qwe": True, "asd": None}),
    ("""[true, /* some \n multi-line \n comment */ false]""", [True, False]),
    ("""[true, // some comment \n false]""", [True, False]),
    ("""[true, /* some \n multi-line \n comment *//* some \n multi-line \n comment */ false]""", [True, False]),
    ("""[true, // some comment \n  // some comment \n // some comment \n false]""", [True, False]),
    ("""[true, // some comment \n/* some \n multi-line \n comment */ false]""", [True, False]),
    ("""[true, false] // some comment""", [True, False]),
])
def test_parse_json(input, expected):
    assert parse_json(input) == expected


@pytest.mark.parametrize("input,expected", [
    ("123", 123),
    ("-123", -123),
    ("-123.425", -123.425),

    ("123e3", 123000),
    ("-123E3", -123000),
    ("-123.425e3", -123425),

    ("123e-2", 1.23),
    ("-123E-2", -1.23),
    ("-123.425e-2", -1.23425),
])
def test_tokenize_number(input, expected):
    assert list(Tokenizer(input))[0].value == expected


def test_tokenize():
    input = """{
        "qwe": [true, false, 13],
        "asd": null
    }"""
    expected = [
        LeftBrace(), String("qwe"), Colon(), LeftBracket(), BoolTrue(), Comma(), BoolFalse(), Comma(), Number(13),
        RightBracket(), Comma(), String("asd"), Colon(), Null(), RightBrace()]
    assert list(Tokenizer(input)) == expected


def test_improper_float__raise_error():
    with pytest.raises(ParseError) as e_info:
        list(Tokenizer("23."))
    assert str(e_info.value) == "Parse error: There should be a fractional part after dot."


def test_improper_comment__raise_error():
    with pytest.raises(ParseError) as e_info:
        parse_json("[true, / some comment \n false]")
    assert str(e_info.value) == "Parse error: unexpected character '/'."


def test_improper_exponent__raise_error():
    with pytest.raises(ParseError) as e_info:
        list(Tokenizer("23.13e"))
    assert str(e_info.value) == "Parse error: There should be an exponent after e/E."


def test_unknown_character__raise_error():
    with pytest.raises(ParseError) as e_info:
        list(Tokenizer("{#}"))
    assert str(e_info.value) == "Parse error: unexpected character '#'."

def test_unclosed_string__raise_error():
    with pytest.raises(ParseError) as e_info:
        list(Tokenizer('"qweasd'))
    assert str(e_info.value) == "Parse error: EOF reached while looking for end of string."

def test_unclosed_quoted_string__raise_error():
    with pytest.raises(ParseError) as e_info:
        list(Tokenizer('"qweasd\\"'))
    assert str(e_info.value) == "Parse error: EOF reached while looking for end of string."


def test_tokenize_lookahead():
    tokenizer = Tokenizer("[ 3 ]")

    assert tokenizer.get_next_token() == LeftBracket()
    assert tokenizer.peek() == Number(3)
    assert tokenizer.get_next_token() == Number(3)
    assert tokenizer.get_next_token() == RightBracket()
    assert tokenizer.is_empty
