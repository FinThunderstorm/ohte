from entities.image import Image
from utils.helpers import get_type_image, get_type_id, get_type_user


class ImageRepository:

    def new(self, image):
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
        updated_image = image.save()
        return updated_image

    def remove(self, image):
        if not isinstance(image, get_type_image()):
            return False
        if self.__get_id(image.id):
            image.delete()
            return True
        return False

    def __get_all_images(self):
        all_images = Image.objects  # pylint: disable=no-member
        return all_images

    def __get_id(self, search_term):
        if isinstance(search_term, get_type_id()):
            return self.__get_all_images()(id=search_term).first()
        return None

    def __get_author(self, search_term):
        if isinstance(search_term, get_type_user()):
            authors_images = []
            for image in self.__get_all_images():
                if image.author == search_term:
                    authors_images.append(image)
            return authors_images
        return None

    def get(self, mode="all", search_term=None):
        cases = {
            "all": self.__get_all_images(),
            "id": self.__get_id(search_term),
            "name": self.__get_all_images()(name__icontains=search_term),
            "author": self.__get_author(search_term),
        }
        return cases[mode]

    def count(self, mode="all", search_term=None):
        images = self.get(mode, search_term)
        if isinstance(images, get_type_image()) or images is None:
            return 1 if images else 0
        return len(images)


image_repository = ImageRepository()
