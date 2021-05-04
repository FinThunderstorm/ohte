from entities.image import Image
from utils.helpers import get_type_image, get_type_id, get_type_user


class ImageRepository:
    """Class for handling images in database.
    """

    def new(self, image):
        """new is used to create and save new image into database

        Args:
            image: dictionary with all image's values: author as User, name as str,
                   image as base64 encoded string, filetype as str, width as int

        Returns:
            Image: returns created image with id assigned by the database
        """
        new_image = Image(
            author=image["author"],
            name=image["name"],
            image=image["image"],
            filetype=image["filetype"],
            width=image["width"],
        )
        saved_image = new_image.save()
        return saved_image

    def update(self, image):
        """update is used to save alternated image object into database;
        used to save changes to its values.

        Args:
            image: image object that is going to be saved

        Returns:
            Image: returns updated image object with same values as
            database has after save.
        """
        updated_image = image.save()
        return updated_image

    def remove(self, image):
        """remove is used to remove images from database

        Args:
            image: image object that is going to be removed from datbase

        Returns:
            bool: returns True if removed the memo successfully, False if memo was
            not instance of image or was given with image that is not in the database.
        """
        if not isinstance(image, get_type_image()):
            return False
        if self.__get_id(image.id):
            image.delete()
            return True
        return False

    def __get_all_images(self):
        """__get_all_images is function for get function to call, when requested
        all images in the database.

        Returns:
            QuerySet: returns mongoengine's QuerySet, that functions like any lists.
        """
        all_images = Image.objects  # pylint: disable=no-member
        return all_images

    def __get_id(self, search_term):
        """__get_id is function for get function to call, when requested image
        with specific id. Handles finding the image with given id.

        Args:
            search_term (ObjectId): search_term given by get function

        Returns:
            Union([Memo, None]): returns image object if found, None if none images with given id
                                 in the database.
        """
        if isinstance(search_term, get_type_id()):
            return self.__get_all_images()(id=search_term).first()
        return None

    def __get_author(self, search_term):
        """__get_author is function for get function to call, when requested image
        by specific author. Handles finding all images by given author.

        Args:
            search_term (User): search term given by get function

        Returns:
            Union([List, None]): returns list with images found if in search_term is User,
            otherwise returns None.
        """
        if isinstance(search_term, get_type_user()):
            authors_images = []
            for image in self.__get_all_images():
                if image.author == search_term:
                    authors_images.append(image)
            return authors_images
        return None

    def get(self, mode="all", search_term=None):
        """get handles finding images from database.

        Args:
            mode: controls what kind of filtering is used when getting images from
                  database. Defaults to "all".
            search_term: carries value for functions to filter images. Defaults to None.

        Returns:
            Union([List, QuerySet, Image, None]): returns objects based on used function
            in the cases dictionary.
        """
        cases = {
            "all": self.__get_all_images(),
            "id": self.__get_id(search_term),
            "name": self.__get_all_images()(name__icontains=search_term),
            "author": self.__get_author(search_term),
        }
        return cases[mode]

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
        images = self.get(mode, search_term)
        if isinstance(images, get_type_image()) or images is None:
            return 1 if images else 0
        return len(images)


image_repository = ImageRepository()
