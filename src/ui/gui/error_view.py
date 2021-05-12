from PyQt5.QtWidgets import QApplication, QWidget, QDialog, QFileDialog, QScrollArea, QGridLayout, QVBoxLayout, QHBoxLayout, QTabWidget, QLabel, QPushButton, QTextEdit, QLineEdit, QFrame, QComboBox
from PyQt5.QtCore import Qt


class ErrorView(QDialog):
    """ErrorView handles showing error messages.

    Args:
        QDialog: imported from PyQt5.QtWidgets
    """

    def __init__(self, screen, title, message):
        """Constructor for ErrorView, initializes it and runs it.

        Args:
            screen: available screen width and height
            title: messages title in window
            message: error message that is shown to user
        """
        super().__init__()
        self.__screen_width, self.__screen_height = screen
        self.__active_width = 400
        self.__active_height = 150

        self.objects = {}

        self.__message = message
        self.__title = title

        self.layout = QVBoxLayout()

        self.__initialize()
        self.__run()

    def __initialize(self):
        width_pos = self.__screen_width//2 - self.__active_width//2
        height_pos = self.__screen_height//2 - self.__active_height//2

        self.setGeometry(width_pos, height_pos,
                         self.__active_width, self.__active_height)
        self.setFixedSize(self.__active_width, self.__active_height)
        self.setWindowTitle(self.__title)
        self.setLayout(self.layout)

        self.objects["message"] = QLabel('<center>'+self.__message+'</center>')
        self.objects["message"].setWordWrap(True)
        self.objects["ok"] = QPushButton("Ok")

        self.objects["ok"].clicked.connect(self.__ok)

        self.layout.addWidget(self.objects["message"])
        self.layout.addWidget(self.objects["ok"])

    def __ok(self):
        self.done(1)

    def __run(self):
        self.exec_()
