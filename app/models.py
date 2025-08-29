from app.extensions import db
from datetime import datetime, UTC
from sqlalchemy.orm import validates
from werkzeug.security import generate_password_hash, check_password_hash
import re

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, index=True)
    email = db.Column(db.String(256), unique=True, nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(UTC))
    password_digest = db.Column(db.String, nullable=False)

    # These are not stored in the DB, just for validation
    _password = None
    _password_confirmation = None

    # -------------------------
    # Password Property
    # -------------------------
    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        if not value or not value.strip():
            raise ValueError("Password can not be blank")
        if len(value.strip()) < 6:
            raise ValueError("Password must be at least 6 characters")
        self._password = value
        self.password_digest = generate_password_hash(value)

    # -------------------------
    # Password Confirmation
    # -------------------------
    @property
    def password_confirmation(self):
        return self._password_confirmation

    @password_confirmation.setter
    def password_confirmation(self, value):
        self._password_confirmation = value
        if self._password and value != self._password:
            raise ValueError("Password confirmation does not match")

    # -------------------------
    # Validate Name
    # -------------------------
    @validates("name")
    def validate_name(self, key, value):
        if not value or not value.strip():
            raise ValueError("Name cannot be empty or whitespace")
        if len(value) > 50:
            raise ValueError("Name can not be longer than 50 characters")
        return value

    # -------------------------
    # Validate Email
    # -------------------------
    @validates("email")
    def validate_email(self, key, value):
        value = value.strip().lower()
        if not value or not value.strip():
            raise ValueError("Email cannot be empty or whitespace")
        if len(value) > 255:
            raise ValueError("Email cannot be longer than 255 characters")

        EMAIL_REGEX = re.compile(r"^[\w\.\+\-]+@[a-z\d\.\-]+\.[a-z]+$", re.IGNORECASE)
        if not EMAIL_REGEX.match(value):
            raise ValueError("Invalid email format")

        existing_user = User.query.filter_by(email=value).first()
        if existing_user and existing_user.id != self.id:
            raise ValueError("Email already exists")
        return value

    # -------------------------
    # Password Check Helper
    # -------------------------
    def check_password(self, password):
        return check_password_hash(self.password_digest, password)

    def __repr__(self):
        return f"<User {self.name}>"
