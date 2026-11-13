# Specyfikacja projektu: symulacja ruchu rowerowego w Krakowie

> **Status:** specyfikacja koncepcyjna do uzupełnienia po audycie danych. Nie opisuje
> zwalidowanego modelu predykcyjnego. Nierozstrzygnięte kwestie są oznaczone jako
> **[DO UZUPEŁNIENIA — pytanie]**.

## 1. Cel dokumentu

Dokument określa cel, zakres, wymagania dotyczące danych i modelu oraz kryteria
oceny projektu symulacji przepływów rowerowych w wybranym obszarze Krakowa.
Stanowi podstawę implementacji i raportu końcowego. Uzasadnienie metod i szerszy
przegląd literatury znajdują się w [state-of-the-art.md](state-of-the-art.md);
opis koncepcji, dostępnych danych i planu projektu — w [README.md](README.md).

## 2. Cel i problem badawczy

### 2.1. Cel główny

Opracować powtarzalny, przestrzenny model sieciowy, który pozwala analizować
rozkład syntetycznych podróży rowerowych w wybranym obszarze Krakowa oraz
porównywać przepływy w sieci w scenariuszach zmian infrastruktury.

### 2.2. Problem

Dostępne liczniki rejestrują przekroczenia punktów pomiarowych, a nie kompletne
trasy ani pary źródło–cel (OD). Nie można zatem bezpośrednio odczytać z nich
macierzy OD ani liczby unikalnych podróży w całym obszarze. Ponadto wybór trasy
może zależeć od cech innych niż długość, zaś jakość i kompletność danych
przestrzennych oraz licznikowych wymagają weryfikacji.

Model ma jawnie reprezentować te ograniczenia. Jeśli popytu OD nie da się
zidentyfikować, wyniki scenariuszy należy interpretować warunkowo względem
przyjętych założeń, a nie jako rekonstrukcję rzeczywistych podróży lub
bezwarunkową prognozę.

### 2.3. Pytania badawcze

- **RQ1:** W jakim stopniu model odtwarza natężenie zaobserwowane na licznikach
  w wybranym obszarze i okresie?
- **RQ2:** Jak zmienia się rozkład przepływów przy wyborze trasy według czasu
  lub długości w porównaniu z kosztem uwzględniającym jakość infrastruktury?
- **RQ3:** Jak dodanie, zamknięcie lub zmiana parametrów odcinka wpływa na
  przepływy i koszt podróży?
- **RQ4:** Jak wrażliwe są wyniki na nieznany popyt OD, parametry trasowania
  oraz niekompletność danych?
- **RQ5:** Czy uwzględnienie zmienności dobowej poprawia zgodność symulacji
  z profilami liczników, dla których profile są dostępne?

## 3. Zakres

### 3.1. Wersja bazowa obejmuje

- jeden ograniczony, uzasadniony danymi obszar Krakowa;
- skierowany graf odcinków dopuszczonych do ruchu rowerowego;
- syntetyczne podróże OD, bez przypisywania ich rzeczywistym osobom;
- co najmniej dwa warianty kosztu wyboru trasy;
- przepływy zagregowane na odcinkach i w lokalizacjach liczników;
- porównanie wyników z pomiarami oraz jawne raportowanie niepewności;
- eksperymenty scenariuszowe dotyczące zmian infrastruktury.

### 3.2. Poza zakresem wersji bazowej

- odtwarzanie rzeczywistych, indywidualnych tras mieszkańców;
- prognozowanie całkowitego popytu rowerowego dla całego Krakowa;
- mikrosymulacja interakcji rowerów, samochodów i pieszych;
- modelowanie rzeczywistych cykli sygnalizacji świetlnej;
- wiarygodne modelowanie kolejek lub przepustowości bez odpowiednich danych;
- wnioskowanie przyczynowe wyłącznie na podstawie korelacji licznikowych.

Ruch rowerów elektrycznych może być rozszerzeniem, ale nie należy go łączyć
z bazową populacją bez jawnego uzasadnienia i parametrów.

## 4. Wymagania funkcjonalne

