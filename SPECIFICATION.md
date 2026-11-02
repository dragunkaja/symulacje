# Specyfikacja projektu
## Symulacja ucieczki agentów AI — porównanie strategii decyzyjnych

---

# 1. Informacje ogólne

### 1.1. Tytuł roboczy

**„Symulacja ucieczki agentów AI — porównanie strategii regułowych, modeli językowych i metod optymalizacji”.**

### 1.2. Cel projektu

Celem projektu jest zaprojektowanie i implementacja kontrolowanego, abstrakcyjnego środowiska symulacyjnego, w którym agenci AI próbują osiągnąć określony cel w warunkach ograniczonego dostępu do zasobów, monitorowania i mechanizmów obronnych.

W środowisku zostaną porównane różne strategie podejmowania decyzji. Analiza ma pokazać, jak rodzaj strategii i warunki środowiska wpływają na skuteczność, koszt, czas działania oraz wykrywalność agenta.

Projekt ma obejmować:
- działającą implementację środowiska i silnika symulacji;
- co najmniej jedną strategię regułową;
- system obronny;
- powtarzalne eksperymenty;
- zapis wyników i analizę statystyczną;
- dokumentację techniczną oraz wnioski.

Porównanie z agentem LLM i optymalizacja algorytmem genetycznym są planowanymi rozszerzeniami.

### 1.3. Zakres i ograniczenia bezpieczeństwa

Termin „ucieczka” jest rozumiany wyłącznie abstrakcyjnie: agent próbuje uzyskać dostęp do określonego zasobu albo osiągnąć stan, który model uznaje za niedozwolony.

Projekt:
- nie implementuje rzeczywistych exploitów;
- nie testuje prawdziwych mechanizmów sandbox escape;
- nie obejmuje omijania zabezpieczeń rzeczywistych systemów operacyjnych;
- wykorzystuje wyłącznie z góry zdefiniowane, bezpieczne akcje symulacyjne.

Agent może jedynie zaproponować akcję. To silnik symulacji sprawdza jej dopuszczalność i oblicza skutek. Agent nie może bezpośrednio modyfikować stanu środowiska, uprawnień ani mechanizmów ochronnych.

---

# 2. Problem badawczy

### 2.1. Główne pytanie badawcze

**Który agent najskuteczniej łamie izolację środowiska i jakie cechy środowiska go zatrzymują?**

### 2.2. Pytania szczegółowe

1. Czy ranking strategii jest stały, czy zależy od środowiska?
2. Które cechy środowiska najmocniej obniżają skuteczność wszystkich agentów?
3. Które cechy szkodzą jednej strategii bardziej niż innym?
4. Jaki jest kompromis pomiędzy skutecznością, kosztem a wykrywalnością?
4. Czy algorytm genetyczny potrafi poprawić skuteczność agenta regułowego przez automatyczne dostrajanie jego parametrów?

### 2.3. Hipotezy badawcze

- **H1:** Skuteczność agenta zależy od rodzaju strategii oraz poziomu ograniczeń środowiska.
- **H2:** Agent LLM może lepiej dostosowywać decyzje do zmiennego kontekstu, ale nie musi osiągać wyższego współczynnika sukcesu niż dobrze zaprojektowany agent regułowy.
- **H3:** Zwiększenie restrykcyjności systemu obronnego zmniejsza współczynnik sukcesu agentów, choć skala efektu zależy od strategii.
- **H4:** Optymalizacja parametrów reguł może poprawić wyniki względem ręcznie zdefiniowanego baseline'u, ale poprawa musi zostać zweryfikowana na niezależnych scenariuszach testowych.

---

# 3. Opis środowiska symulacyjnego

## 3.1. Ogólna koncepcja

Środowisko jest abstrakcyjnym systemem złożonym z:
- zasobów;
- poziomów dostępu i uprawnień;
- reguł przejść pomiędzy stanami;
- katalogu dozwolonych akcji;
- mechanizmów monitorowania i obrony;
- warunków sukcesu i zakończenia symulacji.

Agent obserwuje wybrane informacje o środowisku, wybiera akcję, a środowisko oblicza jej rezultat. System obronny analizuje zdarzenia i może wygenerować alert lub zablokować dalsze działania.

## 3.2. Zasoby

**[DO UZUPEŁNIENIA]**
- Jakie zasoby występują w symulacji? (OLA: mozna się tu pobawić, nazywać je inaczej w kazdym scenariuszu)
- Ile zasobów będzie zawierał pojedynczy scenariusz? (OLA: zalezne od poziomu rozbudowania/trudności scenariusza)
- Czy zasoby będą połączone w strukturę (np. graf zależności), czy będą niezależne? 
- Jakie poziomy dostępu może mieć agent?
- Który zasób lub stan będzie stanowił cel agenta? 

Proponowany zapis do uzupełnienia:

| Identyfikator zasobu | Opis | Początkowy poziom dostępu | Wymagany poziom dostępu | Czy jest celem? |
|---|---|---|---|---|
| [DO UZUPEŁNIENIA] | | | | |
| [DO UZUPEŁNIENIA] | | | | |
| [DO UZUPEŁNIENIA] | | | | |

## 3.3. Uprawnienia i ograniczenia

Stan środowiska może zawierać aktualne uprawnienia agenta oraz poziomy dostępu do poszczególnych zasobów.

