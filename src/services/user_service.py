from repositories.user_repository import user_repository as default_user_repository
from utils.helpers import check_password, generate_password_hash, get_type_user


class UserService:
    """UserService is business logic interaction with users.
    """

    def __init__(self, user_repository=default_user_repository):
        """Class contructor for UserService. Takes care of importing needed repositories.

        Args:
            user_repository : interaction repository with users in the database.
                              Defaults to default_user_repository.
        """
        self.user_repository = user_repository

    def create(self, firstname, lastname, username, password):
        """create is used to add new users into database. Handles preparing the user
        for saving.

        Args:
            firstname: user's firstname as string
            lastname: user's lastname as string
            username: user's username as string
            password: user's password as string

        Returns:
            Union(User, None): returns created User with id assigned by the database
             and None if given username is not unique or any arg is empty.
        """
        if firstname == "" or lastname == "" or username == "" or password == "":
            return None
        user = {
            "firstname": firstname,
            "lastname": lastname,
            "username": username,
            "password": str(generate_password_hash(password), 'utf-8'),
        }
        saved_user = self.user_repository.new(user)
        return saved_user

    def update(self, user_id, firstname, lastname, username, password):
        """update is used to handle updates into user in the database.

        Args:
            user_id: user's id as ObjectId
            firstname: user's firstname as string
            lastname: user's lastname as string
            username: user's username as string
            password: user's password as string

        Returns:
            Union(User, None): returns updated user object with same values as database
                               has after save and none if username is not unique.
        """
        user = self.user_repository.get('id', user_id)
        user.firstname = firstname
        user.lastname = lastname
        user.username = username
        password_hash = str(generate_password_hash(password), 'utf-8')
        user.password = user.password if user.password == password else password_hash

        updated_user = self.user_repository.update(user)
        return updated_user

    def remove(self, user_id):
        """remove is used to remove users from database.

        Args:
            user_id: user's id as ObjectId.

        Returns:
            bool: returns True if removed the user successfully, False if user id was not instance of
            ObjectID or was given with user that is not in the database.
        """
        old_user = self.user_repository.get('id', user_id)
        user_result = self.user_repository.remove(old_user)
        return user_result

    def get(self, mode="all", search_term=None):
        """get is used for getting users from database. Uses same syntax
        as repository.

        Modes:
            all: all users in the database
            id: user with given id
            username: user with given username

        Args:
            mode: mode as string. Defaults to "all".
            search_term: search term for selected mode. Defaults to None.

        Returns:
            Union([List, QuerySet, User, None]): returns objects based on used mode.
        """
        result = self.user_repository.get(mode, search_term)
        return result

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
            return 1 if self.user_repository.count(mode, search_term) else 0
        result = self.user_repository.count(mode, search_term)
        return result

    def login(self, username, password):
        """login is used to log the user into software.

        Args:
            username: username for user that is going to login as string
            password: password for user as plain text string

        Returns:
            Union(User, None): returns User if password is matching with user and user
                               exists, else None.
        """
        user = self.user_repository.get("username", username)
        if not isinstance(user, get_type_user()):
            return None
        if check_password(password, user.password):
            return user
        return None


user_service = UserService()
