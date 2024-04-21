from .lexer import Lexer
from .exceptions import ParseError

def parse_json(input):
    return Lexer(input).parse()


__all__ = ['parse_json', 'ParseError']
