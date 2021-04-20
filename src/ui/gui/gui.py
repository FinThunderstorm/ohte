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
        self.__user = None

        self.__memo_view = MemoView(
            self.__screen_available, self.__memo_service, self.__user)

    def start(self):
        self.__memo_view.run()

        # window = QWidget()
        # main_layout = QGridLayout()
        # menu_layout = QVBoxLayout()
        # editor_layout = QVBoxLayout()

        # main_layout.addLayout(menu_layout, 0, 0)
        # main_layout.addLayout(editor_layout, 0, 1)

        # window.setWindowTitle('Muistio')
        # window.setGeometry(2760, 1360, 1080, 800)

        # # editor side
        # memo_title = "Title of Memo"
        # memo_date = "Sun 18.4.2021 16:54"
        # memo_author_name = "Niilo Nönnönnöö"

        # title_label = QLabel('<h1><u>'+memo_title+'</u></h1>')
        # info_label = QLabel('<p>'+memo_date+' | '+memo_author_name+'</p>')
        # text_edit = QPlainTextEdit('Testing preloaded text')

        # toolbar_layout = QHBoxLayout()
        # save_button = QPushButton('Save')
        # cancel_button = QPushButton('Cancel')
        # remove_button = QPushButton('Remove')
        # toolbar_layout.addWidget(save_button)
        # toolbar_layout.addWidget(cancel_button)
        # toolbar_layout.addWidget(remove_button)
        # toolbar_layout.addStretch()

        # editor_layout.addWidget(title_label)
        # editor_layout.addWidget(info_label)
        # editor_layout.addWidget(text_edit)
        # editor_layout.addLayout(toolbar_layout)

        # # menu and memo selector
        # main_menu_button = QPushButton('Main menu')
        # menu_layout.addWidget(main_menu_button)
        # menu_layout.addSpacing(25)

        # memos = self.__memo_service.get()
        # memo_index = 1
        # for memo in memos:
        #     memo = QPushButton(memo.title)
        #     menu_layout.addWidget(memo)
        #     memo_index += 1

        # menu_layout.addStretch()

        # new_memo_button = QPushButton('New memo')
        # menu_layout.addWidget(new_memo_button)

        # window.setLayout(main_layout)
        # window.show()

        sys.exit(self.__app.exec_())

    def run(self):
        print('tööt')
