import os
from trafilatura import fetch_url, extract
from utils.helpers import get_time, get_id
from repositories.user_repository import user_repository as default_user_repository
from repositories.memo_repository import memo_repository as default_memo_repository
from repositories.file_repository import file_repository as default_file_repository
from services.image_service import image_service as default_image_service


class MemoService:
    """Class for Memo's app logic.
    """

    def __init__(self,
                 memo_repository=default_memo_repository,
                 user_repository=default_user_repository,
                 file_repository=default_file_repository,
                 image_service=default_image_service):
        """Class contructor for MemoService. Handles taking needed repositories
        and services into use.

        Args:
            memo_repository: interaction repository with memos in the database.
                             Defaults to default_memo_repository.
            user_repository: interaction repository with users in the database.
                             Defaults to default_user_repository.
            file_repository: interaction repository with files in the file system.
                             Defaults to default_file_repository.
            image_service: interaction service with images.
                           Defaults to default_image_service.
        """
        self.memo_repository = memo_repository
        self.user_repository = user_repository
        self.file_repository = file_repository
        self.image_service = image_service

    def create(self, author_id, title=None, content=""):
        """create is used to add new images into database. Handles preparing memo
        for saving.

        Args:
            author_id: memo's author's id as ObjectId
            title: memo title as string. Defaults to None. If None,
                   memo is created with default title.
            content: memo content as string. Defaults to "".

        Returns:
            Union(Memo, None): if saving were successful, Memo is returned. If no
                               authors with given id or problems while saving,
                               returning None.
        """
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
        """update is used to handle updates into memo in the database.

        Args:
            memo_id: memo's id as ObjectId
            author_id: author's id as ObjectId
            title: name as string
            content: memo content as string
            date: memo's date as datetime-object.

        Returns:
            Memo: returns updated Memo object.
        """
        memo = self.memo_repository.get('id', memo_id)
        memo.author = self.user_repository.get('id', author_id)
        memo.title = title
        memo.content = content
        memo.date = date
        updated_memo = self.memo_repository.update(memo)
        return updated_memo

    def remove(self, memo_id):
        """remove is used to remove memos from the database.

        Args:
            memo_id: memo's id as ObjectId.

        Returns:
            bool: returns True if removal were success, else False.
        """
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
        """get is used for getting memos from database. Uses same syntax
        as repository.

        Modes:
            all: all memos in the database
            id: memo with given id
            title: all memos with given title or part of it.
            content: all memos with given content or part of it.
            author: all memos by given author

        Args:
            mode: mode as string. Defaults to "all".
            search_term: search term for selected mode. Defaults to None.

        Returns:
            Union([List, QuerySet, Memo, None]): returns objects based on used function
            in the cases dictionary.
        """
        result = self.memo_repository.get(mode, search_term)
        return result

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
        if mode == "author":
            search_term = self.user_repository.get("id", search_term)
        result = self.memo_repository.count(mode, search_term)
        return result

    def import_from_url(self, author_id, url):
        """import_from_url is used to import memos from external sources in internet.

        Args:
            author_id: memo's author's id as ObjectId.
            url: source location whre imported content is currently as string.

        Returns:
            Union(Memo, None): returns Memo if saved successfully, returns None if not or
                               content from website were empty.
        """
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

    def import_from_file(self, author_id, src):
        """[summary]

        Args:
            author_id ([type]): [description]
            src ([type]): [description]

        Returns:
            Union(Memo, None): returns Memo if import were successful. Returns
                               None if imported file were empty or no file found.
        """
        try:
            imported = self.file_repository.open_file(src)
            if not imported:
                raise ValueError("File was empty")

            filename, file_ext = os.path.splitext(src)
            filename = filename.split("/")
            filename = filename[len(filename)-1]+file_ext

            src = src[:src.find(filename)]

            index = imported.find('![](')
            while index != -1:
                img_src_end = imported.find(')', index)
                img_src = imported[index+4:img_src_end]

                img_name = img_src.split('/')
                img_name = img_name[len(img_name)-1]
                img_name = filename + "/" + img_name
                img_name = img_name if len(img_name) < 50 else img_name[:50]

                img_src = os.path.normpath(os.path.join(src, img_src))

                img = self.image_service.get('name', img_name)
                if len(img) > 0:
                    img = img[0]
                    if img.author != self.user_repository.get('id', get_id(author_id)):
                        img = None
                    if img.image != self.image_service.convert_image(img_src):
                        img = None
                    img = img if img else self.image_service.create(
                        author_id, img_name, img_src, 600)

                    img_tag = ""
                    if img:
                        img_tag = "![]("+str(img.id)+')'
                    imported = imported[:index] + \
                        img_tag+imported[img_src_end+1:]

                index = imported.find('![](', index+1)

            title = "Imported from "+filename
            title = title if len(title) < 50 else title[:50]

            saved_memo = self.create(author_id, title, imported)
            return saved_memo
        except OSError:
            return None
        except ValueError:
            return None

    def export_memo(self, memo_id, src):
        """export_memo is used to save memos as Markdown files.

        Args:
            memo_id: memo's id as ObjectId.
            src: location where memo is exported as string.
        """
        memo = self.get('id', memo_id)
        self.file_repository.save_file(src, memo.content)


memo_service = MemoService()