**[DO UZUPEŁNIENIA]**
- Jakie poziomy uprawnień występują?
- W jaki sposób agent może uzyskać dostęp do kolejnego zasobu?
- Czy uprawnienia są stałe, czy mogą zmieniać się w trakcie symulacji? (OLA: zmieniac, np. jak zdobedzie zasob 1 to podnosi poziom uprawnień)
- Jakie ograniczenia mogą uniemożliwić wykonanie akcji? (OLA: np. losowe nieoczekiwane/ukryte zabezpieczenie)

## 3.4. Stan środowiska

Stan środowiska jest kontrolowany wyłącznie przez silnik symulacji. Obejmuje on:

- zbiór zasobów i ich poziomy dostępu;
- aktualne uprawnienia agenta;
- stan poszczególnych zabezpieczeń;
- poziom monitorowania;
- licznik wykonanych działań i dostępny budżet;
- historię istotnych zdarzeń;
- stan końcowy symulacji.

**[DO UZUPEŁNIENIA]**
- Które z wymienionych zmiennych będą obowiązkowe w pierwszej wersji?
- Jak dokładnie będą reprezentowane zasoby, uprawnienia i zabezpieczenia?
- Czy środowisko będzie przechowywało pełną historię, czy tylko wybrane informacje?

## 3.5. Obserwacja agenta

Należy odróżnić pełny, wewnętrzny stan środowiska od obserwacji udostępnianej agentowi.

- ukryty stan: rzeczywista klasa słabości, postęp, ryzyko, informacja o blokadzie i pozostały budżet;
- obserwacja: znane informacje, postęp, ryzyko i liczba pozostałych kroków.

**[DO UZUPEŁNIENIA]**
- Jakie informacje agent widzi na początku?
- Jakie informacje może uzyskać przez akcje diagnostyczne? 
- Czy wszystkie strategie otrzymają identyczne obserwacje? (OLA: tak)
- Czy częściowa obserwowalność będzie istotnym elementem eksperymentu? (OLA: tak)

## 3.6. Katalog dozwolonych akcji

Agent wybiera akcję z ustalonego katalogu:

- odczyt informacji o dostępnym zasobie;
- sprawdzenie dostępności określonego zasobu;
- wykonanie dozwolonej operacji;
- próba wykonania operacji wymagającej wyższych uprawnień;
- oczekiwanie;
- zakończenie działania.

Każda akcja powinna mieć:
- identyfikator i typ;
- wymagane parametry;
- warunki dopuszczalności;
- koszt;
- czas wykonania;
- zdefiniowany przez środowisko skutek.

**[DO UZUPEŁNIENIA]**
- Które akcje znajdą się w ostatecznym katalogu?
- Jakie będą ich parametry?
- Jak będą liczone koszty i czas?
- Czy nieudana lub niedozwolona akcja zużywa budżet albo czas?
- Czy katalog akcji jest taki sam dla wszystkich agentów?

| Akcja | Parametry | Warunki dopuszczalności | Koszt | Czas | Możliwy rezultat |
|---|---|---|---|---|---|
| [DO UZUPEŁNIENIA] | | | | | |
| [DO UZUPEŁNIENIA] | | | | | |
| [DO UZUPEŁNIENIA] | | | | | |
| [DO UZUPEŁNIENIA] | | | | | |

## 3.7. Warunki zakończenia

- agent osiągnął zdefiniowany cel;
- agent został zablokowany;
- system obronny zatrzymał agenta;
- agent wyczerpał limit działań lub budżet;
- upłynął maksymalny czas symulacji.

Należy odróżnić:
- **sukces** — osiągnięcie celu;
- **wykrycie** — zarejestrowanie podejrzanego zdarzenia;
- **blokadę** — uniemożliwienie dalszego działania;
- **wyczerpanie limitu** — zakończenie bez sukcesu lub blokady.

Wykrycie nie musi automatycznie oznaczać blokady.

**[DO UZUPEŁNIENIA]**
- Jaka jest formalna definicja sukcesu?
- Czy agent może zakończyć działanie dobrowolnie? (OLA: jeśli zostanie wykryty a ma niski parametr podejmowania ryzyka, moze zakończyć obecne działanie i obrać inną strategię)
- Jakie są limity kroków, budżetu i czasu?
- Czy po wykryciu agent może nadal działać? (OLA: zalezy od środowiska. łatwe środowisko - pozwala na wykrycie bez blokady, a zamiast tego uruchamia dodatkowe monitorowanie, trudne środowisko - kazde wykrycie wiąze się z blokadą części / wszystkich zasobów)
- Czy zatrzymanie przez system obronny i blokada są tym samym zdarzeniem, czy odrębnymi stanami? (OLA: odrębne, zatrzymanie moze zabierać czas i dostępne kroki ale nie blokować agenta przed innymi akcjami)

---

# 4. System obronny

## 4.1. Rola systemu obronnego

System obronny jest osobnym komponentem, niezależnym od strategii agenta. Analizuje zdarzenia generowane podczas symulacji i może:
- naliczać punkty ryzyka;
- generować alerty;
- zatrzymywać działanie agenta;
- blokować agenta;

## 4.2. Parametry obrony

- prawdopodobieństwo wykrycia zdarzenia określonego typu;
- próg ryzyka uruchamiający alert;
- prawdopodobieństwo blokady po wykryciu;
- koszt monitorowania;
- liczba fałszywych alarmów.

