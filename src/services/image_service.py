import base64
import os
from utils.helpers import get_type_id
from repositories.image_repository import image_repository as default_image_repository
from repositories.user_repository import user_repository as default_user_repository
from repositories.file_repository import file_repository as default_file_repository


class ImageService:
    """ImageService is class for interacting with images in database.
    """

    def __init__(self, image_repository=default_image_repository,
                 user_repository=default_user_repository,
                 file_repository=default_file_repository):
        """Class constructor for ImageService, handles taking all needed
        repositories into use.

        Args:
            image_repository: interaction repository with images in the database.
                              Defaults to default_image_repository.
            user_repository: interaction repository with users in the database.
                             Defaults to default_user_repository.
            file_repository: interaction repository with files in the file system.
                             Defaults to default_file_repository.
        """
        self.image_repository = image_repository
        self.user_repository = user_repository
        self.file_repository = file_repository

    def create(self, author_id, name, image_src, width):
        """create is used to add new images into database. Handles preparing the image
        for saving.

        Args:
            author_id: image's author's id as ObjectId.
            name: image name as string
            image_src: image file location in file system as string.
            width: image width in memo as int.

        Returns:
            Union(Image, None): returns image is successfully saved. If image author,
                                image string or saved image is not present, returns None.
        """
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
            name = name[len(name)-1]
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
        """convert_image is used to open image file from file system and covert it
        into base64 string.

        Args:
            image_src: image file location in file system as string.

        Returns:
            string: image content as base64 encrypted string.
        """
        img_file = self.file_repository.open_file(
            image_src, byte=True)
        if img_file is None:
            return None
        image_string = base64.b64encode(img_file).decode('utf-8')
        return image_string

    def update(self, image_id, author_id, name, image_string, filetype, width):
        """update is used to handle updates into image in the database.

        Args:
            image_id: image's id as ObjectId
            author_id: author's id as ObjectId
            name: name as string
            image_string: image content as base64 encoded string
            filetype: images filetype as string
            width: image width for rendering in GUI as int

        Returns:
            Image: returns updated Image object.
        """
        image = self.image_repository.get('id', image_id)
        image.author = self.user_repository.get('id', author_id)
        image.name = name
        image.image = image_string
        image.filetype = filetype
        image.width = width
        updated_image = self.image_repository.update(image)
        return updated_image

    def remove(self, image_id):
        """remove is used to remove imgaes from the database.

        Args:
            image_id: image's id as ObjectId.

        Returns:
            bool: returns True if removal were success, else False.
        """
        old_image = self.image_repository.get('id', image_id)
        image_result = self.image_repository.remove(old_image)
        return image_result

    def get(self, mode="all", search_term=None):
        """get is used for getting images from database. Uses same syntax
        as repository.

        Modes:
            all: all images in the database
            id: image with given id
            name: all images with given name
            author: all images by given author

        Args:
            mode: mode as string. Defaults to "all".
            search_term: search term for selected mode. Defaults to None.

        Returns:
            Union([List, QuerySet, Image, None]): returns objects based on used mode.
        """
        if mode == "author" and isinstance(search_term, get_type_id()):
            search_term = self.user_repository.get('id', search_term)
        result = self.image_repository.get(mode, search_term)
        return result

    def count(self, mode="all", search_term=None):
        """count handles counting images in the database based on selected mode by
        using get-function. Mainly used for testing purposes. In future can be used
        in statistics.

        Args:
            mode: controls what kind of filtering is used when counting images from
                  database. Defaults to "all".
            search_term: carries value for functions to filter images. Defaults to None.

        Returns:
            int: returns number of images with given args.
        """
        if mode == "author":
            search_term = self.user_repository.get('id', search_term)
        result = self.image_repository.count(mode, search_term)
        return result


image_service = ImageService()
