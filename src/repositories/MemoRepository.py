from entities.memo import Memo
from utils.database_handler import connect_database
from utils.helpers import get_time


class MemoRepository:
    def __init__(self, prod=True):
        self.connection = connect_database(prod)
        print(self.connection)

    def new_memo(self, memo):
        new_memo = Memo(
            author_id=memo["author_id"],
            title=memo["title"],
            content=memo["content"],
            date=get_time(),
        )
        saved_memo = new_memo.save()
        return saved_memo

    def get_all_memos(self):
        all_memos = Memo.objects
        print(type(all_memos))
        return all_memos

    def count_memos(self):
        memos = self.get_all_memos()
        count = 0
        for memo in memos:
            count += 1
        return count

    def find_memo(self, search_term):
        pass
