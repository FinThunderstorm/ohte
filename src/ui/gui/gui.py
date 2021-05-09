import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QPlainTextEdit
from ui.gui.memo_view import MemoView
from ui.gui.login_view import LoginView
from ui.gui.setup_view import SetupView
from utils.helpers import get_test_memo_user


class GUI:
    """Main class for handling different graphical interface's pieces.
    """

    def __init__(self, config, memo_service, user_service, image_service, file_service):
        """Constructor for GUI. Prepares all needed views for operation.

        Args:
            config: handles configs for application
            memo_service: service handler for memos
            user_service: service handler for users
            image_service: service handler for images
            file_service: service handler for files
        """
        self.__app = QApplication(sys.argv)
        self.__screen = self.__app.primaryScreen()
        self.__screen_available = (self.__screen.availableGeometry(
        ).width(), self.__screen.availableGeometry().height())

        self.config = config

        self.__memo_service = memo_service
        self.__user_service = user_service
        self.__image_service = image_service
        self.__file_service = file_service
        self.__user = [get_test_memo_user(
            '6072d33e3a3c627a49901ce8', "notvalid")]

        self.objects = [{}]
        self.layouts = [{}]
        self.frames = [{}]

        self.__memo_view = MemoView(
            self.__screen_available, self.__memo_service, self.__image_service, self.__user, self.objects, self.layouts, self.frames)
        self.__login_view = LoginView(
            self.__screen_available, self.__user_service, self.__user, self.objects, self.layouts, self.frames)
        self.__setup_view = SetupView(
            self.__screen_available, self.objects, self.layouts, self.frames, self.config)

        self.frames[0]["memoview"] = self.__memo_view
        self.frames[0]["loginview"] = self.__login_view

        self.__memo_view.initialize()
        self.__login_view.initialize()

    def first_time(self):
        """first_time is used for showing partial setting view for setting
        settings for the first time and if db-connection is not established.
        """
        self.__setup_view.run_standalone()

    def error(self, message):
        """error is used to show user messages about problems while
        using the app.

        Args:
            message: string displayed in error dialog
        """
        print(message)

    def start(self):
        """start is used to start application
        """
        self.__login_view.show()
        sys.exit(self.__app.exec_())
