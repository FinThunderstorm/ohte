import base64
import os
from repositories.image_repository import image_repository as default_image_repository
from repositories.user_repository import user_repository as default_user_repository
from repositories.memo_repository import memo_repository as default_memo_repository


class ImageService:
    def __init__(self, image_repository=default_image_repository,
                 user_repository=default_user_repository, memo_repository=default_memo_repository):
        self.image_repository = image_repository
        self.user_repository = user_repository
        self.memo_repository = memo_repository

    def create(self, author_id, name, image_src, width):
        author = self.user_repository.get('id', author_id)
        if not author:
            return None

        try:
            with open(image_src, 'rb') as image_file:
                image_string = base64.b64encode(
                    image_file.read()).decode('utf-8')
        except FileNotFoundError:
            return None

        _, file_ext = os.path.splitext(image_src)
        filetype = "jpeg" if file_ext[1:] == "jpg" else file_ext[1:]

        image = {
            "author": author,
            "name": name,
            "image": image_string,
            "filetype": filetype,
            "width": width
        }
        saved_image = self.image_repository.new(image)

        return saved_image

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
