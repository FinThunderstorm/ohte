from utils.database_handler import connect_database, disconnect_database
from services.memo_service import memo_service
from services.user_service import user_service
from services.image_service import image_service
# from ui.text_ui.text_ui import TextUi
from ui.gui.gui import GUI


def main():
    success = True
    conn = connect_database()

    if not conn:
        success = False

    if success:
        gui = GUI(memo_service, user_service, image_service)

        gui.start()
        gui.run()

    # text_ui = TextUi(memoservice)

    # if success:
    #     text_ui.run()

    disconnect_database()


if __name__ == "__main__":
    main()
