from bson.objectid import ObjectId


class TextUi:
    def __init__(self, memo_service):
        self.memo_service = memo_service

    def run(self):
        print('Tervetuloa Muistioon!')
        while True:
            print(
                'Komennot: 1 - listaa kaikki muistiot, 2 - lisää uusi muistio, X - lopettaa \n')
            command = input('Komento: ')
            if command == "1":
                memos = self.memo_service.get()
                print()
                for memo in memos:
                    print('Luotu:', memo.date.strftime('%a %d.%m.%Y %H:%M'))
                    print('Kirjoittaja:', memo.author.firstname,
                          memo.author.lastname)
                    print('Otsikko:', memo.title)
                    print('Muistio:', memo.content)
                    print()
            elif command == "2":
                title = input('Otsikko: ')
                content = input('Muistio: ')
                saved_memo = self.memo_service.create(
                    ObjectId('6072d33e3a3c627a49901ce8'), title, content)
                if saved_memo:
                    print('\nUusi muistio', saved_memo.title, 'käyttjältä', saved_memo.author.firstname,
                          saved_memo.author.lastname, 'tallennettu onnistuneesti! \n')
            elif command.lower() == "x":
                break

            else:
                print('- Tuntematon komento, yritä uudelleen - \n')
