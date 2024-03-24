from .calculate import CalculateVisitor
from .lexer import Lexer


def evaluate(expression):
    ast = Lexer(expression).get_ast()
    return CalculateVisitor().calculate(ast)
