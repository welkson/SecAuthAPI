class AuthService(object):
    def connection(self):
        raise NotImplementedError

    def create_policy(self, name, description, content):
        raise NotImplementedError

    def update_policy(self):
        raise NotImplementedError

    def delete_policy(self):
        raise NotImplementedError

    def get_policy(self):
        raise NotImplementedError
