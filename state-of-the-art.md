# State of the art: modelowanie ruchu rowerowego w sieciach miejskich

**Przegląd metod, narzędzi, danych i podstaw metodologicznych dla projektu symulacji ruchu rowerowego w Krakowie**

> Dokument stanowi przegląd ukierunkowany na decyzje projektowe, a nie katalog wszystkich publikacji o transporcie rowerowym. Rozróżnia: (1) modele popytu i wyboru trasy, (2) modele agentowe, (3) mikrosymulatory ruchu, (4) dane i metody kalibracji. Wnioski odnoszą się do ograniczeń danych dostępnych dla zespołu.

## 1. Cel przeglądu i kryteria wyboru podejścia

Projekt ma analizować rozkład ruchu rowerowego na miejskiej sieci, porównywać reguły wyboru tras i oceniać scenariusze zmian infrastruktury. Kluczowym ograniczeniem empirycznym jest dostępność pomiarów punktowych z liczników, bez bezpośrednich danych o pełnych trasach OD.

Z tego powodu przegląd koncentruje się na pięciu pytaniach:

1. Jak reprezentować sieć rowerową i ograniczenia przejazdu?
2. Jak modelować wybór trasy, skoro rowerzyści nie zawsze wybierają najkrótszą drogę?
3. Jak odtworzyć popyt OD z danych licznikowych, które nie obserwują kompletnych podróży?
4. Jaki silnik jest adekwatny do wymaganej skali szczegółowości?
5. Jak zweryfikować model, aby wyniki scenariuszy miały naukowo uzasadnioną interpretację?

Kryteria porównania narzędzi:
- jawna obsługa ruchu rowerowego;
- możliwość pracy na sieci OSM i danych GIS;
- kontrola nad zachowaniem agentów i regułami wyboru trasy;
- integracja z licznikami i własnym pipeline danych;
- koszt implementacji i krzywa uczenia;
- możliwość kalibracji i walidacji;
- ograniczenia modelu rowerowego udokumentowane przez autorów.

## 2. Modele ruchu rowerowego: poziomy abstrakcji

### 2.1. Modele makroskopowe i transportowe

Modele transportowe opisują popyt i przepływy pomiędzy strefami, zwykle w postaci macierzy OD, przypisania podróży do sieci oraz kosztów podróży. Są przydatne do analiz planistycznych i scenariuszy infrastrukturalnych. Ich słabszą stroną w kontekście tego projektu jest konieczność posiadania lub estymacji popytu OD i odpowiednich parametrów wyboru trasy.

**Development of a large-scale transport model with focus on cycling** (2020), *Transportation Research Part A*, DOI: https://doi.org/10.1016/j.tra.2020.02.010

Praca opisuje rozwój modelu transportowego z naciskiem na ruch rowerowy: szczegółową sieć rowerową, alternatywne modele kosztu uogólnionego, mniejsze strefy transportowe i uwzględnienie roweru jako środka dojazdu do transportu publicznego.

**Znaczenie dla projektu:**
- sieć rowerowa powinna być odrębną, szczegółową reprezentacją, a nie tylko filtrem na sieci samochodowej;
- rozmiar stref OD wpływa na reprezentację krótkich podróży;
- wybór trasy powinien uwzględniać więcej niż odległość;
- model scenariuszowy wymaga jawnego opisu popytu.

Źródło: https://www.sciencedirect.com/science/article/abs/pii/S096585641930374X

### 2.2. Modele agentowe ruchu rowerowego

ABM reprezentuje podróże jako indywidualnych agentów, którym można przypisać cechy, cele, preferencje i reguły decyzyjne. Dzięki temu można badać heterogeniczność wyborów oraz powstawanie zagregowanych przepływów.

**Simulating Spatio-Temporal Patterns of Bicycle Flows with an Agent-Based Model** (2021), *ISPRS International Journal of Geo-Information*, 10(2), 88.

Praca opisuje agentowy model przepływów rowerowych, wykorzystujący przestrzenną sieć dróg, agenty, rozkład populacji i liczniki do weryfikacji oraz walidacji. W modelu uwzględniono topologiczną poprawność sieci, połączenia jedno- i dwukierunkowe oraz ograniczenia. Sieć jest ważona m.in. wskaźnikiem bezpieczeństwa.

