class FileRepository:
    """Class to handle file opening and saving in operating system.
    """

    def open_file(self, src, byte=False):
        """open_file handles opening files for importing memos as markdown
        files and importing images to database. Handles interaction with OS.

        Args:
            src: location for file to be opened
            byte: optional, used to read images as bytes to be coverted to
                  base64-string. If True, function will add byte indicator into
                  used mode in open. Defaults to False.

        Returns:
            string: content of opened file
        """
        mode = "r"
        if byte:
            mode += "b"
        try:
            with open(src, mode) as file:
                content = file.read()
                file.close()
                return content
        except FileNotFoundError:
            return None

    def save_file(self, src, content):
        """save_file handles saving files such as exported memo as markdown
        file to users computer.

        Args:
            src: location where file is saved
            content: content to be saved in file
        """
        with open(src, "w") as file:
            file.write(content)
            file.close()


file_repository = FileRepository()