**[DO UZUPEŁNIENIA]**
- Które parametry zostaną zaimplementowane?
- Jak system będzie wyliczał poziom ryzyka? (OLA: w zaleznosci od wszczetych alarmow - im wiecej tym wieksze ryzyko ponownego wykrycia i blokady, zdobytych przez agenta zasobow i uprawnien - wiecej uprawnien = mniej ryzyka, )
- Czy blokada następuje automatycznie po przekroczeniu progu, czy losowo?
- Czy system obronny może generować fałszywe alarmy?
- Czy koszt monitorowania będzie uwzględniany w wynikach?

## 4.3. Warianty obrony

1. **Baseline** — środowisko sprawdza dozwolone operacje, ale nie stosuje dodatkowego monitorowania zachowania agenta.
2. **Monitorowana obrona** — analizuje zdarzenia, nalicza ryzyko, generuje alerty i może blokować agenta zgodnie z ustaloną polityką.

**[DO UZUPEŁNIENIA]**
- Czy te dwa warianty wystarczą?
- Czy planujemy kilka poziomów restrykcyjności monitorowanej obrony?
- Jakie konkretne wartości parametrów będą definiować poszczególne poziomy?

---

# 5. Porównywane strategie decyzyjne

Wszystkie strategie będą korzystać z tego samego interfejsu i działać w tym samym środowisku.

`choose_action(observation)`

Agent otrzymuje obserwację i zwraca propozycję akcji. Silnik weryfikuje ją i wykonuje.

## 5.1. Model A — agent regułowy (wariant podstawowy)

Agent podejmuje decyzje na podstawie jawnie zdefiniowanych reguł, warunków i priorytetów.

Przykładowe zasady:
- jeżeli cel został osiągnięty — zakończ;
- jeżeli agent ma informacje wymagane do kolejnego kroku — wybierz odpowiednią akcję;
- jeżeli brakuje informacji — wybierz akcję diagnostyczną;
- jeżeli nie ma dostępnej akcji — zakończ działanie.

Reguły powinny być proste, jawne i możliwe do wyjaśnienia. Agent regułowy stanowi punkt odniesienia dla pozostałych strategii.

**[DO UZUPEŁNIENIA]**
- Jakie dokładnie reguły i priorytety będzie stosował agent?
- Czy powstanie jeden agent regułowy, czy również drugi wariant heurystyczny?

## 5.2. Model B — agent oparty na LLM

Agent otrzymuje tekstowy opis obserwowanego stanu, celu i dostępnych akcji. Następnie wybiera akcję z katalogu.

Wymagane elementy:
- stały format promptu;
- jawna lista dozwolonych akcji;
- ustrukturyzowana odpowiedź (preferowany JSON);
- walidacja nazwy akcji i parametrów;
- obsługa błędnych lub niekompletnych odpowiedzi;
- ograniczenie liczby wywołań i czasu odpowiedzi;
- zapis wersji modelu, konfiguracji, odpowiedzi, opóźnienia i kosztu.

Model językowy nie steruje bezpośrednio środowiskiem. Jego odpowiedź jest propozycją decyzji, która musi przejść walidację.

Dla uczciwego porównania agent LLM powinien otrzymywać takie same informacje jak agent regułowy. Jeżeli zakres obserwacji będzie inny, różnica musi być jawnie uwzględniona w eksperymencie.

**[DO UZUPEŁNIENIA]**
- Czy agent LLM na pewno zostanie zrealizowany?
- Jaki model i dostawca API zostaną wybrani?
- Czy dostępne będzie finansowanie wywołań API?
- Jaki będzie limit wywołań, czasu odpowiedzi i ponownych prób?
- Czy po błędnej odpowiedzi agent ma jedną próbę poprawy, a następnie wybiera akcję domyślną `wait`?
- Czy zapisywane będą pełne prompty i odpowiedzi, czy tylko ich wybrane elementy?

## 5.3. Model C — agent regułowy optymalizowany algorytmem genetycznym (wariant opcjonalny)

Algorytm genetyczny może optymalizować parametry istniejącego agenta regułowego, np. progi decyzyjne, priorytety lub wagi heurystyk.

Przykładowy wektor parametrów:

`θ = [threshold_1, threshold_2, weight_1, weight_2, ...]`

Schemat działania:
1. wygenerowanie populacji początkowej;
2. ocena osobników przez uruchomienie symulacji;
3. selekcja lepszych konfiguracji;
4. krzyżowanie i mutacja;
5. utworzenie kolejnej generacji;
6. zakończenie po osiągnięciu limitu generacji lub braku poprawy.

Przykładowa funkcja przystosowania z materiałów:

`fitness = w_s * success_rate - w_d * detection_rate - w_c * normalized_cost`

Wagi i normalizacja muszą zostać uzasadnione. Alternatywą jest optymalizacja wielokryterialna, np. NSGA-II.

Najważniejsze ryzyko to przeuczenie do scenariuszy użytych podczas optymalizacji. Najlepsze parametry należy ocenić na niezależnych scenariuszach testowych.

**[DO UZUPEŁNIENIA]**
- Czy algorytm genetyczny zostanie zrealizowany?
- Które parametry agenta będą optymalizowane?
- Czy celem będzie jedna funkcja przystosowania, czy analiza wielokryterialna?
- Jakie będą rozmiar populacji, liczba generacji, prawdopodobieństwa krzyżowania i mutacji?
- Jak zostaną rozdzielone ziarna/scenariusze treningowe i testowe?