**Znaczenie dla projektu:**
- agentowa reprezentacja podróży jest adekwatna do badania rozkładu tras;
- liczniki mogą służyć do walidacji zagregowanych przepływów;
- poprawność topologiczna grafu jest warunkiem koniecznym;
- lokalizacja źródeł popytu ma znaczenie dla wyników.

Źródło: https://www.mdpi.com/2220-9964/10/2/88

### 2.3. Wnioski z porównania poziomów

| Podejście | Co reprezentuje | Zalety | Ograniczenia dla projektu |
|---|---|---|---|
| Model makroskopowy / OD | Zagregowany popyt między strefami | Dobre do planowania i scenariuszy sieciowych | Wymaga macierzy OD i kalibracji |
| ABM sieciowy | Indywidualne syntetyczne podróże na grafie | Elastyczne reguły zachowania i heterogeniczność | Zachowania i popyt mogą być słabo identyfikowalne |
| Mikrosymulacja ruchu | Ruch jednostek w czasie, interakcje i konflikty | Kolejki, skrzyżowania, dynamika ruchu | Większa złożoność i potrzeba szczegółowej kalibracji |
| Model trasowania | Koszt i wybór ścieżki w sieci | Prosty, interpretowalny baseline | Sam nie generuje realistycznego popytu ani interakcji |

**Wniosek:** dla projektu semestralnego najlepszym punktem startowym jest sieciowy ABM na poziomie mezo, z syntetycznym OD i jawną kalibracją do liczników. Nie należy deklarować pełnej mikrosymulacji ruchu, jeśli nie modelujemy rzeczywistych interakcji na skrzyżowaniach i odcinkach.

## 3. Wybór trasy rowerzysty

### 3.1. Dlaczego najkrótsza ścieżka nie wystarcza?

Rowerzyści mogą uwzględniać:
- czas przejazdu;
- długość trasy;
- obecność wydzielonej infrastruktury;
- natężenie i prędkość ruchu samochodowego;
- bezpieczeństwo i subiektywny stres;
- nawierzchnię;
- nachylenie;
- liczbę skrzyżowań i zatrzymań;
- otoczenie trasy.

Nie wszystkie te cechy będą dostępne w danych krakowskich. Należy odróżniać atrybuty mierzalne od zastępczych wskaźników oraz od założeń.

### 3.2. Przegląd badań nad wyborem tras

**Łukawska (2024), Quantitative modelling of cyclists’ route choice behaviour on utilitarian trips based on GPS data: associated factors and behavioural implications**, *Transport Reviews*, 44(5), DOI: https://doi.org/10.1080/01441647.2024.2355468.

Przegląd 33 badań wykorzystujących GPS i metody statystyczne. Czynniki wyboru trasy podzielono na sieciowe, kontekstowe i indywidualne. Wyniki wskazują m.in. na znaczenie infrastruktury rowerowej i nachylenia, ale część zależności jest niejednoznaczna i zależna od lokalnego kontekstu.

**Wniosek:** nie należy przyjmować uniwersalnych wag preferencji bez kalibracji lokalnej. W projekcie wagi będą parametrami do analizy wrażliwości, chyba że pojawią się dane GPS lub inne źródło pozwalające je oszacować.

Źródło: https://www.tandfonline.com/doi/abs/10.1080/01441647.2024.2355468

**Ehrgott et al. (2012), A bi-objective cyclist route choice model**, *Transportation Research Part A*, 46(4), 652–663, DOI: https://doi.org/10.1016/j.tra.2011.11.015.

Praca podkreśla wielokryterialny charakter wyboru trasy rowerowej: rowerzyści mogą równoważyć czas przejazdu i przydatność / atrakcyjność trasy, obejmującą m.in. bezpieczeństwo, natężenie ruchu, infrastrukturę i ukształtowanie terenu.

**Wniosek:** sensowne jest porównanie modelu minimalizującego czas z modelem kosztu uogólnionego, zamiast zakładania jednego uniwersalnego kryterium.

Źródło: https://www.sciencedirect.com/science/article/pii/S0965856411001844

**Road infrastructures, spatial surroundings, and the demand and route choices for cycling: Evidence from a GPS-based mode detection study from Oslo, Norway** (2023).

