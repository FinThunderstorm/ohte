from trafilatura import fetch_url, extract
from utils.helpers import get_time
from repositories.user_repository import user_repository as default_user_repository
from repositories.memo_repository import memo_repository as default_memo_repository


class MemoService:
    def __init__(self,
                 memo_repository=default_memo_repository,
                 user_repository=default_user_repository):
        self.memo_repository = memo_repository
        self.user_repository = user_repository

    def create(self, author_id, title=None, content=""):
        author = self.user_repository.get('id', author_id)
        if not author:
            return None

        memo = {
            "author": author,
            "title": title if title else "Memo "+str(get_time()),
            "content": content,
            "date": get_time(),
        }
        saved_memo = self.memo_repository.new(memo)

        author.memos.append(saved_memo.id)
        self.user_repository.update(author)

        return saved_memo

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
        memo_result = self.memo_repository.remove(old_memo)
        if memo_result:
            author = old_memo.author
            authors_memos = []
            for memo in author.memos:
                if memo.id != old_memo.id:
                    authors_memos.append(memo)
            author.memos = authors_memos
            self.user_repository.update(author)
            return True
        return False

    def get(self, mode="all", search_term=None):
        result = self.memo_repository.get(mode, search_term)
        return result

    def count(self, mode="all", search_term=None):
        if mode == "author":
            search_term = self.user_repository.get("id", search_term)
        result = self.memo_repository.count(mode, search_term)
        return result

    def import_from_url(self, author_id, url):
        try:
            imported = fetch_url(url)
            content = extract(imported,
                              include_comments=False,
                              include_tables=True,
                              output_format="txt")
            if not content:
                raise ValueError

            index = content.find('\n')
            while index != -1:
                content = content[:index] + "\n" + content[index:]
                index = content.find('\n', index+2)
            url_i_start = url.find("://")
            url_i_end = url.find("/", url_i_start+3)
            site_name = url[url_i_start+3:url_i_end] if len(
                url[url_i_start+3:url_i_end]) < 36 else url[url_i_start+3:36]
            title = "Imported from " + site_name
            saved_memo = self.create(author_id, title, content)
            return saved_memo
        except ValueError:
            return None


memo_service = MemoService()