| ID | Wymaganie |
|---|---|
| F-01 | Zaimportować dzienne dane licznikowe i zachować oryginalne pliki bez ręcznej edycji. |
| F-02 | Odróżniać brak pomiaru od prawidłowej wartości zerowej. |
| F-03 | Wytworzyć raport jakości dla każdego licznika: zakres dat, obserwacje, braki, zera i podejrzane serie. |
| F-04 | Zbudować i sprawdzić topologicznie spójny skierowany graf przejezdny dla rowerów. |
| F-05 | Powiązać liczniki z krawędziami na podstawie lokalizacji i dostępnych informacji o kierunku; nie opierać dopasowania wyłącznie na najbliższej geometrii. |
| F-06 | Generować syntetyczne podróże OD i przypisywać je do tras w grafie. |
| F-07 | Obliczać co najmniej wariant najkrótszego/najszybszego kosztu i wariant kosztu uogólnionego. |
| F-08 | Agregować symulowane przepływy na krawędziach i licznikach w jednostkach zgodnych z obserwacjami. |
| F-09 | Porównywać obserwacje i symulacje, raportując metryki oraz błędy per licznik i okres. |
| F-10 | Uruchamiać scenariusze zmian infrastruktury względem wariantu bazowego. |
| F-11 | Umożliwiać powtarzalne uruchomienia poprzez jawne konfiguracje i ziarna losowe. |
| F-12 | Zapisywać metadane pochodzenia, licencji, daty pobrania, CRS, zakresu dat i wersji pipeline dla użytych danych. |

## 5. Dane wejściowe

### 5.1. Dane dostępne według README

| Zbiór | Wykorzystanie | Ograniczenia i wymagane kontrole |
|---|---|---|
| `Liczniki - dzienne.csv` | Sezonowość, natężenia, kalibracja i walidacja punktowa | 20 kolumn liczników; zakres całego pliku 18.11.2016–31.10.2026; braki nie są zerami; pochodzenie części kolumn i rozbieżność z publicznym opisem liczników wymagają wyjaśnienia. |
| `rowerowy-otwarty-plan_profil-dobowy_wielicka_month-2026-10.csv` | Względny profil godzinowy dla licznika Wielicka | Dotyczy jednego licznika i miesiąca; typowy profil jest statystyką historyczną, a nie surowym pomiarem konkretnego dnia. |
| Zrzut ekranu licznika Wielicka | Pomocnicza kontrola orientacyjna | Migawka, nie szereg czasowy; nie jest samodzielnym źródłem kalibracji. |

README podaje wstępne wyniki audytu tych danych. W implementacji należy
ponownie wyliczyć statystyki z oryginalnych plików i zapisać raport, zamiast
traktować wstępne sumy lub anomalie jako zweryfikowane fakty.

### 5.2. Źródła do pozyskania

- **OpenStreetMap:** geometria, topologia, kierunki i tagi dostępności
  rowerowej.
- **ZTP / MSIP Kraków / Otwarte Dane Krakowa:** miejska infrastruktura
  rowerowa oraz pomoc w weryfikacji przebiegu i typów infrastruktury.
- **ZTP / Otwarty Plan:** lokalizacje, charakterystyka i ewentualne profile
  liczników.
- **GUGiK / NMT:** opcjonalne dane wysokościowe do wyznaczania nachylenia.
- **IMGW:** opcjonalna pogoda historyczna, po sprawdzeniu pokrycia.
- **BDL GUS / MSIP:** opcjonalne dane ludności lub zagospodarowania do
  uzasadnienia źródeł i celów popytu.

Pozyskanie dodatkowych danych zależy od dostępności, licencji i przydatności
dla wybranego obszaru. Dane o ludności, pogodzie, GPS lub ankietach nie są
warunkiem bazowym, dopóki zespół ich nie zatwierdzi.

### 5.3. Reguły przygotowania

- Zachować dane źródłowe w postaci niezmienionej; oddzielić `raw`, `interim`
  i `processed`.
- Parsować daty i wartości licznikowe jawnie, z uwzględnieniem formatu pliku.
- Braków nie uzupełniać zerami. Podejrzane zera i awarie oznaczać do kontroli.
- Tworzyć tabelę licznikową w formacie long, co najmniej z polami
  `date`, `sensor_id`, `count` i `quality_flag`.
- Ustalać wspólny okres analityczny po raporcie kompletności, nie z góry.
- Zachowywać skierowanie grafu, ograniczenia rowerowe i identyfikatory źródłowe.
- Przeliczać odległości w odpowiednim układzie metrycznym; deklarować CRS
  wyjściowych warstw.
- Nie przenosić profilu godzinowego jednego licznika na inne lokalizacje bez
  jawnego uzasadnienia.
- Jeśli dzienny pomiar \(N_d\) jest rozdzielany profilem godzinowym \(p_h\),
  zachować \(\sum_h \hat{N}_{d,h}=N_d\), np. metodą największych reszt po
  zaokrągleniu.

## 6. Model

### 6.1. Typ i architektura

