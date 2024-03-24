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