Analiza 25 915 podróży GPS wykazała, że trasy rowerowe mogą istotnie odbiegać od najkrótszych ścieżek; w badaniu średnio były o 59% dłuższe. Znaczenie miały m.in. infrastruktura rowerowa, płaskość trasy, otoczenie i zakłócenia na skrzyżowaniach.

**Wniosek:** najkrótsza ścieżka jest użytecznym baseline'em, ale nie powinna być przedstawiana jako realistyczny model zachowania rowerzystów.

Źródło: https://journals.sagepub.com/doi/10.1177/23998083221141431

### 3.3. Rekomendowane modele trasowania

**Baseline A — shortest / fastest path**

Koszt trasy:
\[
C_r = \sum_{e \in r} t_e
\]

Czas krawędzi można przybliżyć jako długość / założona prędkość. Ten model jest łatwy do implementacji i stanowi punkt odniesienia.

**Model B — generalized cost**

\[
C_r = \sum_{e \in r}(\beta_t t_e+\beta_i I_e+\beta_s S_e+\beta_g G_e)
\]

Wagi \(\beta\) nie są znane a priori. Powinny być estymowane z danych tras lub badane scenariuszowo. Jeżeli brak wiarygodnego wskaźnika bezpieczeństwa, nie należy udawać, że `S_e` jest obiektywną miarą bezpieczeństwa.

**Model C — probabilistyczny wybór trasy (logit)**

\[
P(r \mid OD)=\frac{\exp(-\mu C_r)}{\sum_{k\in R_{OD}}\exp(-\mu C_k)}
\]

Model logit pozwala reprezentować różnorodność decyzji agentów i nie wymaga, by wszyscy wybierali identyczną trasę. Wymaga jednak zestawu alternatywnych tras i parametru skali \(\mu\). Dla projektu można go wprowadzić po uruchomieniu dwóch pierwszych wariantów.

## 4. Macierz OD i kalibracja z liczników

### 4.1. Fundamentalne ograniczenie danych

Licznik rowerowy rejestruje przekroczenia określonego przekroju sieci. Nie rejestruje automatycznie:
- miejsca rozpoczęcia podróży;
- celu podróży;
- całej trasy;
- tożsamości rowerzysty;
- informacji, czy ta sama osoba została policzona przez kolejny licznik.

Zatem suma wskazań wielu liczników nie jest liczbą unikalnych podróży. Liczniki nie dostarczają bezpośrednio macierzy OD.

### 4.2. Podejście do estymacji

Dla ograniczonego obszaru można:
1. zdefiniować strefy źródłowe i docelowe;
2. wygenerować kandydackie trasy między strefami;
3. zbudować macierz przypisania \(A\), gdzie element informuje, czy trasa przechodzi przez dany licznik;
4. dopasować przepływy nieujemne do pomiarów.

\[
\mathbf{y}\approx A\mathbf{q}
\]

\(\mathbf{y}\) — obserwacje liczników, \(A\) — macierz licznik–trasa, \(\mathbf{q}\) — nieznane przepływy OD.

Można rozważyć NNLS (non-negative least squares), ale samo zastosowanie NNLS nie rozwiązuje problemu identyfikowalności. Jeżeli kolumny \(A\) są podobne lub liczba niezależnych pomiarów jest zbyt mała, istnieje wiele rozwiązań dających podobne dopasowanie.

Należy raportować:
- wymiar macierzy;
- rząd macierzy;
- liczbę niewiadomych i obserwacji;
- kondycję / współliniowość;
- błąd dopasowania;
- zależność wyniku od założeń i regularizacji.

Jeżeli OD nie jest identyfikowalne, należy ograniczyć liczbę stref, dodać niezależne dane (np. GPS, ankiety, dane planistyczne) lub raportować zestaw scenariuszy popytu zamiast jednej „oszacowanej prawdy”.

### 4.3. Znaczenie dla projektu

To najważniejsza luka badawcza i ryzyko techniczne. Zespół powinien przeprowadzić test identyfikowalności przed implementacją rozbudowanego modelu agentowego. W przeciwnym razie możliwe jest stworzenie symulacji, która wizualnie wygląda realistycznie, ale jej popyt nie jest empirycznie uzasadniony.

## 5. Silniki i frameworki symulacyjne

### 5.1. SUMO — Simulation of Urban MObility

Oficjalna dokumentacja: https://eclipse.dev/sumo/docs/

SUMO to otwarty, mikroskopowy i ciągły symulator ruchu, obsługujący duże sieci i transport multimodalny.

