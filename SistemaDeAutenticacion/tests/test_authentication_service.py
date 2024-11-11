import pytest
import sys
import os

# Agrega el directorio raíz del proyecto al PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import bcrypt
from src.services.authentication_service import AuthenticationService
from src.models.user import User
from src.exceptions import AuthenticationError, UserAlreadyExistsError

class MockUserRepository:
    def __init__(self):
        self.users = {}
        self.next_id = 1
    
    def save(self, user):
        user.id = self.next_id
        self.next_id += 1
        self.users[user.username] = user
        return user
    
    def find_by_username(self, username):
        return self.users.get(username)
    
    def find_by_email(self, email):
        return next((u for u in self.users.values() if u.email == email), None)
    
    def find_by_id(self, user_id):
        return next((u for u in self.users.values() if u.id == user_id), None)

class MockTokenService:
    def generate_token(self, user):
        return f"mock_token_{user.username}"
    
    def validate_token(self, token):
        return {"user_id": 1}
    
    def get_user_from_token(self, token):
        return User("test", "hash", "test@test.com", 1)

def test_successful_registration():
    auth_service = AuthenticationService(MockUserRepository(), MockTokenService())
    user = auth_service.register("testuser", "password123", "test@test.com")
    assert user.username == "testuser"
    assert user.email == "test@test.com"
    assert bcrypt.checkpw("password123".encode(), user.password_hash.encode())

def test_duplicate_username():
    auth_service = AuthenticationService(MockUserRepository(), MockTokenService())
    auth_service.register("testuser", "password123", "test@test.com")
    with pytest.raises(UserAlreadyExistsError):
        auth_service.register("testuser", "password123", "other@test.com")

def test_successful_authentication():
    auth_service = AuthenticationService(MockUserRepository(), MockTokenService())
    auth_service.register("testuser", "password123", "test@test.com")
    token = auth_service.authenticate("testuser", "password123")
    assert token == "mock_token_testuser"

def test_failed_authentication():
    auth_service = AuthenticationService(MockUserRepository(), MockTokenService())
    auth_service.register("testuser", "password123", "test@test.com")
    with pytest.raises(AuthenticationError):
        auth_service.authenticate("testuser", "wrongpassword")
