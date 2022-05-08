# wprowadz odpowiednie parametry
# w wyniku otrzymasz macierz z wartościami procentowymi

import klasa

sciezka_pliku = 'Data/wplaty_klientow.xlsx'
ilosc_wierzytelnosci = 5000
kolumna_kwota_wplat = 'kwota'
kolumna_daty_wplat = 'data'
kolumna_pakiet = 'id'
parametry = [sciezka_pliku,ilosc_wierzytelnosci,kolumna_kwota_wplat,kolumna_daty_wplat,
             kolumna_pakiet]

if __name__=='__main__':
    przejscia = klasa.StworzMacierzTN(parametry)
    macierz_przejsc = przejscia.stworz_mp_tn()
    print(macierz_przejsc)
