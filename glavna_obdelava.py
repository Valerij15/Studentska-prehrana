import os
import re

mapa = 'html_datoteke'
datoteka = 'glavna_stran.html'

def datoteka_v_niz(mapa, ime_datoteke):
    with open(os.path.join(mapa, ime_datoteke), encoding='utf-8') as vhodna_datoteka:
        return vhodna_datoteka.read()

def stran_v_lokale(stran):
    vzorec = r'<div class="row restaurant-row(.*?)</div>'
    narejen_vzorec = re.compile(vzorec, re.DOTALL)
    return re.findall(narejen_vzorec, stran)

vsebina = datoteka_v_niz(mapa, datoteka)
seznam = stran_v_lokale(vsebina)
print(len(seznam))

