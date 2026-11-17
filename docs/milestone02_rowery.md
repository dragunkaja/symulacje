# Kamień milowy 2 — wybór i formalizacja modelu

**Projekt:** Symulacja ruchu rowerowego na wybranym obszarze Krakowa  
**Obszar:** Grzegórzki i okolice ul. Kotlarskiej (granice przyjęte w notebooku)

## 1. Cel

Chcemy zasymulować przejazdy rowerzystów na rzeczywistej sieci ulic i dróg rowerowych, a następnie porównać liczbę przejazdów przez wybrane punkty z danymi miejskich liczników. Dodatkowo sprawdzimy, jak reguła wyboru trasy wpływa na rozkład ruchu.

**Pytanie badawcze:** czy uwzględnienie preferencji dla infrastruktury rowerowej pozwoli lepiej odtworzyć obserwowane natężenia niż wybieranie wyłącznie najkrótszej drogi?

## 2. Dostępne dane

| Dane | Co zawierają | Przeznaczenie |
|---|---|---|
| OSM/OpenStreetMap przez OSMnx | Graf połączeń możliwych do przejazdu rowerem, długości krawędzi | Sieć, po której poruszają się rowerzyści |
| ZTP — ciągi rowerowe | Geometria, rodzaj, nawierzchnia | Późniejsze przypisanie jakości infrastruktury do krawędzi grafu |
| ZTP — automatyczne liczniki | Obserwowane przejazdy w punktach pomiarowych | Kalibracja i walidacja, **po pozyskaniu i uporządkowaniu szeregów pomiarowych** |

W dostarczonym notebooku pobrano graf **796 węzłów i 1660 krawędzi** oraz **92 obiekty infrastruktury ZTP**. Kod zapisuje pliki `osm_kotlarska.graphml` i `cycleways_kotlarska.geojson` do `data/raw/` (ścieżka zależy od katalogu roboczego notebooka). Te dane **nie zawierają liczby podróży ani źródeł i celów przejazdów**.

ZTP publikuje m.in. pomiary dla ul. Kotlarskiej i Grzegórzeckiej. Przed użyciem należy sprawdzić ich dokładne położenie, kierunki zliczania, interwał czasowy i jakość pomiarów.

## 3. Wybór metody

| Podejście | Zalety | Ograniczenia | Decyzja |
|---|---|---|---|
| DES — symulacja zdarzeń dyskretnych | Proste przejścia między odcinkami, wydajna | Sama w sobie nie wyjaśnia wyboru trasy | Używamy do obsługi zdarzeń |
| ABM — model agentowy | Każdy rowerzysta ma trasę, prędkość i preferencje | Trzeba przyjąć reguły zachowania i źródła/cel podróży | Podstawa modelu |
| Model hybrydowy ABM + zdarzenia | Łączy czytelne zachowanie rowerzysty z prostym planowaniem przejazdów | Więcej elementów niż najprostszy DES | Wybrany wariant alfa |

Nie modelujemy jeszcze ruchu samochodów, pieszych, świateł ani wyprzedzania. Nie implementujemy automatów komórkowych i nie potrzebujemy bibliotek SimPy/Mesa do pierwszej wersji.

## 4. Model formalny — wersja alfa

### 4.1. Sieć

Sieć rowerowa to **graf skierowany** $G=(V,E)$:

- $V$ — węzły (połączenia ulic / odcinków),
- $E$ — przejezdne odcinki; między dwoma węzłami mogą istnieć równoległe krawędzie,
- $L_e$ — długość odcinka $e$ w metrach,
- $R_e$ — informacja, czy odcinek jest oznaczony w OSM jako droga rowerowa.

W pierwszej wersji alfa wczytujemy graf GraphML i wybieramy największą **silnie spójną** część, aby każda para wybranych węzłów była połączona. Trzeba sprawdzić, ile sieci przez to odpada; jest to uproszczenie techniczne, nie właściwość Krakowa.

### 4.2. Rowerzysta

Rowerzysta $i$ ma stan:

$$a_i=(o_i,d_i,t_i^{start},v_i,p_i,k_i)$$

- $o_i,d_i$ — węzeł początku i końca podróży,
- $t_i^{start}$ — chwila rozpoczęcia przejazdu,
- $v_i$ — prędkość rowerzysty,
- $p_i$ — wybrana trasa (lista kolejnych węzłów),
- $k_i$ — numer aktualnego odcinka trasy.

**Uwaga:** w pierwszym prototypie początki i cele są losowane z grafu, prędkość przyjmowana z przedziału 12–18 km/h, a liczba rowerzystów wynosi przykładowo 200. To **parametry demonstracyjne, a nie estymacje z pomiarów**.

### 4.3. Reguły wyboru trasy

**Strategia A — najkrótsza trasa.** Koszt krawędzi:

$$c_e=L_e$$

**Strategia B — preferowanie dróg rowerowych.** Koszt krawędzi:

$$c_e=\begin{cases}0{,}7L_e & \text{gdy oznaczono ją jako cycleway w OSM},\\L_e&\text{w przeciwnym razie.}\end{cases}$$

