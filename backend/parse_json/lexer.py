"""
Grammar:

document
    : value
    ;

value
    : object
    | array
    | string
    | number
    | "true"
    | "false"
    | "null"
    ;

object
    : '{' '}'
    | '{' member (',' member)* '}'
    ;

member
    : string ':' value
    ;

array
    : '[' ']'
    | '[' value (',' value)* ']'
    ;
"""
from .exceptions import ParseError
from .tokenize import Tokenizer
from . import tokens


class Lexer(object):
    def __init__(self, input):
        self._tokenizer = Tokenizer(input)

    def parse(self):
        rv = self._value()
        if not self._tokenizer.is_empty:
            raise ParseError("unexpected characters after parsed json document")
        return rv

    def _value(self):
        if isinstance(self._tokenizer.peek(), (tokens.Number, tokens.String, tokens.Null, tokens.BoolTrue, tokens.BoolFalse)):
            token = self._tokenizer.get_next_token()
            return token.value
        if isinstance(self._tokenizer.peek(), tokens.LeftBrace):
            return self._object()
        if isinstance(self._tokenizer.peek(), tokens.LeftBracket):
            return self._array()
        raise ParseError(f"Unexpected token: {self._tokenizer.peek()}")

    def _assert_pop(self, expected_type):
        token = self._tokenizer.get_next_token()
        if not isinstance(token, expected_type):
            raise ParseError(f"Unexpected token. Got: {type(token)}, expected: {expected_type}")
        return token

    def _object(self):
        rv = {}
        self._assert_pop(tokens.LeftBrace)
        self._member(rv)
        while isinstance(self._tokenizer.peek(), tokens.Comma):
            self._tokenizer.get_next_token()
            if isinstance(self._tokenizer.peek(), tokens.RightBrace):
                break
            self._member(rv)
        self._assert_pop(tokens.RightBrace)
        return rv

    def _member(self, rv):
        key = self._assert_pop(tokens.String).value
        self._assert_pop(tokens.Colon)
        value = self._value()
        rv[key] = value

    def _array(self):
        rv = []
        self._assert_pop(tokens.LeftBracket)
        rv.append(self._value())
        while isinstance(self._tokenizer.peek(), tokens.Comma):
            self._tokenizer.get_next_token()
            if isinstance(self._tokenizer.peek(), tokens.RightBracket):
                break
            rv.append(self._value())
        self._assert_pop(tokens.RightBracket)
        return rv
