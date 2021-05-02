from utils.helpers import get_empty_memo, get_id
from PyQt5.QtWidgets import QApplication, QWidget, QDialog, QFileDialog, QScrollArea, QGridLayout, QVBoxLayout, QHBoxLayout, QTabWidget, QLabel, QPushButton, QTextEdit, QLineEdit, QFrame, QComboBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIntValidator
from markdown2 import markdown
from functools import partial


class SetupView(QDialog):
    def __init__(self, screen, objects, layouts, frames, config):
        super().__init__()
        self.__screen_width, self.__screen_height = screen
        self.__active_width = 400
        self.__active_height = 600

        self.objects = objects if objects else {}
        self.layouts = layouts if layouts else {}
        self.frames = frames if frames else {}

        self.config = config

        self.layout = QGridLayout()

    def __initialize(self):
        self.setWindowTitle('Settings')
        width_pos = self.__screen_width//2 - self.__active_width//2
        height_pos = self.__screen_height//2 - self.__active_height//2

        self.setGeometry(width_pos, height_pos,
                         self.__active_width, self.__active_height)

        self.setLayout(self.layout)

    def __initalize_shared_objects(self):
        self.__initialize()
        self.objects[0]["settings_view"] = {}

        self.objects[0]["settings_view"]["info_label"] = QLabel(
            '<h1>Settings</h1>')
        self.layout.addWidget(
            self.objects[0]["settings_view"]["info_label"], 0, 0)

        self.objects[0]["settings_view"]["app_settings_info"] = QLabel(
            '<h3>App settings</h3>')
        self.layout.addWidget(
            self.objects[0]["settings_view"]["app_settings_info"], 1, 0)

        # resoluutio
        self.objects[0]["settings_view"]["resolution_label"] = QLabel(
            'Screen resolution:')
        self.layout.addWidget(
            self.objects[0]["settings_view"]["resolution_label"], 2, 0)

        self.objects[0]["settings_view"]["resolution_selector"] = QComboBox()
        self.objects[0]["settings_view"]["resolution_selector"].addItems(
            ["", "auto", "800x600", "1280x720", "1366x768", "1920x1080", "1920x1200", "3840x2160"])
        self.layout.addWidget(
            self.objects[0]["settings_view"]["resolution_selector"], 2, 1)

        self.objects[0]["settings_view"]["db_settings_label"] = QLabel(
            '<h3>Database settings</h3>')
        self.layout.addWidget(
            self.objects[0]["settings_view"]["db_settings_label"], 3, 0)

        # database_user
        self.objects[0]["settings_view"]["db_user_label"] = QLabel(
            'Database username:')
        self.layout.addWidget(
            self.objects[0]["settings_view"]["db_user_label"], 4, 0)

        self.objects[0]["settings_view"]["db_user_edit"] = QLineEdit()
        self.layout.addWidget(
            self.objects[0]["settings_view"]["db_user_edit"], 4, 1)

        # database_password
        self.objects[0]["settings_view"]["db_pw_label"] = QLabel(
            'Database password:')
        self.layout.addWidget(
            self.objects[0]["settings_view"]["db_pw_label"], 4, 0)

        self.objects[0]["settings_view"]["db_pw_edit"] = QLineEdit()
        self.objects[0]["settings_view"]["db_pw_edit"].setEchoMode(
            QLineEdit.Password)
        self.layout.addWidget(
            self.objects[0]["settings_view"]["db_pw_edit"], 4, 1)

        self.objects[0]["settings_view"]["save_button"] = QPushButton('Save')
        self.objects[0]["settings_view"]["save_button"].clicked.connect(
            self.__handle_settings_save)
        self.layout.addWidget(
            self.objects[0]["settings_view"]["save_button"], 5, 0)

        self.objects[0]["settings_view"]["cancel_button"] = QPushButton(
            'Cancel')
        self.objects[0]["settings_view"]["cancel_button"].clicked.connect(
            self.__close)
        self.layout.addWidget(
            self.objects[0]["settings_view"]["cancel_button"], 5, 1)

    def run(self):
        self.exec_()

    def __close(self):
        self.done(1)

    def initialize_first_time(self):
        self.__initialize_shared_objects()

    def initialize_settings(self):
        self.__load_current_configuration()
        self.__initalize_shared_objects()

        # käyttäjän tietojen muokkaaminen / poistaminen
        self.objects[0]["settings_view"]["user_label"] = QLabel(
            '<h3>User settings</h3>')
        self.layout.addWidget(
            self.objects[0]["settings_view"]["user_label"], 6, 0)

        self.__load_current_user()

    def __handle_settings_save(self):
        try:
            self.config.set_value(
                "res_index", self.objects[0]["settings_view"]["resolution_selector"].currentIndex())
            self.config.set_value(
                "res_format", self.objects[0]["settings_view"]["resolution_selector"].currentText())
            self.config.set_value(
                "db_user", self.objects[0]["settings_view"]["db_user_edit"].text())
            self.config.set_value(
                "db_password", self.objects[0]["settings_view"]["db_pw_edit"].text())
        except ValueError:
            return

        self.config.save()
        self.__close()

    def __load_current_configuration(self):
        configs = self.config.check()

        if not configs:
            self.__handle_load_error()
            self.__close()

        self.objects[0]["settings_view"]["resolution_selector"].setCurrentIndex(
            configs["res_index"])
        self.objects[0]["settings_view"]["db_user_edit"].setText(
            configs["db_user"])

    def __load_current_user(self):
        pass
