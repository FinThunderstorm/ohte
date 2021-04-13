# **Ohjelmistotekniikka**, _kevät 2021_ - kurssitehtävien palautukset

Kurssisuoritus Helsingin yliopiston [**Ohjelmistotekniikan**](https://ohjelmistotekniikka-hy.github.io) kurssille _keväällä 2021_.

## Muistio

Ohjelmalla hallitaan käyttäjän muistiinpanoja, joita voidaan käsitellä useammalla eri laitteella verkon ylitse.

### Dokumentaatio

- [Vaatimusmäärittely](./dokumentaatio/vaatimusmäärittely.md)
- [Työaikakirjanpito](./dokumentaatio/tyoaikakirjanpito.md)

### Asentaminen

1. Alusta .env tiedosto uudelleennimeämällä _.examle.env_ muotoon _.env_ ja täydennä tietokannan käyttäjätiedot korvaamalla _username_ ja _password_ Labtoolista löytyvillä tai pyytämällä Telegramista _@finthunderstorm_. Tiedosto näyttää lopulta seuraavalta:

```
DATABASE_URI=mongodb+srv://username:password@ohte.bu0r9.mongodb.net/muistio?retryWrites=true&w=majority
```

2. Asenna sovelluksen tarvitsemat kirjastot komennolla:

```bash
poetry install
```

3. Käynnistä sovellus:

```bash
poetry run invoke start
```

### Komennot

- Ohjelman suorittaminen tapahtuu komennolla `poetry run invoke start`
- Testien suorittaminen tapahtuu komennolla `poetry run invoke test`
- Testikattavuuden luominen tapahtuu komennolla `poetry run invoke coverage-report`, joka löytyy htmlcov-kansiosta.

### Notes to myself:

- Pymongon sertifikaatin validointiongelman ratkaisu: <https://stackoverflow.com/a/54511693>
