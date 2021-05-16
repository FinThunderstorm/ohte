# Testausdokumentti

Sovelluksen testaaminen suoritetaan sovelluslogiikan ja tietokannan kanssa keskustelevien luokkien osin automatisoiduilla yksikkö- ja integraatiotestein ja käyttöliittymän osin manuaalisesti tapahtunein testein.

## Yksikkö- ja integraatiotestaus

Tietokantayhteys mallinnetaan yhdistämällä tuotantotietokannan sijasta [_mongomock_](https://pypi.org/project/mongomock/)-kirjaston tarjoamaan mallinnukseen tuotantotietokantaa vastaavasta tietokannasta.

### Tietokannan kanssa keskustelevat luokat (Repositoryt)

Tietokannan kanssa keskustelevien luokkien [`MemoRepository`](https://github.com/FinThunderstorm/ohte/blob/master/src/repositories/memo_repository.py), [`FileRepository`](https://github.com/FinThunderstorm/ohte/blob/master/src/repositories/file_repository.py) ja [`UserRepository`](https://github.com/FinThunderstorm/ohte/blob/master/src/repositories/user_repository.py) testaus suoritetaan vastaavilla luokilla [`TestMemoRepository`](https://github.com/FinThunderstorm/ohte/blob/master/src/tests/repositories/test_memorepository.py), [`TestFileRepository`](https://github.com/FinThunderstorm/ohte/blob/master/src/tests/repositories/test_filerepository.py) ja [`TestUserRepository`](https://github.com/FinThunderstorm/ohte/blob/master/src/tests/repositories/test_userrepository.py). Testaus suoritetaan siten, että toiminta vastaa tuotantotietokannassa toimimista.

Luokan [`ImageRepository`](https://github.com/FinThunderstorm/ohte/blob/master/src/repositories/image_repository.py) testaus suoritetaan vastaavan sovelluslogiikan luokan [`ImageService`](https://github.com/FinThunderstorm/ohte/blob/master/src/services/image_service.py) testausluokan [`TestImageService`](https://github.com/FinThunderstorm/ohte/blob/master/src/tests/services/test_imageservice.py) kautta johtuen kuvien käsittelemisestä tietokantaan tallennettavaan muotoon. Poistamistoiminnallisuus tietokannasta jo poistetun kuvan osalta testataan testausluokassa [`TestImageRepository`](https://github.com/FinThunderstorm/ohte/blob/master/src/tests/repositories/test_imagerepository.py), koska [`ImageService`](https://github.com/FinThunderstorm/ohte/blob/master/src/services/image_service.py) tarkastaa poistettaessa, että kuva on jo tietokannassa.

### Sovelluslogiikka

Sovelluslogiikasta vastaavien luokkien [`MemoService`](https://github.com/FinThunderstorm/ohte/blob/master/src/services/memo_service.py), [`UserService`](https://github.com/FinThunderstorm/ohte/blob/master/src/services/user_service.py), [`FileService`](https://github.com/FinThunderstorm/ohte/blob/master/src/services/file_service.py) ja [`ImageService`](https://github.com/FinThunderstorm/ohte/blob/master/src/services/image_service.py) testaus suoritetaan vastaavilla testausluokilla [`TestMemoService`](https://github.com/FinThunderstorm/ohte/blob/master/src/tests/services/test_memoservice.py), [`TestUserService`](https://github.com/FinThunderstorm/ohte/blob/master/src/tests/services/test_userservice.py), [`TestFileService`](https://github.com/FinThunderstorm/ohte/blob/master/src/tests/services/test_fileservice.py) ja [`TestImageService`](https://github.com/FinThunderstorm/ohte/blob/master/src/tests/services/test_imageservice.py) avulla. Testaus suoritetaan siten, että toiminta vastaa tuotantotietokannassa toimimista.

### Testauskattavuus

Testien haaraumakattavuus on 98%, kun huomioon ei oteta testejä ja käyttöliittymäkerrosta.

Testauksen ulkopuolella on tietokantayhteydestä vastaavan tiedosto [_database_handler.py_](https://github.com/FinThunderstorm/ohte/blob/master/src/utils/database_handler.py) ja testien sekä käyttöliittymän aputyökaluista vastaava tiedosto [_helpers.py_](https://github.com/FinThunderstorm/ohte/blob/master/src/utils/helpers.py). Näiden kohdalla testauskattavuuden ulkopuolelle jättämistä olisi voitu harkita.

![](./kuvat/testauskattavuus.png)

## Käyttöliittymän testaus

Käyttöliittymän testaus on suoritettu manuaalisesti käyttäen sekä macOS-, että Ubuntu-käyttöjärjestelmiä. Sovelluksessa on kokeiltu myös eri konfiguraatiotiedoston arvojen vaikutukset.

Sovellusta on kokeiltu noudattamalla käyttöohjeiden antamia ohjeita sovelluksen asentamisesta ja myös tilanteissa, joissa konfiguraatiotiedostoa ei ole luotu ennen ensimmäistä käyttökertaa.

Kaikki sovelluksen käyttöohjeiden mukaiset päätoiminnallisuudet on testattu ja todettu toimiviksi. Myös virheellisten syötteiden antamista on testattu.
