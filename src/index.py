from utils.database_handler import connect_database, disconnect_database
from services.memo_service import memo_service
from ui.text_ui.text_ui import TextUi
from ui.gui.gui import GUI


def main():
    success = True
    conn = connect_database()

    # if not conn:
    #     success = False
    # memoservice = memo_service
    # text_ui = TextUi(memoservice)

    # if success:
    #     text_ui.run()

    disconnect_database()


if __name__ == "__main__":
    main()
