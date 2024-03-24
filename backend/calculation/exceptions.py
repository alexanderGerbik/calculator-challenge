class InvalidExpressionError(ValueError):
    def __init__(self, detail):
        self.detail = detail

    def __str__(self):
        return f"Invalid expression: {self.detail}"