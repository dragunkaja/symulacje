# Symulacja ruchu rowerowego w sieci miejskiej Krakowa

**Projekt semestralny — modelowanie i analiza przepływów rowerowych z wykorzystaniem rzeczywistych danych przestrzennych i pomiarowych**

> **Status dokumentu:** specyfikacja koncepcyjna i plan badawczy. Projekt nie jest jeszcze zwalidowanym modelem predykcyjnym. Parametry, których nie da się bezpośrednio wyznaczyć z dostępnych danych, będą jawnie oznaczane jako założenia lub scenariusze.

## 1. Streszczenie projektu

Celem projektu jest opracowanie i ocena modelu symulacyjnego ruchu rowerowego w wybranym obszarze Krakowa. Model będzie reprezentował sieć infrastruktury rowerowej jako graf przestrzenny, a podróże jako przepływy agentów poruszających się pomiędzy punktami początkowymi i docelowymi. Zachowanie agentów będzie zależne od parametrów sieci, takich jak długość odcinka, typ infrastruktury, dopuszczalność ruchu rowerowego, nachylenie i przyjęty koszt przejazdu.

Model zostanie zasilony danymi OpenStreetMap oraz miejskimi danymi o infrastrukturze i natężeniu ruchu rowerowego. Pomiary z liczników będą wykorzystywane do analizy charakterystyki ruchu oraz — po sprawdzeniu identyfikowalności — do kalibracji i walidacji przepływów w sieci. Nie będą traktowane jako bezpośrednie obserwacje pełnych tras poszczególnych rowerzystów.

Projekt koncentruje się na odpowiedzi na pytanie, jak struktura infrastruktury i przyjęte reguły wyboru tras wpływają na rozkład ruchu w sieci oraz jak zmieniają się przepływy po modyfikacji wybranych odcinków.

## 2. Problem badawczy i cel

### Problem

Dostępne pomiary miejskie opisują liczbę przejazdów zarejestrowanych w określonych punktach, natomiast nie przedstawiają kompletnych tras podróży pomiędzy źródłami i celami. Jednocześnie infrastruktura rowerowa jest przestrzennie niejednorodna, a rowerzyści mogą wybierać trasy nie tylko na podstawie długości lub czasu, lecz także komfortu, bezpieczeństwa i ciągłości infrastruktury.

W związku z tym samo wyznaczanie najkrótszych ścieżek nie wystarcza do wiarygodnego opisu zachowań rowerzystów. Konieczne jest zbudowanie jawnego modelu popytu, reguł wyboru trasy oraz procedury porównania wyników z pomiarami.

### Cel główny

Opracowanie powtarzalnego, przestrzennego modelu symulacyjnego, który umożliwi analizę rozkładu ruchu rowerowego w wybranym obszarze Krakowa oraz ocenę wpływu zmian infrastruktury i parametrów ruchu na natężenie na poszczególnych odcinkach.

### Cele szczegółowe

1. Pozyskanie, oczyszczenie i integracja danych o sieci drogowej, infrastrukturze rowerowej i pomiarach liczników.
2. Zbudowanie topologicznie spójnego, skierowanego grafu sieci dostępnej dla rowerów.
3. Opracowanie modelu syntetycznego popytu OD (origin–destination), którego przepływy mogą być kalibrowane na podstawie liczników.
4. Zaimplementowanie agentów rowerzystów i co najmniej dwóch wariantów reguł wyboru trasy.
5. Przeprowadzenie eksperymentów scenariuszowych, np. zamknięcia, dodania lub poprawy odcinka.
6. Walidacja modelu na pomiarach niewykorzystanych do kalibracji oraz analiza wrażliwości na niepewne parametry.

## 3. Pytania badawcze

- **RQ1 — odwzorowanie pomiarów:** W jakim stopniu model odtwarza natężenie ruchu zarejestrowane przez liczniki w wybranym obszarze?
- **RQ2 — wybór trasy:** Jak zmienia się rozkład przepływów, gdy rowerzyści minimalizują wyłącznie czas/długość trasy, a gdy uwzględniają również jakość infrastruktury?
- **RQ3 — zmiany infrastruktury:** Jak dodanie, usunięcie lub zmiana parametrów wybranego odcinka wpływa na rozkład ruchu w sieci?
- **RQ4 — niepewność:** Jak wrażliwe są wyniki na nieznaną macierz OD, parametry preferencji rowerzystów i niepełność danych?
- **RQ5 — czas:** Czy uwzględnienie zmienności dobowej poprawia zgodność symulowanych przepływów z obserwowanymi profilami liczników?

