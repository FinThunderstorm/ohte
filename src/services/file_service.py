import base64
import os
from repositories.file_repository import file_repository as default_file_repository


class FileService:
    def __init__(self, file_repository=default_file_repository):
        self.file_repository = file_repository

    def open_file(self, src, byte=False):
        try:
            content = self.file_repository.open_file(src, byte)
            return content
        except OSError:
            return None

    def save_file(self, src, content):
        self.file_repository.save_file(src, content)


file_service = FileService()
