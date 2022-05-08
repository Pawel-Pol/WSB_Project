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
parametry=[ilosc_wplat,ilosc_osob,data_startowa,data_koncowa,najnizsza_wplata,najwyzsza_wplata]

def stworz_dane(parametry):
    """
    Przyjmuje 1 liste zawierającą 6 argumentów

    parametry : list(ilosc_wplat, ilosc_osob, data_startowa,
    data_koncowa, najnizsza_wplata, najwyzsza_wplata)
        ilosc_wplat : int
            Ilość wpłat
        ilosc_osob : int
            lość osób/długów/wierzytelności
        data_startowa : str "YYYY-mm-DD"
            ata pierwszej wpłaty
        data_koncowa : str "YYYY-mm-DD"
            Data ostatniej wpłaty
        najnizsza_wplata : int
            Najniższa wpłata
        najwyzsza_wplata : int
            Najwyższa wpłata
    """
    a = pd.DataFrame([])
    for i in range(parametry[0]):
        id = 'A'+str(random.randint(1, parametry[1]))
        wplata = random.randint(parametry[4], parametry[5])
        data_start = datetime.datetime.strptime(parametry[2], '%Y-%m-%d')
        data_koniec = datetime.datetime.strptime(parametry[3],'%Y-%m-%d')
        czas_pomiedzy_datami = data_koniec - data_start
        dni_pomiedzy_datami = czas_pomiedzy_datami.days
        losowa_ilosc_dni = random.randrange(dni_pomiedzy_datami)
        losowa_data = data_start + datetime.timedelta(days=losowa_ilosc_dni)
        tymczasowe = pd.DataFrame({'id':id,'kwota':wplata,'data':losowa_data}, index = [0])
        a = pd.concat([a,tymczasowe])

    a.to_excel(f'../Data/wplaty_klientow.xlsx', index = False)

if __name__=='__main__':
    stworz_dane(parametry)
    a = pd.read_excel('../Data/wplaty_klientow.xlsx').copy()
    print(a)