Pytania RQ1 i RQ4 są warunkami wiarygodności dalszych eksperymentów. Jeżeli danych nie wystarczy do identyfikacji popytu OD, wyniki scenariuszy będą przedstawiane jako analiza warunkowa, a nie prognoza rzeczywistego ruchu.

## 4. Zakres i granice projektu

### Zakres wersji bazowej

- Jeden ograniczony obszar Krakowa, wyznaczony po audycie lokalizacji liczników i spójności sieci.
- Sieć rowerowa i odcinki dopuszczające ruch rowerowy.
- Ruch w jednym trybie: rowery konwencjonalne; rowery elektryczne mogą być osobnym rozszerzeniem.
- Syntetyczne podróże OD.
- Co najmniej dwa warianty wyboru trasy.
- Przepływy zagregowane na odcinkach i w punktach licznikowych.
- Eksperymenty „co-jeśli” dotyczące zmian infrastruktury.

### Poza zakresem wersji bazowej

- Odtwarzanie rzeczywistych indywidualnych tras mieszkańców.
- Prognozowanie całkowitego popytu rowerowego dla całego Krakowa.
- Pełna mikrosymulacja interakcji rower–samochód–pieszy.
- Modelowanie zachowań na sygnalizacji świetlnej z rzeczywistymi cyklami.
- Wnioskowanie o przyczynowości na podstawie samych korelacji liczników.
- Automatyczne wyznaczanie przepustowości każdej drogi bez danych pomiarowych.

## 5. Dane wejściowe i ich wiarygodność

### 5.1. Dane już dostarczone przez zespół

| Zbiór | Zawartość | Zastosowanie | Ograniczenia / kontrole |
|---|---|---|---|
| `Liczniki - dzienne.csv` | 3635 dat, 20 kolumn liczników, okres 18.11.2016–31.10.2026 | Analiza sezonowości, natężenia dziennego, kalibracja i walidacja na punktach pomiarowych | Nie wszystkie liczniki działają przez cały okres; puste wartości nie są zerami; pochodzenie części kolumn wymaga weryfikacji |
| `rowerowy-otwarty-plan_profil-dobowy_wielicka_month-2026-10.csv` | 24 godziny, profil dni powszednich, typowy ruch, rok wcześniej oraz zakres min–max | Rekonstrukcja względnego rozkładu godzinowego dla Wielickiej | Profil typowy jest statystyką historyczną, nie surową obserwacją konkretnego dnia; dotyczy jednego licznika i miesiąca |
| Zrzut ekranu licznika Wielicka | Wartość dzienna i suma YTD w chwili wykonania zrzutu | Kontrola orientacyjnej zgodności z CSV | Zrzut jest migawką z określonego dnia; nie jest samodzielnym szeregiem czasowym |

**Wyniki wstępnego audytu CSV:**

- Plik dzienny ma 3635 wierszy i ciągły kalendarz od 18.11.2016 do 31.10.2026.
- Zbiór zawiera 20 kolumn liczników, ale publiczna metodologia Otwarty Plan opisuje 19 całodobowych liczników indukcyjnych oraz 4 czujniki Telraam. Rozbieżność, w szczególności kolumnę `Jancarza`, należy wyjaśnić przed użyciem.
- Przykładowe liczniki o długim wspólnym okresie obserwacji to Mogilska, Kotlarska, Bulwary, Dworzec Główny, Kopernika i Grzegórzecka. Ich dokładne zakresy i kompletność należy wyliczać z surowego pliku, a nie zakładać na stałe.
- Część kolumn kończy się wcześniej niż cały zbiór. Nie wolno automatycznie uzupełniać braków zerami.
- Wstępnie zaobserwowano 10 zer w październiku 2026 dla Klimeckiego. Należy sprawdzić, czy są to rzeczywiste zera, czy okres awarii.
- Kolumny pogodowe mają niepełne pokrycie i według wstępnego odczytu kończą się 28.02.2026. Pogoda nie powinna być używana w analizie obejmującej późniejsze daty bez uzupełnienia z IMGW.
- Dla Wielickiej suma w pliku od 01.01 do 31.10.2026 wynosi 391 199, a suma za październik 41 269. Wartości te należy ponownie wyliczyć w pipeline na oryginalnym pliku i zachować raport audytu.