Dokumentacja rowerowa: https://eclipse.dev/sumo/docs/Simulation/Bicycles.html

**Możliwości:**
- pojazdy typu `bicycle`;
- parametry prędkości, przyspieszenia i zachowania;
- import infrastruktury rowerowej z OSM;
- odrębne prędkości rowerów przy trasowaniu;
- symulacja ruchu w czasie i interakcji w sieci.

**Ograniczenia udokumentowane przez SUMO:**
- nie ma odrębnego, dedykowanego modelu ruchu rowerowego; istniejące modele są adaptowane;
- dokumentacja wskazuje problemy z ruchem dwukierunkowym na drogach rowerowych;
- domyślny model skrzyżowań nie jest specjalnie dostosowany do rowerów;
- część problemów wymaga dodatkowych modeli lub zewnętrznej kontroli.

**Ocena dla projektu:** SUMO jest właściwym kandydatem, jeżeli celem stanie się mikrosymulacja interakcji, kolejek, skrzyżowań i współdzielenia infrastruktury. Jest jednak cięższy konfiguracyjnie i wymaga sprawdzenia, czy jego reprezentacja rowerów jest adekwatna dla wybranego krakowskiego scenariusza. Nie powinien być automatycznie uznany za „bardziej realistyczny” bez kalibracji.

Źródła:
- https://eclipse.dev/sumo/docs/
- https://eclipse.dev/sumo/docs/Simulation/Bicycles.html
- Alvarez Lopez et al. (2018), *Microscopic Traffic Simulation using SUMO*, IEEE ITSC.

### 5.2. MATSim

Dokumentacja: https://www.matsim.org/docs/

MATSim to agentowy framework transportowy do symulacji dużych systemów transportowych i planów podróży. Ma silne zaplecze badań transportowych i obsługuje koncepcję agentów, planów, aktywności i tras.

**Ograniczenie istotne dla projektu:** obsługa danego trybu w MATSim zależy od konfiguracji i modułu symulacji. Dokumentacja wskazuje, że nieznany silnikowi tryb może być domyślnie teleportowany między początkiem i końcem podróży, zamiast być symulowany na sieci. Nie wolno więc zakładać, że samo ustawienie `mode=bike` zapewnia mikrosymulację ruchu rowerowego.

**Ocena:** wartościowy punkt odniesienia dla planowania transportowego i agentów z planami podróży, ale większy próg wejścia i ryzyko dodatkowej konfiguracji. Nie jest pierwszym wyborem dla małego projektu w Pythonie.

Źródła:
- https://www.matsim.org/docs/
- https://matsim.org/files/book/partOne-latest.pdf

### 5.3. Mesa

Dokumentacja: https://mesa.readthedocs.io/

Mesa jest frameworkiem ABM w Pythonie. Dostarcza struktury agentów, modelu, harmonogramowania, przestrzeni i narzędzi analitycznych.

**Zalety:**
- naturalna reprezentacja agentów i ich stanu;
- pełna kontrola nad logiką wyboru trasy;
- integracja z ekosystemem Python;
- łatwe eksperymentowanie z regułami i heterogenicznością agentów.

**Ograniczenia:**
- Mesa nie jest gotowym symulatorem transportu;
- nie dostarcza automatycznie wiarygodnego modelu rowerowego, przepustowości ani zachowania na skrzyżowaniach;
- reguły ruchu, trasowanie, popyt i walidację trzeba zaprojektować.

**Ocena:** rekomendowany framework dla własnego, sieciowego ABM na poziomie mezo, jeżeli celem jest kontrola nad zachowaniem agentów i analiza scenariuszy infrastruktury, a nie pełna mikrosymulacja fizycznego ruchu.

Źródła:
- https://mesa.readthedocs.io/
- https://joss.theoj.org/papers/10.21105/joss.07668
- https://github.com/projectmesa/mesa

### 5.4. OSMnx i NetworkX

OSMnx: https://osmnx.readthedocs.io/en/stable/

NetworkX: https://networkx.org/documentation/stable/

OSMnx umożliwia pobieranie, analizę i wizualizację sieci ulicznych z OpenStreetMap. Typ sieci `bike` filtruje sieć według dostępności rowerowej. Wynik jest grafem NetworkX, który można dalej analizować.