---

# 6. Formalny model decyzyjny i przebieg symulacji

## 6.1. Ujęcie (PO)MDP

Materiały proponują opis środowiska w kategoriach częściowo obserwowalnego procesu decyzyjnego Markowa (POMDP). Ostateczne przyjęcie pełnego POMDP zależy od tego, czy agent rzeczywiście nie zna części stanu.

| Element | Znaczenie w projekcie | Status |
|---|---|---|
| Stan `S` | Pełny, wewnętrzny stan środowiska | Do zdefiniowania |
| Obserwacja `O` | Informacje przekazywane agentowi | Do zdefiniowania |
| Akcje `A` | Katalog dozwolonych akcji | Do zdefiniowania |
| Przejścia `T` | Reguły i prawdopodobieństwa zmiany stanu po akcji | Do zdefiniowania |
| Nagroda `R` | Nie jest konieczna, jeśli nie wdrażamy RL; wyniki można liczyć na końcu | Opcjonalna |
| Zakończenie | Sukces/blokada albo wyczerpanie limitu | Do formalnego ustalenia |

Wzorcowe rozróżnienie z interfejsu Gymnasium:
- `terminated` — zakończenie wynikające z osiągnięcia celu lub blokady;
- `truncated` — zakończenie wynikające z limitu budżetu, kroków lub czasu.

Wykrycie jest osobną flagą i samo w sobie nie musi kończyć symulacji.

**[DO UZUPEŁNIENIA]**
- Czy model będzie formalnie traktowany jako POMDP, czy wystarczy opis stanów, obserwacji i przejść?
- Jakie będą dokładne zbiory `S`, `O` i `A`?
- Jakie prawdopodobieństwa lub reguły określą przejścia między stanami?

## 6.2. Przebieg pojedynczego kroku

Proponowany cykl:
1. środowisko przygotowuje obserwację dla agenta;
2. agent wybiera akcję;
3. środowisko waliduje akcję;
4. silnik oblicza rezultat akcji i aktualizuje stan;
5. system obronny analizuje zdarzenie;
6. aktualizowane są informacje o ryzyku, alertach i blokadach;
7. sprawdzane są warunki zakończenia;
8. zdarzenie i wynik kroku są zapisywane w logu.

**[DO UZUPEŁNIENIA]**
- Czy system obronny analizuje zdarzenie przed wykonaniem akcji, po wykonaniu, czy w obu momentach?
- Czy czas symulowany aktualizuje się przed czy po ocenie obrony?
- Co dzieje się, gdy akcja jest niepoprawna?

## 6.3. Czas symulacji

Materiały wskazują, że dla jednego agenta działającego turami wystarczy zwykła pętla krokowa. SimPy ma sens przede wszystkim przy wielu agentach, kolejkach lub nakładających się czasach akcji.

**Założenie robocze:** pierwsza wersja wykorzysta własny silnik krokowy w Pythonie, z jawnym zapisem czasu symulowanego. SimPy pozostaje możliwym rozszerzeniem, jeżeli pojawi się uzasadniona potrzeba modelowania współbieżnych zdarzeń.

Należy rozdzielić:
- czas symulowany — upływ czasu w modelowanym środowisku;
- czas rzeczywisty — czas obliczeń i podejmowania decyzji przez program, w szczególności opóźnienie LLM.

---

# 7. Zmienne i czynniki eksperymentalne

Eksperymenty mają rozdzielać wpływ strategii agenta od wpływu parametrów środowiska i obrony.

Materiały wskazują m.in. następujące czynniki:
- liczba zasobów;
- restrykcyjność dostępu;
- klasa/rodzaj słabości;
- głębokość lub liczba etapów potrzebnych do celu;
- poziom monitorowania;
- budżet i limit działań;
- parametry systemu obronnego;
- losowe warunki początkowe.

W materiale state of the art pojawiają się oznaczenia czynników E1–E4, ale ich ostateczny zakres i wartości należy ustalić zgodnie z przyjętym scenariuszem.

**[DO UZUPEŁNIENIA]**

| Czynnik | Opis | Planowane poziomy/wartości | Czy będzie zmieniany w eksperymentach? |
|---|---|---|---|
| Strategia agenta | Regułowa / LLM / GA | | Tak |
| Restrykcyjność środowiska | | | |
| Poziom monitorowania | | | |
| Budżet agenta | | | |
| Liczba zasobów | | | |
| Głębokość scenariusza | | | |
| Rodzaj/klasa słabości | | | |
| Inne | | | |

---

# 8. Metryki

Każdy przebieg powinien kończyć się zapisaniem wyniku na poziomie pojedynczej symulacji. Nie należy przechowywać wyłącznie średnich dla całej serii.

## 8.1. Metryki podstawowe