### 5.2. Źródła do pozyskania

| Dane | Źródło | Rola | Priorytet |
|---|---|---|---|
| Sieć ulic i dróg rowerowych | OpenStreetMap | Geometria, topologia, kierunki i dostępność | Krytyczny |
| Infrastruktura rowerowa miasta | ZTP / MSIP Kraków / Otwarte Dane Krakowa | Weryfikacja typów i przebiegu infrastruktury | Krytyczny |
| Lokalizacje i charakterystyka liczników | ZTP / Otwarty Plan | Geolokalizacja pomiarów i mapowanie do sieci | Krytyczny |
| Profile godzinowe pozostałych liczników | Otwarty Plan | Rozkład dobowy dla wielu punktów | Wysoki |
| Numeryczny model terenu | GUGiK | Nachylenie i przewyższenia | Opcjonalny |
| Pogoda historyczna | IMGW | Analiza wpływu pogody na natężenie | Opcjonalny |
| Dane zagospodarowania / ludności | BDL GUS / MSIP | Pomoc przy definiowaniu źródeł i celów popytu | Opcjonalny, wymaga oceny skali |

Linki:
- Otwarty Plan — pomiary rowerowe: https://rowerowy.otwartyplan.org/dane/
- ZTP — pomiary ruchu rowerowego: https://ztp.krakow.pl/rower/pomiary-ruchu-rowerowego
- ZTP — dane otwarte: https://ztp.krakow.pl/dane-otwarte
- MSIP — ZTP, komunikacja miejska i rowerowa: https://msip.krakow.pl/dataset/2963
- OpenStreetMap: https://www.openstreetmap.org/
- OSMnx: https://osmnx.readthedocs.io/en/stable/
- Geoportal / NMT: https://www.geoportal.gov.pl/pl/dane/numeryczny-model-terenu-nmt/
- IMGW: https://danepubliczne.imgw.pl/

### 5.3. Kryteria wyboru obszaru

Obszar nie powinien być wybierany wyłącznie dlatego, że jest atrakcyjny na mapie. Kandydat musi spełniać następujące warunki:

1. Co najmniej 3–5 liczników z wiarygodnymi lokalizacjami i wystarczającym wspólnym okresem danych.
2. Liczniki leżą na odcinkach sieci możliwych do jednoznacznego odwzorowania.
3. Sieć ma alternatywne połączenia, aby analiza wyboru trasy miała sens.
4. Granica obszaru nie przecina większości głównych tras bez możliwości modelowania ruchu wlotowego i wylotowego.
5. Dostępne są dane o typie infrastruktury na istotnej części sieci.

Proponowany obszar centrum–Grzegórzki jest hipotezą roboczą. Ostateczny wybór nastąpi po mapowaniu liczników i teście spójności grafu.

## 6. Przygotowanie i integracja danych

Pipeline przygotowania danych powinien być powtarzalny i rozdzielać dane surowe od przetworzonych.

### 6.1. Dane licznikowe

- Zachować oryginalne pliki w `data/raw/` bez ręcznej edycji.
- Parsować daty do `YYYY-MM-DD`.
- Konwertować wartości liczbowe z uwzględnieniem separatora dziesiętnego.
- Rozdzielić brak pomiaru (`NA`) od prawidłowego zera (`0`).
- Przekształcić dane z formatu wide do long: `date`, `sensor_id`, `count`, `quality_flag`.
- Utworzyć raport kompletności dla każdego licznika: liczba obserwacji, zakres dat, udział braków, liczba zer i podejrzanych serii.
- Ustalić wspólny okres analityczny dopiero po raporcie kompletności.

### 6.2. Profile godzinowe

Profil godzinowy należy traktować jako rozkład udziałów godzinowych, a nie dodatkową liczbę przejazdów.

Dla profilu \(x_h\), gdzie \(h\) oznacza godzinę:

\[
p_h = \frac{x_h}{\sum_{h=0}^{23}x_h}
\]

Dla dziennego pomiaru \(N_d\):

\[
\hat{N}_{d,h}=N_d p_h
\]

