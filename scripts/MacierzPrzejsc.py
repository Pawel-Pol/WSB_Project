import pandas as pd
import numpy as np


class TworcaMacierzyTN:
    def __init__(self, sciezka_pliku: str, ilosc_wierzytelnosci: int,
                 kolumna_pakiet: str, kolumna_kwota_wplat: str, kolumna_daty_wplat: str):
        """
            Klasa do obliczenia macierzy przejsc markova wpłat
        Buduje wszystkie potrzebne atrybuty klasy StworzMacierzTN
        """
        self.sciezka_pliku = sciezka_pliku
        self.ilosc_wierzytelnosci = ilosc_wierzytelnosci
        self.kolumna_pakiet = kolumna_pakiet
        self.kolumna_kwota_wplat = kolumna_kwota_wplat
        self.kolumna_daty_wplat = kolumna_daty_wplat

    def wczytaj_tabele_wplat(self) -> pd.DataFrame:
        """
        Wczytuje kopie tabeli wpłat (id, wpłata, data wpłaty)
        """
        wczytany_plik = pd.read_excel(self.sciezka_pliku,
                                      usecols=[self.kolumna_pakiet, self.kolumna_kwota_wplat, self.kolumna_daty_wplat]
                                      ).copy()
        return wczytany_plik

    def wczytaj_tabele_przestawna_wplat(self) -> pd.DataFrame:
        """
        Wczytuje tabele przestawną wpłat z id wierzytelnosci w pierwszej kolumnie
        , datami w pierwszym wierszu oraz wartościami wpłat w środku tabeli
        """
        wczytany_plik = pd.read_excel(self.sciezka_pliku, index_col=0, header=0).copy()
        return wczytany_plik

    @staticmethod
    def zapisz_table_do_excela(tabela: pd.DataFrame, jak_zapisac_plik: str):
        tabela.to_excel(f'{jak_zapisac_plik}', index=False)

    def grupuj_daty(self, tabela_wplat: pd.DataFrame) -> pd.DataFrame:
        """
        Grupuje tabele (pakiet/id, wplaty, daty) po kolumnie pakiet/id oraz roku i miesiącu
        """
        tabela_do_grupowania = tabela_wplat.copy()
        tabela_pogrupowana = tabela_do_grupowania.groupby(
            [pd.Grouper(key=self.kolumna_daty_wplat, freq='M'), self.kolumna_pakiet]
        ).sum()
        return tabela_pogrupowana

    def stworz_tabele_przestawna_wplat(self, tabela: pd.DataFrame) -> pd.DataFrame:
        """
        Tworzy tabelę przestawną i wypełnia puste komórki zerami \n
        wiersze: pakiet \n
        kolumny: daty \n
        wartości: wpłaty
        """
        tabela_przestawna = pd.pivot_table(tabela,
                                           values=self.kolumna_kwota_wplat,
                                           index=[self.kolumna_pakiet],
                                           columns=[self.kolumna_daty_wplat],
                                           aggfunc=np.sum).fillna(0).copy()
        return tabela_przestawna

    def stworz_macierz_wartosci(self, tabela_przestawna_wplat: pd.DataFrame) -> pd.DataFrame:
        """
        1.Tworzy tabele przejsc tzn. tabele, w której wartosci mowią czy byla wplata
        w poprzednim miesiacu i czy jest teraz. Np. 01 znaczy, że w poprzednim miesiącu nie
        było wpłaty ale w tym już była  \n
        2.Tworzy macierz wartości 2x2 czyli zlicza ile było oznaczeń 11,01,10,00 \n
        3.Dolicza wierzytelności, które nie były podane w tabeli wpłat, ale były podane w parametrach \n
        Przyjmuje: tabele przestawną z wierszami jako id, kolumnami jako daty i
        komórkami jako wartosci \n
        Zwraca: macierz wartości 2x2
        """
        tabela_przejsc = pd.DataFrame()
        tabela_przestawna = pd.DataFrame(tabela_przestawna_wplat).copy().astype(int)
        tabela_przestawna = tabela_przestawna.mask(tabela_przestawna > 0, 1)
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

    @staticmethod
    def stworz_macierz_przejsc(macierz_wartosci: pd.DataFrame) -> pd.DataFrame:
        """
        Tworzy macierz przejść markova 2x2 TAK/NIE
        :param macierz_wartosci:
        Przyjmuje maicerz wartości 2x2
        :return:
        Zwraca macierz przejsc markova 2x2 TAK/NIE, wartości podaje w %
        """
        macierz_przejsc = macierz_wartosci.copy()
        macierz_przejsc.iloc[0, 0] = macierz_wartosci.iloc[0, 0] / macierz_wartosci.iloc[0, :].sum()
        macierz_przejsc.iloc[0, 1] = macierz_wartosci.iloc[0, 1] / macierz_wartosci.iloc[0, :].sum()
        macierz_przejsc.iloc[1, 0] = macierz_wartosci.iloc[1, 0] / macierz_wartosci.iloc[1, :].sum()
        macierz_przejsc.iloc[1, 1] = macierz_wartosci.iloc[1, 1] / macierz_wartosci.iloc[1, :].sum()
        return macierz_przejsc * 100

    def stworz_mp_tn(self) -> pd.DataFrame:
        """
        Tworzy macierz przejść markova 2x2 TAK/NIE przyjmując parametry tego obiektu
        :return:
        Zwraca macierz przejść markova 2x2 TAK/NIE
        """
        wczytany_plik = self.wczytaj_tabele_wplat()
        pogrupowana_tabela = self.grupuj_daty(wczytany_plik)
        tabela_przestawna_wplat = self.stworz_tabele_przestawna_wplat(pogrupowana_tabela)
        macierz_wartosci = self.stworz_macierz_wartosci(tabela_przestawna_wplat)
        macierz_przejsc = self.stworz_macierz_przejsc(macierz_wartosci)
        return macierz_przejsc
