import os
import re
import csv

mapa = 'html_datoteke'
datoteka = 'glavna_stran.html'

vzorec_stran_v_lokale = re.compile(r'<div class="row restaurant-row(.*?<img src.*?)</div>', re.DOTALL)

vzorec_podatki_lokalov = re.compile(
    r'data-naslov="(?P<naslov>.*?)".*?'
    r'data-doplacilo="(?P<doplacilo>.*?)".*?'
    r'data-posid="(?P<id>.*?)".*?'
    r'data-lokal="(?P<ime>.*?)".*?'
    r'data-city="(?P<mesto>.*?)".*?',
    re.DOTALL
)

vzorec_loci_strani = re.compile(r'<nova_stran>(.*?)</nova_stran>', re.DOTALL)

vzorec_pridobi_posebnost = re.compile(r'alt="(.*?)"', re.DOTALL)

vzorec_pridobi_id = re.compile(r'data-posid="(.*?)"', re.DOTALL)

vzorec_prirejen_id = re.compile(r'<strid=(.*?)>', re.DOTALL)

vzorec_ocene = re.compile(
    r'data-posid="(?P<id>.*?)".*?'
    r'<form>.*?checked="checked".*?value="(?P<ocena>.*?)".*?',
    re.DOTALL
)

vzorec_meni = re.compile(
    r'<p class="text-bold color-blue"><h5><strong class=" color-blue">.*?'
    r'&nbsp;\s*(?P<jed>.*?)</strong>.*?'
    r'title="(?P<vrsta>.*?)".*?',
    re.DOTALL
)


def datoteka_v_niz(mapa, ime_datoteke):
    with open(os.path.join(mapa, ime_datoteke), encoding='utf-8') as vhodna_datoteka:
        return vhodna_datoteka.read()

def stran_v_lokale(stran):
    seznam_lokalov = re.findall(vzorec_stran_v_lokale, stran)
    seznam_podatkov_lokalov = [
        pridobi_podatke_lokala(lokal, vzorec_podatki_lokalov) for lokal in seznam_lokalov
    ]
    for slovar in seznam_podatkov_lokalov:
        slovar['ime'] = slovar['ime'].replace('&quot;','').replace('&amp;', '&')
        slovar['doplacilo'] = float(slovar['doplacilo'].replace(',','.'))
        
    napisi_csv(['id', 'ime', 'naslov', 'doplacilo', 'mesto'], seznam_podatkov_lokalov, 'csv_datoteke', 'lokali.csv')

def stran_v_posebnosti(stran):
    posebnosti = set()
    seznam_posebnosti = []
    seznam_lokalov = re.findall(vzorec_stran_v_lokale, stran)

    for lokal in seznam_lokalov:
        nove_posebnosti = re.findall(vzorec_pridobi_posebnost, lokal)
        id_lokala = re.findall(vzorec_pridobi_id, lokal)[0]
        slovar = {}
        slovar['id_lokala'] = id_lokala
        for posebnost in nove_posebnosti:
            slovar[posebnost] = "Da"
            posebnosti.add(posebnost)
        seznam_posebnosti.append(slovar)

    for lokal in seznam_posebnosti:
        for posebnost in posebnosti:
            if posebnost not in lokal.keys():
                lokal[posebnost] = "Ne"

    imena = list(posebnosti)
    imena.insert(0,'id_lokala')
    napisi_csv(imena, seznam_posebnosti, 'csv_datoteke', 'posebnosti.csv')

def stran_v_ocene(stran):
    seznam_ocen = []
    seznam_lokalov = re.findall(vzorec_stran_v_lokale, stran)
    for lokal in seznam_lokalov:
        slovar = pridobi_podatke_lokala(lokal, vzorec_ocene)
        if slovar is not None:
            seznam_ocen.append(slovar)
    napisi_csv(['id', 'ocena'], seznam_ocen, 'csv_datoteke', 'ocene.csv')

def pridobi_jedi(mapa):
    uporaben_seznam = []
    seznam_jedi = []

    for i in range(1, 19):
        vse = datoteka_v_niz(mapa, f'podrobne_informacije{i}.html')
        tab = re.findall(vzorec_loci_strani, vse)
        for str in tab:
            uporaben_seznam.append(str)
    
    for lokal in uporaben_seznam:
        id_lokala = re.findall(vzorec_prirejen_id, lokal)[0]
        najdeno = [slovar.groupdict() for slovar in vzorec_meni.finditer(lokal)]
        for slovar in najdeno:
            slovar['id_lokala'] = id_lokala
            seznam_jedi.append(slovar)

    napisi_csv(['id_lokala', 'jed', 'vrsta'], seznam_jedi, 'csv_datoteke', 'jedi.csv')


def pridobi_podatke_lokala(lokal, vzorec):
    najdeno = re.search(vzorec, lokal)
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
            pisar.writerow(vrstica)


vsebina = datoteka_v_niz(mapa, datoteka)

stran_v_lokale(vsebina)
stran_v_ocene(vsebina)
stran_v_posebnosti(vsebina)
pridobi_jedi(mapa)









#napisi_csv(['id_lokala', 'jed', 'vrsta'], seznam_strani, 'csv_datoteke', 'jedi.csv')
