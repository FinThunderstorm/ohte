# Työaikakirjanpito

| Milloin? | Kauan? | Mitä?                                                                          |
| -------- | ------ | ------------------------------------------------------------------------------ |
| 20.3     | 2h     | Vaatimusmäärittely & suunnittelu                                               |
| 27.3     | 0,5h   | Tietokantayhteyden määrittely                                                  |
| 27.3     | 2h     | Memon määritteleminen                                                          |
| 27.3     | 2h     | Vaihto pymongo -> mongoengine, refaktorointi vastaamaan vaihtoa                |
| 28.3     | 5,5h   | MemoRepositoryn tunkkaaminen, testikannan määrittely                           |
| 2.4      | 0,5h   | Invoken asetuksien määrittäminen                                               |
| 2.4      | 3h     | Userin määritteleminen                                                         |
| 5.4      | 0,5h   | UserRepositoryn viimeistely                                                    |
| 5.4      | 2h     | MemoService versio 1                                                           |
| 8.4-11.4 | 8h     | Refaktorointi ja ongelmien korjaamista                                         |
| 13.4     | 2h     | Viikon 3 palautuksen valmistelu, alkeellinen tekstikäyttöliittymä demoa varten |
| Yhteensä | 28h    |                                                                                |

## Todo-lista

- Refaktorointia repositoryille, siirrä servisiin puolelle - repository on vain tiedon tallennus eli funktiot get one, get all, update, remove - WIP
- Uudelleen nimeä repositorien tiedostonimet ja refaktoroi muutos kaikiin vaikuttaviin tiedostoihin - WIP
- Refaktoroi funktioiden nimet viisaammiksi repositoryistä, eli turhaan olevat tarkenteet new memo user jne.
- Luo try-catch-logiikka kaikkeen tiedon siirtoon, jotta voidaan välttää kaatumiset.
- selvitä objectidfield - toimiiko referenssaus kuten jäsässä; tuleeko userin mukana kuinka paljon kyseisestä memosta tietoa mukana.
- tsekkaa testit kondikseen memoservicestä
- muuta logiikka, että servicet ei palauta uutta oliota, vaan ainoastaan true-false onnistuiko toiminnallisuus vaiko eikö... tämän toteuttamista pitää selvittää...

- laskarit
