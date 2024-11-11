import bcrypt
from src.models.user import User
from src.interfaces.user_repository import UserRepository
from src.interfaces.token_service import TokenService
from src.exceptions import AuthenticationError, UserAlreadyExistsError


class AuthenticationService:
    def __init__(self, user_repository: UserRepository,
                 token_service: TokenService):
        self.user_repository = user_repository
        self.token_service = token_service

    def register(self, username: str, password: str, email: str) -> User:
        if self.user_repository.find_by_username(username):
            raise UserAlreadyExistsError("El usuario ya existe")
        if self.user_repository.find_by_email(email):
            raise UserAlreadyExistsError("El email ya está en uso")

        password_hash = bcrypt.hashpw(password.encode(),
                                      bcrypt.gensalt()).decode()
        user = User(username=username,
                    password_hash=password_hash,
                    email=email,
                    id=None,
                    roles=["user"])
        return self.user_repository.save(user)

    def authenticate(self, username: str, password: str) -> str:
        user = self.user_repository.find_by_username(username)
        if not user:
            raise AuthenticationError("Credenciales inválidas")

        if not bcrypt.checkpw(password.encode(), user.password_hash.encode()):
            raise AuthenticationError("Credenciales inválidas")

        return self.token_service.generate_token(user)

    def validate_token(self, token: str) -> User:
        return self.token_service.get_user_from_token(token)