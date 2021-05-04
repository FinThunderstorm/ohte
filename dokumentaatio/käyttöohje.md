# Käyttöohje

Aloita lataamalla viimeisin (relase)[https://github.com/FinThunderstorm/ohte/releases] ja noudata siinä annettuja asennusohjeita.

## Konfiguraatiotiedosto .env

Sovellus luo tämän tiedoston ensimmäisellä käynnistyskerralla ja sen sisältöön voi vaikuttaa käyttämällä graafista asetustyökalua.

Tiedoston rakenne on seuraava:

```
RES_INDEX=1
RES_FORMAT=auto
DB_USERNAME=username
DB_PASSWORD=password
DB_SERVER=ohte.bu0r9.mongodb.net
DB_NAME=muistio
DATABASE_URI=mongodb+srv://${DB_USERNAME}:${DB_PASSWORD}@${DB_SERVER}/${DB_NAME}?retryWrites=true&w=majority
```

## Ohjelman käynnistäminen

Ohjelman suorittaminen tapahtuu komennolla `poetry run invoke start`. Ensimmäisellä käyttökerralla sovellus haluaa tarkistaa asetukset kohdilleen.

## Ensimmäinen käynnistys

Sovellus avautuu ensimmäisellä käynnistyskerralla asetusvalikkoon, jossa täydennetään tietokannan käyttäjätiedot ja valitaan haluttu resoluutio muistioiden käsittelemiselle.

![](./kuvat/setup-view.png)

## Kirjautuminen

Kirjautuminen sovellukseen tapahtuu täyttämällä käyttäjätiedot kenttiin ja painamalla "Login"-painiketta.

![](./kuvat/login.png)

## Muistion katseleminen

Muistion katseleminen tapahtuu valitsemalla haluttu muistio vasemmasta sivupalkista klikkaamalla oikean muistion otsikon kohdalta.

![](./kuvat/memo-viewer.png)

Tästä näkymästä voidaan alapalkista löytyvillä työkaluilla muokata, poistaa tai viedä muistion erilliseen Markdown-tiedostoon.

## Muistion muokkaaminen

Muistion muokkaamistilassa voidaan muistion otsikkoa ja sisältöä muuttaa. Alapalkista löytyy muokkauksien tallentamisen ja keskeyttämisen toiminnallisuudet sekä kuvien lisäämistoiminnallisuus "Add image".

!()[./kuvat/memo-editor.png]
