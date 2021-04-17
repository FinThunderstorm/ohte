from utils.database_handler import connect_database, disconnect_database
from services.memo_service import memo_service
from ui.text_ui.text_ui import TextUi


def main():
    success = True
    if not connect_database():
        success = False
    memoservice = memo_service
    text_ui = TextUi(memoservice)

    if success:
        text_ui.run()

    disconnect_database()


if __name__ == "__main__":
    main()
