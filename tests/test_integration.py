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

def test_contact(client):
    response = client.get("/contact")
    assert response.status_code == 200
    assert b"<title>Contact</title>" in response.data

def test_signup(client):
    response = client.get("/signup")
    assert response.status_code == 200
    assert b"<title>New user</title>" in response.data

def test_static_css_served(client):
    """Integration test: confirm compiled SCSS -> CSS is served"""
    response = client.get("/static/css/style.css")
    assert response.status_code == 200
    assert b"body" in response.data  # Ensure CSS contains valid content

def test_404_page(client):
    """Integration test: hitting an invalid route returns 404"""
    response = client.get("/not-a-real-page")
    assert response.status_code == 404

def test_navbar_links_present(client):
    response = client.get("/")
    assert b"Home" in response.data
    assert b"Help" in response.data
    assert b"Log in" in response.data