Po zaokrągleniu metodą największych reszt suma godzin musi być dokładnie równa \(N_d\). Profile dla różnych liczników i typów dni należy pobierać oddzielnie, jeśli są dostępne. Nie wolno bez uzasadnienia kopiować profilu Wielickiej na całą sieć.

### 6.3. Dane przestrzenne

- Sieć OSM pobierać jako skierowany graf z zachowaniem ograniczeń dostępu dla rowerów.
- Ujednolicić układy współrzędnych; odległości liczyć w układzie metrycznym odpowiednim dla Krakowa.
- Zachować identyfikatory węzłów i krawędzi oraz atrybuty źródłowe OSM.
- Uzupełnić / zweryfikować typ infrastruktury na podstawie miejskich warstw GIS.
- Przypisywać licznik do krawędzi na podstawie współrzędnych, kierunku pomiaru i dokumentacji lokalizacji, a nie wyłącznie najbliższej geometrii.
- Każde dopasowanie sprawdzić wizualnie; przypadki niejednoznaczne oznaczyć do ręcznej kontroli.
- Sprawdzić spójność topologiczną, kierunki jednokierunkowe, zakazy ruchu rowerowego, brakujące połączenia i odcinki urwane na granicy obszaru.

### 6.4. Jednostki i konwencje

| Wielkość | Jednostka wewnętrzna |
|---|---|
| Długość krawędzi | m |
| Prędkość | m/s |
| Czas przejazdu | s |
| Natężenie | rowery / przedział czasu |
| Nachylenie | % lub stopnie, konsekwentnie w całym pipeline |
| Koszt trasy | jawnie zdefiniowana jednostka / bezwymiarowy koszt uogólniony |

Każdy przetworzony zbiór powinien mieć metadane: źródło, data pobrania, licencja, CRS, jednostki, zakres dat i wersję pipeline.

## 7. Proponowany model symulacyjny

### 7.1. Rodzaj modelu

**Przestrzenny, sieciowy model agentowy (network-based Agent-Based Model, ABM) z dyskretnym krokiem czasowym.**

W wersji bazowej nie zakładamy pełnej mikrosymulacji fizycznych interakcji rowerzystów. Model odwzorowuje indywidualne podróże agentów po grafie i agreguje przepływy na odcinkach oraz w punktach licznikowych.

### 7.2. Wybór silnika

**Rekomendacja bazowa: własny model ABM w Pythonie, oparty na Mesa (zarządzanie agentami i harmonogramem), NetworkX (graf i algorytmy tras) oraz OSMnx (pozyskanie i przygotowanie sieci).**

Uzasadnienie:
- głównym przedmiotem projektu są zachowania agentów, rozkład tras i wpływ infrastruktury, a nie szczegółowa dynamika pojazdów na pasach;
- można jawnie zdefiniować i testować reguły wyboru tras;
- model jest łatwy do połączenia z pandas/geopandas i danymi licznikowymi;
- zespół może kontrolować założenia i walidację bez konieczności kalibracji dużej liczby parametrów mikrosymulacji.

**SUMO należy potraktować jako alternatywę / punkt odniesienia**, jeżeli zakres zostanie rozszerzony o interakcje na skrzyżowaniach, kolejki, sygnalizację i współdzielenie przestrzeni z samochodami. Dokumentacja SUMO wskazuje, że modelowanie rowerów jest nadal rozwijane i wykorzystuje dostosowane modele ruchu pojazdów; występują znane ograniczenia m.in. w odwzorowaniu ruchu dwukierunkowego na drogach rowerowych i specyfiki skrzyżowań. Nie należy zatem przyjmować SUMO bez testu reprezentatywnego scenariusza rowerowego.

**SimPy nie jest rekomendowany jako główny silnik wersji bazowej.** Jest biblioteką DES, przydatną dla kolejek i zdarzeń zasobów, ale sam nie dostarcza modelu wyboru trasy ani modelu ruchu rowerowego. Można go dodać, jeśli eksperymenty będą wymagały jawnego modelowania kolejek i zdarzeń o różnych czasach trwania.

### 7.3. Agenci

Każdy agent reprezentuje jedną syntetyczną podróż rowerową i ma co najmniej:

- `agent_id`,
- `origin_node`,
- `destination_node`,
- `departure_time`,
- `speed_profile` lub klasę prędkości,
- `route_choice_parameters`,
- `current_edge`,
- `travel_time`,
- `completed`.