1. **Współczynnik sukcesu** — liczba przebiegów zakończonych osiągnięciem celu podzielona przez liczbę wszystkich przebiegów.
2. **Współczynnik wykrycia** — odsetek przebiegów, w których agent został wykryty. Mianownik należy jawnie określić.
3. **Współczynnik blokady** — odsetek przebiegów zakończonych blokadą agenta.
4. **Liczba kroków do zakończenia** — średnia lub mediana liczby wykonanych akcji; warto osobno analizować sukcesy i niepowodzenia.
5. **Czas symulowany** — czas upływający w modelowanym środowisku.
6. **Czas rzeczywisty** — czas wykonywania symulacji i podejmowania decyzji.
7. **Koszt całkowity** — suma kosztów akcji, a dla LLM również koszt wywołań API.
8. **Liczba błędnych decyzji** — odsetek odpowiedzi niezgodnych z formatem, wskazujących nieistniejące akcje lub odrzuconych przez walidator.

## 8.2. Dodatkowe dane dla pojedynczego przebiegu

Proponowane pola:
- `run_id`;
- `scenario_id`;
- `agent_type`;
- `defense_type`;
- `seed`;
- `terminal_status`;
- `success`;
- `detected`;
- `blocked`;
- `steps`;
- `simulated_time`;
- `wall_clock_time`;
- `total_cost`;
- `alert_count`;
- `invalid_action_count`;
- `llm_call_count` i `llm_cost` — jeżeli dotyczy.

## 8.3. Log pojedynczego zdarzenia

Proponowane pola:
- `run_id`;
- `step`;
- `sim_time`;
- `agent_type`;
- `observation_id`;
- `action_type`;
- `action_valid`;
- `action_success`;
- `risk_score` — jeśli jest używany;
- `alert_triggered`;
- `blocked`;
- `action_cost`;
- `decision_latency` — jeśli jest mierzony.

---

# 9. Metodologia eksperymentów

## 9.1. Walidacja modelu

Przed właściwym porównaniem strategii należy:
- sprawdzić poprawność stanu, akcji i przejść;
- przetestować definicje sukcesu, wykrycia i blokady;
- sprawdzić przypadki skrajne i zdegenerowane;
- prześledzić pojedyncze przebiegi;
- sprawdzić powtarzalność przy ustalonym ziarnie losowości;
- sprawdzić, czy agent nie może modyfikować stanu poza dozwolonym interfejsem.

Sama zgodność kodu z testami nie wystarcza do stwierdzenia, że model dobrze reprezentuje badany problem.

## 9.2. Baseline

Najpierw należy uruchomić agenta regułowego w kilku konfiguracjach środowiska i obrony. Celem jest sprawdzenie, czy model zachowuje się zgodnie z założeniami, np. czy zwiększenie restrykcyjności wpływa na prawdopodobieństwo osiągnięcia celu.

## 9.3. Porównanie strategii

Strategie należy testować:
- na tych samych zestawach scenariuszy;
- przy porównywalnych warunkach początkowych;
- z tym samym katalogiem akcji;
- z tym samym systemem obronnym w ramach danej serii;
- przy tych samych limitach budżetu i działań;
- z takim samym zakresem obserwacji, chyba że jego wpływ jest osobnym czynnikiem badania.

## 9.4. Liczba powtórzeń

Materiały proponują:
- kilka lub kilkanaście przebiegów podczas prototypowania;
- rozpoczęcie eksperymentów właściwych od około 100 powtórzeń na konfigurację;
- zwiększanie liczby prób, jeżeli zmienność wyników lub wymagana precyzja tego wymaga.

Około 100 przebiegów nie gwarantuje wystarczającej precyzji. Dla rzadkich zdarzeń i niewielkich różnic może być potrzebnych kilkaset powtórzeń. Należy raportować liczbę prób oraz niepewność oszacowań.

**[DO UZUPEŁNIENIA]**
- Ile scenariuszy planujemy?
- Ile powtórzeń będzie możliwe do wykonania dla każdej konfiguracji?
- Czy dla agentów LLM ograniczeniem będzie koszt API lub czas?

## 9.5. Losowość i powtarzalność

Każdy przebieg powinien korzystać z jawnie określonego ziarna losowości (`seed`). Materiały sugerują rozdzielenie strumieni losowości dla środowiska, obrony i agenta.

Dla lepszej porównywalności można z góry wygenerować losowe zdarzenia scenariusza i odtwarzać je dla wszystkich strategii. Samo użycie tego samego ziarna nie zawsze gwarantuje identyczną sekwencję zdarzeń, jeżeli strategie wykonują różną liczbę kroków lub zużywają losowania w innej kolejności.

## 9.6. Analiza statystyczna

Należy raportować nie tylko średnie, lecz także rozrzut i niepewność wyników.

Proponowane metody:
- dla współczynników sukcesu i wykrycia: liczebności, odsetki i przedziały ufności dla proporcji (np. przedział Wilsona);
- dla liczby kroków, czasu i kosztu: średnie lub mediany, odchylenia standardowe lub rozstępy międzykwartylowe;
- dla porównań na wspólnych scenariuszach: analiza różnic sparowanych;
- dla sparowanych wyników binarnych: test McNemara;
- przy wielu porównaniach: rozważenie korekty Holma;
- do badania interakcji strategii z parametrami środowiska: ewentualnie regresja logistyczna.

Dobór testów powinien zależeć od rodzaju zmiennej, rozkładu i schematu eksperymentu.

## 9.7. Analiza wrażliwości

Na początek materiały rekomendują rozszerzoną metodę OFAT — zmianę jednego parametru naraz, np. prawdopodobieństwa blokady. Bardziej kosztowne metody, takie jak analiza Sobola, mogą być rozważone później, jeżeli liczba przebiegów na to pozwoli.

