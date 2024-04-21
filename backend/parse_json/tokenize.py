import string

from .exceptions import ParseError
from .tokens import CharToken, KeywordToken, String, Number

DIGITS = set(string.digits)
WHITESPACE = set(string.whitespace)


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
        rv = self._parse_next_token_no_ws()
        self._skip_whitespace()
        return rv

    def _parse_next_token_no_ws(self):
        if self:
            return None
        token = CharToken.try_parse(self._current_char)
        if token is not None:
            self._pos += 1
            return token
        token = KeywordToken.try_parse(self._input, self._pos)
        if token is not None:
            self._pos += token.length
            return token
        token = self._try_parse_string()
        if token:
            return token
        token = self._try_parse_number()
        if not token:
            raise ParseError(f"unexpected character '{self._current_char}'.")
        return token

    def _try_parse_string(self):
        if self or self._current_char != '"':
            return None
        self._pos += 1
        start_pos = self._pos
        while not (self or self._is_string_end(self._pos)):
            self._pos += 1
        if self:
            raise ParseError("EOF reached while looking for end of string.")
        end_pos = self._pos
        self._pos += 1
        return String(self._input[start_pos:end_pos])

    def _is_string_end(self, pos):
         return self._input[pos-1] != "\\" and self._input[pos] == '"'

    def _try_parse_number(self):
        is_negative = self._parse_sign()
        integer_part = self._try_parse_digits()
        if not integer_part:
            return None
        fractional_part = self._parse_fractional()
        exponent = self._parse_exponent()
        value = int(integer_part)
        value += fractional_part
        value = value * exponent
        if is_negative:
            value = -value
        return Number(value)

    def _parse_fractional(self):
        if not self and self._current_char == ".":
            self._pos += 1
            fractional_part = self._try_parse_digits()
            if not fractional_part:
                raise ParseError("There should be a fractional part after dot.")
            return float(f".{fractional_part}")
        return 0

    def _parse_exponent(self):
        if not self and self._current_char.lower() == "e":
            self._pos += 1
            is_negative = self._parse_sign()
            exponent = self._try_parse_digits()
            if not exponent:
                raise ParseError("There should be an exponent after e/E.")
            exponent = int(exponent)
            if is_negative:
                exponent = - exponent
            return 10 ** exponent
        return 1

    def _parse_sign(self):
        if not self and self._current_char == "-":
            self._pos += 1
            return True
        if not self and self._current_char == "+":
            self._pos += 1
            return False
        return False

    def _try_parse_digits(self):
        result = ""
        while not self and self._current_char in DIGITS:
            result += self._current_char
            self._pos += 1
        return result

    def _skip_whitespace(self):
        while True:
            while not self and self._current_char in WHITESPACE:
                self._pos += 1
            a = self._skip_comment()
            if not a:
                break

    def _skip_comment(self):
        if not self and self._current_char == "/":
            self._pos += 1
            if not self and self._current_char == "/":
                self._pos += 1
                while not self and self._current_char != "\n":
                    self._pos += 1
                if not self:
                    self._pos += 1
                return True
            elif not self and self._current_char == "*":
                self._pos += 2
                while not self and (self._input[self._pos-1] != "*" or self._current_char != "/"):
                    self._pos += 1
                if not self:
                    self._pos += 1
                return True
            else:
                self._pos -= 1
                raise ParseError(f"unexpected character '{self._current_char}'.")
        return False

    def __bool__(self):
        return self._pos >= len(self._input)

    @property
    def _current_char(self):
        return self._input[self._pos]
