from entities.user import User
from utils.database_handler import connect_database
from utils.helpers import generate_password_hash, check_password, get_id


class UserRepository:
    def __init__(self):
        #self.connection = connect_database(prod)
        pass

    def new(self, user):
        try:
            new_user = User(
                firstname=user["firstname"],
                lastname=user["lastname"],
                username=user["username"],
                password=generate_password_hash(user["password"]),
            )
            saved_user = new_user.save()
            return saved_user
        except Exception as e:
            print(e)
            return None

    def __get_all(self):
        return User.objects

    def __get_id(self, search_term):
        if type(search_term) == type(get_id()):
            return self.__get_all()(id=get_id(search_term)).first()
        return None

    def __get_username(self, search_term):
        if search_term:
            return self.__get_all()(username=search_term).first()
        return None

    def get(self, mode="all", search_term=None):
        cases = {
            "all": self.__get_all(),
            "id": self.__get_id(search_term),
            "username": self.__get_username(search_term),
        }
        return cases[mode]

    def count(self, mode="all", search_term=None):
        return self.get(mode, search_term).count()

    def login(self, username, password):
        user = self.get("username", username)
        try:
            if check_password(bytes(password, 'utf-8'), bytes(user.password, 'utf-8')):
                return user
        except:
            return None

    def update(self, user):
        updated_user = user.save()
        return updated_user

    def remove(self, user):
        try:
            user.delete()
            return True
        except:
            return False


user_repository = UserRepository()
