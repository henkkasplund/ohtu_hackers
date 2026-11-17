# ohtu_hackers
ohtu 2026 miniproject

## Pelisäännöt

[Ryhmän pelisäännöt](pelisaannot.md)

## Backlogit

[Projektin backlogit](https://github.com/users/henkkasplund/projects/1/views/1)

## Definition of done

- vaatimus analysoitu (käyty läpi daily scrumissa tai chatissä)
- suuniteltu
- ohjelmoitu
- testit tehtynä
- robot testit toimivat
- viety tuotantoympäristöön ja tarkistettu uudelleen, että se toimii

## Sovelluksen käyttöönotto
### Asentaa oikeat riippuvuudet
+ Vain ensimmäisellä kerralla, tai jos asennettu uusi riippuvuus uv add ...
+ uv sync
### Luo tietokannat 
+ uv run python src/db_helper.py
### Käynnistys 
+ uv run flask --app src/app run  
Tai
+ uv run flask --app src/app run --debug