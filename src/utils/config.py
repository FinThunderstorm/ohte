from os import getenv, path
from dotenv import load_dotenv, dotenv_values

env_location = path.join(path.dirname(__file__), '..', '..', '.env')
load_dotenv(env_location)

database_uri = getenv("DATABASE_URI")


class Config:
    def __init__(self, file_service):
        self.__file_service = file_service

        self.__env_location = path.join(
            path.dirname(__file__), '..', '..', '.env')
        self.__configs = dotenv_values(self.__env_location)

    def get(self, setting):
        return self.__configs[setting]

    def set_value(self, setting, value):
        if value == "":
            raise ValueError("Value can not be empty")

        self.__configs[setting] = value

    def save(self):
        file_content = ""
        for setting in self.__configs:
            value = self.__configs[setting]
            file_content += setting.upper()+"="+value+"\n"
        print(file_content)
