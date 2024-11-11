# Mis excepciones personalizadas
class AuthenticationError(Exception):
    pass

class UserAlreadyExistsError(Exception):
    pass

class InvalidTokenError(Exception):
    pass
