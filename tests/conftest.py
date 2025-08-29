import pytest
from app import create_app, db
from app.models import User  # ✅ ADD THIS LINE

@pytest.fixture(scope="function")
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",  # ✅ Fresh DB per test
        "WTF_CSRF_ENABLED": False
    })
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope="function")
def client(app):
    return app.test_client()


@pytest.fixture(scope="function")
def db_session(app):
    with app.app_context():
        db.create_all()
        yield db.session
        db.session.remove()
        db.drop_all()

# ✅ Ensures the DB is clean before every test
@pytest.fixture(autouse=True)
def clean_database(db_session):
    db_session.query(User).delete()
    db_session.commit()
