from utils.helpers import get_empty_memo, get_id
from PyQt5.QtWidgets import QApplication, QWidget, QDialog, QFileDialog, QScrollArea, QGridLayout, QVBoxLayout, QHBoxLayout, QTabWidget, QLabel, QPushButton, QTextEdit, QLineEdit, QFrame
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIntValidator
from markdown2 import markdown
from functools import partial


class MemoView(QFrame):
    def __init__(self, screen, memo_service, image_service, user, objects, layouts, frames, app):
        super().__init__()
        self.__screen_width, self.__screen_height = screen
        self.__active_width = 1650 if self.__screen_width > 1650 else self.__screen_width
        self.__active_height = 1050 if self.__screen_height > 1050 else self.__screen_height
        # self.setFixedWidth(self.__active_width)
        self.setFixedSize(self.__active_width, self.__active_height)

        self.memo_service = memo_service
        self.image_service = image_service

        self.objects = objects if objects else {}
        self.layouts = layouts if layouts else {}
        self.frames = frames if frames else {}

        self.user = user
        self.memos = []
        self.testing_memo = get_empty_memo()
        self.__app = app

        self.main_menu_handlers = {
            "show_memo": "toot",
        }
        self.editor_handlers = {
            "edit_memo": "toot",
        }
        self.viewer_handlers = {}

        self.layout = QGridLayout()
        self.__active_screen = 'viewer'
        self.__extended_menu = 'hidden'
        self.__viewer_state = 'hidden'
        self.__editor_state = 'hidden'

        self.__viewer_memo = None if len(self.memos) > 0 else get_empty_memo()
        self.__editor_memo = None if len(self.memos) > 0 else get_empty_memo()

    def initialize(self):
        self.__initialize_viewer()
        self.__initialize_editor()
        self.__initialize_mainmenu()

        self.setWindowTitle('Muistio')
        # self.setGeometry(2760, 1360, 1080, 800)  # used for dev purposes only
        width_pos = self.__screen_width//2 - self.__active_width//2
        height_pos = self.__screen_height//2 - self.__active_height//2

        self.setGeometry(width_pos, height_pos,
                         self.__active_width, self.__active_height)

        self.layout.addWidget(self.frames[0]["mainmenu"], 0, 0)
        # self.layout.addLayout(self.layouts[0]["editor"], 0, 1)
        self.layout.addWidget(self.frames[0]["editor"], 0, 1)
        self.layout.addWidget(self.frames[0]["viewer"], 0, 1)
        # self.layout.addLayout(self.layouts[0]["viewer"], 0, 1)

        self.layout.setAlignment(self.frames[0]["mainmenu"], Qt.AlignLeft)
        self.layout.setAlignment(self.frames[0]["editor"], Qt.AlignRight)
        self.layout.setAlignment(self.frames[0]["viewer"], Qt.AlignRight)

        self.setLayout(self.layout)

    def run(self):
        self.show()

        self.__update_memos_into_mainmenu()

        # self.__set_viewer_memo(self.testing_memo)
        # self.__set_editor_memo(self.testing_memo)

    def __initialize_mainmenu(self):
        self.frames[0]["mainmenu"] = QFrame()
        self.objects[0]["mainmenu"] = {}
        self.objects[0]["mainmenu_memos"] = {}
        self.layouts[0]["mainmenu"] = QVBoxLayout()

        self.frames[0]["mainmenu"].setFixedWidth(400)

        self.__initialize_extended_menu()

        self.objects[0]["mainmenu"]["mainmenu_button"] = QPushButton(
            'Main menu')
        self.objects[0]["mainmenu"]["mainmenu_button"].clicked.connect(
            self.__show_hide_extended_menu)
        self.layouts[0]["mainmenu"].addWidget(
            self.objects[0]["mainmenu"]["mainmenu_button"])

        self.layouts[0]["mainmenu"].addWidget(self.frames[0]["extended_menu"])

        self.layouts[0]["mainmenu"].addSpacing(25)

        self.layouts[0]["mainmenu_memos"] = QVBoxLayout()

        self.layouts[0]["mainmenu"].addLayout(
            self.layouts[0]["mainmenu_memos"])
        self.layouts[0]["mainmenu"].addStretch()

        new_memo_button = QPushButton('New memo')
        self.objects[0]["mainmenu"]["new_memo_button"] = new_memo_button
        self.objects[0]["mainmenu"]["new_memo_button"].clicked.connect(
            self.__new_memo)
        self.layouts[0]["mainmenu"].addWidget(new_memo_button)

        self.frames[0]["mainmenu"].setLayout(self.layouts[0]["mainmenu"])

    def __update_memos_into_mainmenu(self):
        memos = self.memo_service.get('author', self.user[0])
        if memos:
            for memo in memos:
                memo_button = QPushButton(memo.title)
                memo_button.clicked.connect(partial(self.__show_memo, memo.id))
                self.objects[0]["mainmenu_memos"][memo.id] = memo_button
                self.layouts[0]["mainmenu_memos"].addWidget(memo_button)

    def __empty_memos_from_mainmenu(self):
        for button in self.objects[0]["mainmenu_memos"].values():
            button.setParent(None)

    def __initialize_viewer(self):
        self.frames[0]["viewer"] = QFrame()
        self.objects[0]["viewer"] = {}
        self.layouts[0]["viewer"] = QVBoxLayout()
        self.frames[0]["viewer"].setLayout(self.layouts[0]["viewer"])
        self.frames[0]["viewer"].setFixedWidth(self.__active_width-400)

        self.__initialize_viewer_toolbar()
        self.__viewer_memo = None

        self.objects[0]["viewer"]["title_label"] = QLabel()
        self.objects[0]["viewer"]["info_label"] = QLabel()
        self.objects[0]["viewer"]["content_label"] = QLabel()
        self.objects[0]["viewer"]["content_scroll"] = QScrollArea()
        self.objects[0]["viewer"]["content_scroll"].setWidget(
            self.objects[0]["viewer"]["content_label"])

        self.layouts[0]["viewer"].addWidget(
            self.objects[0]["viewer"]["title_label"])
        self.layouts[0]["viewer"].addWidget(
            self.objects[0]["viewer"]["info_label"])
        self.layouts[0]["viewer"].addWidget(
            self.objects[0]["viewer"]["content_scroll"])

        self.objects[0]["viewer"]["content_scroll"].setWidgetResizable(True)
        self.objects[0]["viewer"]["content_scroll"].ensureWidgetVisible(
            self.objects[0]["viewer"]["content_label"])
        self.objects[0]["viewer"]["content_label"].setWordWrap(True)
        self.objects[0]["viewer"]["content_label"].setAlignment(Qt.AlignTop)
        self.objects[0]["viewer"]["content_scroll"].setAlignment(Qt.AlignTop)
        self.objects[0]["viewer"]["content_scroll"].setFixedSize(
            self.__active_width-450, self.__active_height-200)
        self.objects[0]["viewer"]["content_scroll"].setStyleSheet(
            'QScrollArea { border: 0px;}')
        self.layouts[0]["viewer"].addStretch()
        self.layouts[0]["viewer"].addLayout(self.layouts[0]["viewer_toolbar"])

        self.frames[0]["viewer"].hide()

    def __format_images(self, content):
        content_in_html = content
        img_tag = content_in_html.find("<img")
        while img_tag != -1:
            img_tag_src_starts = img_tag + 10
            img_tag_src_ends = content_in_html.find('"', img_tag_src_starts)
            img_src = content_in_html[img_tag_src_starts:img_tag_src_ends]

            img_id = get_id(img_src)

            if img_id:
                image = self.image_service.get('id', get_id(img_src))
                img_string = "data:image/"+image.filetype+";base64,"+image.image
                width = image.width if image.width < self.__active_width - \
                    500 else self.__active_width - 500

                content_in_html = content_in_html[:img_tag_src_ends+1] + \
                    ' width="'+str(width)+'" ' + \
                    content_in_html[img_tag_src_ends+1:]

                content_in_html = content_in_html[:img_tag_src_starts] + \
                    img_string+content_in_html[img_tag_src_ends:]
            img_tag = content_in_html.find("<img", img_tag_src_ends)

        return content_in_html

    def __set_viewer_memo(self, memo):
        self.__viewer_memo = memo

        content_in_html = markdown(self.__viewer_memo.content, extras=[
                                   "tables", "task_list", "cuddled-lists", "code-friendly"])

        content_in_html = self.__format_images(content_in_html)

        self.objects[0]["viewer"]["title_label"].setText(
            '<h1><u>'+self.__viewer_memo.title+'</u></h1>')
        self.objects[0]["viewer"]["info_label"].setText('<p>'+self.__viewer_memo.date.strftime(
            '%a %d.%m.%Y %H:%M')+' | '+self.__viewer_memo.author.firstname+" "+self.__viewer_memo.author.lastname+'</p>')
        self.objects[0]["viewer"]["content_label"].setText(content_in_html)

        self.objects[0]["viewer_toolbar"]["edit_button"].clicked.connect(
            partial(self.__edit_memo, self.__viewer_memo.id))

        self.frames[0]["viewer"].show()
        self.__viewer_state = "shown"

    def __initialize_editor(self):
        self.objects[0]["editor"] = {}
        self.layouts[0]["editor"] = QVBoxLayout()
        self.frames[0]["editor"] = QFrame()
        self.frames[0]["editor"].setLayout(self.layouts[0]["editor"])
        self.frames[0]["editor"].hide()
        self.frames[0]["editor"].setFixedWidth(self.__active_width-450)

        self.__initialize_editor_toolbar()

        self.objects[0]["editor"]["title_edit"] = QLineEdit()
        self.objects[0]["editor"]["info_label"] = QLabel()
        self.objects[0]["editor"]["content_edit"] = QTextEdit()

        self.layouts[0]["editor"].addWidget(
            self.objects[0]["editor"]["title_edit"])
        self.layouts[0]["editor"].addWidget(
            self.objects[0]["editor"]["info_label"])
        self.layouts[0]["editor"].addWidget(
            self.objects[0]["editor"]["content_edit"])
        self.layouts[0]["editor"].addLayout(self.layouts[0]["editor_toolbar"])

    def __set_editor_memo(self, memo):
        self.__editor_memo = memo

        self.objects[0]["editor"]["title_edit"].setText(
            self.__editor_memo.title)
        self.objects[0]["editor"]["info_label"].setText('<p>'+self.__editor_memo.date.strftime(
            '%a %d.%m.%Y %H:%M')+' | '+self.__editor_memo.author.firstname+" "+self.__editor_memo.author.lastname+'</p>')
        self.objects[0]["editor"]["content_edit"].setPlainText(
            self.__editor_memo.content)

    def __initialize_editor_toolbar(self):
        self.objects[0]["editor_toolbar"] = {}
        self.layouts[0]["editor_toolbar"] = QHBoxLayout()

        self.objects[0]["editor_toolbar"]["save_button"] = QPushButton('Save')
        self.objects[0]["editor_toolbar"]["cancel_button"] = QPushButton(
            'Cancel')
        self.objects[0]["editor_toolbar"]["remove_button"] = QPushButton(
            'Remove')
        self.objects[0]["editor_toolbar"]["add_image_button"] = QPushButton(
            'Add image')

        self.objects[0]["editor_toolbar"]["save_button"].clicked.connect(
            self.__save_memo)
        self.objects[0]["editor_toolbar"]["cancel_button"].clicked.connect(
            self.__cancel_edit)
        self.objects[0]["editor_toolbar"]["add_image_button"].clicked.connect(
            self.__handle_image)

        self.layouts[0]["editor_toolbar"].addWidget(
            self.objects[0]["editor_toolbar"]["save_button"])
        self.layouts[0]["editor_toolbar"].addWidget(
            self.objects[0]["editor_toolbar"]["cancel_button"])
        self.layouts[0]["editor_toolbar"].addStretch()
        self.layouts[0]["editor_toolbar"].addWidget(
            self.objects[0]["editor_toolbar"]["add_image_button"])

    def __handle_image(self):
        self.frames[0]["image_selector"] = QDialog()
        self.objects[0]["image_selector"] = {}
        self.frames[0]["image_selector"].setWindowTitle("Image selector")

        self.layouts[0]["image_selector"] = QVBoxLayout()
        self.objects[0]["image_selector"]["tabs"] = QTabWidget()

        self.frames[0]["image_selector_select"] = QFrame()
        self.frames[0]["image_selector_add"] = QFrame()
        self.__initialize_image_selector_add()

        self.objects[0]["image_selector"]["tabs"].addTab(
            self.frames[0]["image_selector_select"], "Select")
        self.objects[0]["image_selector"]["tabs"].addTab(
            self.frames[0]["image_selector_add"], "Add new")

        self.layouts[0]["image_selector"].addWidget(
            self.objects[0]["image_selector"]["tabs"])

        columns = (self.__active_width-800) // 250

        self.layouts[0]["image_selector_select"] = QVBoxLayout()
        self.objects[0]["image_selector"]["title_label"] = QLabel(
            '<h1>All images</h1>')
        self.layouts[0]["image_selector_select"].addWidget(
            self.objects[0]["image_selector"]["title_label"])

        images = self.image_service.get("author", self.user[0])
        imgs_in_row = 0
        current_row = 1
        self.objects[0]["image_selector"]["img_grid"] = {}
        self.layouts[0]["image_selector_grid"] = {}
        self.frames[0]["image_selector_grid"] = QFrame()
        self.layouts[0]["image_selector_select_grid"] = QGridLayout()
        self.frames[0]["image_selector_grid"].setLayout(
            self.layouts[0]["image_selector_select_grid"])
        for image in images:
            self.layouts[0]["image_selector_grid"][image.id] = QVBoxLayout()
            self.objects[0]["image_selector"]["img_grid"][image.id] = {}
            self.objects[0]["image_selector"]["img_grid"][image.id]["image_label"] = QLabel(
            )
            self.objects[0]["image_selector"]["img_grid"][image.id]["name_label"] = QLabel(
                image.name+'<br />Width: '+str(image.width))
            self.objects[0]["image_selector"]["img_grid"][image.id]["select_button"] = QPushButton(
                'Select')

            self.objects[0]["image_selector"]["img_grid"][image.id]["image_label"].setText(
                '<img src="data:image/'+image.filetype+';base64,' +
                image.image+'" width="250"  alt="" />'
            )
            self.objects[0]["image_selector"]["img_grid"][image.id]["select_button"].clicked.connect(
                partial(self.__add_image, image.id))

            self.layouts[0]["image_selector_grid"][image.id].addStretch()
            self.layouts[0]["image_selector_grid"][image.id].addWidget(
                self.objects[0]["image_selector"]["img_grid"][image.id]["image_label"])
            self.layouts[0]["image_selector_grid"][image.id].addWidget(
                self.objects[0]["image_selector"]["img_grid"][image.id]["name_label"])
            self.layouts[0]["image_selector_grid"][image.id].addWidget(
                self.objects[0]["image_selector"]["img_grid"][image.id]["select_button"])
            self.layouts[0]["image_selector_select_grid"].addLayout(
                self.layouts[0]["image_selector_grid"][image.id], current_row, imgs_in_row)
            imgs_in_row += 1
            if imgs_in_row == columns:
                imgs_in_row = 0
                current_row += 1

        self.layouts[0]["image_selector_toolbar"] = QHBoxLayout()
        self.objects[0]["image_selector"]["close_button"] = QPushButton(
            'Close')

        self.objects[0]["image_selector"]["close_button"].clicked.connect(
            self.__close_image_selector)

        self.layouts[0]["image_selector_toolbar"].addWidget(
            self.objects[0]["image_selector"]["close_button"])

        self.objects[0]["image_selector"]["content_scroll"] = QScrollArea()
        self.objects[0]["image_selector"]["content_scroll"].setWidget(
            self.frames[0]["image_selector_grid"])
        self.objects[0]["image_selector"]["content_scroll"].ensureWidgetVisible(
            self.frames[0]["image_selector_grid"])
        self.objects[0]["image_selector"]["content_scroll"].ensureVisible(
            0, 0, 0, 0)
        self.objects[0]["image_selector"]["content_scroll"].setWidgetResizable(
            True)
        self.objects[0]["image_selector"]["content_scroll"].setAlignment(
            Qt.AlignTop)
        self.objects[0]["image_selector"]["content_scroll"].setFixedSize(
            self.__active_width-500, self.__active_height-400)
        self.objects[0]["image_selector"]["content_scroll"].setStyleSheet(
            'QScrollArea { border: 0px;}')

        self.layouts[0]["image_selector_select"].addWidget(
            self.objects[0]["image_selector"]["content_scroll"])
        self.layouts[0]["image_selector_select"].addLayout(
            self.layouts[0]["image_selector_toolbar"])

        self.frames[0]["image_selector_select"].setLayout(
            self.layouts[0]["image_selector_select"])

        self.frames[0]["image_selector"].setLayout(
            self.layouts[0]["image_selector"])

        self.frames[0]["image_selector"].exec_()

    def __initialize_image_selector_add(self):
        self.layouts[0]["image_selector_add"] = QGridLayout()
        self.objects[0]["image_selector_add"] = {}

        self.objects[0]["image_selector_add"]["title_label"] = QLabel(
            '<h1>Add new image</h1>')
        self.layouts[0]["image_selector_add"].addWidget(
            self.objects[0]["image_selector_add"]["title_label"], 0, 0)

        self.objects[0]["image_selector_add"]["loc_label"] = QLabel(
            'Image location:')
        self.layouts[0]["image_selector_add"].addWidget(
            self.objects[0]["image_selector_add"]["loc_label"], 1, 0)

        self.objects[0]["image_selector_add"]["file_loc_edit"] = QLineEdit()
        self.layouts[0]["image_selector_add"].addWidget(
            self.objects[0]["image_selector_add"]["file_loc_edit"], 1, 1)

        self.objects[0]["image_selector_add"]["select_button"] = QPushButton(
            'Select')
        self.objects[0]["image_selector_add"]["select_button"].clicked.connect(
            self.__handle_add_image_filedialog)
        self.layouts[0]["image_selector_add"].addWidget(
            self.objects[0]["image_selector_add"]["select_button"], 1, 2)

        self.objects[0]["image_selector_add"]["name_label"] = QLabel(
            'Name:')
        self.layouts[0]["image_selector_add"].addWidget(
            self.objects[0]["image_selector_add"]["name_label"], 2, 0)

        self.objects[0]["image_selector_add"]["name_edit"] = QLineEdit()
        self.layouts[0]["image_selector_add"].addWidget(
            self.objects[0]["image_selector_add"]["name_edit"], 2, 1)

        self.objects[0]["image_selector_add"]["width_label"] = QLabel(
            'Width:')
        self.layouts[0]["image_selector_add"].addWidget(
            self.objects[0]["image_selector_add"]["width_label"], 3, 0)

        self.objects[0]["image_selector_add"]["width_edit"] = QLineEdit()
        self.objects[0]["image_selector_add"]["width_edit"].setValidator(
            QIntValidator(0, 7680, self))
        self.layouts[0]["image_selector_add"].addWidget(
            self.objects[0]["image_selector_add"]["width_edit"], 3, 1)

        self.objects[0]["image_selector_add"]["error_label"] = QLabel()
        self.layouts[0]["image_selector_add"].addWidget(
            self.objects[0]["image_selector_add"]["error_label"], 4, 0)

        self.objects[0]["image_selector_add"]["add_button"] = QPushButton(
            'Add')
        self.objects[0]["image_selector_add"]["add_button"].clicked.connect(
            self.__handle_add_image_to_db)
        self.layouts[0]["image_selector_add"].addWidget(
            self.objects[0]["image_selector_add"]["add_button"], 5, 0)

        self.frames[0]["image_selector_add"].setLayout(
            self.layouts[0]["image_selector_add"])

    def __handle_add_image_to_db(self):
        self.objects[0]["image_selector_add"]["error_label"].setText('')
        name = self.objects[0]["image_selector_add"]["name_edit"].text()
        width = int(self.objects[0]["image_selector_add"]["width_edit"].text())
        file_location = self.objects[0]["image_selector_add"]["file_loc_edit"].text(
        )
        if name == "" or width == "" or file_location == "":
            pass
        image = self.image_service.create(
            self.user[0].id, name, file_location, width)
        if image:
            self.__add_image(image.id)
            self.__close_image_selector()
        else:
            self.objects[0]["image_selector_add"]["error_label"].setText(
                'error while uploading image, try again')

    def __handle_add_image_filedialog(self):
        filename, _ = QFileDialog.getOpenFileName(
            self.frames[0]["image_selector_add"], "Add image", "~/", "Image files (*.jpg *.jpeg *.png *.gif *.svg)")

        self.objects[0]["image_selector_add"]["file_loc_edit"].setText(
            filename)

    def __close_image_selector(self):
        self.frames[0]["image_selector"].done(1)

    def __add_image(self, image_id):
        cursor = self.objects[0]["editor"]["content_edit"].textCursor()
        cursor_pos = cursor.position()
        image_string = "![]("+str(image_id)+")"

        content = self.objects[0]["editor"]["content_edit"].toPlainText()

        content = content[:cursor_pos] + image_string + content[cursor_pos:]
        self.objects[0]["editor"]["content_edit"].setPlainText(content)
        cursor = self.objects[0]["editor"]["content_edit"].textCursor()
        cursor.setPosition(cursor_pos+len(image_string))
        self.objects[0]["editor"]["content_edit"].setTextCursor(cursor)

        self.frames[0]["image_selector"].done(1)

    def __cancel_edit(self):
        if self.__active_screen == "editor":
            self.frames[0]["editor"].hide()
            self.frames[0]["viewer"].show()
            self.__active_screen = "viewer"

    def __initialize_viewer_toolbar(self):
        self.objects[0]["viewer_toolbar"] = {}
        self.layouts[0]["viewer_toolbar"] = QHBoxLayout()

        self.objects[0]["viewer_toolbar"]["edit_button"] = QPushButton('Edit')
        self.objects[0]["viewer_toolbar"]["remove_button"] = QPushButton(
            'Remove')

        self.objects[0]["viewer_toolbar"]["remove_button"].clicked.connect(
            self.__remove_memo)

        self.layouts[0]["viewer_toolbar"].addWidget(
            self.objects[0]["viewer_toolbar"]["edit_button"])
        self.layouts[0]["viewer_toolbar"].addWidget(
            self.objects[0]["viewer_toolbar"]["remove_button"])
        self.layouts[0]["viewer_toolbar"].addStretch()

    def __show_memo(self, memo_id):
        if self.__active_screen == "editor":
            self.frames[0]["editor"].hide()
            self.frames[0]["viewer"].show()
            self.__active_screen = "viewer"
        memo = self.memo_service.get("id", memo_id)
        self.__set_viewer_memo(memo)
        if not self.__editor_memo:
            self.__set_editor_memo(memo)

    def __edit_memo(self, memo_id):
        if self.__active_screen == "viewer":
            self.frames[0]["viewer"].hide()
            self.frames[0]["editor"].show()
            self.__active_screen = "editor"
        self.__set_editor_memo(self.__viewer_memo)

    def __save_memo(self):
        title = self.objects[0]["editor"]["title_edit"].text()
        content = self.objects[0]["editor"]["content_edit"].toPlainText()
        updated_memo = self.memo_service.update(
            self.__editor_memo.id, self.__editor_memo.author.id, title, content, self.__editor_memo.date)
        if updated_memo:
            self.__show_memo(updated_memo.id)

    def __handle_new_memo(self):
        title = self.objects[0]["new_memo"]["title_edit"].text()
        new_memo = self.memo_service.create(self.user[0].id, title)
        if new_memo:
            self.__set_editor_memo(new_memo)

            memo_button = QPushButton(new_memo.title)
            memo_button.clicked.connect(partial(self.__show_memo, new_memo.id))
            self.objects[0]["mainmenu_memos"][new_memo.id] = memo_button
            self.layouts[0]["mainmenu_memos"].addWidget(memo_button)

            self.frames[0]["new_memo"].done(1)
            if self.__active_screen == "viewer":
                self.frames[0]["viewer"].hide()
                self.frames[0]["editor"].show()

    def __new_memo(self):
        self.frames[0]["new_memo"] = QDialog()
        self.objects[0]["new_memo"] = {}
        self.frames[0]["new_memo"].setWindowTitle("New memo")

        self.layouts[0]["new_memo"] = QVBoxLayout()
        self.objects[0]["new_memo"]["title_label"] = QLabel("Title:")
        self.layouts[0]["new_memo"].addWidget(
            self.objects[0]["new_memo"]["title_label"])
        self.objects[0]["new_memo"]["title_edit"] = QLineEdit()
        self.layouts[0]["new_memo"].addWidget(
            self.objects[0]["new_memo"]["title_edit"])
        self.objects[0]["new_memo"]["create_button"] = QPushButton('Create')
        self.objects[0]["new_memo"]["create_button"].clicked.connect(
            self.__handle_new_memo)
        self.layouts[0]["new_memo"].addWidget(
            self.objects[0]["new_memo"]["create_button"])

        self.frames[0]["new_memo"].setLayout(self.layouts[0]["new_memo"])

        self.frames[0]["new_memo"].exec_()

    def __remove_memo(self):
        memo_to_be_removed = self.__editor_memo
        if self.__active_screen == "viewer":
            memo_to_be_removed = self.__viewer_memo

        self.frames[0]["remove_memo"] = QDialog()
        self.objects[0]["remove_memo"] = {}
        self.frames[0]["remove_memo"].setWindowTitle("Are you sure?")

        self.layouts[0]["remove_memo"] = QVBoxLayout()
        self.objects[0]["remove_memo"]["info_label"] = QLabel(
            "Confirm removal of memo '"+memo_to_be_removed.title+"'")
        self.layouts[0]["remove_memo"].addWidget(
            self.objects[0]["remove_memo"]["info_label"])

        self.objects[0]["remove_memo"]["cancel_button"] = QPushButton('Cancel')
        self.objects[0]["remove_memo"]["cancel_button"].clicked.connect(
            self.__handle_remove_cancel)
        self.layouts[0]["remove_memo"].addWidget(
            self.objects[0]["remove_memo"]["cancel_button"])

        self.objects[0]["remove_memo"]["confirm_button"] = QPushButton(
            'Confirm')
        self.objects[0]["remove_memo"]["confirm_button"].clicked.connect(
            self.__handle_remove_memo)
        self.layouts[0]["remove_memo"].addWidget(
            self.objects[0]["remove_memo"]["confirm_button"])

        self.frames[0]["remove_memo"].setLayout(self.layouts[0]["remove_memo"])

        self.frames[0]["remove_memo"].exec_()

    def __handle_remove_cancel(self):
        self.frames[0]["remove_memo"].done(1)

    def __handle_remove_memo(self):
        memo_to_be_removed = self.__viewer_memo
        result = self.memo_service.remove(memo_to_be_removed.id)
        if result:
            self.objects[0]["mainmenu_memos"][memo_to_be_removed.id].setParent(
                None)
            self.frames[0]["viewer"].hide()
            self.__viewer_state = "hidden"
            self.objects[0]["viewer"]["title_label"].setText('')
            self.objects[0]["viewer"]["info_label"].setText('')
            self.objects[0]["viewer"]["content_label"].setText('')
            # if self.__active_screen == "editor":
            #     self.__editor_memo = None
            #     self.frames[0]["editor"].hide()
            #     self.frames[0]["viewer"].show()
            #     self.__active_screen = "viewer"

        self.frames[0]["remove_memo"].done(1)

    def __initialize_extended_menu(self):
        self.frames[0]["extended_menu"] = QFrame()
        self.objects[0]["extended_menu"] = {}

        self.layouts[0]["extended_menu"] = QVBoxLayout()
        self.objects[0]["extended_menu"]["name_label"] = QLabel(
            self.user[0].firstname+" "+self.user[0].lastname)
        self.layouts[0]["extended_menu"].addWidget(
            self.objects[0]["extended_menu"]["name_label"])
        self.objects[0]["extended_menu"]["logout_button"] = QPushButton(
            'Log out')
        self.objects[0]["extended_menu"]["logout_button"].clicked.connect(
            self.__handle_logout)
        self.layouts[0]["extended_menu"].addWidget(
            self.objects[0]["extended_menu"]["logout_button"])
        self.objects[0]["extended_menu"]["settings_button"] = QPushButton(
            'Settings')
        self.objects[0]["extended_menu"]["settings_button"].clicked.connect(
            self.__handle_settings)
        self.layouts[0]["extended_menu"].addWidget(
            self.objects[0]["extended_menu"]["settings_button"])

        self.frames[0]["extended_menu"].setLayout(
            self.layouts[0]["extended_menu"])

        self.frames[0]["extended_menu"].hide()

    def __handle_logout(self):
        self.user[0] = None
        self.__empty_memos_from_mainmenu()

        self.frames[0]["viewer"].hide()
        self.__viewer_state = "hidden"
        self.frames[0]["editor"].hide()
        self.__editor_state = "hidden"

        self.frames[0]["extended_menu"].hide()
        self.__extended_menu = "hidden"

        self.frames[0]["memoview"].hide()
        self.frames[0]["loginview"].show()

    def __handle_settings(self):
        pass

    def __show_hide_extended_menu(self):
        if self.__extended_menu == 'hidden':
            self.frames[0]["extended_menu"].show()
            self.__extended_menu = "shown"
        else:
            self.frames[0]["extended_menu"].hide()
            self.__extended_menu = "hidden"