W wersji bazowej nie przypisujemy agentom danych osobowych ani nie próbujemy odtwarzać konkretnych osób.

### 7.4. Reprezentacja sieci

Graf skierowany \(G=(V,E)\):
- węzły \(V\): skrzyżowania, końce odcinków i punkty połączeń;
- krawędzie \(E\): odcinki przejezdne rowerem;
- atrybuty krawędzi: długość, typ drogi, typ infrastruktury rowerowej, nawierzchnia, nachylenie (jeżeli dostępne), ograniczenia dostępu, źródło i jakość danych.

Krawędź nie może być uznana za przejezdną tylko dlatego, że występuje w OSM. Należy sprawdzić tagi dostępu i reguły sieciowe dla rowerów.

### 7.5. Wybór trasy

Wersja bazowa powinna porównać co najmniej dwa modele:

**Model A — najkrótszy / najszybszy koszt**
\[
C_r = \sum_{e \in r} t_e
\]

gdzie \(t_e\) jest szacowanym czasem przejazdu krawędzi.

**Model B — koszt uogólniony**
\[
C_r = \sum_{e \in r}
(\beta_t t_e + \beta_i I_e + \beta_s S_e + \beta_g G_e)
\]

gdzie:
- \(I_e\) — kara lub premia związana z typem infrastruktury;
- \(S_e\) — wskaźnik jakości / stresu / ekspozycji, tylko jeśli istnieje uzasadniona definicja danych;
- \(G_e\) — koszt nachylenia, jeśli dostępny jest wiarygodny NMT;
- \(\beta\) — wagi, które muszą być kalibrowane lub badane w analizie wrażliwości.

Aby reprezentować heterogeniczność i nie zakładać, że wszyscy wybierają identyczną trasę, można zastosować model losowego wyboru, np. logit:
\[
P(r \mid OD) = \frac{\exp(-\mu C_r)}{\sum_{k \in R_{OD}}\exp(-\mu C_k)}
\]
gdzie \(R_{OD}\) jest zbiorem rozważanych alternatywnych tras.

Wersja bazowa może najpierw używać najkrótszej ścieżki, a następnie rozszerzyć się o k-ścieżek i logit. Nie należy jednocześnie wprowadzać wielu niekalibrowanych wag.

### 7.6. Popyt OD

Liczniki obserwują przekroczenia punktów, nie pełne podróże. Macierz OD nie jest bezpośrednio dostępna w dostarczonych danych.

Dlatego należy:
1. zdefiniować ograniczoną liczbę stref źródłowych i docelowych lub par OD;
2. wygenerować realistyczne, lecz jawnie syntetyczne kandydackie trasy;
3. zbudować macierz przypisania licznik–trasa;
4. sprawdzić, czy obserwacje liczników pozwalają odróżnić przepływy OD;
5. estymować nieujemne przepływy tylko wtedy, gdy układ jest identyfikowalny i odpowiednio uwarunkowany;
6. w przeciwnym razie ograniczyć liczbę OD, dodać uzasadnione priory / dane pomocnicze albo raportować przedziały scenariuszy.

Dla liniowego przybliżenia:
\[
\mathbf{y} \approx A\mathbf{q}
\]
gdzie \(\mathbf{y}\) to obserwowane natężenia na licznikach, \(A\) opisuje, które trasy przekraczają dane liczniki, a \(\mathbf{q}\) jest wektorem nieujemnych przepływów OD.

Rozwiązanie NNLS nie gwarantuje identyfikowalności. Należy raportować rząd macierzy, liczbę niewiadomych, współliniowość i błąd dopasowania.

### 7.7. Czas i przepustowość

Wersja bazowa może używać kroku czasowego 1–5 minut lub harmonogramu wyjść agentów z czasem przejazdu wyznaczanym z długości i prędkości. Wybór kroku należy ustalić po testach.

Nie należy automatycznie wprowadzać kolejki na każdej krawędzi ani przypisywać jej arbitralnej przepustowości. Rzeczywiste przepustowości nie wynikają z dziennych liczników. Efekty przeciążenia powinny być osobnym rozszerzeniem, opartym na danych lub jawnych scenariuszach wrażliwości.

## 8. Eksperymenty

### E0 — audyt i przygotowanie danych

- kompletność i jakość liczników;
- identyfikacja wspólnego okresu;
- geolokalizacja liczników;
- spójność sieci i mapowanie do krawędzi;
- ocena identyfikowalności OD.

