import pytest
from app import create_app


@pytest.fixture
def app():
    app = create_app()
    return app


@pytest.fixture
def client(app):
    return app.test_client()


def test_valid_expression__result_is_provided(client):
    response = client.post("/api/evaluate", json={"expression": "2+3*(4+5)"})
    assert response.status_code == 200
    assert response.json == {"result": 29}


@pytest.mark.parametrize("expression,expected_detail", [
    ("3 * (4 + 5) 15", "Invalid expression: unexpected characters after parsed expression"),
    ("3 * (4 + 5", "Invalid expression: no matching closing parenthesis"),
    ("3 * 4 + 5)", "Invalid expression: unexpected characters after parsed expression"),
    ("3 * 4 + )5", "Invalid expression: expected number at pos 8"),
    ("3 * ( + 5)", "Invalid expression: expected number at pos 6"),
    (".", "Invalid expression: no sole '.' is allowed, number should contain either integer or fractional part"),
    ("3 - 5 # 7", f"Invalid expression: unexpected character '#'."),
])
def test_invalid_expression__detailed_error(client, expression, expected_detail):
    response = client.post("/api/evaluate", json={"expression": expression})
    assert response.status_code == 400
    assert response.json == {"detail": expected_detail}
