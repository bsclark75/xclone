import re
from bs4 import BeautifulSoup
from app.models import User
from app import db
from tests.utils import create_user, login, get_user_count

def test_index_including_pagination_and_delete_links(client, new_user, test_user):
    # log in as admin
    login(client, new_user.email, "password123", follow=True)

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


    # --- VERIFY PROFILE LINKS ---
    profile_links = [a["href"] for a in soup.select("ul.users li a") if re.match(r"^/users/\d+$", a.get("href", ""))]
    assert profile_links, "Expected at least one profile link"

    # --- VERIFY DELETE LINKS (only if admin) ---
    if new_user.admin:
        #print(soup.prettify())
        delete_links = [a["href"] for a in soup.select("ul.users li a") if re.match(r"^/users/\d+/delete$", a.get("href", ""))]
        assert delete_links, "Expected at least one delete link for admin"

    # remove a user
    before_count = get_user_count()
    response = client.post(f"/users/{test_user.id}/delete")
    after_count = get_user_count()
    assert after_count == before_count - 1

def test_index_as_non_admin(client, test_user):
    login(client, test_user.email, "password123")
    response = client.get("/users")
    soup = BeautifulSoup(response.data, "html.parser")
    delete_links = [a["href"] for a in soup.select("ul.users li a") if re.match(r"^/users/\d+/delete$", a.get("href", ""))]
    assert len(delete_links) == 0