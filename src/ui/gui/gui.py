import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel


class GUI:
    def __init__(self, memo_service, user_service):
        self.__memo_service = memo_service
        self.__user_service = user_service
        self.__user = None

    def start(self):
        app = QApplication(sys.argv)

        window = QWidget()

        window.setWindowTitle('Muistio')
        window.setGeometry(100, 100, 500, 500)

        label = QLabel('<h1>Muistio</h1>', parent=window)
        window.show()

        sys.exit(app.exec_())

    def run(self):
        print('tööt')
