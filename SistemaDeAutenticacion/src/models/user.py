class User:
    def __init__(self, username: str, password_hash: str, email: str, id = None,
                 roles = None):
        self.username = username
        self.password_hash = password_hash
        self.email = email
        self.id = id
        if roles is None:
            self.roles = ["user"]
        else:
            self.roles = roles
