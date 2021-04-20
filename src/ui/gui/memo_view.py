from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QPlainTextEdit, QLineEdit


class EditorToolbar:
    def __init__(self, main):
        self.layout = QHBoxLayout()
        self.__handlers = main.editor_handlers
        self.__main = main

        self.__initialize()

    def __initialize(self):
        save_button = QPushButton('Save')
        cancel_button = QPushButton('Cancel')
        remove_button = QPushButton('Remove')
        self.layout.addWidget(save_button)
        self.layout.addWidget(cancel_button)
        self.layout.addWidget(remove_button)
        self.layout.addStretch()


class ViewToolbar():
    def __init__(self, main):
        self.layout = QHBoxLayout()
        self.__handlers = main.viewer_handlers
        self.__main = main

        self.__initialize()

    def __initialize(self):
        edit_button = QPushButton('Edit')
        remove_button = QPushButton('Remove')
        self.layout.addWidget(edit_button)
        self.layout.addWidget(remove_button)
        self.layout.addStretch()


class Editor:
    def __init__(self, main):
        self.layout = QVBoxLayout()
        self.__handlers = main.editor_handlers
        self.__main = main

        self.__toolbar = EditorToolbar(self.__main)

        self.__memo = None
        self.__objects = {}

        self.__initialize()

    def __initialize(self):
        self.__objects["title_edit"] = QLineEdit()
        self.__objects["info_label"] = QLabel()
        self.__objects["content_edit"] = QPlainTextEdit()

        self.layout.addWidget(self.__objects["title_edit"])
        self.layout.addWidget(self.__objects["info_label"])
        self.layout.addWidget(self.__objects["content_edit"])
        self.layout.addLayout(self.__toolbar.layout)

    def set_memo(self, memo):
        self.__memo = memo

        self.__objects["title_edit"].setText(self.__memo.title)
        self.__objects["info_label"].setText('<p>'+self.__memo.date.strftime(
            '%a %d.%m.%Y %H:%M')+' | '+self.__memo.author.firstname+" "+self.__memo.author.lastname+'</p>')
        self.__objects["content_edit"].insertPlainText(self.__memo.content)


class Viewer:
    def __init__(self, main):
        self.layout = QVBoxLayout()
        self.__handlers = main.viewer_handlers
        self.__main = main

        self.__toolbar = ViewToolbar(self.__main)
        self.__memo = None
        self.__objects = {}

        self.__initialize()

    def __initialize(self):
        self.__objects["title_label"] = QLabel()
        self.__objects["info_label"] = QLabel()
        self.__objects["content_label"] = QLabel()

        self.layout.addWidget(self.__objects["title_label"])
        self.layout.addWidget(self.__objects["info_label"])
        self.layout.addWidget(self.__objects["content_label"])
        self.layout.addStretch()
        self.layout.addLayout(self.__toolbar.layout)

    def set_memo(self, memo):
        self.__memo = memo

        print(memo)

        self.__objects["title_label"].setText(
            '<h1><u>'+self.__memo.title+'</u></h1>')
        self.__objects["info_label"].setText('<p>'+self.__memo.date.strftime(
            '%a %d.%m.%Y %H:%M')+' | '+self.__memo.author.firstname+" "+self.__memo.author.lastname+'</p>')
        self.__objects["content_label"].setText(self.__memo.content)


class MainMenu:
    def __init__(self, main):
        self.__main = main
        self.layout = QVBoxLayout()
        self.__handlers = main.main_menu_handlers

        self.__memos = main.memos

        self.__initialize()

    def __initialize(self):
        main_menu_button = QPushButton('Main menu')
        self.layout.addWidget(main_menu_button)
        self.layout.addSpacing(25)

        for memo in self.__memos:
            memo_button = QPushButton(memo.title)
            memo_button.clicked.connect(
                self.__handlers["show_memo"](self.__main, memo.id))
            self.layout.addWidget(memo_button)

        self.layout.addStretch()

        new_memo_button = QPushButton('New memo')
        self.layout.addWidget(new_memo_button)


class MemoView(QWidget):
    def __init__(self, screen, memo_service, user):
        super().__init__()
        self.__screen_width, self.__screen_height = screen
        self.memo_service = memo_service
        self.objects = {}

        self.user = user
        self.memos = self.memo_service.get()
        self.testing_memo = self.memo_service.get(
            'id', self.memos[2].id)

        self.main_menu_handlers = {
            "show_memo": self.show_memo,
        }
        self.editor_handlers = {
            "edit_memo": self.edit_memo,
        }
        self.viewer_handlers = {}

        self.layout = QGridLayout()
        self.active_screen = 'viewer'

        self.main_menu = MainMenu(self)
        self.editor = Editor(self)
        self.viewer = Viewer(self)

        self.__initialize()

    def __initialize(self):
        self.setWindowTitle('Muistio')
        # self.setGeometry(2760, 1360, 1080, 800) # used for dev purposes only
        self.setGeometry(0, 0, self.__screen_width, self.__screen_height)

        self.layout.addLayout(self.main_menu.layout, 0, 0)
        #self.__layout.addLayout(self.__editor.layout, 0, 1)
        self.layout.addLayout(self.viewer.layout, 0, 1)

        self.setLayout(self.layout)

    def show_memo(self, main, memo_id):
        main.viewer.set_memo(main.memo_service.get('id', memo_id))
        if main.active_screen == "editor":
            # tee varmistus dialog ikkuna, et ooksä tosissas vaihtamassa
            main.layout.removeItem(self.viewer.layout)
            main.layout.addLayout(self.editor.layout, 0, 1)

    def edit_memo(self, main, memo_id):
        main.editor.set_memo(main.memo_service.get('id', memo_id))
        main.layout.removeItem(main.viewer.layout)
        main.layout.addLayout(main.editor.layout, 0, 1)

    def run(self):
        self.show()
        self.viewer.set_memo(self.testing_memo)
        self.editor.set_memo(self.testing_memo)
