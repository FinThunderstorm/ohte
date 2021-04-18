from mongoengine.queryset import NotUniqueError
from entities.user import User
from utils.helpers import get_id, get_type_id, get_type_user


class UserRepository:
    def __init__(self):
        pass

    def new(self, user):
        try:
            new_user = User(
                firstname=user["firstname"],
                lastname=user["lastname"],
                username=user["username"],
                password=user["password"],
            )
            saved_user = new_user.save()
            return saved_user
        except NotUniqueError:
            return None

    def update(self, user):
        try:
            updated_user = user.save()
            return updated_user
        except NotUniqueError:
            return None

    def remove(self, user):
        if not isinstance(user, get_type_user()):
            return False
        if self.__get_id(user.id):
            user.delete()
            return True
        return False

    def __get_all_users(self):
        users = User.objects  # pylint: disable=no-member
        return users

    def __get_id(self, search_term):
        if isinstance(search_term, get_type_id()):
            return self.__get_all_users()(id=get_id(search_term)).first()
        return None

    def __get_username(self, search_term):
        if search_term:
            return self.__get_all_users()(username=search_term).first()
        return None

    def get(self, mode="all", search_term=None):
        cases = {
            "all": self.__get_all_users(),
            "id": self.__get_id(search_term),
            "username": self.__get_username(search_term),
        }
        return cases[mode]

    def count(self, mode="all", search_term=None):
        if mode == "id" or mode == "username":
            return 1 if self.get(mode, search_term) else 0
        return self.get(mode, search_term).count()


user_repository = UserRepository()