Model bazowy to sieciowy, przestrzenny ABM na poziomie mezo. Agent oznacza
syntetyczną podróż rowerową, a nie osobę poruszającą się w fizycznej
mikrosymulacji. Model nie odwzorowuje w wersji bazowej konfliktów, kolejek ani
przepustowości.

Rekomendowany stos:

- **OSMnx:** pozyskanie i przygotowanie sieci OSM;
- **NetworkX:** graf i algorytmy trasowania;
- **Mesa:** zarządzanie agentami i przebiegami ABM;
- **Pandas / GeoPandas / NumPy:** dane tabelaryczne, przestrzenne i obliczenia;
- **SciPy:** ewentualna estymacja nieujemnych przepływów (NNLS) i optymalizacja;
- **Matplotlib / Folium:** wykresy i mapy.

Mesa nie dostarcza gotowego modelu transportu rowerowego: reguły ruchu,
trasowania, popyt i walidację trzeba zdefiniować w projekcie. SUMO jest
alternatywą do rozważenia, jeśli zakres obejmie interakcje i skrzyżowania;
SimPy nie jest silnikiem bazowym, bo sam nie zapewnia transportowego modelu
sieciowego ani reguł wyboru trasy.

### 6.2. Sieć

Graf skierowany \(G=(V,E)\) reprezentuje połączenia dostępne rowerem.

- Węzły oznaczają skrzyżowania, końce odcinków i punkty połączeń.
- Krawędzie oznaczają odcinki przejezdne rowerem w danym kierunku.
- Atrybuty mogą obejmować długość, typ drogi i infrastruktury, nawierzchnię,
  nachylenie, ograniczenia dostępu, źródło i jakość danych.
- Niepełne tagi OSM należy w miarę możliwości weryfikować danymi miejskimi
  i kontrolą wizualną.
- Krawędzi nie uznaje się za rowerową wyłącznie na podstawie obecności
  w OSM; należy sprawdzić dostęp i połączenia topologiczne.

Jednostki wewnętrzne: długość w metrach, prędkość w m/s, czas w sekundach,
natężenie jako liczba rowerów na jawnie określony przedział czasu. Koszt
uogólniony musi mieć udokumentowaną definicję i jednostkę lub być oznaczony
jako bezwymiarowy.

### 6.3. Agenci

Każdy agent reprezentuje jedną syntetyczną podróż i powinien zawierać co
najmniej:

- identyfikator;
- węzeł źródłowy i docelowy;
- czas wyjazdu;
- prędkość lub klasę prędkości;
- parametry wyboru trasy;
- stan aktualnej krawędzi/trasy, czas podróży i informację o zakończeniu.

Nie przechowuje się ani nie symuluje danych osobowych.

### 6.4. Popyt OD

Macierz OD nie jest bezpośrednio dostępna z liczników. Proponowana procedura:

1. Zdefiniować ograniczoną liczbę stref lub par OD.
2. Wygenerować kandydackie trasy między nimi.
3. Zbudować macierz przypisania \(A\), łączącą trasy z licznikami, oraz
   wektor obserwacji \(\mathbf{y}\).
4. Ocenić identyfikowalność: raportować liczbę obserwacji i niewiadomych,
   rząd macierzy, współliniowość/uwarunkowanie oraz błąd dopasowania.
5. Estymować nieujemne przepływy \(\mathbf{q}\) (np. NNLS) tylko z jawnym
   opisem ograniczeń; NNLS samo w sobie nie zapewnia identyfikowalności.
6. Gdy OD nie jest identyfikowalne, ograniczyć liczbę stref, uzasadnić dane
   pomocnicze lub przedstawić zestaw scenariuszy popytu.

Przybliżenie \(\mathbf{y}\approx A\mathbf{q}\) nie uprawnia do przedstawiania
jednego dopasowania jako jedynej prawdziwej macierzy podróży.

### 6.5. Koszt i wybór trasy

Wymagane są co najmniej dwa porównywalne warianty:

1. **Czas/długość:** koszt ścieżki to suma szacowanego czasu krawędzi
   (albo długości, jeśli taki wariant zostanie jawnie wybrany).
2. **Koszt uogólniony:** koszt może uwzględniać czas, infrastrukturę oraz
   nachylenie lub wskaźnik jakości/stresu, ale wyłącznie wtedy, gdy ich
   definicja i źródło są jawne.

Przykładowo:

\[
C_r=\sum_{e\in r}(\beta_t t_e+\beta_i I_e+\beta_s S_e+\beta_g G_e)
\]

Wagi nie są znane a priori; należy je kalibrować z odpowiednich danych albo
analizować scenariuszowo. Nie należy określać wskaźnika jako obiektywnego
bezpieczeństwa bez podstaw empirycznych. Probabilistyczny wybór (np. logit
na alternatywnych trasach) może być rozszerzeniem; wymaga określenia zbioru
tras i parametru skali.

