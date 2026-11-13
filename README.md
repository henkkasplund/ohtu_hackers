# ohtu_hackers
ohtu 2026 miniproject

## Pelisäännöt

[Ryhmän pelisäännöt](pelisaannot.md)

## Backlogit

[Projektin backlogit](https://github.com/users/henkkasplund/projects/1/views/1)

## Sovelluksen käyttöönotto
### Asentaa oikeat riippuvuudet
+ uv sync
### Luo tietokannat 
+ uv run python src/db_helper.py
### Käynnistys 
+ uv run flask --app src/app run  
Tai
+ uv run flask --app src/app run --debug