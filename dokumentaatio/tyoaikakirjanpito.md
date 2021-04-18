# Työaikakirjanpito

| Milloin? | Kauan? | Mitä?                                                                                 |
| -------- | ------ | ------------------------------------------------------------------------------------- |
| 20.3     | 2h     | Vaatimusmäärittely & suunnittelu                                                      |
| 27.3     | 0,5h   | Tietokantayhteyden määrittely                                                         |
| 27.3     | 2h     | Memon määritteleminen                                                                 |
| 27.3     | 2h     | Vaihto pymongo -> mongoengine, refaktorointi vastaamaan vaihtoa                       |
| 28.3     | 5,5h   | MemoRepositoryn tunkkaaminen, testikannan määrittely                                  |
| 2.4      | 0,5h   | Invoken asetuksien määrittäminen                                                      |
| 2.4      | 3h     | Userin määritteleminen                                                                |
| 5.4      | 0,5h   | UserRepositoryn viimeistely                                                           |
| 5.4      | 2h     | MemoService versio 1                                                                  |
| 8.4-11.4 | 8h     | Refaktorointi ja ongelmien korjaamista                                                |
| 13.4     | 2h (l) | Viikon 3 palautuksen valmistelu, alkeellinen tekstikäyttöliittymä demoa varten        |
| 17.4     | 2h     | MemoRepositoryn testien viimeistely ja kokonaisuuden saattaminen valmiiksi v1         |
| 17.4     | 1h     | UserRepositoryn testien viimeistely ja kokonaisuuden saattaminen valmiiksi v1         |
| 17.4     | 0,5h   | Aiemman tekstikäyttöliittymän eristäminen tulevan GUI:n tieltä omaksi luokaksi        |
| 17.4     | 2h     | MemoServicen testit kuntoon ja sovelluslogiikan v1                                    |
| 17.4     | 3h     | UserServicen versio 1 ja testit                                                       |
| 18.4     | 1h     | Tietokannan yhdistämisen testien räpeltäminen, pytest-socket ei saanut estettyä - WIP |
| Yhteensä | 28h    |                                                                                       |

1,5h - 18.4
(l) = yhteensä laskettu tähän saakka

## Todo-lista

- Uudelleen nimeä repositorien tiedostonimet ja refaktoroi muutos kaikiin vaikuttaviin tiedostoihin - WIP
- Refaktoroi repositoryt nostamaan virheitä sen sijasta, että ne palauttelevat nonea, muutetaan mielummin try catch -logiikka serviceihin ja repositoryt nostaa virheen kun homma seis. Servicien catchit sitten käsittelee aina oikeat virheet.