### 6.6. Czas i przepustowość

Ruch czasowy może być realizowany dyskretnym krokiem lub przez harmonogram
wyjazdów i czasów przejazdu. Dziennych liczników nie należy interpretować jako
danych o przepustowości. Kolejki i przeciążenia nie należą do modelu bazowego,
chyba że zostaną poparte danymi lub wyraźnie oznaczone jako scenariusz.

## 7. Scenariusze i analiza

Minimalny plan eksperymentów:

- **E0 — audyt:** kompletność danych, lokalizacje i kierunki liczników,
  topologia sieci, mapowanie do krawędzi i identyfikowalność OD.
- **E1 — model bazowy:** istniejąca sieć, syntetyczny popyt i bazowa reguła
  trasowania.
- **E2 — reguły trasowania:** porównanie czasu/długości z kosztem
  uogólnionym oraz wrażliwość na jego parametry.
- **E3 — infrastruktura:** co najmniej dwa scenariusze, np. dodanie,
  zamknięcie lub poprawa odcinka.
- **E4 — zmienność czasowa:** profile godzinowe, dni robocze/weekendy
  i warianty popytu, o ile dane na to pozwalają.
- **E5 — niepewność:** popyt OD, prędkości, parametry trasowania, jakość
  danych i ziarna losowe.

Obszar i okres analityczny należy wybrać na podstawie audytu, a nie wyłącznie
atrakcyjności kartograficznej. Kandydat powinien mieć kilka wiarygodnych
liczników o wspólnym okresie, możliwe do mapowania lokalizacje, alternatywne
połączenia oraz sensownie obsłużone granice modelu.

## 8. Weryfikacja, kalibracja i walidacja

### 8.1. Weryfikacja implementacji

Testować co najmniej, że:

- krawędzie mają dodatnią długość, a trasy łączą źródło z celem;
- agent korzysta wyłącznie z dozwolonych krawędzi;
- czas przejazdu jest dodatni;
- ustalone ziarno daje powtarzalny wynik;
- rozdzielenie dziennego ruchu na godziny zachowuje sumę;
- modyfikacja infrastruktury zmienia zamierzone elementy grafu;
- przepływ przez licznik jest liczony zgodnie z przyjętą definicją
  przekroczenia i nie jest przypadkowo podwajany.

### 8.2. Kalibracja i walidacja

- Kalibrację wykonywać wyłącznie na wskazanym okresie/punktach.
- Walidację czasową prowadzić na odłożonym okresie, uwzględniając sezonowość.
- Walidację przestrzenną stosować, jeśli liczba i rozmieszczenie liczników
  na to pozwalają.
- Raportować błędy osobno dla liczników i okresów, nie tylko jedną średnią.
- Jeśli popyt OD nie jest identyfikowalny, opisywać wyniki jako warunkowe.
- Analizować, czy wnioski scenariuszowe utrzymują się przy wiarygodnych
  założeniach i wielu powtórzeniach.

### 8.3. Metryki

- **MAE** — średni błąd bezwzględny;
- **RMSE** — pierwiastek z błędu średniokwadratowego;
- **WAPE** — błąd ważony natężeniem, z komentarzem przy małym mianowniku;
- **bias** — systematyczne przeszacowanie/niedoszacowanie;
- **GEH** — pomocniczo, tylko przy zgodnych jednostkach i agregacji;
- dodatkowo: przepływ na krawędzi, czas i długość podróży, objazd oraz udział
  tras korzystających z klas infrastruktury.

## 9. Kryteria ukończenia

Projekt można uznać za ukończony, gdy:

1. Istnieje powtarzalny pipeline od danych surowych do przetworzonych wraz
   z raportem jakości i metadanymi.
2. Udokumentowano wybór obszaru, okresu i liczników oraz mapę ich dopasowania
   do grafu.
3. Graf jest skierowany, topologicznie sprawdzony i uwzględnia dostępność
   rowerową w zakresie możliwym do zweryfikowania.
4. Działa model syntetycznych podróży i co najmniej dwa warianty trasowania.
5. Raport kalibracji/walidacji zawiera metryki per licznik i okres oraz
   wyraźnie opisuje ograniczenia identyfikacji OD.
6. Przeprowadzono co najmniej dwa scenariusze infrastrukturalne i analizę
   wrażliwości.
7. Opisano założenia, ograniczenia, reprodukowalność i interpretację wyników;
   dokumentację modelu można uzupełnić protokołem ODD.

