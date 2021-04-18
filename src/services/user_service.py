from repositories.user_repository import user_repository as default_user_repository
from utils.helpers import check_password, generate_password_hash, get_type_user


class UserService:
    def __init__(self, user_repository=default_user_repository):
        self.user_repository = user_repository

    def create(self, firstname, lastname, username, password):
        user = {
            "firstname": firstname,
            "lastname": lastname,
            "username": username,
            "password": str(generate_password_hash(password), 'utf-8'),
        }
        saved_user = self.user_repository.new(user)
        return saved_user

    def update(self, user_id, firstname, lastname, username, password):
        user = self.user_repository.get('id', user_id)
        user.firstname = firstname
        user.lastname = lastname
        user.username = username
        password_hash = str(generate_password_hash(password), 'utf-8')
        user.password = user.password if user.password == password else password_hash

        updated_user = self.user_repository.update(user)
        return updated_user

    def remove(self, user_id):
        old_user = self.user_repository.get('id', user_id)
        user_result = self.user_repository.remove(old_user)
        # tähän väliin käyttäjän vanhojen muistioiden poistaminen kannasta, jos halutaan
        return user_result

    def get(self, mode="all", search_term=None):
        result = self.user_repository.get(mode, search_term)
        return result

    def count(self, mode="all", search_term=None):
        if mode in ("id", "username"):
            return 1 if self.user_repository.count(mode, search_term) else 0
        result = self.user_repository.count(mode, search_term)
        return result

    def login(self, username, password):
        user = self.user_repository.get("username", username)
        if not isinstance(user, get_type_user()):
            return None
        if check_password(password, user.password):
            return user
        return None


user_service = UserService()
