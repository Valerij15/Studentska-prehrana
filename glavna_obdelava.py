import os
import re
import csv

mapa = 'html_datoteke'
datoteka = 'glavna_stran.html'

def datoteka_v_niz(mapa, ime_datoteke):
    with open(os.path.join(mapa, ime_datoteke), encoding='utf-8') as vhodna_datoteka:
        return vhodna_datoteka.read()

def stran_v_lokale(stran):
    vzorec = r'<div class="row restaurant-row(.*?<img src.*?)</div>'
    narejen_vzorec = re.compile(vzorec, re.DOTALL)
    return re.findall(narejen_vzorec, stran)

def loci_strani(strani):
    vzorec = r'<nova_stran>(.*?)</nova_stran>'
    narejen_vzorec = re.compile(vzorec, re.DOTALL)
    return re.findall(narejen_vzorec, strani)

def pridobi_podatke_lokala(lokal, vzorec):
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
            #vrstica['ime'] = vrstica['ime'].replace('&quot;','').replace('&amp;', '&')
            pisar.writerow(vrstica)


vsebina = datoteka_v_niz(mapa, datoteka)
seznam = stran_v_lokale(vsebina)
seznam_ocen = []
seznam_strani = []
posebnosti = set()
seznam_posebnosti = []
vzorec = r'data-naslov="(?P<naslov>.*?)".*?data-doplacilo="(?P<doplacilo>.*?)".*?data-posid="(?P<id>.*?)".*?data-lokal="(?P<ime>.*?)".*?data-city="(?P<mesto>.*?)".*?'
seznam_podatkov = [
    pridobi_podatke_lokala(lokal, vzorec) for lokal in seznam
]
for lokal in seznam:
    vzorec = r'alt="(.*?)"'
    vzorec = re.compile(vzorec, re.DOTALL)
    nove_posebnosti = re.findall(vzorec, lokal)
    vzorec_id = r'data-posid="(.*?)"'
    vzorec_id = re.compile(vzorec_id, re.DOTALL)
    id_lokala = re.findall(vzorec_id, lokal)[0]
    slovar = {}
    slovar['id_lokala'] = id_lokala
    for posebnost in nove_posebnosti:
        slovar[posebnost] = "Da"
        posebnosti.add(posebnost)
    seznam_posebnosti.append(slovar)

for lok in seznam_posebnosti:
    for posebnost in posebnosti:
        if posebnost not in lok.keys():
            lok[posebnost] = "Ne"


vzorec = r'data-posid="(?P<id>.*?)".*?data-lokal="(?P<ime>.*?)".*?<form>.*?checked="checked".*?value="(?P<ocena>.*?)".*?'
for lokal in seznam:
    slovar = pridobi_podatke_lokala(lokal, vzorec)
    if slovar is not None:
        seznam_ocen.append(slovar)

for seznam in seznam_podatkov:
    seznam['ime'] = seznam['ime'].replace('&quot;','').replace('&amp;', '&')

uporaben_seznam = []

for i in range(1, 19):
    vse = datoteka_v_niz(mapa, f'podrobne_informacije{i}.html')
    tab = loci_strani(vse)
    for str in tab:
        uporaben_seznam.append(str)

lokal = uporaben_seznam[0]
for lokal in uporaben_seznam:
    vzorec_id = r'<strid=(.*?)>'
    vzorec_id = re.compile(vzorec_id, re.DOTALL)
    id_lokala = re.findall(vzorec_id, lokal)[0]
    vzorec_meni = r'<p class="text-bold color-blue"><h5><strong class=" color-blue">.*?&nbsp;\s*(?P<jed>.*?)</strong>.*?title="(?P<vrsta>.*?)".*?'
    vzorec_meni = re.compile(vzorec_meni, re.DOTALL)
    najdeno = [slovar.groupdict() for slovar in vzorec_meni.finditer(lokal)]
    for slovar in najdeno:
        slovar['id_lokala'] = id_lokala
        seznam_strani.append(slovar)

#seznam_strani.append((id_lokala, pridobi_podatke_lokala(lokal, vzorec_meni)))
#for lokal in uporaben_seznam:
#    vzorec_id = r'<strid=(.*?)>'
#    id_lokala = pridobi_podatke_lokala(lokal, vzorec_id)
#    vzorec_meni = r'<p class="text-bold color-blue"><h5><strong class=" color-blue">\d+ &nbsp;\s+(?P<jed>.*?)</strong>.*?<title="(?P<vrsta>.*?)"'
#    seznam_strani.append((id_lokala, pridobi_podatke_lokala(lokal, vzorec_meni)))


posebnosti = list(posebnosti)
posebnosti.insert(0,'id_lokala')


#napisi_csv(['id', 'ime', 'naslov', 'doplacilo','mesto'], seznam_podatkov, 'csv_datoteke', 'lokali.csv')
napisi_csv(posebnosti, seznam_posebnosti, 'csv_datoteke', 'posebnosti.csv')
#napisi_csv(['id_lokala', 'jed', 'vrsta'], seznam_strani, 'csv_datoteke', 'jedi.csv')
#napisi_csv(['id', 'ime', 'ocena'], seznam_ocen, 'csv_datoteke', 'ocene.csv')
