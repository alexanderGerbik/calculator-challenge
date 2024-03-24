from flask import (
    Blueprint, request
)

from calculation import evaluate, InvalidExpressionError

bp = Blueprint('api', __name__, url_prefix='/api')


@bp.after_request
def after_request(response):
    header = response.headers
    header["Access-Control-Allow-Origin"] = "*"
    header["Access-Control-Allow-Headers"] = "*"
    header["Access-Control-Allow-Methods"] = "*"
    return response


# worth adding versioning "/v1/evaluate" right away
# in order to be able to make backward incompatible API changes in future
@bp.route("/evaluate", methods=["POST"])
def evaluate_expression():
    data = request.json
    expression = data["expression"]
    try:
        result = evaluate(expression)
    except InvalidExpressionError as e:
        return ({"detail": str(e)}, 400)
    return {"result": result}
