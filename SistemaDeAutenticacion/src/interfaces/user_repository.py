from abc import ABC, abstractmethod
from src.models.user import User


class UserRepository(ABC):

    @abstractmethod
    def save(self, user: User) -> User:
        pass

    @abstractmethod
    def find_by_username(self, username: str) -> User:
        pass

    @abstractmethod
    def find_by_email(self, email: str) -> User:
        pass

    @abstractmethod
    def find_by_id(self, user_id: int) -> User:
        pass
