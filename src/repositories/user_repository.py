from mongoengine.queryset import NotUniqueError
from entities.user import User
from utils.helpers import get_id, get_type_id, get_type_user


class UserRepository:
    """Class for handling users in the database.
    """

    def new(self, user):
        """new is used for creating and saving new users into database.

        Args:
            user: dictionary with all users's values: firstname as str, lastname as str,
                  username as str, password as encrypted str.

        Returns:
            Union(User, None): returns created User with id assigned by the database and none if
                               given username is not unique.
        """
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
        """update is used to save alternated user object into database; used to save changes to
        its values

        Args:
            user: user object that is going to be saved

        Returns:
            Union(User, None): returns updated user object with same values as database
                               has after save and none if username is not unique.
        """
        try:
            updated_user = user.save()
            return updated_user
        except NotUniqueError:
            return None

    def remove(self, user):
        """remove is used to remove users from database.

        Args:
            user: user object that is going to be removed from database.

        Returns:
            bool: returns True if removed the user successfully, False if user was
            not instance of user object or was given with user that is not in the database.
        """
        if not isinstance(user, get_type_user()):
            return False
        if self.__get_id(user.id):
            user.delete()
            return True
        return False

    def __get_all_users(self):
        """__get_all_users is function for get function to call, when requested
        all users in the database.

        Returns:
            QuerySet: returns mongoengine's QuerySet, that functions like any lists
        """
        users = User.objects  # pylint: disable=no-member
        return users

    def __get_id(self, search_term):
        """__get_id is function for get function to call, when requested user with specific id.
        Handles finding the user with given id.

        Args:
            search_term (ObjectId): search term given by get function

        Returns:
            Union([User, None]): return user object if found, None if none users with given id
                                 in the database.
        """
        if isinstance(search_term, get_type_id()):
            return self.__get_all_users()(id=get_id(search_term)).first()
        return None

    def __get_username(self, search_term):
        """__get_username is function for get function to call, when requested user with specific
        username. Handles finding the user with given username.

        Args:
            search_term (str): search term given by get function

        Returns:
            Union([User, None]): return user object if found, None if none users with given
                                 username in the database.
        """
        if search_term:
            return self.__get_all_users()(username=search_term).first()
        return None

    def get(self, mode="all", search_term=None):
        """get handles finding users from database.

        Args:
            mode: controls what kind of filtering is used when getting users from
                  database. Defaults to "all".
            search_term: carries value for functions to filter users. Defaults to None.

        Returns:
            Union([List, QuerySet, User, None]): returns objects based on used function
            in the cases dictionary.
        """
        cases = {
            "all": self.__get_all_users(),
            "id": self.__get_id(search_term),
            "username": self.__get_username(search_term),
        }
        return cases[mode]

    def count(self, mode="all", search_term=None):
        """count handles counting users in the database based on selected mode by
        using get-function. Mainly used for testing purposes. In future can be used
        in statistics.

        Args:
            mode: controls what kind of filtering is used when counting users from
                  database. Defaults to "all".
            search_term: carries value for functions to filter users. Defaults to None.

        Returns:
            int: returns number of users with given args.
        """
        if mode in ("id", "username"):
            return 1 if self.get(mode, search_term) else 0
        return self.get(mode, search_term).count()


user_repository = UserRepository()
