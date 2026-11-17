# Postępy prac — symulacja ruchu rowerowego w Krakowie

## Co zrobiliśmy

1. Wybraliśmy niewielki obszar Grzegórzek / ul. Kotlarskiej.
2. Pobraliśmy sieć rowerową z OpenStreetMap oraz infrastrukturę ZTP.
3. Przeanalizowaliśmy trzy artykuły dotyczące modelowania ruchu rowerowego.
4. Wybraliśmy prosty model agentowy z kolejką zdarzeń.
5. Przygotowaliśmy demonstracyjny prototyp wyznaczania tras i liczenia przejazdów na odcinkach.

## 1. Problem i cel

- **Cel:** zasymulować przejazdy rowerzystów na rzeczywistej sieci ulic i porównać ich natężenie z danymi liczników.
- **Pytanie:** czy model uwzględniający preferowanie infrastruktury rowerowej odtworzy rozkład ruchu lepiej niż model oparty na najkrótszej trasie?
- Nie symulujemy na razie ruchu samochodowego, pieszych ani świateł.

## 2. Dane i obszar

- OSMnx: **796 węzłów, 1660 krawędzi** (graf pobrany w notebooku).
- ZTP: **92 obiekty infrastruktury** w wyniku zapytania o zasięg obszaru.
- Potencjalne punkty weryfikacji: liczniki **Kotlarska** i **Grzegórzecka** — ich dokładne lokalizacje i zgodność z granicami grafu wymagają sprawdzenia.
- Nadal brakuje: gotowych tabel z pomiarami w jednym interwale czasu oraz wiarygodnego rozkładu źródeł i celów podróży.

**Graf i infrastruktura to nie dane o natężeniu ruchu.**

## 3. Wybór modelu — dlaczego nie automat komórkowy?

| Metoda | Plus | Minus |
|---|---|---|
| DES | Proste planowanie przejazdów przez odcinki | Bez reguł zachowania jest bardzo uproszczony |
| ABM | Osobna trasa, prędkość i preferencje rowerzysty | Wymaga przyjęcia reguł i popytu |
| ABM + zdarzenia | Niewiele kodu i zachowuje indywidualne trasy | Na początku nie modeluje interakcji |

**Decyzja:** agentowy model przejazdów na grafie, z realizacją kolejnych odcinków jako zdarzeń. To prostsze od symulowania każdego metra ruchu na siatce komórek.

## 4. Schemat działania symulacji

1. Wczytaj skierowany graf rowerowy.
2. Wygeneruj rowerzystów z początkiem, celem, czasem startu i prędkością.
3. Oblicz trasę algorytmem Dijkstry.
4. Kolejka zdarzeń przenosi rowerzystów między odcinkami.
5. Zapisz liczby przejazdów i czasy podróży.
6. W kolejnej iteracji: porównaj przejazdy w punktach liczników z obserwacjami.

**W pierwszej wersji OD, liczba rowerzystów i prędkości są syntetyczne.** Nie twierdzimy, że wyniki są już zgodne z Krakowem.

## 5. Dwa algorytmy do porównania

**A. Trasa najkrótsza:** $c_e=L_e$.

**B. Trasa preferująca drogę rowerową:** $c_e=0{,}7L_e$ dla odcinka oznaczonego jako `cycleway` w OSM; w pozostałych przypadkach $c_e=L_e$.

Mnożnik 0,7 jest roboczy; wymaga sprawdzenia w danych. Obie strategie dostają **te same podróże i te same prędkości**.

## 6. Pierwszy prototyp — wynik prac

- Skrypt: `src/model_alpha.py`.
- Na grafie testowym działa generowanie tras, obliczanie czasów przejazdu i zliczanie ruchu na krawędziach.
- Wyniki dwóch strategii są zapisywane do CSV.
- Przygotowano i uruchomiono **4 testy jednostkowe**.
- **Nie przeprowadziliśmy jeszcze kalibracji ani walidacji na danych dwóch liczników.**

## 7. Następne zadania

1. Uruchomić prototyp na rzeczywistym `osm_kotlarska.graphml`, obejrzeć najczęściej używane krawędzie.
2. Ustalić dokładne lokalizacje dwóch liczników i pozyskać ich pomiary.
3. Zamienić losowanie OD z całego grafu na kilka realistycznych stref wejścia i wyjścia.
4. Kalibrować natężenie popytu, ewentualnie parametr preferencji trasy.
5. Porównać oba warianty na **odłożonych godzinach lub dniach** (MAE i wykres liczników).

## Materiały

- Ordinez i in. (2018): https://www.mdpi.com/2504-3900/2/19/1220
- Ziemke i in. (2017): https://doi.org/10.1016/j.procs.2017.05.424
- Broach i in. (2012): https://doi.org/10.1016/j.tra.2012.07.005
- ZTP — pomiary: https://ztp.krakow.pl/rower/pomiary-ruchu-rowerowego