**Znaczenie:**
- OSMnx jest narzędziem do budowy danych sieciowych, nie silnikiem symulacji;
- NetworkX dostarcza algorytmy trasowania i operacje na grafach;
- atrybuty OSM wymagają kontroli jakości i mogą być niekompletne;
- dane OSM należy uzupełniać i weryfikować miejskimi warstwami infrastruktury.

### 5.5. SimPy

Dokumentacja: https://simpy.readthedocs.io/en/latest/

SimPy jest biblioteką symulacji zdarzeń dyskretnych (DES), z procesami, zdarzeniami, timeoutami i zasobami o ograniczonej pojemności.

**Zalety:** przydatny do kolejek, zasobów, zdarzeń o różnych czasach trwania i synchronizacji procesów.

**Ograniczenia:** nie jest frameworkiem transportowym ani ABM sieciowym. Nie zapewnia wyboru tras, modelu ruchu rowerowego ani kalibracji.

**Ocena:** opcjonalny komponent, jeżeli projekt będzie modelował kolejki lub ograniczone zasoby w sposób zdarzeniowy. Nie powinien być wybierany tylko dlatego, że projekt jest „symulacją dyskretną”.

### 5.6. Porównanie narzędzi

| Narzędzie | Główna rola | Ruch rowerowy | Kontrola nad agentem | Koszt wdrożenia | Rekomendacja |
|---|---|---|---|---|---|
| SUMO | Mikrosymulacja ruchu | Tak, z opisanymi ograniczeniami | Średnia / przez API i konfigurację | Wysoki | Alternatywa dla interakcji i skrzyżowań |
| MATSim | Agentowy model transportowy | Zależny od konfiguracji modułów | Wysoka na poziomie planów i agentów | Wysoki | Punkt odniesienia dla transportu |
| Mesa | Framework ABM | Trzeba zbudować | Bardzo wysoka | Średni | **Wybór dla modelu mezo** |
| OSMnx | Pobieranie sieci OSM | Filtr sieci bike | Nie dotyczy | Niski–średni | **Warstwa danych sieciowych** |
| NetworkX | Graf i algorytmy | Nie modeluje zachowania | Wysoka na poziomie grafu | Niski | **Warstwa trasowania** |
| SimPy | DES | Nie ma wbudowanego modelu rowerowego | Własna logika procesów | Średni | Opcjonalnie dla kolejek |

## 6. Dane przestrzenne i źródła miejskie

### 6.1. OpenStreetMap

OSM jest podstawowym źródłem geometrii i atrybutów sieci. Istotne tagi obejmują m.in.:
- `highway`;
- `cycleway`;
- `bicycle`;
- `oneway`;
- `surface`;
- `smoothness`;
- `incline` (jeżeli występuje);
- ograniczenia dostępu.

Tagi nie są kompletne ani zawsze jednolicie stosowane. OSM nie może być traktowany jako bezbłędny rejestr miejskiej infrastruktury.

### 6.2. OSMnx

OSMnx pobiera grafy i przekształca je do struktur NetworkX / GeoDataFrame. Jest odpowiedni do zbudowania bazowej sieci rowerowej i kontroli geometrii. Trzeba zachować skierowanie grafu i sprawdzić ograniczenia przejazdu rowerem.

### 6.3. ZTP i MSIP Kraków

ZTP udostępnia otwarte dane przestrzenne związane z transportem i infrastrukturą. MSIP opisuje zasób „ZTP – Komunikacja Miejska i Rowerowa”, z danymi wektorowymi i układem odniesienia EPSG:2178.

Dane te mogą posłużyć do weryfikacji:
- przebiegu infrastruktury;
- lokalizacji stojaków i elementów infrastruktury;
- atrybutów miejskich warstw rowerowych;
- geolokalizacji liczników, o ile dana warstwa jest dostępna.

Źródła:
- https://ztp.krakow.pl/dane-otwarte
- https://msip.krakow.pl/dataset/2963
- https://krakow.pl/aktualnosci/284482,1912,komunikat,sprawdz_przystanki__infrastrukture_rowerowa_i_parkingi_p+r__czyli_otwarte_dane_w_ztp.html

## 7. Dane licznikowe Otwarty Plan i ich wykorzystanie

### 7.1. Charakter źródła

