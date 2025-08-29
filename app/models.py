from app.extensions import db
from datetime import datetime, UTC
from sqlalchemy.orm import validates
import re

class User(db.Model):
    __tablename__ = "users"  # optional, defaults to class name lowercased
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, index=True)
    email = db.Column(db.String(256), unique=True, nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(UTC))
    def __repr__(self):
        return f"<User {self.name}>"


    @validates("name")
    def validate_name(self, key, value):
        if not value or not value.strip():
            raise ValueError("Name cannot be empty or whitespace")
        if len(value) > 50:
            raise ValueError("Name can not be longer than 50 characters")
        return value

    @validates("email")
    def validate_email(self, key, value):
        # Normalize to lowercase for uniqueness
        value = value.strip().lower()

        # Check empty or whitespace
        if not value or not value.strip():
            raise ValueError("Email cannot be empty or whitespace")

        # Check max length
        if len(value) > 255:
            raise ValueError("Email cannot be longer than 255 characters")

        # Validate format using regex
        EMAIL_REGEX = re.compile(r"^[\w\.\+\-]+@[a-z\d\.\-]+\.[a-z]+$", re.IGNORECASE)
        if not EMAIL_REGEX.match(value):
            raise ValueError("Invalid email format")

        # Check uniqueness
        existing_user = User.query.filter_by(email=value).first()
        if existing_user and existing_user.id != self.id:
            raise ValueError("Email already exists")

        return value
