import jwt
from datetime import datetime, timedelta
from src.interfaces.token_service import TokenService
from src.interfaces.user_repository import UserRepository
from src.models.user import User
from src.exceptions import InvalidTokenError


# Usamos la clase abstracta TokenService para definir la interfaz
class JWTTokenService(TokenService):
    def __init__(self, secret_key: str, user_repository: UserRepository):
        self.secret_key = secret_key
        self.user_repository = user_repository

    def generate_token(self, user: User) -> str:
        payload = {
            'user_id': user.id,
            'username': user.username,
            'roles': user.roles,
            'exp': datetime.now() + timedelta(hours=24)
        }
        return jwt.encode(payload, self.secret_key, algorithm='HS256')

    def validate_token(self, token: str) -> dict:
        try:
            return jwt.decode(token, self.secret_key, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise InvalidTokenError("El token ha expirado")
        except jwt.InvalidTokenError:
            raise InvalidTokenError("Token inválido")

    def get_user_from_token(self, token: str) -> User:
        payload = self.validate_token(token)
        user = self.user_repository.find_by_id(payload['user_id'])
        if not user:
            raise InvalidTokenError("Usuario no encontrado")
        return user