import re
from bs4 import BeautifulSoup
from app.models import User
from app import db
from tests.utils import create_user, login

def test_index_including_pagination(client):
    # Create a user and log in
    user1 = create_user()
    login(client, user1.email, "password123", follow=True)

    # Create extra users so pagination exists
    for i in range(6):
        create_user(name=f"User {i}", email=f"user{i}@example.com")

    # Request /users page
    response = client.get("/users?page=1&size=5")
    assert response.status_code == 200

    # Parse HTML using BeautifulSoup
    soup = BeautifulSoup(response.data, "html.parser")

    # --- VERIFY PAGINATION EXISTS ---
    pagination_container = soup.select_one("div.text-center")
    assert pagination_container is not None, "Pagination container missing"

    # If more than 1 page, expect links
    if "page=2" in response.data.decode():
        pagination_links = pagination_container.find_all("a")
        assert len(pagination_links) > 0, "Expected pagination links, found none"


    # --- VERIFY USER LINKS ARE VALID ---
    user_links = soup.select("ul.users li a")
    assert len(user_links) > 0, "Expected at least one user link"

    for link in user_links:
        href = link.get("href")
        assert href is not None, "User link missing href attribute"
        assert re.match(r"^/users/\d+$", href), f"Invalid user link format: {href}"


    