from sqlalchemy import Column, String
from db import Base
import random
import string


def generate_random_id():
    """Generate a random 10-character alphanumeric ID."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10))


class AdminUser(Base):
    __tablename__ = "admin_users"

    id = Column(String(10), primary_key=True, index=True, default=generate_random_id)
    password = Column(String(255), nullable=False)
