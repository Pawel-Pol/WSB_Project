# wprowadz odpowiednie parametry
# w wyniku otrzymasz macierz z wartościami procentowymi

import klasa

sciezka_pliku = 'Data/wplaty_klientow.xlsx'
ilosc_wierzytelnosci = 7000
kolumna_kwota_wplat = 'kwota'
kolumna_daty_wplat = 'data'
kolumna_pakiet = 'id'
parametry = [sciezka_pliku,ilosc_wierzytelnosci,kolumna_kwota_wplat,kolumna_daty_wplat,
             kolumna_pakiet]

if __name__=='__main__':
    przejscia = klasa.stworz_macierz_tn(parametry)
    macierz_przejsc = przejscia.create_mc_yn()
    print(macierz_przejsc)
