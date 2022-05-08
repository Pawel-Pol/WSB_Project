# tylko po to aby stworzyc przykladowe dane

import pandas as pd
import random
import datetime

ilosc_wplat = 43729
ilosc_osob = 5000
data_startowa = '2021-01-01'
data_koncowa = '2022-01-31'
najnizsza_wplata = 0
najwyzsza_wplata = 2000

def stworz_dane():
    a = pd.DataFrame([])
    for i in range(ilosc_wplat):
        id = 'A'+str(random.randint(1, ilosc_osob))
        wplata = random.randint(najnizsza_wplata, najwyzsza_wplata)
        data_start = datetime.datetime.strptime(data_startowa, '%Y-%m-%d')
        data_koniec = datetime.datetime.strptime(data_koncowa,'%Y-%m-%d')
        czas_pomiedzy_datami = data_koniec - data_start
        dni_pomiedzy_datami = czas_pomiedzy_datami.days
        losowa_ilosc_dni = random.randrange(dni_pomiedzy_datami)
        losowa_data = data_start + datetime.timedelta(days=losowa_ilosc_dni)
        tymczasowe = pd.DataFrame({'id':id,'kwota':wplata,'data':losowa_data}, index = [0])
        a = pd.concat([a,tymczasowe])

    a.to_excel(f'../Data/wplaty_klientow.xlsx', index = False)

if __name__=='__main__':
    stworz_dane()
    a = pd.read_excel('../Data/wplaty_klientow.xlsx').copy()
    print(a)

