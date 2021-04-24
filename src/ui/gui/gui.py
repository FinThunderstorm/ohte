import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QPlainTextEdit
from ui.gui.memo_view import MemoView
from ui.gui.login_view import LoginView


class GUI:
    def __init__(self, memo_service, user_service):
        self.__app = QApplication(sys.argv)
        self.__screen = self.__app.primaryScreen()
        self.__screen_available = (self.__screen.availableGeometry(
        ).width(), self.__screen.availableGeometry().height())

        self.__memo_service = memo_service
        self.__user_service = user_service
        self.__user = [self.__user_service.get()[0]]

        self.objects = [{}]
        self.layouts = [{}]
        self.frames = [{}]

        self.__memo_view = MemoView(
            self.__screen_available, self.__memo_service, self.__user, self.objects, self.layouts, self.frames)
        self.__login_view = LoginView(
            self.__screen_available, self.__user_service, self.__user, self.objects, self.layouts, self.frames)

        self.frames[0]["memoview"] = self.__memo_view
        self.frames[0]["loginview"] = self.__login_view

        self.__memo_view.initialize()
        self.__login_view.initialize()

    def start(self):
        # self.__memo_view.run()
        self.__login_view.show()

        sys.exit(self.__app.exec_())

    def run(self):
        print('tööt')