Otwarty Plan prezentuje automatyczne pomiary ruchu rowerowego w Krakowie. Według opisu metodologii:
- źródłem jest system 19 całodobowych liczników indukcyjnych;
- dodatkowo prezentowane są 4 optyczne czujniki Telraam, działające tylko w świetle dziennym;
- profile godzinowe i dzienne są analizowane w rozdzielczości godzinowej;
- „typowy ruch” jest medianą wartości z analogicznych okresów historycznych;
- w analizach uwzględniane są liczniki o pokryciu danych co najmniej 95%;
- dane pogodowe pochodzą z IMGW;
- dane są udostępniane do analiz z obowiązkiem wskazania źródła, na licencji CC BY 4.0 (zgodnie z opisem portalu).

Źródło: https://rowerowy.otwartyplan.org/dane/

### 7.2. Co można wyznaczyć?

- dzienne i godzinowe natężenie w lokalizacji licznika;
- sezonowość i różnice między dniami roboczymi a weekendami;
- zmiany w czasie w obrębie jednego licznika;
- podobieństwo profili między licznikami;
- obserwowane przekroczenia punktów pomiarowych.

### 7.3. Czego nie można wyznaczyć bez dodatkowych danych?

- pełnych tras;
- macierzy OD;
- liczby unikalnych rowerzystów w całym obszarze;
- udziału osób, które przejechały przez dwa lub więcej liczników;
- dokładnej prędkości i czasu podróży;
- kierunku ruchu, jeżeli licznik agreguje kierunki.

### 7.4. Wymagany audyt

Każdy licznik otrzyma profil:
- `first_valid_date`;
- `last_valid_date`;
- `n_observed`;
- `coverage_ratio`;
- `n_zeros`;
- `max_missing_run`;
- `suspected_outage`;
- `location_verified`;
- `direction_known`;
- `mapped_edge_id`.

Dopiero po audycie wybieramy liczniki do kalibracji i walidacji.

## 8. Metody kalibracji i walidacji

### 8.1. Weryfikacja a walidacja

Weryfikacja odpowiada na pytanie, czy program został poprawnie zaimplementowany zgodnie ze specyfikacją. Walidacja sprawdza, czy model jest wystarczająco adekwatny do zamierzonego zastosowania.

Podstawowym źródłem metodologicznym jest:

Sargent, R. G. (2013), *Verification and validation of simulation models*, Journal of Simulation, 7, 12–24. Materiał dydaktyczny: https://ics.uu.nl/docs/vakken/msosi/VerificationValidationSargent.pdf

### 8.2. Weryfikacja implementacji

- każda krawędź ma dodatnią długość;
- agent porusza się wyłącznie po dopuszczonych krawędziach;
- trasa łączy origin z destination;
- czas przejazdu jest dodatni;
- suma przepływów godzinowych odpowiada wartości dziennej;
- dla ustalonego seed przebieg jest powtarzalny;
- zmiana infrastruktury wpływa wyłącznie na oczekiwane elementy grafu;
- nie ma podwójnego liczenia agentów na tym samym liczniku w tym samym przekroczeniu.

### 8.3. Walidacja empiryczna

- porównanie przepływów symulowanych i obserwowanych na licznikach;
- osobne raporty dla każdego licznika;
- walidacja czasowa na okresie nieużytym do kalibracji;
- walidacja przestrzenna na licznikach odłożonych, jeśli liczba punktów jest wystarczająca;
- sprawdzenie wzorców dobowych i tygodniowych, jeśli profile są dostępne.

### 8.4. Metryki

- MAE — średni błąd bezwzględny;
- RMSE — pierwiastek z błędu średniokwadratowego;
- WAPE — błąd bezwzględny ważony natężeniem;
- bias — systematyczne przeszacowanie lub niedoszacowanie;
- GEH — pomocniczo, przy zgodnych jednostkach i agregacji.

Nie należy opierać walidacji wyłącznie na jednej metryce. Trzeba pokazać rozkład błędów między licznikami i okresami.

### 8.5. Analiza wrażliwości

Parametry, których nie da się wiarygodnie oszacować z danych, należy testować scenariuszowo:
- średnia prędkość;
- preferencja dla infrastruktury wydzielonej;
- kara za ruch w jezdni;
- waga nachylenia;
- rozkład popytu OD;
- stopień losowości wyboru trasy.

