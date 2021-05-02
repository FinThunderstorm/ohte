import base64
import os
from repositories.image_repository import image_repository as default_image_repository
from repositories.user_repository import user_repository as default_user_repository
from repositories.memo_repository import memo_repository as default_memo_repository
from repositories.file_repository import file_repository as default_file_repository


class ImageService:
    def __init__(self, image_repository=default_image_repository,
                 user_repository=default_user_repository, memo_repository=default_memo_repository, file_repository=default_file_repository):
        self.image_repository = image_repository
        self.user_repository = user_repository
        self.memo_repository = memo_repository
        self.file_repository = file_repository

    def create(self, author_id, name, image_src, width):
        author = self.user_repository.get('id', author_id)
        if not author:
            return None

        image_string = self.convert_image(image_src)
        if not image_string:
            return None

        filename, file_ext = os.path.splitext(image_src)
        filetype = "jpeg" if file_ext[1:] == "jpg" else file_ext[1:]

        if name == "":
            name = filename.split('/')
            name = filename[len(name)-1]
            name = name if len(name) < 50 else name[:50]

        image = {
            "author": author,
            "name": name,
            "image": image_string,
            "filetype": filetype,
            "width": width
        }
        saved_image = self.image_repository.new(image)

        return saved_image

    def convert_image(self, image_src):
        try:
            img_file = self.file_repository.open_file(
                image_src, byte=True)
            image_string = base64.b64encode(img_file).decode('utf-8')
            return image_string
        except FileNotFoundError:
            return None

    def update(self, image_id, author_id, name, image_string, filetype, width):
        image = self.image_repository.get('id', image_id)
        image.author = self.user_repository.get('id', author_id)
        image.name = name
        image.image = image_string
        image.filetype = filetype
        image.width = width
        updated_image = self.image_repository.update(image)
        return updated_image

    def remove(self, image_id):
        old_image = self.image_repository.get('id', image_id)
        image_result = self.image_repository.remove(old_image)
        return image_result

    def get(self, mode="all", search_term=None):
        result = self.image_repository.get(mode, search_term)
        return result

    def count(self, mode="all", search_term=None):
        if mode == "author":
            search_term = self.user_repository.get('id', search_term)
        result = self.image_repository.count(mode, search_term)
        return result


image_service = ImageService()
