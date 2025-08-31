from app.extensions import db, bcrypt
from datetime import datetime, UTC
from sqlalchemy.orm import validates
import re

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, index=True)
    email = db.Column(db.String(256), unique=True, nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(UTC))
    password_digest = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"<User {self.name}>"

    # Use property-style setter to handle password hashing automatically
    def set_password(self, plaintext_password):
        if not plaintext_password or not plaintext_password.strip():
            raise ValueError("Password cannot be blank")
        if len(plaintext_password) < 6:
            raise ValueError("Password must be at least 6 characters")
        self.password_digest = bcrypt.generate_password_hash(plaintext_password).decode("utf-8")

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_digest, password)

    @validates("name")
    def validate_name(self, key, value):
        if not value or not value.strip():
            raise ValueError("Name cannot be empty or whitespace")
        if len(value) > 50:
            raise ValueError("Name cannot be longer than 50 characters")
        return value

    @validates("email")
    def validate_email(self, key, value):
        value = value.strip().lower()
        if not value:
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

