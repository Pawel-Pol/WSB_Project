# WSB_Project
Projekt WSB 2022 python developer - Paweł Polkowski
https://github.com/Pawel-Pol/WSB_Project

# Cel:
1. Stworzenie macierzy przejść markova na podstawie wpłat pieniężnych w kolejnych miesiącach
2. Macierz umożliwia między innymi przewidywanie ilości wpływów pieniężnych w grupie osób w kolejnych miesiącach

# Opis działania
1. Bazowo aby odpalić program wystarczy uruchomić plik main.py
#

2. skrypt stworz_przykladowe_dane pozwala nam na stowrzenie losowych danych
- ilosc_wpłat = ile było wpłat
- ilość_osob = ilosc osob/wierzytelnosci/długów
- data_startowa = od kiedy pojawiają się wpłaty
- data_koncowa = do kiedy pojawiają się wpłaty
- najniższa_wpłata = najniższa wpłata
- najwyzsza_wplata = najwyzsza wpłata

2. skrypt klasa zawiera klasę która oblicza macierz przejść Markova

3. Plikiem main odpalamy działanie programu - wyliczamy macierz przejsc markova. 
- ścieżka pliku = ścieżka do pliku z danymi
- ilosc wierzytelności = ilość osob = ilość długów
- kolumna_kwota_wpłat = wartości wpłat
- kolumna_daty_wpłat = daty wpłat
- kolumna_pakiet = id osoby/wierzytelności/długu

