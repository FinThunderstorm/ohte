from utils.database_handler import connect_database, disconnect_database
from datetime import datetime
from entities.memo import Memo
from entities.user import User
from bson.objectid import ObjectId
from mongoengine import connect
from utils.config import database_uri
from repositories.MemoRepository import memo_repository
from services.memo_service import memo_service
from repositories.UserRepository import user_repository
from utils.helpers import get_test_memo, get_test_user, get_id, get_test_memo_user
from sys import exit


def main():

    print('Tervetuloa Muistioon!')

    try:
        connect_database()
        memoservice = memo_service
        memoservice.count()
    except:
        print('Ongelma yhdistettäessä tietokantaan, lopetetaan sovellus.')
        exit()

    print('Komennot: 1 - listaa kaikki muistiot, 2 - lisää uusi muistio, X - lopettaa \n')
    while True:
        command = input('Komento: ')
        if command == "1":
            memos = memoservice.get()
            print()
            for memo in memos:
                print('Luotu:', memo.date.strftime('%a %d.%m.%Y %H:%M'))
                print('Kirjoittaja:', memo.author.firstname, memo.author.lastname)
                print('Otsikko:', memo.title)
                print('Muistio:', memo.content)
                print()
        elif command == "2":
            title = input('Otsikko: ')
            content = input('Muistio: ')
            saved_memo = memoservice.create(
                ObjectId('6072d33e3a3c627a49901ce8'), title, content)
            if saved_memo:
                print('\nUusi muistio', saved_memo.title, 'käyttjältä', saved_memo.author.firstname,
                      saved_memo.author.lastname, 'tallennettu onnistuneesti! \n')
        elif command.lower() == "x":
            break

        else:
            print('- Tuntematon komento, yritä uudelleen - \n')

    disconnect_database()


if __name__ == "__main__":
    main()
