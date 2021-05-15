from os import path
from dotenv import dotenv_values


class Config:
    """Class for handling configs and loading them from .env-file.

    Arguments:
        file_service: handler for saving values into .env-file.
    """

    def __init__(self, file_service, src=None):
        """Constructor for the class, loads current configs into memory if
        present, or if not, creates default config.

        Args:
            file_service: service handler for saving files into file system.
        """
        self.__file_service = file_service

        self.__env_location = src if src else path.join(
            path.dirname(__file__), '..', '..', '.env')
        self.__configs = dotenv_values(self.__env_location)

        self.initialized_first_time = False

        if not self.__configs:
            self.__initialize_first_time()
            self.initialized_first_time = True

    def __reload(self):
        """__reload is used to convert database uri to understand changes
        after save.
        """
        self.__configs = dotenv_values(self.__env_location)

    def get(self, setting):
        """get returns asked value from config.

        Args:
            setting: key for asked setting value

        Returns:
            str: setting value
        """
        return self.__configs[setting.upper()]

    def get_all(self):
        """get_all returns all config values

        Returns:
            dict: dictionary including all settings, name as key and
                  setting value as value.
        """
        return self.__configs

    def set_value(self, setting, value):
        """set_value is used for setting new values into config.

        Args:
            setting: key for setting in config
            value: value for given setting

        Raises:
            ValueError: if trying to add empty setting, raises ValueError
        """
        if value == "":
            raise ValueError("Value can not be empty")

        self.__configs[setting.upper()] = value

    def save(self):
        """save is used to save current values in config into .env-file.
        """
        file_content = ""
        for setting in self.__configs:
            value = self.__configs[setting.upper()]
            if setting.upper() == "DATABASE_URI":
                value = "mongodb+srv://${DB_USERNAME}:${DB_PASSWORD}" \
                    + "@${DB_SERVER}/${DB_NAME}?retryWrites=true&w=majority"
            file_content += setting.upper()+"="+str(value)+"\n"
        self.__file_service.save_file(self.__env_location, file_content)
        self.__reload()

    def __initialize_first_time(self):
        """__initialize_first_time is used for initializing .env-file for the first time
        """
        self.__configs = {}
        self.__configs["RES_INDEX"] = 0
        self.__configs["RES_FORMAT"] = ""
        self.__configs["DB_USERNAME"] = ""
        self.__configs["DB_PASSWORD"] = ""
        self.__configs["DB_SERVER"] = "ohte.bu0r9.mongodb.net"
        self.__configs["DB_NAME"] = "muistio"
        self.__configs["DATABASE_URI"] = "mongodb+srv://${DB_USERNAME}:${DB_PASSWORD}" \
            + "@${DB_SERVER}/${DB_NAME}?retryWrites=true&w=majority"
