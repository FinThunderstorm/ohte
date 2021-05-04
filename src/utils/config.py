from os import path
from dotenv import dotenv_values


class Config:
    def __init__(self, file_service):
        self.__file_service = file_service

        self.__env_location = path.join(
            path.dirname(__file__), '..', '..', '.env')
        self.__configs = dotenv_values(self.__env_location)

        self.initialized_first_time = False

        if not self.__configs:
            self.__initialize_first_time()
            self.initialized_first_time = True

    def get(self, setting):
        return self.__configs[setting.upper()]

    def get_all(self):
        return self.__configs

    def set_value(self, setting, value):
        if value == "":
            raise ValueError("Value can not be empty")

        self.__configs[setting.upper()] = value

    def save(self):
        file_content = ""
        for setting in self.__configs:
            value = self.__configs[setting.upper()]
            if setting.upper() == "DATABASE_URI":
                value = "mongodb+srv://${DB_USERNAME}:${DB_PASSWORD}" \
                    + "@${DB_SERVER}/${DB_NAME}?retryWrites=true&w=majority"
            file_content += setting.upper()+"="+str(value)+"\n"
        self.__file_service.save_file(self.__env_location, file_content)

    def __initialize_first_time(self):
        self.__configs = {}
        self.__configs["RES_INDEX"] = 0
        self.__configs["RES_FORMAT"] = ""
        self.__configs["DB_USERNAME"] = ""
        self.__configs["DB_PASSWORD"] = ""
        self.__configs["DB_SERVER"] = "ohte.bu0r9.mongodb.net"
        self.__configs["DB_NAME"] = "muistio"
        self.__configs["DATABASE_URI"] = "mongodb+srv://${DB_USERNAME}:${DB_PASSWORD}" \
            + "@${DB_SERVER}/${DB_NAME}?retryWrites=true&w=majority"
