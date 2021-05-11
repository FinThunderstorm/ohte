from PyQt5.QtWidgets import QApplication, QWidget, QDialog, QGridLayout, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QPlainTextEdit, QLineEdit, QFrame


class LoginView(QFrame):
    """LoginView handles user login and user creation parts of GUI.

    Args:
        QFrame: imported from PyQt5.QtWidgets
    """

    def __init__(self, screen, user_service, user, objects, layouts, frames):
        """Constructor for preparing the LoginView.

        Args:
            screen: available screen width and height
            user_service: service handler for users
            user: ref to current logged user in list.
            objects: shared dict between views holding each others objects
            layouts: shared dict between views holding each others layouts
            frames: shared dict between views holding each others frames
        """
        super().__init__()
        self.__screen_width, self.__screen_height = screen
        self.user_service = user_service
        self.objects = objects if objects else {}
        self.layouts = layouts if layouts else {}
        self.frames = frames if frames else {}

        self.layout = QVBoxLayout()
        self.__active_screen = "login"

        self.__user = user

    def initialize(self):
        """initialize is used to build the view up.
        """
        self.__initialize_login()
        self.__initialize_create_user()

        self.setWindowTitle('Muistio')
        width = 400
        height = 600
        width_pos = self.__screen_width//2 - width//2
        height_pos = self.__screen_height//2 - height//2

        self.setGeometry(width_pos, height_pos, width, height)

        self.layout.addWidget(self.frames[0]["login"])
        self.layout.addWidget(self.frames[0]["create_new_user"])

        self.frames[0]["create_new_user"].hide()

        self.setLayout(self.layout)

    def __initialize_login(self):
        self.frames[0]["login"] = QFrame()
        self.objects[0]["login"] = {}
        self.layouts[0]["login"] = QGridLayout()
        self.frames[0]["login"].setLayout(self.layouts[0]["login"])

        self.objects[0]["login"]["app_name_label"] = QLabel(
            "<h1>muistio</h1>")
        self.layouts[0]["login"].addWidget(
            self.objects[0]["login"]["app_name_label"], 0, 0, 1, 2)

        self.objects[0]["login"]["username_label"] = QLabel("username")
        self.layouts[0]["login"].addWidget(
            self.objects[0]["login"]["username_label"], 1, 0)

        self.objects[0]["login"]["username_edit"] = QLineEdit()
        self.objects[0]["login"]["username_edit"].returnPressed.connect(
            self.__login)
        self.layouts[0]["login"].addWidget(
            self.objects[0]["login"]["username_edit"], 1, 1)

        self.objects[0]["login"]["password_label"] = QLabel("password")
        self.layouts[0]["login"].addWidget(
            self.objects[0]["login"]["password_label"], 2, 0)

        self.objects[0]["login"]["password_edit"] = QLineEdit()
        self.objects[0]["login"]["password_edit"].setEchoMode(
            QLineEdit.Password)
        self.objects[0]["login"]["password_edit"].returnPressed.connect(
            self.__login)
        self.layouts[0]["login"].addWidget(
            self.objects[0]["login"]["password_edit"], 2, 1)

        self.objects[0]["login"]["login_button"] = QPushButton("login")
        self.objects[0]["login"]["login_button"].clicked.connect(self.__login)
        self.layouts[0]["login"].addWidget(
            self.objects[0]["login"]["login_button"], 3, 0, 1, 2)

        self.objects[0]["login"]["create_button"] = QPushButton(
            "create new user")
        self.objects[0]["login"]["create_button"].clicked.connect(
            self.__show_create_new_user)
        self.layouts[0]["login"].addWidget(
            self.objects[0]["login"]["create_button"], 4, 0, 1, 2)

    def __show_create_new_user(self):
        self.frames[0]["login"].hide()
        self.frames[0]["create_new_user"].show()
        self.objects[0]["login"]["username_edit"].setText('')
        self.objects[0]["login"]["password_edit"].setText('')

    def __login(self):
        username = self.objects[0]["login"]["username_edit"].text()
        password = self.objects[0]["login"]["password_edit"].text()
        result = self.user_service.login(username, password)
        if result:
            self.__user[0] = result

            self.objects[0]["extended_menu"]["name_label"].setText(
                self.__user[0].firstname+" "+self.__user[0].lastname)

            self.frames[0]["loginview"].hide()
            self.frames[0]["memoview"].run()
        else:
            self.__login_error()

        username = self.objects[0]["login"]["username_edit"].setText('')
        password = self.objects[0]["login"]["password_edit"].setText('')

    def __login_error(self):
        self.frames[0]["login_error"] = QDialog()
        self.objects[0]["login_error"] = {}
        self.frames[0]["login_error"].setWindowTitle("Error while logging in")

        self.layouts[0]["login_error"] = QVBoxLayout()
        self.objects[0]["login_error"]["error_message"] = QLabel(
            "username or password incorrect")
        self.layouts[0]["login_error"].addWidget(
            self.objects[0]["login_error"]["error_message"])

        self.objects[0]["login_error"]["ok_button"] = QPushButton('ok')
        self.objects[0]["login_error"]["ok_button"].clicked.connect(
            self.__handle_ok)
        self.layouts[0]["login_error"].addWidget(
            self.objects[0]["login_error"]["ok_button"])

        self.frames[0]["login_error"].setLayout(self.layouts[0]["login_error"])
        self.frames[0]["login_error"].exec_()

    def __handle_ok(self):
        self.frames[0]["login_error"].done(1)

    def __initialize_create_user(self):
        self.frames[0]["create_new_user"] = QFrame()
        self.objects[0]["create_new_user"] = {}
        self.layouts[0]["create_new_user"] = QGridLayout()
        self.frames[0]["create_new_user"].setLayout(
            self.layouts[0]["create_new_user"])

        self.objects[0]["create_new_user"]["page_title_label"] = QLabel(
            "<h1>create</h1><h2>new user</h2>")
        self.layouts[0]["create_new_user"].addWidget(
            self.objects[0]["create_new_user"]["page_title_label"], 0, 0, 1, 2)

        self.objects[0]["create_new_user"]["firstname_label"] = QLabel(
            "firstname")
        self.layouts[0]["create_new_user"].addWidget(
            self.objects[0]["create_new_user"]["firstname_label"], 1, 0)

        self.objects[0]["create_new_user"]["firstname_edit"] = QLineEdit()
        self.layouts[0]["create_new_user"].addWidget(
            self.objects[0]["create_new_user"]["firstname_edit"], 1, 1)

        self.objects[0]["create_new_user"]["lastname_label"] = QLabel(
            "lastname")
        self.layouts[0]["create_new_user"].addWidget(
            self.objects[0]["create_new_user"]["lastname_label"], 2, 0)

        self.objects[0]["create_new_user"]["lastname_edit"] = QLineEdit()
        self.layouts[0]["create_new_user"].addWidget(
            self.objects[0]["create_new_user"]["lastname_edit"], 2, 1)

        self.objects[0]["create_new_user"]["username_label"] = QLabel(
            "username")
        self.layouts[0]["create_new_user"].addWidget(
            self.objects[0]["create_new_user"]["username_label"], 3, 0)

        self.objects[0]["create_new_user"]["username_edit"] = QLineEdit()
        self.layouts[0]["create_new_user"].addWidget(
            self.objects[0]["create_new_user"]["username_edit"], 3, 1)

        self.objects[0]["create_new_user"]["password_label"] = QLabel(
            "password")
        self.layouts[0]["create_new_user"].addWidget(
            self.objects[0]["create_new_user"]["password_label"], 4, 0)

        self.objects[0]["create_new_user"]["password_edit"] = QLineEdit()
        self.objects[0]["create_new_user"]["password_edit"].setEchoMode(
            QLineEdit.Password)
        self.objects[0]["create_new_user"]["password_edit"].returnPressed.connect(
            self.__create_new_user)
        self.layouts[0]["create_new_user"].addWidget(
            self.objects[0]["create_new_user"]["password_edit"], 4, 1)

        self.objects[0]["create_new_user"]["create_new_user_button"] = QPushButton(
            "Create")
        self.objects[0]["create_new_user"]["create_new_user_button"].clicked.connect(
            self.__create_new_user)
        self.layouts[0]["create_new_user"].addWidget(
            self.objects[0]["create_new_user"]["create_new_user_button"], 5, 0, 1, 2)

        self.objects[0]["create_new_user"]["cancel_button"] = QPushButton(
            "Back to login")
        self.objects[0]["create_new_user"]["cancel_button"].clicked.connect(
            self.__handle_create_cancel)
        self.layouts[0]["create_new_user"].addWidget(
            self.objects[0]["create_new_user"]["cancel_button"], 6, 0, 1, 2)

    def __create_new_user(self):
        firstname = self.objects[0]["create_new_user"]["firstname_edit"].text()
        lastname = self.objects[0]["create_new_user"]["lastname_edit"].text()
        username = self.objects[0]["create_new_user"]["username_edit"].text()
        password = self.objects[0]["create_new_user"]["password_edit"].text()

        result = self.user_service.create(
            firstname, lastname, username, password)
        if result:
            self.frames[0]["create_new_user"].hide()
            self.frames[0]["login"].show()
        self.objects[0]["create_new_user"]["firstname_edit"].setText('')
        self.objects[0]["create_new_user"]["lastname_edit"].setText('')
        self.objects[0]["create_new_user"]["username_edit"].setText('')
        self.objects[0]["create_new_user"]["password_edit"].setText('')

    def __handle_create_cancel(self):
        self.frames[0]["create_new_user"].hide()
        self.frames[0]["login"].show()
        self.objects[0]["create_new_user"]["firstname_edit"].setText('')
        self.objects[0]["create_new_user"]["lastname_edit"].setText('')
        self.objects[0]["create_new_user"]["username_edit"].setText('')
        self.objects[0]["create_new_user"]["password_edit"].setText('')

    def run(self):
        """run is used to show this part of GUI.
        """
        self.show()
