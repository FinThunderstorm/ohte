from repositories.UserRepository import user_repository as default_user_repository


class UserService:
    def __init__(self, user_repository=default_user_repository):
        self.user_repository = user_repository

    def login(self, username, password):
        user = self.get("username", username)
        try:
            if check_password(bytes(password, 'utf-8'), bytes(user.password, 'utf-8')):
                return user
        except:
            return None


user_service = UserService()
