from authservice import AuthService

class AuthZForce(AuthService):
    """AuthZForce Authorization Services"""
    def __init__(self, url, auth_type, user, password, token):
        self.url = url
        self.auth_type = auth_type
        self.user = user
        self.password = password
        self.token = token

    def connection(self):
        return NotImplemented

    def get_policy(self):
        return NotImplemented

    def create_policy(self):
        return NotImplemented

