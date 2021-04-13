from utils.helpers import get_time
from bson.objectid import ObjectId
from repositories.UserRepository import user_repository as default_user_repository
from repositories.MemoRepository import memo_repository as default_memo_repository


class MemoService:
    def __init__(self,
                 memo_repository=default_memo_repository,
                 user_repository=default_user_repository):
        self.memo_repository = memo_repository
        self.user_repository = user_repository

    def create(self, author_id, title=None, content=""):
        # handle memoside

        author = self.user_repository.get('id', author_id)
        memo = {
            "author": author,
            "title": title if title else "Memo "+str(get_time()),
            "content": content,
            "date": get_time(),
        }
        saved_memo = self.memo_repository.new(memo)

        # handle user side -> add new memo to user field
        author.memos.append(saved_memo.id)
        updated_user = self.user_repository.update(author)

        if saved_memo and updated_user:
            return saved_memo
        return None

    def update(self, memo_id, author_id, title, content, date):
        memo = self.memo_repository.get('id', memo_id)
        memo.author = self.user_repository.get('id', author_id)
        memo.title = title
        memo.content = content
        memo.date = date
        updated_memo = self.memo_repository.update(memo)
        return updated_memo

    def remove(self, memo_id):
        old_memo = self.memo_repository.get('id', memo_id)
        author = old_memo.author
        memo_result = self.memo_repository.remove(old_memo)
        if memo_result:
            authors_memos = []
            for memo in author.memos:
                if memo.id != old_memo.id:
                    authors_memos.append(memo)
            author.memos = authors_memos
            user_result = self.user_repository.update(author)
            if user_result:
                return True
        return False

    def get(self, mode="all", search_term=None):
        result = self.memo_repository.get(mode, search_term)
        return result

    def count(self, mode="all", search_term=None):
        result = self.memo_repository.count(mode, search_term)
        return result


memo_service = MemoService()