Najpierw zalecana jest analiza OFAT (one-factor-at-a-time), a następnie — jeżeli zakres eksperymentów pozwoli — analiza wieloczynnikowa lub globalna.

## 9. Opis modelu — ODD Protocol

Do dokumentacji ABM należy zastosować protokół ODD (Overview, Design concepts, Details).

Grimm et al. (2020), *The ODD Protocol for Describing Agent-Based and Other Simulation Models: A Second Update to Improve Clarity, Replication, and Structural Realism*, JASSS 23(2), DOI: https://doi.org/10.18564/jasss.4259

ODD obejmuje siedem elementów:
1. Purpose and patterns;
2. Entities, state variables and scales;
3. Process overview and scheduling;
4. Design concepts;
5. Initialization;
6. Input data;
7. Submodels.

W aktualizacji protokołu podkreślono również znaczenie opisu uzasadnienia modelu i kryteriów oceny jego przydatności. W projekcie ODD powinien być częścią `model-specification.md` lub raportu końcowego, a README ma zawierać jedynie syntetyczny opis.

Źródła:
- https://www.jasss.org/23/2/7.html
- https://www.usgs.gov/publications/odd-protocol-describing-agent-based-and-other-simulation-models-a-second-update

## 10. Rekomendacja architektoniczna

### 10.1. Wybór dla wersji bazowej

**Network-based mesoscopic ABM: Mesa + NetworkX + OSMnx + GeoPandas + Pandas.**

| Warstwa | Narzędzie | Odpowiedzialność |
|---|---|---|
| Dane tabelaryczne | Pandas | Import, czyszczenie, agregacja |
| Dane przestrzenne | GeoPandas | Warstwy GIS, CRS, mapowanie liczników |
| Sieć | OSMnx | Pobieranie i przygotowanie grafu OSM |
| Graf / trasy | NetworkX | Reprezentacja sieci i algorytmy ścieżek |
| Agenci | Mesa | Stan agentów, harmonogram i przebiegi |
| Optymalizacja / estymacja | SciPy | NNLS i optymalizacja parametrów |
| Analiza | NumPy, Matplotlib, Statsmodels | Metryki, statystyka i wykresy |
| Wizualizacja mapowa | Folium / GeoPandas | Mapa wyników |

### 10.2. Dlaczego nie SUMO jako domyślny wybór?

SUMO jest bardziej odpowiedni do mikrosymulacji interakcji i ruchu w czasie, ale projekt na obecnym etapie nie ma danych o natężeniu ruchu samochodowego, sygnalizacji, zachowaniu na skrzyżowaniach ani parametrach przepustowości. Uruchomienie SUMO nie rozwiąże problemu braku OD i nie zapewni automatycznie lepszej walidacji. Co więcej, dokumentacja SUMO wymienia specyficzne ograniczenia modelowania rowerów.

Wybór SUMO można ponownie rozważyć po przygotowaniu małego, reprezentatywnego scenariusza i sprawdzeniu, czy model rowerowy daje potrzebne zachowanie.

### 10.3. Dlaczego nie SimPy jako główny silnik?

SimPy rozwiązuje problem harmonogramowania zdarzeń i zasobów, a nie problem reprezentacji sieci transportowej i wyboru trasy. Zastosowanie go do każdej krawędzi jako kolejki wymagałoby założenia przepustowości, której zespół obecnie nie obserwuje. Byłoby to ryzyko pozornej precyzji.

## 11. Najważniejsze luki i plan ich zamknięcia

| Luka | Dlaczego jest ważna | Działanie |
|---|---|---|
| Brak macierzy OD | Nieznany popyt między strefami | Test identyfikowalności z liczników; w razie potrzeby scenariusze syntetyczne |
| Brak kierunków liczników | Niepoprawne przypisanie do krawędzi skierowanych | Pozyskać metadane i zweryfikować lokalizacje |
| Niekompletne profile godzinowe | Nie można odtworzyć godzinowego ruchu całej sieci | Pobrać profile dla wybranych liczników lub ograniczyć analizę |
| Nieznane parametry preferencji | Nieuzasadnione koszty tras | Kalibracja z GPS lub analiza wrażliwości |
| Brak danych o przepustowości | Nie można wiarygodnie modelować kolejek | Nie modelować w bazie; rozważyć osobny scenariusz |
| Niejednolity stan sieci w czasie | Historyczne pomiary mogą dotyczyć innej infrastruktury | Wybrać okres i datę referencyjną sieci |
| Niepewne tagi OSM | Błędna dostępność dróg | Porównać z warstwami miejskimi i wykonać kontrolę ręczną |

