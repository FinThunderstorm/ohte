from entities.memo import Memo
from utils.database_handler import connect_database
from utils.helpers import get_time


class MemoRepository:
    def __init__(self, prod=True):
        self.connection = connect_database(prod)

    def new(self, memo):
        new_memo = Memo(
            author_id=memo["author_id"],
            title=memo["title"],
            content=memo["content"],
            date=get_time(),
        )
        saved_memo = new_memo.save()
        return saved_memo

    def update(self, memo):
        updated_memo = memo.save()
        return updated_memo

    def remove(self, memo_id):
        memo_to_be_removed = self.get('id', memo_id)
        try:
            memo_to_be_removed.delete()
            return True
        except:
            return False

    def __get_all(self):
        all_memos = Memo.objects
        return all_memos

    def get(self, mode, search_term=None):
        cases = {
            "all": self.__get_all(),
            "id": None if not search_term else self.__get_all()(id=search_term).first(),
            "title": self.__get_all()(title__icontains=search_term),
            "content": self.__get_all()(content__icontains=search_term),
            "author_id": self.__get_all()(author_id=search_term),
        }
        return cases[mode]

    def count(self, mode="toot"):
        print(mode, 'mode', type(mode))
        print('smr:', self, type(self))
        memos = self.__get_all()
        result = memos.count()
        return result
