from repositories.MemoRepository import MemoRepository as default_memo_repository
from repositories.UserRepository import UserRepository as defualt_user_repository
from utils.helpers import get_time


class MemoService:
    def __init__(self,
                 memo_repository=default_memo_repository,
                 user_repository=defualt_user_repository):
        self.memo_repository = memo_repository
        self.user_repository = user_repository

    def create(self, author_id, title=None, content=""):
        # handle memoside
        memo = {
            "author_id": author_id,
            "title": title if title else "Memo "+get_time(),
            "content": content,
            "date": get_time(),
        }
        saved_memo = self.memo_repository.new(memo)

        # handle user side -> add new memo to user field
        user = self.user_repository.get(author_id)
        user.memos.append(saved_memo.id)
        updated_user = self.user_repository.update(user)

        if saved_memo and updated_user:
            return saved_memo
        return None

    def update(self, memo_id, author_id, title, content, date):
        memo = self.memo_repository.get(memo_id)
        memo.author_id = author_id
        memo.title = title
        memo.content = content
        memo.date = date
        updated_memo = self.memo_repository.update(memo)
        return updated_memo

    def remove(self, memo_id):
        author_id = self.memo_repository.get("memo_id", memo_id).author_id
        memo_result = self.memo_repository.remove(memo_id)
        if memo_result:
            author = self.user_repository.get("user_id", author_id)
            authors_memos = []
            for memo in author.memos:
                if memo != memo_id:
                    authors_memos.append(memo)
            author.memos = authors_memos
            user_result = self.user_repository.update(author)
            if user_result:
                return True
        return False

    def get(self, mode, search_term=None):
        modes = {
            "all": self.memo_repository.get_all(),
            "memo_id": self.memo_repository.get("memo_id", search_term),
            "author_id": self.memo_repository.get("author_id", search_term),
        }
        result = modes[mode]
        return result

    def count(self, mode):
        amount = self.memo_repository.count(mode)
        return amount
