# Vaatimusmäärittely

## Tarkoitus

Sovelluksen on tarkoitus toimia käyttäjän omana muistikirjana useammmalla laitteella verkon ylitse. Muistikirjat ovat yksilöllisiä ja jokaisella käyttäjällä on oma muistikirja.

## Käyttäjät

Sovelluksessa on ensimmäisessä vaiheessa yhden tasoisia käyttäjiä, eli peruskäyttäjiä - tilannetta tarkastellaan projektin edetessä uudelleen.

## "Tech stack"

- Python 3.6 tuki
  - PyQt5 -graafinen kirjasto
- MongoDB -tietokanta taustalla

## Käyttöliittymähahmotelma

![](./kuvat/interface.png)

## Ensimmäisen vaiheen tarjoamat toiminnallisuudet

### Käyttäjänhallinta

- [x] Käyttäjä voi kirjautua järjestelmään (tehty vko 5)
- [x] Käyttäjä voi luoda itselleen tunnuksen järjestelmään (tehty vko 5)
- [x] Käyttäjä voi kirjautua ulos järjestelmästä (tehty vko 5)

### Muistion toiminnallisuudet

- [x] Käyttäjä voi lukea muistioita
- [x] Käyttäjä voi luoda muistion
- [x] Käyttäjä voi muokata muistiota
- [x] Käyttäjä voi poistaa muistion (tehty vko 5)

## Jatkokehittämismahdollisuudet

Ensimmäisen vaiheen jälkeen ohjelmaa voidaan lähteä jatkokehittämään seuraavien toiminnallisuuksien pohjalta.

- [x] Markdown-muotoilulle tuki käyttäen [markdown2-kirjastoa](https://github.com/trentm/python-markdown2) (tehty vko 5)
  - taulukkotuki ja listatuki lisätty
- [x] Kuvien upottaminen (tehty vko 5)
- [] Mahdollisuus tuoda/viedä Markdown-muotoiltuja tiedostoja (vko 5 todo)
- [] Tyylittely, vakiotyyli tarvitsee parannusta (vko 5 todo)
- [] Asetukset (vko 6 todo)
  - muistion resoluution koon vaihtaminen + tallentaminen .env-tiedostoon
  - muistion db-osoitteen muuttaminen, ensimmäiselle käynnistyskerralle lisättävä gui envin tekemiseen.
  - käyttäjän poistaminen ja tietojen päivittäminen
- [] Muistutusjärjestelmä, muistiolle voidaan asettaa aika, jolloin käyttäjä saa siitä sovelluksessa ilmoituksen. (vko 6)
- [] Muistioiden lajitteleminen kansioittain + värikoodit kansioille, selvitettävä ikonien käyttö (vko 7)
- [] Verkkosisällön tallentaminen muistioon Python kirjaston [trafilatura](https://trafilatura.readthedocs.io/en/latest/) avulla (vko 5-7 todo)
- [] virheilmoitusten parantaminen & lisääminen (vko 5-7 todo)
- [] Lajittelumahdollisuudet (vko 7)
- [] Käyttäjähallinta
- [] Muistikirjan jakaminen toiselle käyttäjälle

## Muut todot

- [] MemoServiceen current user -ajattelumalli. (vko 5 todo)
- [] Testauskattavuus 100% (vko 6 todo)
