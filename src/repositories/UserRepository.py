from entities.user import User
from utils.database_handler import connect_database
from utils.helpers import generate_password_hash, check_password


class UserRepository:
    def __init__(self, prod=True):
        self.connection = connect_database(prod)

    def new_user(self, user):
        try:
            new_user = User(
                firstname=user["firstname"],
                lastname=user["lastname"],
                username=user["username"],
                password=generate_password_hash(user["password"]),
            )
            saved_user = new_user.save()
            return saved_user
        except:
            return None

    def get_all_users(self):
        return User.objects  # tämä on ihan validi, olisiko lintterin ohitus tähän?

    def count_all_users(self):
        return self.get_all_users().count()

    def find_one_user(self, field, search_term):
        cases = {
            "username": self.get_all_users()(username=search_term),
            "id": self.get_all_users()(id=search_term)
        }
        return cases[field].first()

    def login(self, username, password):
        user = self.find_one_user("username", username)
        try:
            if check_password(bytes(password, 'utf-8'), bytes(user.password, 'utf-8')):
                return user
        except:
            return None

    def update_user(self, user):
        updated_user = user.save()
        return updated_user

    def remove_user(self, user_id):
        user_to_be_removed = self.find_one_user("id", user_id)
        try:
            user_to_be_removed.delete()
            return True
        except:
            return False