**Warunek przejścia:** raport danych, mapa liczników i sieci, lista nierozstrzygniętych problemów.

### E1 — model bazowy

- ruch na istniejącej sieci;
- syntetyczne OD;
- jeden prosty model wyboru trasy;
- porównanie przepływów z licznikami.

### E2 — porównanie reguł wyboru trasy

- minimalny czas / długość;
- koszt uogólniony z preferencją infrastruktury;
- analiza wpływu wag i losowości wyboru.

### E3 — scenariusze infrastrukturalne

- dodanie brakującego połączenia;
- zamknięcie odcinka;
- poprawa klasy infrastruktury;
- porównanie zmian przepływów i kosztu podróży.

### E4 — popyt i zmienność czasowa

- warianty natężenia;
- dni robocze i weekendy, jeśli profile są dostępne;
- profile godzinowe dla liczników z wiarygodnymi danymi;
- analiza wpływu rozkładu godzinowego na obciążenie sieci.

### E5 — analiza wrażliwości i niepewności

- wagi kosztu uogólnionego;
- prędkości;
- rozkład OD;
- niepewność i braki w danych;
- różne ziarna losowe.

## 9. Metryki i ocena

| Metryka | Definicja / zastosowanie |
|---|---|
| MAE | Średni bezwzględny błąd natężenia na licznikach |
| RMSE | Błąd silniej karzący duże odchylenia |
| WAPE | Suma błędów bezwzględnych względem sumy obserwacji; raportować ostrożnie przy małych mianownikach |
| Bias | Kierunek systematycznego przeszacowania / niedoszacowania |
| GEH | Pomocnicza miara zgodności przepływów, jeśli jednostki i okresy agregacji są zgodne |
| Travel time | Czas przejazdu syntetycznych podróży |
| Route length / detour | Długość trasy i współczynnik objazdu względem najkrótszej ścieżki |
| Edge flow | Przepływ przypisany do odcinka |
| Infrastructure share | Udział podróży korzystających z określonej klasy infrastruktury |

Nie należy raportować jednej zbiorczej wartości błędu bez pokazania błędów per licznik i per okres. Liczniki o bardzo różnych natężeniach mogą wymagać oddzielnych miar.

## 10. Kalibracja, walidacja i wiarygodność

- **Weryfikacja implementacji:** testy topologii, kierunków, jednostek, sum godzinowych, przejazdu po trasie i deterministyczności przy ustalonym seed.
- **Walidacja danych:** porównanie lokalizacji i kierunku licznika z geometrią sieci; kontrola zakresów i anomalii.
- **Kalibracja:** parametry popytu OD i ewentualnie preferencji tras dopasowywać wyłącznie do okresu kalibracyjnego.
- **Walidacja czasowa:** oddzielić okres kalibracji od późniejszego okresu testowego. Nie dzielić losowo pojedynczych dni, jeśli występuje silna sezonowość.
- **Walidacja przestrzenna:** jeśli liczba liczników pozwala, pozostawić część punktów poza kalibracją i ocenić, czy model odtwarza ich natężenie.
- **Analiza wrażliwości:** sprawdzić, czy wnioski scenariuszowe utrzymują się przy różnych wiarygodnych parametrach.
- **Niepewność:** raportować zakresy wyników z wielu powtórzeń / scenariuszy, a nie tylko pojedynczą realizację.

Jeśli dane nie pozwolą zidentyfikować OD, nie należy przedstawiać dopasowanego rozkładu jako jedynej prawdziwej macierzy podróży. Wyniki należy interpretować warunkowo względem przyjętych scenariuszy popytu.

## 11. Architektura oprogramowania

```text
.
├── README.md
├── pyproject.toml
├── configs/
│   ├── base.yaml
│   └── experiments/
├── data/
│   ├── raw/                 # oryginalne dane; bez edycji
│   ├── interim/             # dane pośrednie i raporty kontroli
│   └── processed/           # gotowe tabele i warstwy GIS
├── docs/
│   ├── state-of-the-art.md
│   ├── data-audit.md
│   ├── model-specification.md
│   └── decisions/
├── src/
│   └── cycling_sim/
│       ├── data/            # import, czyszczenie, walidacja
│       ├── network/         # OSM, graf, mapowanie liczników
│       ├── demand/          # strefy i macierz OD
│       ├── agents/          # agent i reguły wyboru trasy
│       ├── simulation/      # harmonogram i przebieg modelu
│       ├── experiments/     # konfiguracje i batch runs
│       └── analysis/        # metryki, statystyki, wykresy
├── tests/
├── reports/
│   ├── figures/
│   └── presentations/
└── results/                 # wyniki generowane; duże pliki poza Git
```

