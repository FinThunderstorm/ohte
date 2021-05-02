from utils.database_handler import connect_database, disconnect_database
from utils.config import Config
from services.memo_service import memo_service
from services.user_service import user_service
from services.image_service import image_service
from services.file_service import file_service
from ui.gui.gui import GUI


def main():
    config = Config(file_service)

    gui = GUI(config, memo_service, user_service,
              image_service, file_service)

    conn = connect_database(config.get('DATABASE_URI'))

    if conn:
        gui.start()
        gui.run()

    disconnect_database()


if __name__ == "__main__":
    main()
