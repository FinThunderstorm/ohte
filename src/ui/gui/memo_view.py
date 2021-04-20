from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QPlainTextEdit, QLineEdit


class MemoView(QWidget):
    def __init__(self, screen, memo_service, user):
        super().__init__()
        self.__screen_width, self.__screen_height = screen
        self.memo_service = memo_service
        self.objects = {}
        self.layouts = {}

        self.user = user
        self.memos = self.memo_service.get()
        self.testing_memo = self.memo_service.get(
            'id', self.memos[2].id)

        self.main_menu_handlers = {
            "show_memo": "toot",
        }
        self.editor_handlers = {
            "edit_memo": "toot",
        }
        self.viewer_handlers = {}

        self.layout = QGridLayout()
        self.active_screen = 'viewer'

        self.__viewer_memo = None
        self.__editor_memo = None

        self.__initialize()

    def __initialize(self):
        self.__initialize_mainmenu()
        self.__initialize_viewer()
        self.__initialize_editor()

        self.setWindowTitle('Muistio')
        # self.setGeometry(2760, 1360, 1080, 800) # used for dev purposes only
        self.setGeometry(0, 0, self.__screen_width, self.__screen_height)

        self.layout.addLayout(self.layouts["mainmenu"], 0, 0)
        #self.layout.addLayout(self.layouts["editor"], 0, 1)
        self.layout.addLayout(self.layouts["viewer"], 0, 1)

        self.setLayout(self.layout)

    def run(self):
        self.show()
        self.__set_viewer_memo(self.testing_memo)
        self.__set_editor_memo(self.testing_memo)

    def __initialize_mainmenu(self):
        self.objects["mainmenu"] = {}
        self.layouts["mainmenu"] = QVBoxLayout()
        main_menu_button = QPushButton('Main menu')
        self.objects["mainmenu"]["mainmenu_button"] = main_menu_button
        self.layouts["mainmenu"].addWidget(main_menu_button)
        self.layouts["mainmenu"].addSpacing(25)

        for memo in self.memos:
            memo_button = QPushButton(memo.title)
            # memo_button.clicked.connect(
            #    self.__handlers["show_memo"](self.__main, memo.id))
            self.objects["mainmenu"][memo.id] = memo_button
            self.layouts["mainmenu"].addWidget(memo_button)

        self.layouts["mainmenu"].addStretch()

        new_memo_button = QPushButton('New memo')
        self.objects["mainmenu"]["new_memo_button"] = new_memo_button
        self.layouts["mainmenu"].addWidget(new_memo_button)

    def __initialize_viewer(self):
        self.objects["viewer"] = {}
        self.layouts["viewer"] = QVBoxLayout()

        self.__initialize_viewer_toolbar()
        self.__viewer_memo = None

        self.objects["viewer"]["title_label"] = QLabel()
        self.objects["viewer"]["info_label"] = QLabel()
        self.objects["viewer"]["content_label"] = QLabel()

        self.layouts["viewer"].addWidget(self.objects["viewer"]["title_label"])
        self.layouts["viewer"].addWidget(self.objects["viewer"]["info_label"])
        self.layouts["viewer"].addWidget(
            self.objects["viewer"]["content_label"])
        self.layouts["viewer"].addStretch()
        self.layouts["viewer"].addLayout(self.layouts["viewer_toolbar"])

    def __set_viewer_memo(self, memo):
        self.__viewer_memo = memo

        self.objects["viewer"]["title_label"].setText(
            '<h1><u>'+self.__viewer_memo.title+'</u></h1>')
        self.objects["viewer"]["info_label"].setText('<p>'+self.__viewer_memo.date.strftime(
            '%a %d.%m.%Y %H:%M')+' | '+self.__viewer_memo.author.firstname+" "+self.__viewer_memo.author.lastname+'</p>')
        self.objects["viewer"]["content_label"].setText(
            self.__viewer_memo.content)

    def __initialize_editor(self):
        self.objects["editor"] = {}
        self.layouts["editor"] = QVBoxLayout()

        self.__initialize_editor_toolbar()

        self.objects["editor"]["title_edit"] = QLineEdit()
        self.objects["editor"]["info_label"] = QLabel()
        self.objects["editor"]["content_edit"] = QPlainTextEdit()

        self.layouts["editor"].addWidget(self.objects["editor"]["title_edit"])
        self.layouts["editor"].addWidget(self.objects["editor"]["info_label"])
        self.layouts["editor"].addWidget(
            self.objects["editor"]["content_edit"])
        self.layouts["editor"].addLayout(self.layouts["editor_toolbar"])

    def __set_editor_memo(self, memo):
        self.__editor_memo = memo

        self.objects["editor"]["title_edit"].setText(self.__editor_memo.title)
        self.objects["editor"]["info_label"].setText('<p>'+self.__editor_memo.date.strftime(
            '%a %d.%m.%Y %H:%M')+' | '+self.__editor_memo.author.firstname+" "+self.__editor_memo.author.lastname+'</p>')
        self.objects["editor"]["content_edit"].insertPlainText(
            self.__editor_memo.content)

    def __initialize_editor_toolbar(self):
        self.objects["editor_toolbar"] = {}
        self.layouts["editor_toolbar"] = QHBoxLayout()

        self.objects["editor_toolbar"]["save_button"] = QPushButton('Save')
        self.objects["editor_toolbar"]["cancel_button"] = QPushButton('Cancel')
        self.objects["editor_toolbar"]["remove_button"] = QPushButton('Remove')
        self.layouts["editor_toolbar"].addWidget(
            self.objects["editor_toolbar"]["save_button"])
        self.layouts["editor_toolbar"].addWidget(
            self.objects["editor_toolbar"]["cancel_button"])
        self.layouts["editor_toolbar"].addWidget(
            self.objects["editor_toolbar"]["remove_button"])
        self.layouts["editor_toolbar"].addStretch()

    def __initialize_viewer_toolbar(self):
        self.objects["viewer_toolbar"] = {}
        self.layouts["viewer_toolbar"] = QHBoxLayout()

        self.objects["viewer_toolbar"]["edit_button"] = QPushButton('Edit')
        self.objects["viewer_toolbar"]["remove_button"] = QPushButton('Remove')
        self.layouts["viewer_toolbar"].addWidget(
            self.objects["viewer_toolbar"]["edit_button"])
        self.layouts["viewer_toolbar"].addWidget(
            self.objects["viewer_toolbar"]["remove_button"])
        self.layouts["viewer_toolbar"].addStretch()
