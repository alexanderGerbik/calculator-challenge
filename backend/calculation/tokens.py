from typing import Optional


class Token:
    pass


_char_token_factories = {}


class CharToken:
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        assert hasattr(cls, 'char'), "CharToken must have a 'char' attribute"
        assert cls.char not in _char_token_factories, ("Duplicated 'char' used for"
                                                       f" {cls} and {_char_token_factories[cls.char]}")
        _char_token_factories[cls.char] = cls

    @classmethod
    def try_parse(cls, char) -> Optional['CharToken']:
        if char not in _char_token_factories:
            return None
        return _char_token_factories[char]()

    def __repr__(self):
        return self.char

    def __eq__(self, other):
        return type(self) == type(other)


class Plus(CharToken):
    char = "+"


class Minus(CharToken):
    char = "-"


class Asterisk(CharToken):
    char = "*"


class Slash(CharToken):
    char = "/"


class Percent(CharToken):
    char = "%"


class Caret(CharToken):
    char = "^"


class LeftPar(CharToken):
    char = "("


class RightPar(CharToken):
    char = ")"


class Number(Token):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return str(self.value)

    def __eq__(self, other):
        return isinstance(other, Number) and self.value == other.value
