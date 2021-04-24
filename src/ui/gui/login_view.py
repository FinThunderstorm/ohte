from PyQt5.QtWidgets import QApplication, QWidget, QDialog, QGridLayout, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QPlainTextEdit, QLineEdit, QFrame


class LoginView(QFrame):
    def __init__(self, screen, user_service, user, objects, layouts, frames):
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
        for key in self.objects[0].keys():
            print(key)
        self.__initialize_login()

        self.setWindowTitle('Muistio')
        self.setGeometry(2760, 1360, 1080, 800)  # used for dev purposes only
        #self.setGeometry(0, 0, self.__screen_width, self.__screen_height)

        self.layout.addWidget(self.frames[0]["login"])
        # # self.layout.addLayout(self.layouts[0]["editor"], 0, 1)
        # self.layout.addWidget(self.frames[0]["editor"], 0, 1)
        # self.layout.addWidget(self.frames[0]["viewer"], 0, 1)
        # # self.layout.addLayout(self.layouts[0]["viewer"], 0, 1)

        self.setLayout(self.layout)

    def __initialize_login(self):
        self.frames[0]["login"] = QFrame()
        self.objects[0]["login"] = {}
        self.layouts[0]["login"] = QGridLayout()
        self.frames[0]["login"].setLayout(self.layouts[0]["login"])

        self.objects[0]["login"]["app_name_label"] = QLabel(
            "<h1>muistio</h1>")
        self.layouts[0]["login"].addWidget(
            self.objects[0]["login"]["app_name_label"], 0, 0)

        self.objects[0]["login"]["username_label"] = QLabel("username")
        self.layouts[0]["login"].addWidget(
            self.objects[0]["login"]["username_label"], 1, 0)

        self.objects[0]["login"]["username_edit"] = QLineEdit()
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
            self.objects[0]["login"]["login_button"], 3, 0)

        self.objects[0]["login"]["create_button"] = QPushButton(
            "create new user")
        self.layouts[0]["login"].addWidget(
            self.objects[0]["login"]["create_button"], 4, 0)

    def __login(self):
        username = self.objects[0]["login"]["username_edit"].text()
        password = self.objects[0]["login"]["password_edit"].text()
        result = self.user_service.login(username, password)
        if result:
            self.__user[0] = result
            self.objects[0]["login"]["app_name_label"].setText("logged in")
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

    def run(self):
        self.show()
