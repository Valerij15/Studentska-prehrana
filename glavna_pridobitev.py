import requests
import os
import csv
import time


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
        if besedilo is not None:
            izhodna_datoteka.write(besedilo)

def preberi_id_lokalov(mapa, ime_datoteke):
    id_lokalov = []
    os.makedirs(mapa, exist_ok=True)
    pot = os.path.join(mapa, ime_datoteke)
    with open(pot, 'r', encoding='utf-8') as csv_file:
        bralec = csv.DictReader(csv_file, delimiter = ";")
        for vrstica in bralec:
            id_lokalov.append(vrstica['id'])
    return id_lokalov

def preberi_podrobne_informacije(datoteka, num = 20):
    id_lokalov = preberi_id_lokalov('csv_datoteke', datoteka)
    n = 0
    i = 1
    for id in id_lokalov:
       besedilo = prenesi_iz_url(f'{glavna_stran_url}/Details/{id}')
       n += 1
       os.makedirs(mapa, exist_ok=True)
       pot = os.path.join(mapa, f'podrobne_informacije{i}.html')
       with open(pot, 'a', encoding='utf-8') as izhodna_datoteka:
            if besedilo is not None:
                izhodna_datoteka.write(f'\n <nova_stran><strid={id}> \n')
                izhodna_datoteka.write(besedilo)
                izhodna_datoteka.write("\n </nova_stran> \n")

       if n >= num:
        n = 0
        i += 1
            

preberi_podrobne_informacije('lokali.csv', 20)
#besedilo = prenesi_iz_url(glavna_stran_url)
#shrani_v_datoteko(besedilo, mapa, ime_datoteke)
