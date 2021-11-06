import requests
import os


glavna_stran_url = 'https://www.studentska-prehrana.si/sl/restaurant'
mapa = 'html_datoteke'
ime_datoteke = 'glavna_stran.html'


def prenesi_iz_url(url):
    try:
        r = requests.get(url)

    except requests.exceptions.ConnectionError:
        print("Napaka pri povezovanju do:", url)
        return None

    if r.status_code == requests.codes.ok:
        return r.text

    else:
        print('Napaka pri prenosu strani.')
        return None

def shrani_v_datoteko(besedilo, mapa, ime_datoteke):
    os.makedirs(mapa, exist_ok=True)
    pot = os.path.join(mapa, ime_datoteke)
    with open(pot, 'w', encoding='utf-8') as izhodna_datoteka:
        izhodna_datoteka.write(besedilo)


besedilo = prenesi_iz_url(glavna_stran_url)
shrani_v_datoteko(besedilo, mapa, ime_datoteke)