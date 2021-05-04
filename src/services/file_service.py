from repositories.file_repository import file_repository as default_file_repository


class FileService:
    """Class for working with files in UI.

    Args:
        file_repository: file_repository handles interaction with OS file system.
    """

    def __init__(self, file_repository=default_file_repository):
        self.file_repository = file_repository

    def open_file(self, src, byte=False):
        """open_file handles opening files for importing memos as markdown
        files and importing images to database.

        Args:
            src: location for file to be opened
            byte: optional, used to read images as bytes to be coverted to
                  base64-string. If True, function will add byte indicator into
                  used mode in open. Defaults to False.

        Returns:
            string: content of opened file and if file repository raises problems
                    when trying to open file, returns None.
        """
        try:
            content = self.file_repository.open_file(src, byte)
            return content
        except OSError:
            return None

    def save_file(self, src, content):
        """save_file handles saving files such as exported memo as markdown
        file to users computer.

        Args:
            src: location where file is saved
            content: content to be saved in file
        """
        self.file_repository.save_file(src, content)


file_service = FileService()
