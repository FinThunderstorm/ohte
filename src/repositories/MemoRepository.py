from entities.memo import Memo
from utils.database_handler import connect_database
from utils.helpers import get_time


class MemoRepository:
    def __init__(self, prod=True):
        self.connection = connect_database(prod)

    def new_memo(self, memo):
        new_memo = Memo(
            author_id=memo["author_id"],
            title=memo["title"],
            content=memo["content"],
            date=get_time(),
        )
        saved_memo = new_memo.save()
        return saved_memo

    def update_memo(self, memo):
        updated_memo = memo.save()
        return updated_memo

    def remove_memo(self, memo_id):
        memo_to_be_removed = self.get_memo(memo_id)
        try:
            memo_to_be_removed.delete()
            return True
        except:
            return False

    def get_memo(self, memo_id):
        exact_memo = self.get_all_memos()(id=memo_id)
        return exact_memo.first()

    def get_all_memos(self):
        all_memos = Memo.objects
        return all_memos

    def count_memos(self):
        return self.get_all_memos().count()

    def filter_memos(self, field, search_term):
        cases = {
            "title": self.get_all_memos()(title__icontains=search_term),
            "content": self.get_all_memos()(content__icontains=search_term),
            "author_id": self.get_all_memos()(author_id=search_term),
        }
        return cases[field]