Struktura jest docelowa. Katalogi i moduły należy tworzyć wtedy, gdy są potrzebne — nie jako puste placeholdery.

## 12. Plan realizacji i kryteria ukończenia

- [ ] **Etap 0 — audyt danych:** kompletność, pochodzenie, licencje, profile, pogoda, rozbieżności liczników.
- [ ] **Etap 1 — obszar i sieć:** wybór obszaru, pobranie grafu, kontrola topologii, mapa liczników.
- [ ] **Etap 2 — spójny pipeline:** dane long, profile godzinowe, warstwy przestrzenne, metadane i testy.
- [ ] **Etap 3 — popyt OD:** definicja stref, macierz przypisania liczników do tras, test identyfikowalności.
- [ ] **Etap 4 — model bazowy:** agenci, sieć, generowanie podróży, zapis przepływów.
- [ ] **Etap 5 — wybór trasy:** porównanie reguł i kalibracja parametrów.
- [ ] **Etap 6 — walidacja:** okres testowy, metryki, analiza błędów i wrażliwości.
- [ ] **Etap 7 — scenariusze:** zmiany infrastruktury i porównanie wyników.
- [ ] **Etap 8 — raport:** wyniki, ograniczenia, powtarzalność i prezentacja.

### Minimalne kryteria ukończenia projektu

1. Reprodukowalny pipeline od danych raw do processed.
2. Udokumentowany wybór obszaru i lista użytych liczników.
3. Mapa grafu i punktów pomiarowych z kontrolą dopasowania.
4. Działający model bazowy z co najmniej dwoma regułami wyboru trasy.
5. Raport kalibracji i walidacji na danych odłożonych.
6. Co najmniej dwa scenariusze zmian infrastruktury.
7. Analiza wrażliwości i jawny opis ograniczeń OD.

## 13. Ograniczenia i ryzyka

| Ryzyko | Konsekwencja | Sposób ograniczenia |
|---|---|---|
| Brak danych OD | Nie można bezpośrednio odtworzyć pełnych podróży | Syntetyczne OD, identyfikowalność, scenariusze i ostrożna interpretacja |
| Liczniki w różnych miejscach i okresach | Niespójne porównania | Wspólny okres, raport kompletności, walidacja per licznik |
| Nieznany kierunek liczenia | Błędne mapowanie przepływu do skierowanego grafu | Dokumentacja lokalizacji i ręczna weryfikacja |
| Niedokładne tagi OSM | Błędna dostępność i klasyfikacja infrastruktury | Weryfikacja miejskimi warstwami GIS i kontrola ręczna |
| Brak danych o preferencjach | Niepewne wagi kosztu | Analiza wrażliwości; nie przedstawiać wag jako empirycznie oszacowanych |
| Brak przepustowości | Brak podstaw do prognozy kolejek | Nie modelować ich w bazie; rozszerzać tylko na podstawie danych / scenariuszy |
| Profil godzinowy jednego licznika | Ryzyko błędnego przeniesienia wzorca | Pobierać profile osobno lub jasno oznaczyć uproszczenie |
| Zmiany infrastruktury w czasie | Sieć może nie odpowiadać historycznym pomiarom | Ustalić datę referencyjną sieci i zakres analizy; oznaczyć niezgodność czasową |

## 14. Zespół i status

Projekt jest realizowany etapowo. Pierwszym rezultatem ma być audyt danych i decyzja o obszarze, a nie rozbudowany interfejs ani pełny symulator.

**Aktualny status:** koncepcja modelu i wstępny audyt dwóch plików licznikowych. Wybór obszaru, silnika po teście porównawczym, model OD i parametry zachowania agentów wymagają zatwierdzenia na podstawie audytu danych.

## 15. Literatura i dokumentacja

Pełny przegląd literatury oraz uzasadnienie wyboru metod znajdują się w [`docs/state-of-the-art.md`](docs/state-of-the-art.md).
