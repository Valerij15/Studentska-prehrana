# Studentska-prehrana
## Splošne informacije
Analiziral bom imenik lokalov, ki ga nudi spletna stran za študentsko prehrano(https://www.studentska-prehrana.si/sl/restaurant), ter poskušal najti idealen lokal za porabitev bonov.

Za vsak lokal bom zajel:
* ime lokala
* kraj
* oceno lokala
* doplačilo za obrok
* pozitivne lastnosti lokala(vegiterjanske jedi, delavnik ob vikendih, itd.)
* število menijev

Delovne hipoteze:
* Ali obstaja povezava med oceno lokala ter doplačilom za obrok?
* Imajo lokali s več pozitivnimi lastnostmi tudi višje cene?
* Imajo lokali v Ljubljani višje cene?
* Ali obstaja optimalen lokal glede na ceno, oddaljenost od FMF, ter število menijev v primeru, da je kavarna Mafija prepolna?

## Opis datotek
Trenutne datoteke so:
* glavna_pridobitev.py - skripta uporabljena za zajem podatkov iz spletne strani.
* glavna_obdelava.py - skripta uporabljena za pridobitev ključnih podatkov iz html datoteke ter shranjevanje v csv obliko.
* lokali.csv - csv datoteka s ključnimi informacijami o lokalih (id, ime, kraj, cena, doplačilo)
* ocene.csv - csv datoteka s podatki o ocenah

## Opombe
Nameravam zajeti še html strani za posamezne lokale, ter podatke o menijih, ki jih bom tudi spravil v svoje csv datoteke. Žal mi je za zajem tega do današnjega dne zmanjkalo časa.

## Avtorji
* Valerij Jovanov
