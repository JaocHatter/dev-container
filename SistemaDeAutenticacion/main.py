from src.services.authentication_service import AuthenticationService
from src.services.jwt_token_service import JWTTokenService
from src.repositories.memory_user_repository import MemoryUserRepository
from src.exceptions import AuthenticationError, UserAlreadyExistsError, InvalidTokenError


def main():
    # Creamos un repositorio de usuarios en memoria
    user_repository = MemoryUserRepository()
    # Creamos un servicio de tokens PyJWT
    token_service = JWTTokenService("janedoe123", user_repository)
    # Creamos un servicio de autenticación
    auth_service = AuthenticationService(user_repository, token_service)

    print("=== Registro de usuario ===")
    try:
        user = auth_service.register(username="Jared",
                                     password="12345678",
                                     email="jared123@gmail.com")
        print(f"User registered successfully: {user}")
    except Exception as e:
        print(f"Algo ha fallado en el registro: {e}")

    # Caso de autenticación exitosa
    print("\n=== Autenticación ===")
    token = auth_service.authenticate("Jared", "12345678")
    print(f"Autenticación exitosa. Token: {token}")

    # Caso de validación
    print("\n=== Token Validation ===")
    try:
        validated_user = auth_service.validate_token(token)
        print(f"Validación de token exitosa. User: {validated_user}")
    except Exception as e:
        print(f"Validación de token fallida: {e}")

    # Caso de autenticación fallida
    print("\n=== Autenticación fallida ===")
    try:
        auth_service.authenticate("Jared", "3y21b32182yb")
    except AuthenticationError as e:
        print(f"Authentication failed: {e}")

    print("\n=== Registro duplicado ===")
    try:
        auth_service.register("Jared", "87654321", "jared123@gmail.com")
    except UserAlreadyExistsError as e:
        print(f"Registration failed: {e}")


if __name__ == "__main__":
    main()