## 10. Pytania do uzupełnienia

Poniższe decyzje nie są jednoznacznie ustalone w materiałach. Należy je
rozstrzygnąć i odnotować przed lub w trakcie etapu, którego dotyczą.

| ID | Status | Pytanie |
|---|---|---|
| Q-01 | **[DO UZUPEŁNIENIA]** | Jaki dokładnie obszar Krakowa obejmie model? Czy roboczy obszar centrum–Grzegórzki zostaje przyjęty po audycie liczników i grafu? |
| Q-02 | **[DO UZUPEŁNIENIA]** | Które liczniki zostaną użyte do kalibracji, które do walidacji, a które odrzucone? Jaki wspólny okres obserwacji przyjmujemy? |
| Q-03 | **[DO UZUPEŁNIENIA]** | Jak wyjaśnimy rozbieżność między 20 kolumnami w CSV a opisem 19 liczników indukcyjnych i 4 czujników Telraam, w tym pochodzenie kolumny `Jancarza`? |
| Q-04 | **[DO UZUPEŁNIENIA]** | Czy dla wybranych liczników znamy dokładną lokalizację, kierunek pomiaru, agregację kierunków i sposób liczenia przekroczeń? |
| Q-05 | **[DO UZUPEŁNIENIA]** | Czy pozyskamy profile godzinowe dla liczników poza Wielicką? Jeśli nie, czy analiza czasowa zostanie ograniczona do tej lokalizacji, czy użyje jawnych scenariuszy? |
| Q-06 | **[DO UZUPEŁNIENIA]** | Jakie strefy źródłowe/docelowe lub pary OD i jaka metoda ich wyznaczania będą użyte? Jakie dane uzasadnią rozmieszczenie popytu? |
| Q-07 | **[DO UZUPEŁNIENIA]** | Jaki jest próg akceptacji identyfikowalności i dopasowania OD? Co dokładnie zespół zrobi, jeśli macierz przypisania nie pozwoli odróżnić przepływów? |
| Q-08 | **[DO UZUPEŁNIENIA]** | Czy podstawowym kosztem odniesienia będzie czas, długość, czy oba warianty? Jakie prędkości lub klasy prędkości przyjmujemy i na jakiej podstawie? |
| Q-09 | **[DO UZUPEŁNIENIA]** | Jak zdefiniujemy jakość infrastruktury, wskaźnik stresu/ekspozycji i koszt nachylenia? Które z tych atrybutów są dostępne i wiarygodne dla obszaru? |
| Q-10 | **[DO UZUPEŁNIENIA]** | Jakie wagi kosztu uogólnionego i rozkład ich niepewności będą kalibrowane lub testowane? Czy logit i alternatywne trasy wchodzą do wersji bazowej, czy są rozszerzeniem? |
| Q-11 | **[DO UZUPEŁNIENIA]** | Czy symulacja będzie używać stałego kroku czasowego (jaki?) czy harmonogramu wyjazdów z czasami przejazdu? Jak uzasadnimy tę decyzję? |
| Q-12 | **[DO UZUPEŁNIENIA]** | Jaka będzie data referencyjna sieci OSM i infrastruktury miejskiej oraz jak obsłużymy różnicę między datą sieci a okresem liczników? |
| Q-13 | **[DO UZUPEŁNIENIA]** | Czy nachylenie, pogoda, ludność/zagospodarowanie lub dodatkowe dane GPS/ankietowe zostaną pozyskane? Kto sprawdzi ich licencje i pokrycie? |
| Q-14 | **[DO UZUPEŁNIENIA]** | Jakie konkretne progi jakości danych, kryteria przyjęcia licznika i wartości akceptowalnych metryk walidacji uznamy za wystarczające? |
| Q-15 | **[DO UZUPEŁNIENIA]** | Jakie dwa lub więcej scenariuszy infrastrukturalnych zostaną ocenione i kto zatwierdzi ich realistyczność? |
| Q-16 | **[DO UZUPEŁNIENIA]** | Jaki jest docelowy format konfiguracji, wyników i raportów, wymagane wersje Pythona/bibliotek oraz sposób uruchamiania projektu? |

## 11. Odniesienia

- [README.md](README.md) — koncepcja projektu, wstępny audyt danych,
  architektura i plan realizacji.
- [state-of-the-art.md](state-of-the-art.md) — przegląd metod, narzędzi,
  danych i uzasadnienie wyboru modelu.
- Źródła danych lokalnych i dokumentacja narzędzi są wymienione w obu
  powyższych dokumentach. Szczegółowe cytowania naukowe pozostają w
  `state-of-the-art.md`.