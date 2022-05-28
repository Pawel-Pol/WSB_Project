# wprowadz odpowiednie parametry
# w wyniku otrzymasz macierz z wartościami procentowymi

from MacierzPrzejsc import TworcaMacierzyTN as TM


def main():
    wplaty_z_banku = TM(
        'Data/wplaty_klientow.xlsx', 5000, 'id', 'kwota', 'data'
    )
    macierz_przejsc = wplaty_z_banku.stworz_mp_tn()
    print(macierz_przejsc)
    czy_zapisac = input('Czy zapisac plik t/n: ')
    if czy_zapisac == 't':
        TM.zapisz_table_do_excela(macierz_przejsc,
                                  'Data/macierz_przejsc_bank.xlsx')


if __name__ == '__main__':
    main()
