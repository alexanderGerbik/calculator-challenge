from flask import (
    Blueprint, request
)

from calculation import evaluate

bp = Blueprint('api', __name__, url_prefix='/api')


# worth adding versioning "/v1/evaluate" right away
# in order to be able to make backward incompatible API changes in future
@bp.route("/evaluate", methods=["POST"])
def evaluate_expression():
    data = request.json
    expression = data["expression"]
    result = evaluate(expression)
    return {"result": result}