Wartość **0,7 jest jedynie hipotezą testową**. W modelu skalibrowanym parametr trzeba dobrać na danych (lub podać jako analizę scenariuszy). Trasy są wyznaczane algorytmem Dijkstry (`networkx.shortest_path` z wagą).

### 4.4. Zdarzenia i przejścia

Zdarzeniem jest wejście rowerzysty na kolejny odcinek trasy. Kolejka priorytetowa przechowuje: $(t,i,k_i)$. Dla krawędzi długości $L_e$:

$$\Delta t_e = \frac{3{,}6 L_e}{v_i}$$

gdzie $v_i$ jest w km/h, a czas w sekundach. Po zdarzeniu $(t,i,k_i)$ planujemy $(t+\Delta t_e,i,k_i+1)$. Przejazd przez punkt pomiarowy odwzorowany na środek krawędzi rejestrujemy w chwili $t+\Delta t_e/2$.

**Ograniczenie alfa:** rowerzyści nie oddziałują na siebie; nie występują korki, sygnalizacja ani ograniczenia przepustowości. To mikrosymulacja indywidualnych tras, a nie szczegółowa symulacja fizycznego ruchu.

### 4.5. Wyniki

- liczba przejazdów po każdym odcinku grafu,
- czas przejazdu dla każdej podróży i średni czas,
- w kolejnym etapie: liczba przejazdów przez **dwa zweryfikowane punkty pomiarowe**, w porównywalnych przedziałach czasu.

## 5. Kalibracja i walidacja — plan

1. Pozyskać pomiary z dwóch liczników w wybranym **tym samym dniu i przedziale czasowym**. Sprawdzić, czy sumują oba kierunki.
2. Zweryfikować położenie liczników w terenie i ręcznie przypisać je do **właściwych skierowanych odcinków grafu**. Najbliższa krawędź wybrana automatycznie może być błędna.
3. Ustalić kilka **stref wejścia i wyjścia** obszaru i prosty, jawny rozkład OD. Nie da się wiarygodnie wyznaczyć pełnej macierzy OD tylko na podstawie dwóch liczników.
4. Kalibrować maksymalnie **jeden lub dwa jawnie wskazane parametry** (np. wielkość popytu i współczynnik preferencji tras). Stosować kilka powtórzeń z różnymi ziarnami losowymi.
5. Rozdzielić dane na czas kalibracji i **inne godziny / dni do sprawdzenia**. Nie oceniać modelu na tych samych próbkach, na których był dopasowany.
6. Porównać na pomiarach liczników: $MAE=\frac{1}{N}\sum_j|\hat y_j-y_j|$. Używać też wykresów zmienności godzinowej i przedziałów wynikających z losowości symulacji.

Dopasowanie liczby rowerzystów do jednego licznika **nie dowodzi**, że model poprawnie przewiduje ruch na całej sieci.

## 6. Porównanie modeli

W wersji alfa porównujemy **dwie reguły wyboru trasy na tych samych podróżach i w tym samym symulatorze**. Dzięki temu różnice wynikają z algorytmu trasowania, nie z innych danych wejściowych.

Ewentualne porównanie **samodzielnego DES z bardziej szczegółowym ABM** można wykonać później, jeśli dostępne pomiary pozwolą ocenić dodatkowe zachowania (np. czas oczekiwania). Sama zgodność liczników nie rozstrzyga o jakości odwzorowania interakcji między rowerzystami.

## 7. Postęp implementacji

- [x] Notebook do pobrania i obejrzenia grafu OSM oraz infrastruktury ZTP.
- [x] Demonstracyjny skrypt `src/model_alpha.py` — odczyt GraphML, losowe podróże, algorytm Dijkstry, kolejka zdarzeń, dwa warianty trasowania, pliki CSV.
- [x] Cztery testy jednostkowe na małym grafie syntetycznym.
- [ ] Uruchomienie i ocena wyników na rzeczywistym pliku GraphML z Waszego repozytorium.
- [ ] Pozyskanie szeregów z dwóch liczników i przypisanie lokalizacji do grafu.
- [ ] Kalibracja, walidacja oraz porównanie wariantów na prawdziwych pomiarach.

## 8. Materiały źródłowe

1. Ordinez i in. (2018), *A Cyclist Traffic Simulation and Analysis Tool*: https://www.mdpi.com/2504-3900/2/19/1220 — graf miasta, generowanie tras, analiza przejazdów.
2. Ziemke, Metzler, Nagel (2017), *Modeling bicycle traffic in an agent-based transport simulation*: https://depositonce.tu-berlin.de/items/1220e0f8-ab3f-4d97-a851-26576a513ed1 — modelowanie rowerzystów jako agentów z uwzględnieniem infrastruktury.
3. Broach, Dill, Gliebe (2012), *Where do cyclists ride? A route choice model developed with revealed preference GPS data*: https://doi.org/10.1016/j.tra.2012.07.005 — wpływ długości i infrastruktury na wybór tras.
4. ZTP Kraków, *Pomiary ruchu rowerowego*: https://ztp.krakow.pl/rower/pomiary-ruchu-rowerowego
5. ZTP Kraków, *Dane tabelaryczne*: https://ztp.krakow.pl/rower/pomiary-ruchu-rowerowego/dane-tabelaryczne
