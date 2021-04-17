from entities.memo import Memo
from utils.helpers import get_time, get_type_id, get_type_user


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
        if self.__get_id(memo.id):
            memo.delete()
            return True
        return False

    def __get_all(self):
        all_memos = Memo.objects  # pylint: disable=no-member
        return all_memos

    def __get_id(self, search_term):
        if isinstance(search_term, get_type_id()):
            return self.__get_all()(id=search_term).first()
        return None

    def __get_author(self, search_term):
        if isinstance(search_term, get_type_user()):
            authors_memos = []
            for memo in self.__get_all():
                if memo.author == search_term:
                    authors_memos.append(memo)

            return authors_memos
        return None

    def get(self, mode="all", search_term=None):
        cases = {
            "all": self.__get_all(),
            "id": self.__get_id(search_term),
            "title": self.__get_all()(title__icontains=search_term),
            "content": self.__get_all()(content__icontains=search_term),
            "author": self.__get_author(search_term),
        }
        return cases[mode]

    def count(self, mode="all", search_term=None):
        memos = self.get(mode, search_term)
        result = memos.count()
        return result


memo_repository = MemoRepository()
