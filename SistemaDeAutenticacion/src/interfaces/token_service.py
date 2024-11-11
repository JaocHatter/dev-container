from abc import ABC, abstractmethod
from src.models.user import User

class TokenService(ABC):
    @abstractmethod
    def generate_token(self, user: User) -> str:
        pass
    
    @abstractmethod
    def validate_token(self, token: str) -> dict:
        pass
    
    @abstractmethod
    def get_user_from_token(self, token: str) -> User:
        pass
