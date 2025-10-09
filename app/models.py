from app.extensions import db, bcrypt
from sqlalchemy.orm import validates
from app.services.user_mailer import send_password_reset
#from sqlalchemy import event
import re
from datetime import datetime, timezone, timedelta

try:
    UTC = timezone.utc
except AttributeError:
    UTC = timezone.utc  # Fallback for Python < 3.11


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, index=True)
    email = db.Column(db.String(256), unique=True, nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(UTC))
    password_digest = db.Column(db.String, nullable=False)
    remember_digest = db.Column(db.String, nullable=True)
    admin = db.Column(db.Boolean, default=False)
    activation_digest = db.Column(db.String, unique=True, index=True)
    activated = db.Column(db.Boolean, default=False)
    activated_at = db.Column(db.DateTime)
    reset_digest = db.Column(db.String, unique=True, index=True)
    reset_sent_at = db.Column(db.DateTime)

    def __repr__(self):
        return f"<User {self.id, self.name, self.email, self.created_at, self.admin, self.activated}>"

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

    def new_token(self):
        import os
        import base64
        token = base64.urlsafe_b64encode(os.urandom(16)).decode('utf-8')
        return token
    
    def remember(self):
        token = self.new_token()
        self.remember_digest = bcrypt.generate_password_hash(token).decode('utf-8')
        db.session.commit()
        return token
    
    def authenticated(self, attribute: str, token: str) -> bool:
        """
    Checks if the given token matches the stored bcrypt digest
    for the specified attribute on the user object.

    attribute: e.g. 'activation' or 'password'
    token: plain text token to verify
    """
    # Look up e.g. user.activation_digest dynamically
        digest = getattr(self, f"{attribute}_digest", None)
        #print(f"DEBUG: models.py: {digest}")
        if not digest:  # no digest stored
            return False
        #print(f"DEBUG: models.py: token {token}")
        hash = bcrypt.check_password_hash(digest, token)
        #print(f"DEBUG: models.py: hash {hash}")
        return hash
        
    def forget(self):
        self.remember_digest = None
        db.session.commit()

    def create_activation_digest(self):
        token = self.new_token()
        self.activation_digest = bcrypt.generate_password_hash(token).decode('utf-8')
        return token
       
    def activate(self):
        self.activated = True
        self.activated_at = datetime.now(UTC)
        db.session.commit()

    def create_reset_digest(self):
        token = self.new_token()
        self.reset_digest = bcrypt.generate_password_hash(token).decode('utf-8')
        return token
    
    def send_password_reset_email(self, token):
        send_password_reset(self, token)

    def password_reset_expired(self):
        return self.reset_sent_at < datetime.now() - timedelta(hours=2)