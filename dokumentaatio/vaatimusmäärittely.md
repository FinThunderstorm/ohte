# Vaatimusmäärittely

## Tarkoitus

Sovelluksen on tarkoitus toimia käyttäjän omana muistikirjana useammmalla laitteella verkon ylitse. Muistikirjat ovat yksilöllisiä ja jokaisella käyttäjällä on oma muistikirja.

## Käyttäjät

Sovelluksessa on ensimmäisessä vaiheessa yhden tasoisia käyttäjiä, eli peruskäyttäjiä - tilannetta tarkastellaan projektin edetessä uudelleen.

## "Tech stack"

- Python 3.6 tuki
  - tkinter -graafinen kirjasto
- MongoDB -tietokanta taustalla

## Ensimmäisen vaiheen tarjoamat toiminnallisuudet

### Käyttäjänhallinta

- Käyttäjä voi kirjautua järjestelmään
- Käyttäjä voi luoda itselleen tunnuksen järjestelmään
- Käyttäjä voi kirjautua ulos järjestelmästä

### Muistion toiminnallisuudet

- Käyttäjä voi luoda muistion
- Käyttäjä voi muokata muistiota
- Käyttäjä voi poistaa muistion

## Jatkokehittämismahdollisuudet

Ensimmäisen vaiheen jälkeen ohjelmaa voidaan lähteä jatkokehittämään seuraavien toiminnallisuuksien pohjalta.

- Markdown-muotoilulle tuki
- Muistioiden lajitteleminen kansioittain
- Median upottaminen
- Verkkosisällön tallentaminen muistioon Python kirjaston [trafilatura](https://trafilatura.readthedocs.io/en/latest/) avulla
- Muistutusjärjestelmä, muistiolle voidaan asettaa aika, jolloin käyttäjä saa siitä sovelluksessa ilmoituksen.
- Käyttäjähallinta & tiimit
- Muistikirjan jakaminen toiselle käyttäjälle
