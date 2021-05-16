from utils.helpers import get_empty_memo, get_id
from ui.gui.error_view import ErrorView
from PyQt5.QtWidgets import QApplication, QWidget, QDialog, QFileDialog, QScrollArea, QTextBrowser, QGridLayout, QVBoxLayout, QHBoxLayout, QTabWidget, QLabel, QPushButton, QTextEdit, QLineEdit, QFrame
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIntValidator
from markdown2 import markdown
from functools import partial


class MemoView(QFrame):
    """MemoView handles viewing and editing memos in GUI.

    Args:
        QFrame: imported from PyQt5.QtWidgets
    """

    def __init__(self, screen, memo_service, image_service, user, objects, layouts, frames, config):
        """Constructor for preparing the MemoView.

        Args:
            screen: available screen width and height
            memo_service: service handler for memos
            image_service: service handler for images
            user: ref to current logged user in list.
            objects: shared dict between views holding each others objects
            layouts: shared dict between views holding each others layouts
            frames: shared dict between views holding each others frames
            config: apps configuration object
        """
        super().__init__()
        self.config = config
        self.__screen = screen
        self.__screen_width, self.__screen_height = screen

        if self.config.get('RES_FORMAT') == "auto" or self.config.get('RES_FORMAT') == "":
            width = int(self.__screen_width) - 50
            height = int(self.__screen_height) - 50
        else:
            width = int(self.config.get('RES_FORMAT').split("x")[0])
            height = int(self.config.get('RES_FORMAT').split("x")[1])

        self.__active_width = width if self.__screen_width > width else self.__screen_width
        self.__active_height = height if self.__screen_height > height else self.__screen_height
        self.setFixedSize(self.__active_width, self.__active_height)

        self.memo_service = memo_service
        self.image_service = image_service

        self.objects = objects if objects else {}
        self.layouts = layouts if layouts else {}
        self.frames = frames if frames else {}

        self.user = user
        self.memos = []
        self.testing_memo = get_empty_memo()

        self.layout = QGridLayout()
        self.__extended_menu = 'hidden'

        self.__viewer_memo = None if len(self.memos) > 0 else get_empty_memo()
        self.__editor_memo = None if len(self.memos) > 0 else get_empty_memo()

    def initialize(self):
        """initialize is used to build the view up.
        """
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
        """run is used to show this part of GUI.
        """
        self.show()
        self.__update_memos_into_mainmenu()

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

        self.objects[0]["mainmenu_memos_scroll"] = QScrollArea()
        self.frames[0]["mainmenu_memos"] = QFrame()
        self.objects[0]["mainmenu_memos_scroll"].setWidget(
            self.frames[0]["mainmenu_memos"])
        self.objects[0]["mainmenu_memos_scroll"].ensureWidgetVisible(
            self.frames[0]["mainmenu_memos"])
        self.objects[0]["mainmenu_memos_scroll"].setWidgetResizable(True)
        self.objects[0]["mainmenu_memos_scroll"].setAlignment(Qt.AlignTop)
        self.objects[0]["mainmenu_memos_scroll"].setFixedSize(
            self.__active_width-(self.__active_width-375), self.__active_height-300)
        self.objects[0]["mainmenu_memos_scroll"].setStyleSheet(
            'QScrollArea { border: 0px;}')
        self.layouts[0]["mainmenu_memos"] = QVBoxLayout()
        self.layouts[0]["mainmenu_memos_outer"] = QVBoxLayout()
        self.layouts[0]["mainmenu_memos_outer"].addLayout(
            self.layouts[0]["mainmenu_memos"])
        self.layouts[0]["mainmenu_memos_outer"].addStretch()
        self.frames[0]["mainmenu_memos"].setLayout(
            self.layouts[0]["mainmenu_memos_outer"])

        self.layouts[0]["mainmenu"].addWidget(
            self.objects[0]["mainmenu_memos_scroll"])

        self.layouts[0]["mainmenu"].addStretch()

        self.layouts[0]["mainmenu_buttons"] = QHBoxLayout()

        self.objects[0]["mainmenu"]["new_memo_button"] = QPushButton(
            'New memo')
        self.objects[0]["mainmenu"]["new_memo_button"].clicked.connect(
            self.__new_memo)
        self.layouts[0]["mainmenu_buttons"].addWidget(
            self.objects[0]["mainmenu"]["new_memo_button"])

        self.objects[0]["mainmenu"]["import_button"] = QPushButton(
            'Import from')
        self.objects[0]["mainmenu"]["import_button"].clicked.connect(
            self.__import_from_web)
        self.layouts[0]["mainmenu_buttons"].addWidget(
            self.objects[0]["mainmenu"]["import_button"])

        self.layouts[0]["mainmenu"].addLayout(
            self.layouts[0]["mainmenu_buttons"])

        self.frames[0]["mainmenu"].setLayout(self.layouts[0]["mainmenu"])

    def __update_memos_into_mainmenu(self):
        memos = self.memo_service.get('author', self.user[0])
        if memos:
            for memo in memos:
                self.objects[0]["mainmenu_memos"][memo.id] = QPushButton(
                    memo.title)
                self.objects[0]["mainmenu_memos"][memo.id].clicked.connect(
                    partial(self.__show_memo, memo.id))
                self.layouts[0]["mainmenu_memos"].addWidget(
                    self.objects[0]["mainmenu_memos"][memo.id])

    def __empty_memos_from_mainmenu(self):
        for button in self.objects[0]["mainmenu_memos"].values():
            button.setParent(None)

    def __initialize_viewer(self):
        self.frames[0]["viewer"] = QFrame()
        self.objects[0]["viewer"] = {}
        self.layouts[0]["viewer"] = QVBoxLayout()
        self.frames[0]["viewer"].setLayout(self.layouts[0]["viewer"])
        self.frames[0]["viewer"].setFixedWidth(self.__active_width-450)

        self.__initialize_viewer_toolbar()
        self.__viewer_memo = None

        self.objects[0]["viewer"]["title_label"] = QLabel()
        self.objects[0]["viewer"]["info_label"] = QLabel()
        self.objects[0]["viewer"]["content_label"] = QTextBrowser()

        self.layouts[0]["viewer"].addWidget(
            self.objects[0]["viewer"]["title_label"])
        self.layouts[0]["viewer"].addWidget(
            self.objects[0]["viewer"]["info_label"])
        self.layouts[0]["viewer"].addWidget(
            self.objects[0]["viewer"]["content_label"])

        self.objects[0]["viewer"]["content_label"].setAlignment(Qt.AlignTop)

        self.objects[0]["viewer"]["content_label"].setFixedSize(
            self.__active_width-475, self.__active_height-200)
        self.objects[0]["viewer"]["content_label"].setStyleSheet(
            'QTextEdit { border: 0px; background-color: transparent;}')

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
        self.objects[0]["viewer"]["content_label"].setText(
            content_in_html)

        self.objects[0]["viewer_toolbar"]["edit_button"].clicked.connect(
            partial(self.__edit_memo, self.__viewer_memo.id))

        self.frames[0]["viewer"].show()

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
                'Name: '+image.name)
            self.objects[0]["image_selector"]["img_grid"][image.id]["name_edit"] = QLineEdit(
            )
            self.objects[0]["image_selector"]["img_grid"][image.id]["width_label"] = QLabel(
                'Width: '+str(image.width))
            self.objects[0]["image_selector"]["img_grid"][image.id]["width_edit"] = QLineEdit(
            )
            self.objects[0]["image_selector"]["img_grid"][image.id]["save_button"] = QPushButton(
                'Save')
            self.objects[0]["image_selector"]["img_grid"][image.id]["select_button"] = QPushButton(
                'Select')
            self.objects[0]["image_selector"]["img_grid"][image.id]["edit_button"] = QPushButton(
                'Edit')
            self.objects[0]["image_selector"]["img_grid"][image.id]["remove_button"] = QPushButton(
                'Remove')

            self.objects[0]["image_selector"]["img_grid"][image.id]["image_label"].setText(
                '<img src="data:image/'+image.filetype+';base64,' +
                image.image+'" width="250"  alt="" />'
            )
            self.objects[0]["image_selector"]["img_grid"][image.id]["name_edit"].setText(
                image.name)
            self.objects[0]["image_selector"]["img_grid"][image.id]["width_edit"].setText(
                str(image.width))
            self.objects[0]["image_selector"]["img_grid"][image.id]["select_button"].clicked.connect(
                partial(self.__add_image, image.id))
            self.objects[0]["image_selector"]["img_grid"][image.id]["edit_button"].clicked.connect(
                partial(self.__handle_edit_image, image.id))
            self.objects[0]["image_selector"]["img_grid"][image.id]["remove_button"].clicked.connect(
                partial(self.__handle_remove_image, image.id))
            self.objects[0]["image_selector"]["img_grid"][image.id]["save_button"].clicked.connect(
                partial(self.__handle_save_edit_image, image.id))
            self.objects[0]["image_selector"]["img_grid"][image.id]["width_edit"].setValidator(
                QIntValidator(0, 7680, self))

            self.layouts[0]["image_selector_grid"][image.id].addStretch()
            self.layouts[0]["image_selector_grid"][image.id].addWidget(
                self.objects[0]["image_selector"]["img_grid"][image.id]["image_label"])
            self.layouts[0]["image_selector_grid"][image.id].addWidget(
                self.objects[0]["image_selector"]["img_grid"][image.id]["name_label"])
            self.layouts[0]["image_selector_grid"][image.id].addWidget(
                self.objects[0]["image_selector"]["img_grid"][image.id]["name_edit"])
            self.layouts[0]["image_selector_grid"][image.id].addWidget(
                self.objects[0]["image_selector"]["img_grid"][image.id]["width_label"])
            self.layouts[0]["image_selector_grid"][image.id].addWidget(
                self.objects[0]["image_selector"]["img_grid"][image.id]["width_edit"])
            self.layouts[0]["image_selector_grid"][image.id].addWidget(
                self.objects[0]["image_selector"]["img_grid"][image.id]["save_button"])
            self.layouts[0]["image_selector_grid"][image.id].addWidget(
                self.objects[0]["image_selector"]["img_grid"][image.id]["remove_button"])
            self.layouts[0]["image_selector_grid"][image.id].addWidget(
                self.objects[0]["image_selector"]["img_grid"][image.id]["edit_button"])
            self.layouts[0]["image_selector_grid"][image.id].addWidget(
                self.objects[0]["image_selector"]["img_grid"][image.id]["select_button"])

            self.objects[0]["image_selector"]["img_grid"][image.id]["name_edit"].hide()
            self.objects[0]["image_selector"]["img_grid"][image.id]["width_edit"].hide()
            self.objects[0]["image_selector"]["img_grid"][image.id]["save_button"].hide()

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

    def __handle_edit_image(self, iid):
        self.objects[0]["image_selector"]["img_grid"][iid]["name_label"].setText(
            'Name:')
        self.objects[0]["image_selector"]["img_grid"][iid]["width_label"].setText(
            'Width:')
        self.objects[0]["image_selector"]["img_grid"][iid]["name_edit"].show()
        self.objects[0]["image_selector"]["img_grid"][iid]["width_edit"].show()
        self.objects[0]["image_selector"]["img_grid"][iid]["save_button"].show()

        self.objects[0]["image_selector"]["img_grid"][iid]["remove_button"].hide()
        self.objects[0]["image_selector"]["img_grid"][iid]["edit_button"].hide()
        self.objects[0]["image_selector"]["img_grid"][iid]["select_button"].hide()

    def __handle_save_edit_image(self, iid):
        name = self.objects[0]["image_selector"]["img_grid"][iid]["name_edit"].text(
        )
        width = int(self.objects[0]["image_selector"]
                    ["img_grid"][iid]["width_edit"].text())

        img = self.image_service.get('id', iid)
        res = self.image_service.update(
            iid, img.author.id, name, img.image, img.filetype, width)
        if res:
            self.objects[0]["image_selector"]["img_grid"][iid]["name_label"].setText(
                'Name: '+res.name)
            self.objects[0]["image_selector"]["img_grid"][iid]["width_label"].setText(
                'Width: '+str(res.width))
            self.objects[0]["image_selector"]["img_grid"][iid]["name_edit"].hide()
            self.objects[0]["image_selector"]["img_grid"][iid]["width_edit"].hide()
            self.objects[0]["image_selector"]["img_grid"][iid]["save_button"].hide()

            self.objects[0]["image_selector"]["img_grid"][iid]["remove_button"].show()
            self.objects[0]["image_selector"]["img_grid"][iid]["edit_button"].show()
            self.objects[0]["image_selector"]["img_grid"][iid]["select_button"].show()
        else:
            ErrorView(self.__screen, "Error while saving",
                      'There were a problem while trying to save. ' +
                      'Please check your input and try again.')
            return

    def __handle_remove_image(self, iid):
        res = self.image_service.remove(iid)
        if res:
            for widget in self.objects[0]["image_selector"]["img_grid"][iid].values():
                widget.setParent(None)
        else:
            ErrorView(self.__screen, "Error while removing",
                      'There were a problem while trying to remove. ' +
                      'Please try again.')
            return

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
        width = self.objects[0]["image_selector_add"]["width_edit"].text()
        file_location = self.objects[0]["image_selector_add"]["file_loc_edit"].text(
        )
        if name == "" or width == "" or file_location == "":
            ErrorView(self.__screen, "Error while saving",
                      'There were a problem while trying to save. ' +
                      'Please check your input and try again.')
            return
        width = int(width)
        image = self.image_service.create(
            self.user[0].id, name, file_location, width)
        if image:
            self.__add_image(image.id)
            self.__close_image_selector()
        else:
            ErrorView(self.__screen, "Error while saving",
                      'There were a problem while trying to save. ' +
                      'Please check your input and try again.')
            return

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
        self.frames[0]["editor"].hide()
        self.frames[0]["viewer"].show()

    def __initialize_viewer_toolbar(self):
        self.objects[0]["viewer_toolbar"] = {}
        self.layouts[0]["viewer_toolbar"] = QHBoxLayout()

        self.objects[0]["viewer_toolbar"]["edit_button"] = QPushButton('Edit')
        self.objects[0]["viewer_toolbar"]["remove_button"] = QPushButton(
            'Remove')
        self.objects[0]["viewer_toolbar"]["export_button"] = QPushButton(
            'Export')

        self.objects[0]["viewer_toolbar"]["remove_button"].clicked.connect(
            self.__remove_memo)
        self.objects[0]["viewer_toolbar"]["export_button"].clicked.connect(
            self.__export_memo)

        self.layouts[0]["viewer_toolbar"].addWidget(
            self.objects[0]["viewer_toolbar"]["edit_button"])
        self.layouts[0]["viewer_toolbar"].addWidget(
            self.objects[0]["viewer_toolbar"]["remove_button"])
        self.layouts[0]["viewer_toolbar"].addStretch()
        self.layouts[0]["viewer_toolbar"].addWidget(
            self.objects[0]["viewer_toolbar"]["export_button"])

    def __export_memo(self):
        filename, _ = QFileDialog.getSaveFileName(
            self.frames[0]["viewer"], "Select export location", "~/")
        src_folder = filename.split('/')
        save_name = src_folder[len(src_folder)-1]
        if ".md" not in save_name:
            filename += ".md"
        self.memo_service.export_memo(self.__viewer_memo.id, filename)

    def __show_memo(self, memo_id):
        memo = self.memo_service.get("id", memo_id)
        self.__set_viewer_memo(memo)
        self.frames[0]["editor"].hide()
        self.frames[0]["viewer"].show()

    def __edit_memo(self, memo_id):
        self.__set_editor_memo(self.__viewer_memo)
        self.frames[0]["viewer"].hide()
        self.frames[0]["editor"].show()

    def __save_memo(self):
        title = self.objects[0]["editor"]["title_edit"].text()
        content = self.objects[0]["editor"]["content_edit"].toPlainText()
        if title == "" or len(title) > 50:
            ErrorView(self.__screen, "Error while saving",
                      'There were a problem while trying to save. ' +
                      'Please check your input and try again.')
            return
        updated_memo = self.memo_service.update(
            self.__editor_memo.id, self.__editor_memo.author.id, title, content, self.__editor_memo.date)
        if updated_memo:
            self.__set_viewer_memo(updated_memo)
            self.frames[0]["editor"].hide()
            self.frames[0]["viewer"].show()
        else:
            ErrorView(self.__screen, "Error while saving",
                      'There were a problem while trying to save. ' +
                      'Please check your input and try again.')
            return

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
            self.frames[0]["viewer"].hide()
            self.frames[0]["editor"].show()
        else:
            ErrorView(self.__screen, "Error while saving",
                      'There were a problem while trying to save. ' +
                      'Please check your input and try again.')
            return

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

    def __handle_import_from_web(self):
        url = self.objects[0]["import_from_web"]["url_edit"].text()
        new_memo = self.memo_service.import_from_url(self.user[0].id, url)
        if new_memo:
            self.__set_editor_memo(new_memo)

            memo_button = QPushButton(new_memo.title)
            memo_button.clicked.connect(partial(self.__show_memo, new_memo.id))
            self.objects[0]["mainmenu_memos"][new_memo.id] = memo_button
            self.layouts[0]["mainmenu_memos"].addWidget(memo_button)

            self.frames[0]["import_from"].done(1)
            self.frames[0]["viewer"].hide()
            self.frames[0]["editor"].show()
        else:
            ErrorView(self.__screen, "Error while importing",
                      'There were a problem while trying to import. ' +
                      'Please check your input and try again.')
            return

    def __handle_import_from_file(self):
        src = self.objects[0]["import_from_file"]["src_edit"].text()
        new_memo = self.memo_service.import_from_file(self.user[0].id, src)
        if new_memo:
            self.__set_editor_memo(new_memo)

            memo_button = QPushButton(new_memo.title)
            memo_button.clicked.connect(partial(self.__show_memo, new_memo.id))
            self.objects[0]["mainmenu_memos"][new_memo.id] = memo_button
            self.layouts[0]["mainmenu_memos"].addWidget(memo_button)

            self.frames[0]["import_from"].done(1)
            self.frames[0]["viewer"].hide()
            self.frames[0]["editor"].show()
        else:
            ErrorView(self.__screen, "Error while importing",
                      'There were a problem while trying to import. ' +
                      'Please check your input and try again.')
            return

    def __import_from_web(self):
        self.frames[0]["import_from"] = QDialog()
        self.objects[0]["import_from"] = {}
        self.objects[0]["import_from_web"] = {}
        self.objects[0]["import_from_file"] = {}
        self.frames[0]["import_from"].setWindowTitle("Import from")

        self.layouts[0]["import_from"] = QVBoxLayout()
        self.objects[0]["import_from"]["tabs"] = QTabWidget()
        self.layouts[0]["import_from"].addWidget(
            self.objects[0]["import_from"]["tabs"])

        self.frames[0]["import_from_web"] = QFrame()
        self.layouts[0]["import_from_web"] = QVBoxLayout()
        self.objects[0]["import_from_web"]["url_label"] = QLabel("Url:")
        self.layouts[0]["import_from_web"].addWidget(
            self.objects[0]["import_from_web"]["url_label"])
        self.objects[0]["import_from_web"]["url_edit"] = QLineEdit()
        self.layouts[0]["import_from_web"].addWidget(
            self.objects[0]["import_from_web"]["url_edit"])
        self.objects[0]["import_from_web"]["import_button"] = QPushButton(
            'Import')
        self.objects[0]["import_from_web"]["import_button"].clicked.connect(
            self.__handle_import_from_web)
        self.layouts[0]["import_from_web"].addWidget(
            self.objects[0]["import_from_web"]["import_button"])

        self.frames[0]["import_from_web"].setLayout(
            self.layouts[0]["import_from_web"])

        # from file

        self.frames[0]["import_from_file"] = QFrame()
        self.layouts[0]["import_from_file"] = QGridLayout()
        self.objects[0]["import_from_file"]["src_label"] = QLabel(
            "File location:")
        self.layouts[0]["import_from_file"].addWidget(
            self.objects[0]["import_from_file"]["src_label"], 1, 0)
        self.objects[0]["import_from_file"]["src_edit"] = QLineEdit()
        self.layouts[0]["import_from_file"].addWidget(
            self.objects[0]["import_from_file"]["src_edit"], 1, 1)
        self.objects[0]["import_from_file"]["select_button"] = QPushButton(
            'Select')
        self.objects[0]["import_from_file"]["select_button"].clicked.connect(
            self.__handle_import_filedialog)
        self.layouts[0]["import_from_file"].addWidget(
            self.objects[0]["import_from_file"]["select_button"], 1, 2)
        self.objects[0]["import_from_file"]["import_button"] = QPushButton(
            'Import')
        self.objects[0]["import_from_file"]["import_button"].clicked.connect(
            self.__handle_import_from_file)
        self.layouts[0]["import_from_file"].addWidget(
            self.objects[0]["import_from_file"]["import_button"], 2, 0)

        self.frames[0]["import_from_file"].setLayout(
            self.layouts[0]["import_from_file"])
        # add tabs

        self.objects[0]["import_from"]["tabs"].addTab(
            self.frames[0]["import_from_web"], "Web")
        self.objects[0]["import_from"]["tabs"].addTab(
            self.frames[0]["import_from_file"], "File")

        self.frames[0]["import_from"].setLayout(self.layouts[0]["import_from"])
        self.frames[0]["import_from"].exec_()

    def __handle_import_filedialog(self):
        filename, _ = QFileDialog.getOpenFileName(
            self.frames[0]["import_from_file"], "Add image", "~/", "Markdown files (*.md)")

        self.objects[0]["import_from_file"]["src_edit"].setText(
            filename)

    def __remove_memo(self):
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
            self.objects[0]["viewer"]["title_label"].setText('')
            self.objects[0]["viewer"]["info_label"].setText('')
            self.objects[0]["viewer"]["content_label"].setText('')
        else:
            ErrorView(self.__screen, "Error while removing",
                      'There were a problem while trying to remove. ' +
                      'Please try again.')

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
            self.handle_logout)
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

    def handle_logout(self):
        self.user[0] = None
        self.__empty_memos_from_mainmenu()

        self.frames[0]["viewer"].hide()
        self.frames[0]["editor"].hide()

        self.frames[0]["extended_menu"].hide()
        self.__extended_menu = "hidden"

        self.frames[0]["memoview"].hide()
        self.frames[0]["loginview"].show()

    def __handle_settings(self):
        self.frames[0]["setupview"].run()

    def __show_hide_extended_menu(self):
        if self.__extended_menu == 'hidden':
            self.frames[0]["extended_menu"].show()
            self.__extended_menu = "shown"
        else:
            self.frames[0]["extended_menu"].hide()
            self.__extended_menu = "hidden"
