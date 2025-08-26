import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    return app.test_client()

def test_index(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"<title>Home</title>" in response.data

def test_home(client):
    response = client.get("/home")
    assert response.status_code == 200
    assert b"This is the home page" in response.data

def test_help(client):
    response = client.get("/help")
    assert response.status_code == 200
    assert b"This is a holding page" in response.data

def test_about(client):
    response = client.get("/about")
    assert response.status_code == 200
    assert b"This is an about page" in response.data
