# Vaatimusmäärittely

## Tarkoitus

Sovelluksen on tarkoitus toimia käyttäjän omana muistikirjana useammmalla laitteella verkon ylitse. Muistikirjat ovat yksilöllisiä ja jokaisella käyttäjällä on oma muistikirja.

## Käyttäjät

Sovelluksessa on ensimmäisessä vaiheessa yhden tasoisia käyttäjiä, eli peruskäyttäjiä - tilannetta tarkastellaan projektin edetessä uudelleen.

## "Tech stack"

- Python 3.6 tuki
  - PyQt6 -graafinen kirjasto
- MongoDB -tietokanta taustalla

## Käyttöliittymähahmotelma

![](./kuvat/interface.png)

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
- Mahdollisuus tuoda/viedä Markdown-muotoiltuja tiedostoja
- Asetukset
- Käyttäjähallinta
- Muistikirjan jakaminen toiselle käyttäjälle
- Muistutusjärjestelmä, muistiolle voidaan asettaa aika, jolloin käyttäjä saa siitä sovelluksessa ilmoituksen.
- Verkkosisällön tallentaminen muistioon Python kirjaston [trafilatura](https://trafilatura.readthedocs.io/en/latest/) avulla
