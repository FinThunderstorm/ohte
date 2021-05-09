from utils.database_handler import connect_database, disconnect_database
from utils.config import Config
from services.memo_service import memo_service
from services.user_service import user_service
from services.image_service import image_service
from services.file_service import file_service
from ui.gui.gui import GUI


def main():
    """main is used for starting muistio software.
    """
    config = Config(file_service)

    gui = GUI(config, memo_service, user_service,
              image_service, file_service)

    if config.initialized_first_time:
        gui.first_time()

    conn = connect_database(config.get('DATABASE_URI'))
    if conn:
        gui.start()
    else:
        gui.error('No connection established. Check your credentials.' +
                  '\n\n After saving settings, relaunch the app.')
        gui.first_time()

    disconnect_database()


if __name__ == "__main__":
    main()
