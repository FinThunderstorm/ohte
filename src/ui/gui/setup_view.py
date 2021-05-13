from PyQt5.QtWidgets import QApplication, QWidget, QDialog, QFileDialog, QScrollArea, QGridLayout, QVBoxLayout, QHBoxLayout, QTabWidget, QLabel, QPushButton, QTextEdit, QLineEdit, QFrame, QComboBox
from PyQt5.QtCore import Qt
from ui.gui.error_view import ErrorView


class SetupView(QDialog):
    """SetupView handles viewing and editing settings in GUI.

    Args:
        QDialog: imported from PyQt5.QtWidgets
    """

    def __init__(self, screen, objects, layouts, frames, config, user, user_service):
        """Constructor for SetupView.

        Args:
            screen: available screen width and height
            objects: shared dict between views holding each others objects
            layouts: shared dict between views holding each others layouts
            frames: shared dict between views holding each others frames
            config: apps configuration object
            user: current user list to get logged user
            user_service: handler service for users
        """
        super().__init__()
        self.__screen = screen
        self.__screen_width, self.__screen_height = screen
        self.__active_width = 400
        self.__active_height = 300

        self.objects = objects if objects else {}
        self.layouts = layouts if layouts else {}
        self.frames = frames if frames else {}

        self.__user_service = user_service

        self.config = config

        self.__user = user

        self.layout = QGridLayout()

    def __initialize(self):
        width_pos = self.__screen_width//2 - self.__active_width//2
        height_pos = self.__screen_height//2 - self.__active_height//2

        self.setWindowTitle("Settings")

        self.setGeometry(width_pos, height_pos,
                         self.__active_width, self.__active_height)

        self.setLayout(self.layout)

    def __initialize_shared_objects(self):
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
            ["", "auto", "800x600", "1280x720", "1366x768", "1650x1050", "1920x1080", "1920x1200", "3840x2160"])
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
            self.objects[0]["settings_view"]["db_pw_label"], 5, 0)

        self.objects[0]["settings_view"]["db_pw_edit"] = QLineEdit()
        self.objects[0]["settings_view"]["db_pw_edit"].setEchoMode(
            QLineEdit.Password)
        self.layout.addWidget(
            self.objects[0]["settings_view"]["db_pw_edit"], 5, 1)

        self.objects[0]["settings_view"]["save_button"] = QPushButton('Save')
        self.objects[0]["settings_view"]["save_button"].clicked.connect(
            self.__handle_settings_save)
        self.layout.addWidget(
            self.objects[0]["settings_view"]["save_button"], 6, 0)

        self.objects[0]["settings_view"]["cancel_button"] = QPushButton(
            'Cancel')
        self.objects[0]["settings_view"]["cancel_button"].clicked.connect(
            self.__close)
        self.layout.addWidget(
            self.objects[0]["settings_view"]["cancel_button"], 6, 1)

    def run(self):
        """run is used to show settings view
        """
        self.__initialize_settings()
        self.exec_()

    def run_standalone(self):
        """run_standalone is used to show settings view for the first time.
        """
        self.__initialize_first_time()
        self.exec_()

    def __close(self):
        self.done(1)
        for widget in self.objects[0]["settings_view"].values():
            widget.setParent(None)

    def __initialize_first_time(self):
        self.__initialize_shared_objects()
        self.__load_current_configuration()

    def __initialize_settings(self):
        self.__initialize_shared_objects()
        self.__load_current_configuration()

        # käyttäjän tietojen muokkaaminen / poistaminen
        self.objects[0]["settings_view"]["user_label"] = QLabel(
            '<h3>User settings</h3>')
        self.layout.addWidget(
            self.objects[0]["settings_view"]["user_label"], 7, 0)

        self.objects[0]["settings_view"]["firstname_label"] = QLabel(
            'Firstname:')
        self.layout.addWidget(
            self.objects[0]["settings_view"]["firstname_label"], 8, 0)

        self.objects[0]["settings_view"]["firstname_edit"] = QLineEdit()
        self.layout.addWidget(
            self.objects[0]["settings_view"]["firstname_edit"], 8, 1)

        self.objects[0]["settings_view"]["lastname_label"] = QLabel(
            'Lastname:')
        self.layout.addWidget(
            self.objects[0]["settings_view"]["lastname_label"], 9, 0)

        self.objects[0]["settings_view"]["lastname_edit"] = QLineEdit()
        self.layout.addWidget(
            self.objects[0]["settings_view"]["lastname_edit"], 9, 1)

        self.objects[0]["settings_view"]["password_label"] = QLabel(
            'Password:')
        self.layout.addWidget(
            self.objects[0]["settings_view"]["password_label"], 10, 0)

        self.objects[0]["settings_view"]["password_edit"] = QLineEdit()
        self.objects[0]["settings_view"]["password_edit"].setEchoMode(
            QLineEdit.Password)
        self.layout.addWidget(
            self.objects[0]["settings_view"]["password_edit"], 10, 1)

        self.objects[0]["settings_view"]["save_u_button"] = QPushButton('Save')
        self.objects[0]["settings_view"]["save_u_button"].clicked.connect(
            self.__handle_user_save)
        self.layout.addWidget(
            self.objects[0]["settings_view"]["save_u_button"], 11, 0)

        self.objects[0]["settings_view"]["cancel_u_button"] = QPushButton(
            'Remove')
        self.objects[0]["settings_view"]["cancel_u_button"].clicked.connect(
            self.__handle_user_remove)
        self.layout.addWidget(
            self.objects[0]["settings_view"]["cancel_u_button"], 11, 1)

        self.objects[0]["settings_view"]["cancel_u_button"] = QPushButton(
            'Cancel')
        self.objects[0]["settings_view"]["cancel_u_button"].clicked.connect(
            self.__close)
        self.layout.addWidget(
            self.objects[0]["settings_view"]["cancel_u_button"], 12, 0)

        self.__load_current_user()

    def __handle_user_save(self):
        if not self.__user[0]:
            ErrorView(self.__screen, "Error while saving",
                      'There were a problem while trying to save. ' +
                      'Please check your input and try again.')
        firstname = self.objects[0]["settings_view"]["firstname_edit"].text()
        lastname = self.objects[0]["settings_view"]["lastname_edit"].text()
        password = self.objects[0]["settings_view"]["password_edit"].text()
        if password == "":
            password = self.__user[0].password
        res = self.__user_service.update(self.__user[0].id,
                                         firstname, lastname,
                                         self.__user[0].username,
                                         password)
        if res:
            self.objects[0]["extended_menu"]["name_label"].setText(
                res.firstname+" "+res.lastname)
            self.__user[0] = res
            self.__close()
        else:
            ErrorView(self.__screen, "Error while saving",
                      'There were a problem while trying to save. ' +
                      'Please check your input and try again.')

    def __handle_user_remove(self):
        if not self.__user[0]:
            ErrorView(self.__screen, "Error while removing",
                      'There were a problem while trying to remove. ' +
                      'Please try again.')
        res = self.__user_service.remove(self.__user[0].id)
        if res:
            self.frames[0]["memoview"].handle_logout()
            self.__close()
        else:
            ErrorView(self.__screen, "Error while removing",
                      'There were a problem while trying to remove. ' +
                      'Please try again.')

    def __handle_settings_save(self):
        try:
            self.config.set_value(
                "res_index", self.objects[0]["settings_view"]["resolution_selector"].currentIndex())
            self.config.set_value(
                "res_format", self.objects[0]["settings_view"]["resolution_selector"].currentText())
            self.config.set_value(
                "db_username", self.objects[0]["settings_view"]["db_user_edit"].text())
            db_password = self.objects[0]["settings_view"]["db_pw_edit"].text()
            if db_password != "":
                self.config.set_value(
                    "db_password", db_password)
        except ValueError:
            ErrorView(self.__screen, "Error while saving",
                      'There were a problem while trying to save. ' +
                      'Please check your input and try again.')

        self.config.save()
        self.__close()

    def __load_current_configuration(self):
        configs = self.config.get_all()

        if not configs:
            self.__handle_load_error()
            self.__close()

        self.objects[0]["settings_view"]["resolution_selector"].setCurrentIndex(
            int(configs["RES_INDEX"]))
        self.objects[0]["settings_view"]["db_user_edit"].setText(
            configs["DB_USERNAME"])

    def __load_current_user(self):
        if self.__user[0]:
            self.objects[0]["settings_view"]["firstname_edit"].setText(
                self.__user[0].firstname)
            self.objects[0]["settings_view"]["lastname_edit"].setText(
                self.__user[0].lastname)
