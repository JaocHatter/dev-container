import pytest
import sys
import os

# Agrega el directorio raíz del proyecto al PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import jwt
from datetime import datetime, timedelta
from src.services.jwt_token_service import JWTTokenService
from src.models.user import User
from src.exceptions import InvalidTokenError

class MockUserRepository:
    def __init__(self, test_user=None):
        self.test_user = test_user or User(
            username="jared",
            password_hash="hash",
            email="test@test.com",
            id=1,
            roles=["user"]
        )
    
    def find_by_id(self, user_id):
        return self.test_user if user_id == self.test_user.id else None

@pytest.fixture
def token_service():
    return JWTTokenService("janedoe666", MockUserRepository())

@pytest.fixture
def test_user():
    return User(
        username="jared",
        password_hash="hash",
        email="test@test.com",
        id=1,
        roles=["user"]
    )

def test_generate_token(token_service, test_user):
    token = token_service.generate_token(test_user)
    assert isinstance(token, str)
    
    decoded = jwt.decode(token, "janedoe666", algorithms=['HS256'])
    assert decoded['user_id'] == test_user.id
    assert decoded['username'] == test_user.username
    assert decoded['roles'] == test_user.roles
    assert 'exp' in decoded

def test_validate_token(token_service, test_user):
    token = token_service.generate_token(test_user)
    payload = token_service.validate_token(token)
    
    assert payload['user_id'] == test_user.id
    assert payload['username'] == test_user.username
    assert payload['roles'] == test_user.roles

def test_validate_expired_token(token_service, test_user):
    payload = {
        'user_id': test_user.id,
        'username': test_user.username,
        'roles': test_user.roles,
        'exp': datetime.utcnow() - timedelta(hours=1)
    }
    expired_token = jwt.encode(payload, "janedoe666", algorithm='HS256')
    
    with pytest.raises(InvalidTokenError, match="El token ha expirado"):
        token_service.validate_token(expired_token)

def test_validate_invalid_token(token_service):
    with pytest.raises(InvalidTokenError, match="Token inválido"):
        token_service.validate_token("invalid.token.string")

def test_get_user_from_token(token_service, test_user):
    token = token_service.generate_token(test_user)
    user = token_service.get_user_from_token(token)
    
    assert user.id == test_user.id
    assert user.username == test_user.username
    assert user.email == test_user.email

def test_get_user_from_token_user_not_found(token_service):
    non_existent_user = User(
        username="nonexistent",
        password_hash="hash",
        email="none@test.com",
        id=999,
        roles=["user"]
    )
    token = token_service.generate_token(non_existent_user)
    
    with pytest.raises(InvalidTokenError, match="Usuario no encontrado"):
        token_service.get_user_from_token(token)