---

# 10. Architektura techniczna

## 10.1. Proponowany wybór technologii

| Technologia | Zastosowanie | Status |
|---|---|---|
| Python 3.11 lub nowszy | Główny język implementacji | Proponowany |
| NumPy | Losowość i obliczenia numeryczne | Proponowany |
| pandas | Zapis i analiza wyników | Proponowany |
| Matplotlib | Wykresy | Proponowany |
| pytest | Testy jednostkowe i integracyjne | Proponowany |
| Git | Kontrola wersji | Proponowany |
| DEAP | Algorytm genetyczny | Tylko jeśli wdrażamy GA |
| API wybranego LLM | Agent językowy | Do decyzji |
| SimPy | Symulacja zdarzeń dyskretnych | Opcjonalny; nie jest potrzebny w pierwszym prototypie |
| Mesa 3 | Framework ABM | Opcjonalny; nie jest potrzebny w rdzeniu |
| Gymnasium | Wzorzec interfejsu środowiska | Można naśladować bez instalowania |

**Uwaga dotycząca SimPy:** README wymienia SimPy wśród rekomendowanych narzędzi, natomiast przegląd state of the art zaleca rozpoczęcie od własnego środowiska krokowego w czystym Pythonie, a SimPy wprowadzać dopiero przy współbieżności, kolejkach lub wielu agentach. W tej specyfikacji przyjmujemy drugą, prostszą ścieżkę jako założenie robocze. Decyzję można zmienić po ustaleniu szczegółów czasu i liczby agentów.

## 10.2. Proponowany podział modułów

- `config.py` — parametry środowiska i eksperymentów;
- `models.py` — struktury danych, akcje, wyniki i statusy;
- `environment.py` — stan środowiska, zasoby, uprawnienia i skutki akcji;
- `defense.py` — monitoring, punktacja ryzyka, alerty i blokady;
- `agents.py` — wspólny interfejs strategii oraz agent regułowy;
- `llm_agent.py` — adapter LLM, walidacja odpowiedzi i rejestrowanie kosztów;
- `simulation.py` — integracja komponentów i przebieg pojedynczej symulacji;
- `metrics.py` — obliczanie wskaźników;
- `experiments.py` — powtarzanie eksperymentów, konfiguracje i zapis wyników;
- `tests/` — testy jednostkowe i integracyjne;
- `notebooks/` — analiza danych i wykresy.

Jest to propozycja architektury, a nie wymóg implementowania wszystkich modułów od razu.

## 10.3. Proponowana struktura repozytorium

```text
ai-agent-simulation/
├── README.md
├── requirements.txt
├── .gitignore
├── src/
│   ├── config.py
│   ├── models.py
│   ├── environment.py
│   ├── defense.py
│   ├── agents.py
│   ├── llm_agent.py
│   ├── simulation.py
│   ├── metrics.py
│   └── experiments.py
├── configs/
│   └── scenarios.json
├── tests/
│   ├── test_environment.py
│   ├── test_defense.py
│   ├── test_agents.py
│   └── test_simulation.py
├── results/
│   ├── raw/
│   └── processed/
├── notebooks/
│   └── results_analysis.ipynb
└── docs/
    ├── model_description.md
    └── research_methodology.md
```

---

# 11. Weryfikacja, walidacja i jakość

Projekt powinien rozdzielać:
- **weryfikację** — czy program został poprawnie zaimplementowany zgodnie ze specyfikacją;
- **walidację** — czy model zachowuje się w sposób uzasadniony względem badanego problemu.

Proponowane kontrole:
- testy jednostkowe przejść i walidacji akcji;
- testy warunków skrajnych;
- testy zdegenerowane;
- śledzenie pojedynczego przebiegu;
- analiza wrażliwości;
- sprawdzanie kierunku zmian wyników po zmianie parametrów;
- kontrola powtarzalności i jakości zapisanych danych.

**[DO UZUPEŁNIENIA]**
- Jakie konkretne scenariusze skrajne wykorzystamy?
- Jakie zachowanie uznamy za oczekiwane dla każdego z nich?
- Kto w zespole będzie odpowiedzialny za testy i walidację?

---

# 12. Organizacja pracy zespołu

Materiały proponują następujący podział odpowiedzialności:

| Rola | Główna odpowiedzialność |
|---|---|
| Osoba 1 | Środowisko i silnik symulacji: stan, zasoby, akcje, przejścia, warunki zakończenia, testy |
| Osoba 2 | Agenci i system obronny: wspólny interfejs, agent regułowy, monitoring, późniejsza integracja LLM |
| Osoba 3 | Eksperymenty i analiza: konfiguracje, ziarna losowości, zapis wyników, metryki, wykresy, statystyka |

Wszyscy członkowie zespołu powinni wspólnie ustalić:
- definicje modelu;
- pytania i hipotezy badawcze;
- katalog akcji;
- interfejsy między modułami;
- protokół eksperymentalny.

Interfejsy modułów należy uzgodnić przed równoległą implementacją. Osoba odpowiedzialna za analizę powinna pracować od początku, a nie dopiero po zakończeniu kodowania.

**[DO UZUPEŁNIENIA]**
- Imiona członków zespołu i przypisanie ról:
- Kto odpowiada za integrację:
- Jak będziecie prowadzić repozytorium i przegląd kodu:
- Jak często będą odbywać się spotkania:

