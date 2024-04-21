from typing import Optional


class Token:
    pass


_char_token_factories = {}
_keyword_token_factories = {}


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


class Comma(CharToken):
    char = ","


class Colon(CharToken):
    char = ":"


class LeftBrace(CharToken):
    char = "{"


class RightBrace(CharToken):
    char = "}"


class LeftBracket(CharToken):
    char = "["


class RightBracket(CharToken):
    char = "]"


class KeywordToken:
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        assert hasattr(cls, 'keyword'), "KeywordToken must have a 'keyword' attribute"
        assert cls.keyword not in _keyword_token_factories, (
            f"Duplicated 'keyword' used for {cls} and {_keyword_token_factories[cls.keyword]}"
        )
        _keyword_token_factories[cls.keyword] = cls

    @classmethod
    def try_parse(cls, input, pos) -> Optional['KeywordToken']:
        for keyword, factory in _keyword_token_factories.items():
            substr = input[pos:pos+len(keyword)]
            if substr == keyword:
                return factory()
        return None

    @property
    def length(self):
        return len(self.keyword)

    def __repr__(self):
        return self.keyword

    def __eq__(self, other):
        return type(self) == type(other)


class BoolTrue(KeywordToken):
    keyword = "true"

    @property
    def value(self):
        return True


class BoolFalse(KeywordToken):
    keyword = "false"

    @property
    def value(self):
        return False


class Null(KeywordToken):
    keyword = "null"

    @property
    def value(self):
        return None


class String(Token):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return str(self.value)

    def __eq__(self, other):
        return isinstance(other, String) and self.value == other.value


class Number(Token):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return str(self.value)

    def __eq__(self, other):
        return isinstance(other, Number) and self.value == other.value
