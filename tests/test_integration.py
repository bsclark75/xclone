import pytest

@pytest.mark.parametrize("route, expected_text", [
    ("/", b"<title>Home</title>"),
    ("/home", b"This is the home page"),
    ("/help", b"This is a holding page"),
    ("/about", b"This is an about page"),
    ("/contact", b"<title>Contact</title>"),
    ("/signup", b"<title>Sign Up</title>")
])
def test_static_routes(client, route, expected_text):
    """Ensure key routes return 200 and correct content."""
    response = client.get(route)
    assert response.status_code == 200
    assert expected_text in response.data


def test_static_css_served(client):
    response = client.get("/static/css/style.css")
    assert response.status_code == 200
    assert b"body" in response.data


def test_404_page(client):
    response = client.get("/not-a-real-page")
    assert response.status_code == 404


def test_navbar_links_present(client):
    response = client.get("/")
    assert b"Home" in response.data
    assert b"Help" in response.data
    assert b"Log in" in response.data
