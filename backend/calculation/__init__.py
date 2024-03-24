from .calculate import CalculateVisitor
from .lexer import Lexer
from .exceptions import InvalidExpressionError

def evaluate(expression):
    ast = Lexer(expression).get_ast()
    return CalculateVisitor().calculate(ast)


__all__ = ['evaluate', 'InvalidExpressionError']
