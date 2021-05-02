class FileRepository:

    def open_file(self, src, byte=False):
        mode = "r"
        if byte:
            mode += "b"
        with open(src, mode) as file:
            content = file.read()
            file.close()
            return content

    def save_file(self, src, content):
        with open(src, "w") as file:
            file.write(content)
            file.close()


file_repository = FileRepository()
