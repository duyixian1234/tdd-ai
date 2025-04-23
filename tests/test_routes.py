from fastapi.testclient import TestClient
from main import app
import pytest


@pytest.fixture(scope="module")
def client():
    yield TestClient(app)


def test_get_status(client):
    response = client.get("/status")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert isinstance(data["ts"], int)


def test_empty_endpoint(client):
    response = client.get("/")
    assert response.status_code == 404


@pytest.mark.parametrize(
    "email,expected_valid",
    [
        ("test@example.com", True),
        ("user.name+tag+sorting@example.com", True),
        ("user_name@example.co.uk", True),
        ("user-name@sub.example.com", True),
        ("plainaddress", False),
        ("@missingusername.com", False),
        ("username@.com", False),
        ("username@com", False),
        ("username@.com.", False),
        ("username@-example.com", False),
        ("username@example..com", False),
        ("", False),
    ],
)
def test_email_validate(client, email, expected_valid):
    response = client.post("/email-validate", json={"email": email})
    assert response.status_code == 200
    data = response.json()
    assert "valid" in data
    assert data["valid"] == expected_valid