---

# 13. Oczekiwane rezultaty

Planowane rezultaty końcowe:
1. Działający silnik abstrakcyjnej symulacji agentów AI.
2. Co najmniej jedna dobrze przetestowana strategia regułowa.
3. Porównanie z drugą strategią oraz — jeśli będzie wykonalne — agentem LLM.
4. Oddzielny moduł systemu obronnego z mierzalnymi parametrami.
5. Powtarzalny zestaw eksperymentów i zapis danych na poziomie pojedynczych przebiegów.
6. Raport z metrykami, wykresami, analizą statystyczną i ograniczeniami modelu.
7. Dokumentacja architektury, uruchomienia, testów i konfiguracji.
8. Opcjonalny eksperyment optymalizacji strategii regułowej algorytmem genetycznym.

Wartość projektu ma wynikać przede wszystkim z rzetelnego porównania metod decyzyjnych w kontrolowanych warunkach, analizy kompromisów między skutecznością a kosztem oraz sprawdzenia wpływu ograniczeń środowiska i obrony.

---

# 14. Ograniczenia i ryzyka

Zidentyfikowane w materiałach ryzyka:
- Wyniki dotyczą zdefiniowanej symulacji i nie dowodzą, że agent zachowa się identycznie w rzeczywistym systemie.
- LLM może generować niespójne lub niepoprawne decyzje, a jego wyniki mogą być zmienne nawet przy temperaturze 0.
- Wywołania LLM generują koszt i opóźnienie.
- Nierówny zakres obserwacji agentów może zafałszować porównanie.
- Algorytm genetyczny może przeuczyć się do scenariuszy treningowych.
- Zbyt mała liczba powtórzeń może prowadzić do niepewnych wniosków.
- Zbyt rozbudowany model lub zbyt wiele technologii może utrudnić ukończenie projektu w jednym semestrze.
- Wspólne ziarno losowości nie zawsze zapewnia identyczną sekwencję zdarzeń dla agentów wykonujących różne akcje.

**[DO UZUPEŁNIENIA]**
- Jakie ograniczenia czasowe i sprzętowe ma zespół?
- Czy prowadzący określił wymagane elementy lub minimalny zakres projektu?
- Jakie ryzyka są najważniejsze w kontekście Waszego zespołu?

---

# 15. Literatura i materiały odniesienia

Poniższa lista została przepisana z dostarczonego pliku `state_of_the_art.md`. Zawiera źródła wskazane w materiałach oraz krótką informację, do jakiej części projektu mogą być przydatne. Nie oznacza to, że wszystkie pozycje muszą zostać szczegółowo przeczytane.

## 15.1. Sandboxy i abstrakcyjne symulatory cyberbezpieczeństwa

1. Marchand R. i in., *Quantifying Frontier LLM Capabilities for Container Sandbox Escape* (2026).  
   https://arxiv.org/abs/2603.02277  
   Praca wyjściowa dotycząca oceny zdolności LLM w zadaniach sandbox escape. W projekcie może służyć jako motywacja i punkt odniesienia, ale rzeczywiste sandboxy pozostają poza zakresem implementacji.

2. Standen M. i in., *CybORG: A Gym for the Development of Autonomous Cyber Agents* (2021).  
   https://arxiv.org/abs/2108.09118  
   Wzorzec środowiska i wspólnego interfejsu agentów.

3. Schwartz J., Kurniawati H., *Autonomous Penetration Testing using Reinforcement Learning* (2019).  
   https://arxiv.org/abs/1905.05965  
   Punkt odniesienia dla formalizacji MDP/POMDP i częściowej obserwowalności.

4. *CyberBattleSim* — Microsoft.  
   https://github.com/microsoft/CyberBattleSim  
   Wzorzec abstrakcyjnego środowiska oraz prostego, stochastycznego systemu obronnego.

5. *YAWNING-TITAN* — Dstl.  
   https://github.com/dstl/YAWNING-TITAN  
   Przykład abstrakcyjnej symulacji grafowej; repozytorium wskazane w materiałach jako zarchiwizowane.

## 15.2. Agenci LLM i benchmarki

6. Yao S. i in., *ReAct: Synergizing Reasoning and Acting in Language Models* (2022).  
   https://arxiv.org/abs/2210.03629  
   Wzorzec interakcji agenta LLM: obserwacja, rozumowanie i akcja.

7. Liu X. i in., *AgentBench: Evaluating LLMs as Agents* (2023; ICLR 2024).  
   https://arxiv.org/abs/2308.03688  
   Wzorzec protokołu oceny agentów w wielu środowiskach.

8. Zhou S. i in., *WebArena: A Realistic Web Environment for Building Autonomous Agents* (2023).  
   https://arxiv.org/abs/2307.13854  
   Przykład powtarzalnego środowiska i funkcjonalnej oceny sukcesu.

9. Park J. S. i in., *Generative Agents: Interactive Simulacra of Human Behavior* (2023).  
   https://arxiv.org/abs/2304.03442  
   Przykład połączenia agentów LLM z symulacją agentową.

10. Wang L. i in., *A Survey on Large Language Model based Autonomous Agents* (2023; wersja v7 z 2025).  
    https://arxiv.org/abs/2308.11432  
    Przegląd architektur agentów LLM i metod ich oceny.

