from entities.user import User
from utils.helpers import generate_password_hash, get_id, get_type_id


class UserRepository:
    def __init__(self):
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
        except:  # tähän jos saisi tarkenteena mongoenginen not unique key exceptionin niin ois aika jeba
            return None

    def update(self, user):
        updated_user = user.save()
        return updated_user

    def remove(self, user):
        if self.__get_id(user.id):
            user.delete()
            return True
        return False

    def __get_all(self):
        users = User.objects
        return users

    def __get_id(self, search_term):
        if isinstance(search_term, get_type_id()):
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
        if mode == "all":
            return self.get(mode, search_term).count()
        else:
            return 1 if self.get(mode, search_term) else 0


user_repository = UserRepository()
