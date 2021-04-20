from functools import partial
from PyQt5.QtWidgets import QApplication, QWidget, QDialog, QGridLayout, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QPlainTextEdit, QLineEdit, QFrame
from utils.helpers import get_time


class MemoView(QWidget):
    def __init__(self, screen, memo_service, user):
        super().__init__()
        self.__screen_width, self.__screen_height = screen
        self.memo_service = memo_service
        self.objects = {}
        self.layouts = {}
        self.frames = {}

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
        self.__active_screen = 'viewer'

        self.__viewer_memo = None
        self.__editor_memo = None

        self.__initialize()

    def __initialize(self):
        self.__initialize_viewer()
        self.__initialize_editor()
        self.__initialize_mainmenu()

        self.setWindowTitle('Muistio')
        # self.setGeometry(2760, 1360, 1080, 800) # used for dev purposes only
        self.setGeometry(0, 0, self.__screen_width, self.__screen_height)

        self.layout.addLayout(self.layouts["mainmenu"], 0, 0)
        #self.layout.addLayout(self.layouts["editor"], 0, 1)
        self.layout.addWidget(self.frames["editor"], 0, 1)
        self.layout.addWidget(self.frames["viewer"], 0, 1)
        #self.layout.addLayout(self.layouts["viewer"], 0, 1)

        self.setLayout(self.layout)

    def run(self):
        self.show()
        self.__set_viewer_memo(self.testing_memo)
        self.__set_editor_memo(self.testing_memo)

    def __initialize_mainmenu(self):
        self.objects["mainmenu"] = {}
        self.objects["mainmenu_memos"] = {}
        self.layouts["mainmenu"] = QVBoxLayout()
        main_menu_button = QPushButton('Main menu')
        self.objects["mainmenu"]["mainmenu_button"] = main_menu_button
        self.layouts["mainmenu"].addWidget(main_menu_button)
        self.layouts["mainmenu"].addSpacing(25)

        self.layouts["mainmenu_memos"] = QVBoxLayout()
        for memo in self.memos:
            memo_button = QPushButton(memo.title)
            memo_button.clicked.connect(partial(self.__show_memo, memo.id))
            self.objects["mainmenu_memos"][memo.id] = memo_button
            self.layouts["mainmenu_memos"].addWidget(memo_button)

        self.layouts["mainmenu"].addLayout(self.layouts["mainmenu_memos"])
        self.layouts["mainmenu"].addStretch()

        new_memo_button = QPushButton('New memo')
        self.objects["mainmenu"]["new_memo_button"] = new_memo_button
        self.objects["mainmenu"]["new_memo_button"].clicked.connect(
            self.__new_memo)
        self.layouts["mainmenu"].addWidget(new_memo_button)

    def __initialize_viewer(self):
        self.frames["viewer"] = QFrame()
        self.objects["viewer"] = {}
        self.layouts["viewer"] = QVBoxLayout()
        self.frames["viewer"].setLayout(self.layouts["viewer"])

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

        self.objects["viewer_toolbar"]["edit_button"].clicked.connect(
            partial(self.__edit_memo, self.__viewer_memo.id))

    def __initialize_editor(self):
        self.objects["editor"] = {}
        self.layouts["editor"] = QVBoxLayout()
        self.frames["editor"] = QFrame()
        self.frames["editor"].setLayout(self.layouts["editor"])
        self.frames["editor"].hide()

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
        self.objects["editor"]["content_edit"].setPlainText(
            self.__editor_memo.content)

    def __initialize_editor_toolbar(self):
        self.objects["editor_toolbar"] = {}
        self.layouts["editor_toolbar"] = QHBoxLayout()

        self.objects["editor_toolbar"]["save_button"] = QPushButton('Save')
        self.objects["editor_toolbar"]["cancel_button"] = QPushButton('Cancel')
        self.objects["editor_toolbar"]["remove_button"] = QPushButton('Remove')

        self.objects["editor_toolbar"]["save_button"].clicked.connect(
            self.__save_memo)

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

    def __show_memo(self, memo_id):
        if self.__active_screen == "editor":
            self.frames["editor"].hide()
            self.frames["viewer"].show()
            self.__active_screen = "viewer"
        memo = self.memo_service.get("id", memo_id)
        self.__set_viewer_memo(memo)

    def __edit_memo(self, memo_id):
        if self.__active_screen == "viewer":
            self.frames["viewer"].hide()
            self.frames["editor"].show()
            self.__active_screen = "editor"
        memo = self.memo_service.get("id", memo_id)
        self.__set_editor_memo(memo)

    def __save_memo(self):
        title = self.objects["editor"]["title_edit"].text()
        content = self.objects["editor"]["content_edit"].toPlainText()
        updated_memo = self.memo_service.update(
            self.__editor_memo.id, self.__editor_memo.author.id, title, content, self.__editor_memo.date)
        if updated_memo:
            self.__set_viewer_memo(updated_memo)
            self.frames["editor"].hide()
            self.frames["viewer"].show()
            self.__active_screen = "viewer"

    def __handle_new_memo(self):
        title = self.objects["new_memo"]["title_edit"].text()
        print('title >', title)
        new_memo = self.memo_service.create(self.user.id, title)
        if new_memo:
            self.__set_editor_memo(new_memo)

            memo_button = QPushButton(new_memo.title)
            memo_button.clicked.connect(partial(self.__show_memo, new_memo.id))
            self.objects["mainmenu_memos"][new_memo.id] = memo_button
            self.layouts["mainmenu_memos"].addWidget(memo_button)

            self.frames["new_memo"].done(1)
            if self.__active_screen == "viewer":
                self.frames["viewer"].hide()
                self.frames["editor"].show()

    def __new_memo(self):
        self.frames["new_memo"] = QDialog()
        self.objects["new_memo"] = {}
        self.frames["new_memo"].setWindowTitle("New memo")

        self.layouts["new_memo"] = QVBoxLayout()
        self.objects["new_memo"]["title_label"] = QLabel("Title:")
        self.layouts["new_memo"].addWidget(
            self.objects["new_memo"]["title_label"])
        self.objects["new_memo"]["title_edit"] = QLineEdit()
        self.layouts["new_memo"].addWidget(
            self.objects["new_memo"]["title_edit"])
        self.objects["new_memo"]["create_button"] = QPushButton('Create')
        self.objects["new_memo"]["create_button"].clicked.connect(
            self.__handle_new_memo)
        self.layouts["new_memo"].addWidget(
            self.objects["new_memo"]["create_button"])

        self.frames["new_memo"].setLayout(self.layouts["new_memo"])

        self.frames["new_memo"].exec_()

    def __remove_memo_viewer(self):
        pass
