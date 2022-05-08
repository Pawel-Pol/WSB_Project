import pandas as pd
import numpy as np


class StworzMacierzTN:
    # stworzenie macierzy przejsc markova na podstawie wprowadzonych parametrow
    # macierz wynikowa zawiera wartości procentowe

    def __init__(self, parametry):
        self.path = parametry[0]
        self.ilosc_wierzytelnosci = parametry[1]
        self.kolumna_kwota_wplat = parametry[2]
        self.kolumna_daty_wplat = parametry[3]
        self.kolumna_pakiet = parametry[4]


    def wczytaj_tabele(self):
        wczytany_plik = pd.read_excel(self.path).copy()
        self.lista_kolumn = [self.kolumna_kwota_wplat,
                             self.kolumna_daty_wplat,
                             self.kolumna_pakiet]
        return wczytany_plik

    def wczytaj_tabele_przestawna(self):
        wczytany_plik = pd.read_excel(self.path, index_col=0, header=0).copy()
        return wczytany_plik

    def zapisz_table_do_excela(self, tabela, jak_zapisac_plik):
        tabela.to_excel(f'macierz_przejsc_{self.path}', index=False)

    def sprawdzenie(self):
        print(self.min_date, self.max_date)

    def usun_zbedne_kolumny(self, tabela_nieoczyszczona):
        tabela_oczyszczona = []
        for column in list(tabela_nieoczyszczona):
            if column not in self.lista_kolumn:
                tabela_oczyszczona = tabela_nieoczyszczona.drop(column, inplace=True, axis=1)
        return tabela_oczyszczona

    def grupuj_daty(self, tabela_oczyszczona):
        tabela_do_grupowania = tabela_oczyszczona.copy()
        tabela_pogrupowana = tabela_do_grupowania.groupby(
            [pd.Grouper(key=self.kolumna_daty_wplat, freq='M'), self.kolumna_pakiet]).sum()
        return tabela_pogrupowana

    def stworz_tabele_przestawna(self, tabela):
        tabela_przestawna = pd.pivot_table(tabela,
                                           values=self.kolumna_kwota_wplat,
                                           index=[self.kolumna_pakiet],
                                           columns=[self.kolumna_daty_wplat],
                                           aggfunc=np.sum).fillna(0).copy()
        return tabela_przestawna

    def stworz_macierz_wartosci(self, tabela_przestawna1):
        tabela_przejsc = pd.DataFrame([])
        tabela_przestawna = pd.DataFrame(tabela_przestawna1).copy().astype(float)
        tabela_przestawna = tabela_przestawna.mask(tabela_przestawna > 0, 1).astype(int)
        yy = 0
        yn = 0
        ny = 0
        nn = 0
        col_count = tabela_przestawna.shape[1]
        col_names = tabela_przestawna.columns
        for column in range(col_count - 1):
            tabela_przejsc[col_names[column + 1]] = tabela_przestawna.iloc[:, column].astype(
                str) + tabela_przestawna.iloc[:, column + 1].astype(str)
            yy += tabela_przejsc[col_names[column + 1]].str.count('11')
            yn += tabela_przejsc[col_names[column + 1]].str.count('10')
            ny += tabela_przejsc[col_names[column + 1]].str.count('01')
            nn += tabela_przejsc[col_names[column + 1]].str.count('00')
        self.ilosc_wierzytelnosci = (self.ilosc_wierzytelnosci - tabela_przejsc.shape[0]) * tabela_przejsc.shape[1]
        macierz_wartosci = pd.DataFrame(data={'TAK': [yy.sum(), ny.sum()],
                                              'NIE': [yn.sum(), nn.sum() + self.ilosc_wierzytelnosci]},
                                        index=['TAK', 'NIE'])
        return macierz_wartosci

    def stworz_macierz_przejsc(self, macierz_wartosci):
        macierz_przejsc = macierz_wartosci.copy()
        macierz_przejsc.iloc[0, 0] = macierz_wartosci.iloc[0, 0] / macierz_wartosci.iloc[0, :].sum()
        macierz_przejsc.iloc[0, 1] = macierz_wartosci.iloc[0, 1] / macierz_wartosci.iloc[0, :].sum()
        macierz_przejsc.iloc[1, 0] = macierz_wartosci.iloc[1, 0] / macierz_wartosci.iloc[1, :].sum()
        macierz_przejsc.iloc[1, 1] = macierz_wartosci.iloc[1, 1] / macierz_wartosci.iloc[1, :].sum()
        return macierz_przejsc * 100

    def stworz_mp_tn(self):
        wczytany_plik = self.wczytaj_tabele()
        self.usun_zbedne_kolumny(wczytany_plik)
        pogrupowana_tabela = self.grupuj_daty(wczytany_plik)
        tabela_przestawna = self.stworz_tabele_przestawna(pogrupowana_tabela)
        macierz_wartosci = self.stworz_macierz_wartosci(tabela_przestawna)
        macierz_przejsc = self.stworz_macierz_przejsc(macierz_wartosci)
        print(macierz_przejsc)
