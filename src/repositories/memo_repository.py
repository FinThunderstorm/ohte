from entities.memo import Memo
from utils.helpers import get_time, get_type_id, get_type_user, get_type_memo


class MemoRepository:
    """Class for handling memos in database.
    """

    def new(self, memo):
        """new is used for creating and saving new memo into database.

        Args:
            memo: dictionary with all memo's values: author as User, title as str,
                  content as str.

        Returns:
            Memo: returns created memo with id assigned by the database
        """
        new_memo = Memo(
            author=memo["author"],
            title=memo["title"],
            content=memo["content"],
            date=get_time(),
        )
        saved_memo = new_memo.save()
        return saved_memo

    def update(self, memo):
        """update is used to save alternated memo object into database; used to save changes to
        its values

        Args:
            memo: memo object that is going to be saved

        Returns:
            Memo: returns updated memo object with same values as database has after save.
        """
        updated_memo = memo.save()
        return updated_memo

    def remove(self, memo):
        """remove is used to remove memos from database.

        Args:
            memo: memo object that is going to be removed from database.

        Returns:
            bool: returns True if removed the memo successfully, False if memo was
            not instance of memo object or was given with memo that is not in the database.
        """
        if not isinstance(memo, get_type_memo()):
            return False
        if self.__get_id(memo.id):
            memo.delete()
            return True
        return False

    def __get_all_memos(self):
        """__get_all_memos is function for get function to call, when requested
        all memos in the database.

        Returns:
            QuerySet: returns mongoengine's QuerySet, that functions like any lists
        """
        all_memos = Memo.objects  # pylint: disable=no-member
        return all_memos

    def __get_id(self, search_term):
        """__get_id is function for get function to call, when requested memo with specific id.
        Handles finding the memo with given id.

        Args:
            search_term (ObjectId): search term given by get function

        Returns:
            Union([Memo, None]): return memo object if found, None if none memos with given id
                                 in the database.
        """
        if isinstance(search_term, get_type_id()):
            return self.__get_all_memos()(id=search_term).first()
        return None

    def __get_author(self, search_term):
        """__get_author is function for get function to call, when requested memo
        by specific author. Handles finding all memos by given author.

        Args:
            search_term (User): search term given by get function

        Returns:
            Union([List, None]): returns list with memos found if in search_term is User,
            otherwise returns None.
        """
        if isinstance(search_term, get_type_user()):
            authors_memos = []
            for memo in self.__get_all_memos():
                if memo.author == search_term:
                    authors_memos.append(memo)

            return authors_memos
        return None

    def get(self, mode="all", search_term=None):
        """get handles finding memos from database.

        Args:
            mode: controls what kind of filtering is used when getting memos from
                  database. Defaults to "all".
            search_term: carries value for functions to filter memos. Defaults to None.

        Returns:
            Union([List, QuerySet, Memo, None]): returns objects based on used function
            in the cases dictionary.
        """
        cases = {
            "all": self.__get_all_memos(),
            "id": self.__get_id(search_term),
            "author": self.__get_author(search_term),
        }
        return cases[mode]

    def count(self, mode="all", search_term=None):
        """count handles counting memos in the database based on selected mode by
        using get-function. Mainly used for testing purposes. In future can be used
        in statistics.

        Args:
            mode: controls what kind of filtering is used when counting memos from
                  database. Defaults to "all".
            search_term: carries value for functions to filter memos. Defaults to None.

        Returns:
            int: returns number of memos with given args.
        """
        if mode == "id":
            return 1 if self.get(mode, search_term) else 0
        return len(self.get(mode, search_term))


memo_repository = MemoRepository()
