import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QPlainTextEdit
from ui.gui.memo_view import MemoView


class GUI:
    def __init__(self, memo_service, user_service):
        self.__app = QApplication(sys.argv)
        self.__screen = self.__app.primaryScreen()
        self.__screen_available = (self.__screen.availableGeometry(
        ).width(), self.__screen.availableGeometry().height())

        self.__memo_service = memo_service
        self.__user_service = user_service
        self.__user = self.__user_service.get()[0]

        self.__memo_view = MemoView(
            self.__screen_available, self.__memo_service, self.__user)

    def start(self):
        self.__memo_view.run()

        sys.exit(self.__app.exec_())

    def run(self):
        print('tööt')