## 12. Bibliografia i dokumentacja

### Publikacje naukowe

1. *Development of a large-scale transport model with focus on cycling* (2020), Transportation Research Part A. https://doi.org/10.1016/j.tra.2020.02.010
2. *Simulating Spatio-Temporal Patterns of Bicycle Flows with an Agent-Based Model* (2021), ISPRS IJGI 10(2), 88. https://www.mdpi.com/2220-9964/10/2/88
3. Łukawska, M. (2024), *Quantitative modelling of cyclists’ route choice behaviour on utilitarian trips based on GPS data: associated factors and behavioural implications*, Transport Reviews 44(5). https://doi.org/10.1080/01441647.2024.2355468
4. Ehrgott, M., Wang, J. Y. T., Raith, A., van Houtte, C. (2012), *A bi-objective cyclist route choice model*, Transportation Research Part A 46(4), 652–663. https://doi.org/10.1016/j.tra.2011.11.015
5. *Road infrastructures, spatial surroundings, and the demand and route choices for cycling: Evidence from a GPS-based mode detection study from Oslo, Norway* (2023). https://doi.org/10.1177/23998083221141431
6. Grimm, V. et al. (2020), *The ODD Protocol for Describing Agent-Based and Other Simulation Models: A Second Update to Improve Clarity, Replication, and Structural Realism*, JASSS 23(2). https://doi.org/10.18564/jasss.4259
7. Sargent, R. G. (2013), *Verification and validation of simulation models*, Journal of Simulation 7, 12–24. https://ics.uu.nl/docs/vakken/msosi/VerificationValidationSargent.pdf

### Dokumentacja narzędzi

- SUMO: https://eclipse.dev/sumo/docs/
- SUMO — bicycles: https://eclipse.dev/sumo/docs/Simulation/Bicycles.html
- MATSim: https://www.matsim.org/docs/
- Mesa: https://mesa.readthedocs.io/
- OSMnx: https://osmnx.readthedocs.io/en/stable/
- NetworkX: https://networkx.org/documentation/stable/
- GeoPandas: https://geopandas.org/en/stable/
- SimPy: https://simpy.readthedocs.io/en/latest/
- SciPy: https://docs.scipy.org/doc/scipy/

### Dane lokalne

- Otwarty Plan — Kraków, pomiary rowerowe: https://rowerowy.otwartyplan.org/dane/
- ZTP — pomiary ruchu rowerowego: https://ztp.krakow.pl/rower/pomiary-ruchu-rowerowego
- ZTP — dane otwarte: https://ztp.krakow.pl/dane-otwarte
- MSIP — ZTP, komunikacja miejska i rowerowa: https://msip.krakow.pl/dataset/2963
- OpenStreetMap: https://www.openstreetmap.org/
- IMGW: https://danepubliczne.imgw.pl/
- Geoportal / NMT: https://www.geoportal.gov.pl/pl/dane/numeryczny-model-terenu-nmt/

---

## 13. Konkluzja

Literatura potwierdza zasadność wykorzystania sieciowego ABM do analizy przestrzenno-czasowych wzorców ruchu rowerowego. Badania wyboru trasy wskazują, że rowerzyści uwzględniają więcej czynników niż długość lub czas przejazdu, ale siła i kierunek preferencji zależą od lokalnego kontekstu. Narzędzia takie jak SUMO oferują mikrosymulację, lecz ich model rowerowy ma udokumentowane ograniczenia i wymaga odpowiedniej kalibracji.

Dla aktualnego zakresu i dostępnych danych rekomendowany jest kontrolowany, sieciowy ABM na poziomie mezo, z własną logiką trasowania i syntetycznym popytem OD. Najważniejszym warunkiem wiarygodności nie jest wybór biblioteki, lecz sprawdzenie, czy dostępne liczniki, ich lokalizacje i geometria sieci pozwalają zidentyfikować lub przynajmniej ograniczyć możliwe przepływy OD. Jeżeli nie, projekt powinien jasno przejść na analizę scenariuszową z jawnymi założeniami, zamiast deklarować rekonstrukcję rzeczywistych podróży.
