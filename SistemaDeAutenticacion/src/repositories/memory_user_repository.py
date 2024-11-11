from src.interfaces.user_repository import UserRepository
from src.models.user import User

class MemoryUserRepository(UserRepository):
    def __init__(self):
        self.users = {}
        self.email_index = {}
        self.next_id = 1
    
    def save(self, user: User) -> User:
        if user.id is None:
            user.id = self.next_id
            self.next_id += 1
        self.users[user.username] = user
        self.email_index[user.email] = user
        return user
    
    def find_by_username(self, username: str) -> User:
        return self.users.get(username)
    
    def find_by_email(self, email: str) -> User:
        return self.email_index.get(email)
    
    def find_by_id(self, user_id: int) -> User:
        for user in self.users.values():
            if user.id == user_id:
                return user
        return None