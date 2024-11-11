import pytest
import sys
import os

# Agrega el directorio raíz del proyecto al PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.repositories.memory_user_repository import MemoryUserRepository
from src.models.user import User

@pytest.fixture
def repository():
    return MemoryUserRepository()

@pytest.fixture
def sample_user():
    return User(
        username="testuser",
        password_hash="hash123",
        email="test@example.com"
    )

def test_save_new_user(repository, sample_user):
    saved_user = repository.save(sample_user)
    assert saved_user.id is not None
    assert saved_user.username == "testuser"
    assert saved_user.email == "test@example.com"
    assert saved_user.password_hash == "hash123"

def test_save_existing_user(repository, sample_user):
    # First save
    first_save = repository.save(sample_user)
    first_id = first_save.id
    
    # Update and save again
    first_save.email = "updated@example.com"
    updated_user = repository.save(first_save)
    
    assert updated_user.id == first_id
    assert updated_user.email == "updated@example.com"
    assert len(repository.users) == 1

def test_find_by_username(repository, sample_user):
    repository.save(sample_user)
    found_user = repository.find_by_username("testuser")
    assert found_user is not None
    assert found_user.username == "testuser"
    
    # Test non-existent user
    assert repository.find_by_username("nonexistent") is None

def test_find_by_email(repository, sample_user):
    repository.save(sample_user)
    found_user = repository.find_by_email("test@example.com")
    assert found_user is not None
    assert found_user.email == "test@example.com"
    
    # Test non-existent email
    assert repository.find_by_email("nonexistent@example.com") is None

def test_find_by_id(repository, sample_user):
    saved_user = repository.save(sample_user)
    found_user = repository.find_by_id(saved_user.id)
    assert found_user is not None
    assert found_user.id == saved_user.id
    
    # Test non-existent ID
    assert repository.find_by_id(999) is None

def test_multiple_users(repository):
    user1 = User("user1", "hash1", "user1@example.com")
    user2 = User("user2", "hash2", "user2@example.com")
    
    repository.save(user1)
    repository.save(user2)
    
    assert len(repository.users) == 2
    assert repository.find_by_username("user1") is not None
    assert repository.find_by_username("user2") is not None
    assert repository.find_by_email("user1@example.com") is not None
    assert repository.find_by_email("user2@example.com") is not None

def test_id_generation(repository):
    user1 = User("user1", "hash1", "user1@example.com")
    user2 = User("user2", "hash2", "user2@example.com")
    
    saved1 = repository.save(user1)
    saved2 = repository.save(user2)
    
    assert saved1.id == 1
    assert saved2.id == 2