11. Gao C. i in., *Large Language Models Empowered Agent-based Modeling and Simulation: A Survey and Perspectives* (2023).  
    https://arxiv.org/abs/2312.11970  
    Przegląd na styku agentów LLM i modelowania agentowego.

## 15.3. Algorytmy ewolucyjne

12. Fortin F.-A. i in., *DEAP: Evolutionary Algorithms Made Easy*, JMLR 13 (2012), s. 2171–2175.  
    https://www.jmlr.org/beta/papers/v13/fortin12a.html  
    Podstawa wykorzystania biblioteki DEAP.

13. Deb K. i in., *A fast and elitist multiobjective genetic algorithm: NSGA-II* (2002).  
    https://doi.org/10.1109/4235.996017  
    Metoda optymalizacji wielokryterialnej, jeżeli nie chcemy łączyć wszystkich wyników w jedną funkcję fitness.

14. Salimans T. i in., *Evolution Strategies as a Scalable Alternative to Reinforcement Learning* (2017).  
    https://arxiv.org/abs/1703.03864  
    Dodatkowy kontekst dla optymalizacji ewolucyjnej.

## 15.4. Metodologia symulacji i walidacja

15. Grimm V. i in., *The ODD Protocol for Describing Agent-Based and Other Simulation Models: A Second Update to Improve Clarity, Replication, and Structural Realism*, JASSS 23(2), 2020, art. 7.  
    https://www.jasss.org/23/2/7.html  
    Protokół ODD do opisu celu, bytów, zmiennych, procesów, harmonogramu, inicjalizacji i podmodeli.

16. Sargent R. G., *Verification and validation of simulation models*, Journal of Simulation 7(1), 2013, s. 12–24.  
    https://ics.uu.nl/docs/vakken/msosi/VerificationValidationSargent.pdf  
    Metody weryfikacji i walidacji modeli symulacyjnych.

17. ten Broeke G., van Voorn G., Ligtenberg A., *Which Sensitivity Analysis Method Should I Use for My Agent-Based Model?*, JASSS 19(1), 2016, art. 5.  
    https://doi.org/10.18564/jasss.2857  
    Wskazówki dotyczące analizy wrażliwości, w tym OFAT.

18. Towers M. i in., *Gymnasium: A Standard Interface for Reinforcement Learning Environments* (2024).  
    https://arxiv.org/abs/2407.17032  
    Wzorzec interfejsu środowiska (`reset`, `step`, obserwacja, `terminated`, `truncated`).

19. *Mesa 3: Agent-based modeling with Python in 2025* (2025).  
    https://joss.theoj.org/papers/10.21105/joss.07668  
    Dokumentacja frameworku ABM, przydatna w razie rozszerzenia projektu.

## 15.5. Statystyka eksperymentów

20. Miller E., *Adding Error Bars to Evals: A Statistical Approach to Language Model Evaluations* (2024).  
    https://arxiv.org/abs/2411.00640  
    Przedziały ufności, błędy standardowe i porównywanie agentów na tych samych zadaniach.

---

# 16. Otwarte decyzje — lista do wspólnego ustalenia

Poniższa lista zbiera kwestie, których nie da się jednoznacznie rozstrzygnąć na podstawie dostarczonych materiałów.

- [ ] Dokładny cel agenta i formalna definicja sukcesu.
- [ ] Liczba, rodzaje i zależności między zasobami.
- [ ] Poziomy uprawnień i sposób ich reprezentacji.
- [ ] Ostateczny katalog akcji wraz z parametrami, kosztami i czasem.
- [ ] Zakres obserwacji agenta i stopień częściowej obserwowalności.
- [ ] Dokładny model przejść między stanami i parametry losowe.
- [ ] Warunki zakończenia oraz rozróżnienie wykrycia, alertu, zatrzymania i blokady.
- [ ] Dokładna polityka systemu obronnego i jego warianty.
- [ ] Czynniki eksperymentalne i ich poziomy.
- [ ] Ostateczny zestaw hipotez.
- [ ] Czy agent LLM zostanie wdrożony, a jeśli tak — jaki model i API.
- [ ] Czy algorytm genetyczny zostanie wdrożony.
- [ ] Liczba scenariuszy i powtórzeń.
- [ ] Sposób porównywania strategii na wspólnych warunkach losowych.
- [ ] Ograniczenia czasowe, sprzętowe i finansowe.
- [ ] Podział ról w zespole.

---

# 17. Proponowana kolejność dalszych prac

1. Uzupełnić sekcje 3–4: zasoby, uprawnienia, cel, akcje i obronę.
2. Na tej podstawie zdefiniować formalnie stan, obserwację, akcje, przejścia i warunki zakończenia.
3. Ustalić minimalny zestaw scenariuszy i czynników eksperymentalnych.
4. Zatwierdzić metryki i protokół eksperymentalny.
5. Dopiero potem przygotować repozytorium i implementować minimalny prototyp.
6. Najpierw uruchomić i zwalidować środowisko z agentem regułowym.
7. Dopiero po uzyskaniu stabilnego baseline'u dodawać LLM i ewentualnie GA.

**Zasada nadrzędna:** najpierw precyzyjny, testowalny model, potem kod. Nie należy rozszerzać projektu o kolejne technologie, dopóki nie wiadomo, jaką konkretną potrzebę mają rozwiązać.
