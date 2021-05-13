# **Ohjelmistotekniikka**, _kevät 2021_ - kurssitehtävien palautukset

Kurssisuoritus Helsingin yliopiston [**Ohjelmistotekniikan**](https://ohjelmistotekniikka-hy.github.io) kurssille _keväällä 2021_.

## Muistio

Ohjelmalla hallitaan käyttäjän muistiinpanoja, joita voidaan käsitellä useammalla eri laitteella verkon ylitse.

### Releases

- [Viikon 5 release](https://github.com/FinThunderstorm/ohte/releases/tag/viikko5)
- [Viikon 6 release](https://github.com/FinThunderstorm/ohte/releases/tag/viikko6)
- [Viikon 7 / loppupalautuksen release](https://github.com/FinThunderstorm/ohte/releases/tag/viikko7)

### Dokumentaatio

- [Vaatimusmäärittely](./dokumentaatio/vaatimusmäärittely.md)
- [Työaikakirjanpito](./dokumentaatio/tyoaikakirjanpito.md)
- [Arkkitehtuurikuvaus](./dokumentaatio/arkkitehtuuri.md)
- [Käyttöohje](./dokumentaatio/käyttöohje.md)
- [Testausdokumentti](./dokumentaatio/testausraportti.md)

### Asentaminen

1. Asenna sovelluksen tarvitsemat kirjastot komennolla:

```bash
poetry install
```

2. Käynnistä sovellus:

```bash
poetry run invoke start
```

3. Täytä asetustiedot avautuvaan ikkunaan. Tarvittavat tietokannan käyttäjätiedot, _username_ ja _password_, saat pyytämällä Telegramista _@finthunderstorm_.

#### Huomioita Python-versiosta

Sovellus on kehitetty käyttäen Python 3.9.1 -versiota, mutta pitäisi olla yhteensopiva version 3.6.0 alkaen kanssa yhteensopiva. Virhetilanteita voi kuitenkin esiintyä.

#### Ongelmatilanteiden ratkaisuja

- Jos ohjelman suoritus kaatuu sertifikaatin validointiongelmaan, ratkaisuna toimii seuraava: <https://stackoverflow.com/a/54511693>

### Komennot

- Ohjelman suorittaminen tapahtuu komennolla `poetry run invoke start`
- Testien suorittaminen tapahtuu komennolla `poetry run invoke test`
- Testikattavuuden raportin luominen tapahtuu komennolla `poetry run invoke coverage-report`, joka löytyy htmlcov-kansiosta.
- Koodin laadun tarkastaminen tapahtuu komennolla `poetry run invoke lint`
