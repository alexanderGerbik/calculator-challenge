"""
Grammar:

expr
    : expr '+' term
    | expr '-' term
    | term
    ;

term
    : term '*' power
    | term '/' power
    | term '%' power
    | power
    ;

power
    : power '^' factor
    | factor
    ;

factor
    : '-' factor
    | '(' expr ')'
    | number_literal
    ;
"""
from .exceptions import InvalidExpressionError
from .tokenize import Tokenizer
from . import tokens, nodes


NODE_BY_TOKEN = {
    tokens.Plus: nodes.Addition,
    tokens.Minus: nodes.Subtraction,
    tokens.Asterisk: nodes.Multiplication,
    tokens.Slash: nodes.Division,
    tokens.Percent: nodes.Mod,
}


class Lexer(object):
    def __init__(self, input):
        self._tokenizer = Tokenizer(input)

    def get_ast(self):
        rv = self._expr()
        if not self._tokenizer.is_empty:
            raise InvalidExpressionError("unexpected characters after parsed expression")
        return rv

    def _expr(self):
        rv = self._term()
        # + and - are left-associative
        while isinstance(self._tokenizer.peek(), (tokens.Minus, tokens.Plus)):
            op_token = self._tokenizer.get_next_token()
            op = NODE_BY_TOKEN[type(op_token)]
            rhs = self._term()
            rv = op(rv, rhs)
        return rv

    def _term(self):
        rv = self._power()
        # * and / are left-associative
        while isinstance(self._tokenizer.peek(), (tokens.Asterisk, tokens.Slash, tokens.Percent)):
            op_token = self._tokenizer.get_next_token()
            op = NODE_BY_TOKEN[type(op_token)]
            rhs = self._power()
            rv = op(rv, rhs)
        return rv

    def _power(self):
        operands = [self._factor()]
        # ^ is right-associative
        while isinstance(self._tokenizer.peek(), tokens.Caret):
            self._tokenizer.get_next_token()
            rhs = self._factor()
            operands.append(rhs)
        rv = operands.pop()
        while operands:
            rv = nodes.Power(operands.pop(), rv)
        return rv

    def _factor(self):
        if isinstance(self._tokenizer.peek(), tokens.Minus):
            self._tokenizer.get_next_token()
            return nodes.Negation(self._factor())
        if isinstance(self._tokenizer.peek(), tokens.LeftPar):
            self._tokenizer.get_next_token()
            rv = self._expr()
            if not isinstance(self._tokenizer.peek(), tokens.RightPar):
                raise InvalidExpressionError("no matching closing parenthesis")
            self._tokenizer.get_next_token()
            return rv
        if not isinstance(self._tokenizer.peek(), tokens.Number):
            raise InvalidExpressionError(f"expected number at pos {self._tokenizer.peek_pos}")
        token = self._tokenizer.get_next_token()
        return nodes.Value(token.value)
