# Vaatimusmäärittely

## Tarkoitus

Sovelluksen tarkoitus on toimia käyttäjän muistikirjana. Pääidea on tarjota käyttäjälle alusta, jolla hän pystyy hallinnoimaan omia muistioitaan ja käsittelemään muistettavia asioita yhdellä sovelluksella, monella eri laitteella, kun käytössä on verkossa oleva tietokantapalvelin. Käyttäjä voi lisätä, katsella tai muokata muistioita. Käyttäjä voi myös tuoda tiedostosta Markdown-muotoisia tiedostoja tai verkkosivuja haluamastaan verkko-osoitteesta. Käyttäjä voi lisätä valokuvia muistioihin.

## Käyttäjät

Sovelluksessa on ensimmäisessä vaiheessa yhden tasoisia käyttäjiä, eli peruskäyttäjiä. Peruskäyttäjä voi hallita sovelluksella omia tietojaan. Lisättäessä tiimimahdollisuus, harkitaan sekä pääkäyttäjä, että tiiminvetäjän oikeuksien lisääminen.

## "Tech stack"

- Python 3.6 tuki
  - PyQt5 -graafinen kirjasto
- MongoDB -tietokanta taustalla ulkoisella palvelimella, kehitysvaiheessa MongoDB Atlaksessa.

## Käyttöliittymähahmotelma

Käyttöliittymähahmotelmassa on esitetty päätoiminnallisuuksien toiminta sovelluksessa. Käytännössä sovelluksessa on kaksi päänäkymää, ja lisäksi näitä tukevia alinäkymiä. Käyttöliittymähahmotelmassa ei ole huomioitu erilaisten toiminnallisuuksien alinäkymiä., kuten kuvan lisäämistyökalu tai muistion tuominen verkkolähteestä.

![](./kuvat/interface.png)

## Ensimmäisen vaiheen tarjoamat toiminnallisuudet

### Käyttäjänhallinta

- [x] Käyttäjä voi kirjautua järjestelmään
- [x] Käyttäjä voi luoda itselleen tunnuksen järjestelmään
- [x] Käyttäjä voi kirjautua ulos järjestelmästä

### Muistion toiminnallisuudet

- [x] Käyttäjä voi lukea muistioita
- [x] Käyttäjä voi luoda muistion
- [x] Käyttäjä voi muokata muistiota
- [x] Käyttäjä voi poistaa muistion

## Jatkokehittämismahdollisuudet

Ensimmäisen vaiheen jälkeen ohjelmaa voidaan lähteä jatkokehittämään seuraavien toiminnallisuuksien pohjalta.

- [x] Markdown-muotoilulle tuki käyttäen [markdown2-kirjastoa](https://github.com/trentm/python-markdown2)
  - taulukkotuki ja listatuki lisätty
- [x] Kuvien upottaminen
- [x] Mahdollisuus tuoda/viedä Markdown-muotoiltuja tiedostoja
- [x] Verkkosisällön tallentaminen muistioon Python kirjaston [trafilatura](https://trafilatura.readthedocs.io/en/latest/) avulla
- [x] Asetukset

  - [x] muistion resoluution koon tallentaminen .env-tiedostoon
  - [x] muistion db-osoitteen muuttaminen, ensimmäiselle käynnistyskerralle lisättävä gui envin tekemiseen.
  - [x] käyttäjän poistaminen ja tietojen päivittäminen
  - [x] resoluution koon käsittely .env-tiedoston pohjalta

- [x] virheilmoitusten parantaminen & lisääminen

## Kurssin jälkeisen tulevaisuuden kehittämismahdollisuuksia

- [ ] Tyylittely, vakiotyyli tarvitsee parannusta
- [ ] Muistioiden lajitteleminen kansioittain + värikoodit kansioille, selvitettävä ikonien käyttö
- [ ] Lajittelumahdollisuudet
- [ ] Muistutusjärjestelmä, muistiolle voidaan asettaa aika, jolloin käyttäjä saa siitä sovelluksessa ilmoituksen.
- [ ] Käyttäjähallinta
- [ ] Muistikirjan jakaminen toiselle käyttäjälle
- [ ] MemoServiceen current user -ajattelumalli laajemmin.
- [ ] Repositorioihin ja sovelluslogiikkaan järkevämpi poikkeuksien hallintajärjestelmä raise-toiminnallisuutta käyttäen.
- [ ] Kuvan koon määritteleminen abstraktimmin kuvan kokoon pohjautuen
- [ ] Rich Text Editor - pois editor-viewer-ajattelusta. (Idea.)[https://doc.qt.io/qt-5/qtquickcontrols-texteditor-example.html]
