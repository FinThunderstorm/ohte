from entities.memo import Memo
from utils.helpers import get_time, get_id, get_type_id, get_type_user, get_type_memo


class MemoRepository:
    def __init__(self):
        pass

    def new(self, memo):
        new_memo = Memo(
            author=memo["author"],
            title=memo["title"],
            content=memo["content"],
            date=get_time(),
        )
        saved_memo = new_memo.save()
        return saved_memo

    def update(self, memo):
        updated_memo = memo.save()
        return updated_memo

    def remove(self, memo):
        if not isinstance(memo, get_type_memo()):
            return False
        if self.__get_id(memo.id):
            memo.delete()
            return True
        return False

    def __get_all_memos(self):
        all_memos = Memo.objects  # pylint: disable=no-member
        return all_memos

    def __get_id(self, search_term):
        if isinstance(search_term, get_type_id()):
            return self.__get_all_memos()(id=search_term).first()
        return None

    def __get_author(self, search_term):
        if isinstance(search_term, get_type_user()):
            authors_memos = []
            for memo in self.__get_all_memos():
                if memo.author == search_term:
                    authors_memos.append(memo)

            return authors_memos
        return None

    def get(self, mode="all", search_term=None):
        cases = {
            "all": self.__get_all_memos(),
            "id": self.__get_id(search_term),
            "title": self.__get_all_memos()(title__icontains=search_term),
            "content": self.__get_all_memos()(content__icontains=search_term),
            "author": self.__get_author(search_term),
        }
        return cases[mode]

    def count(self, mode="all", search_term=None):
        if mode == "id":
            return 1 if self.get(mode, search_term) else 0
        return len(self.get(mode, search_term))


memo_repository = MemoRepository()
