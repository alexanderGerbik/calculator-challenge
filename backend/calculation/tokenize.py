import string

from .exceptions import InvalidExpressionError
from .tokens import CharToken, Number

DIGITS = set(string.digits)


class Tokenizer:
    def __init__(self, input):
        self._pos = 0
        self._input = input
        self._skip_whitespace()
        self._buffer = None
        self.peek_pos = None

    def __iter__(self):
        while not self.is_empty:
            yield self.get_next_token()

    def get_next_token(self):
        if self._buffer is not None:
            rv = self._buffer
            self._buffer = None
            self.peek_pos = None
            return rv
        return self._parse_next_token()

    def peek(self):
        if self._buffer is None:
            self.peek_pos = self._pos
            self._buffer = self._parse_next_token()
        return self._buffer

    @property
    def is_empty(self):
        return self._buffer is None and self._pos >= len(self._input)

    def _parse_next_token(self):
        if self:
            return None
        token = CharToken.try_parse(self._current_char)
        if token is not None:
            self._pos += 1
            self._skip_whitespace()
            return token
        token = self._try_parse_number()
        if not token:
            raise InvalidExpressionError(f"unexpected character '{self._current_char}'.")
        self._skip_whitespace()
        return token

    def _try_parse_number(self):
        integer_part = self._try_parse_digits()
        if not self and self._current_char == ".":
            self._pos += 1
            fractional_part = self._try_parse_digits()
            if not integer_part and not fractional_part:
                raise InvalidExpressionError("no sole '.' is allowed, number should contain either integer or fractional part")
            return Number(float(f"{integer_part}.{fractional_part}"))
        return Number(int(f"{integer_part}")) if integer_part else None

    def _try_parse_digits(self):
        result = ""
        while not self and self._current_char in DIGITS:
            result += self._current_char
            self._pos += 1
        return result

    def _skip_whitespace(self):
        while not self and self._current_char == " ":
            self._pos += 1

    def __bool__(self):
        return self._pos >= len(self._input)

    @property
    def _current_char(self):
        return self._input[self._pos]
