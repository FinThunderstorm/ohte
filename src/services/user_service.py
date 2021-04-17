from repositories.UserRepository import user_repository as default_user_repository
from utils.helpers import check_password


class UserService:
    def __init__(self, user_repository=default_user_repository):
        self.user_repository = user_repository

    def login(self, username, password):
        user = self.user_repository.get("username", username)
        try:
            if check_password(password, user.password):
                return user
        except:
            return None


user_service = UserService()
