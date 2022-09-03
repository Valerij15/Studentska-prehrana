import os
import re
import csv

mapa = 'html_datoteke'
datoteka = 'glavna_stran.html'

def datoteka_v_niz(mapa, ime_datoteke):
    with open(os.path.join(mapa, ime_datoteke), encoding='utf-8') as vhodna_datoteka:
        return vhodna_datoteka.read()

def stran_v_lokale(stran):
    vzorec = r'<div class="row restaurant-row(.*?)</div>'
    narejen_vzorec = re.compile(vzorec, re.DOTALL)
    return re.findall(narejen_vzorec, stran)

def pridobi_podatke_lokala(lokal):
    vzorec = r'data-naslov="(?P<naslov>.*?)".*?data-doplacilo="(?P<doplacilo>.*?)".*?data-posid="(?P<id>.*?)".*?data-lokal="(?P<ime>.*?)".*?data-city="(?P<mesto>.*?)".*?'
    narejen_vzorec = re.compile(vzorec, re.DOTALL)
    najdeno = re.search(narejen_vzorec, lokal)
    if najdeno:
        return najdeno.groupdict()
    return None

def pridobi_oceno_lokala(lokal):
    vzorec = r'data-posid="(?P<id>.*?)".*?data-lokal="(?P<ime>.*?)".*?<form>.*?checked="checked".*?value="(?P<ocena>.*?)".*?'
    narejen_vzorec = re.compile(vzorec, re.DOTALL)
    najdeno = re.search(narejen_vzorec, lokal)
    if najdeno:
        return najdeno.groupdict()
    return None

def napisi_csv(polja, vrstice, mapa, ime_datoteke):
    os.makedirs(mapa, exist_ok=True)
    pot = os.path.join(mapa, ime_datoteke)
    with open(pot, 'w', encoding='utf-8') as csv_file:
        pisar = csv.DictWriter(csv_file, fieldnames=polja, extrasaction='ignore',delimiter = ";")
        pisar.writeheader()
        for vrstica in vrstice:
            vrstica['ime'] = vrstica['ime'].replace('&quot;','').replace('&amp;', '&')
            pisar.writerow(vrstica)


vsebina = datoteka_v_niz(mapa, datoteka)
seznam = stran_v_lokale(vsebina)
seznam_ocen = []
seznam_podatkov = [
    pridobi_podatke_lokala(lokal) for lokal in seznam
]
for lokal in seznam:
    slovar = pridobi_oceno_lokala(lokal)
    if slovar is not None:
        seznam_ocen.append(slovar)

napisi_csv(['id', 'ime', 'naslov', 'doplacilo','mesto'], seznam_podatkov, 'csv_datoteke', 'lokali.csv')
napisi_csv(['id', 'ime', 'ocena'], seznam_ocen, 'csv_datoteke', 'ocene.csv')
