# hej


# KONTEKST PROJEKTU — SYMULACJA UCIECZKI AGENTÓW AI I PORÓWNANIE STRATEGII DECYZYJNYCH

## 1. Informacje ogólne i kontekst akademicki

Pracujemy nad całosemestralnym projektem informatycznym realizowanym przez trzyosobowy zespół studentów trzeciego roku Informatyki. Projekt jest związany z symulacją systemów dyskretnych i powinien wykorzystywać poprawną metodologię eksperymentalną, uzasadnione modele oraz literaturę naukową. Oczekiwanym rezultatem jest działająca implementacja, eksperymenty, analiza wyników, dokumentacja techniczna i wnioski.

Zespół zna Pythona i podstawy programowania obiektowego. Projekt powinien być ambitny pod względem modelowania, eksperymentów i analizy, ale wykonalny w jednym semestrze bez konieczności trenowania dużych modeli AI od podstaw.

**Roboczy tytuł:**

„Symulacja ucieczki agentów AI — porównanie strategii regułowych, modeli językowych i metod optymalizacji”.

**Główna idea:** stworzyć kontrolowane środowisko symulacyjne, w którym autonomiczni agenci próbują osiągnąć określony cel w warunkach ograniczonego dostępu do zasobów, monitorowania i mechanizmów obronnych. Następnie porównać skuteczność i zachowanie różnych metod podejmowania decyzji.

Pojęcie „ucieczki” należy rozumieć abstrakcyjnie: agent próbuje uzyskać dostęp do określonego zasobu lub osiągnąć stan, który w modelu uznajemy za niedozwolony. Projekt nie polega na opracowywaniu rzeczywistych exploitów, omijaniu zabezpieczeń systemów operacyjnych ani testowaniu prawdziwych mechanizmów sandbox escape. Wszystkie działania są reprezentowane przez bezpieczne, z góry zdefiniowane akcje w symulacji.

## 2. Problem badawczy i motywacja

Wraz z rozwojem dużych modeli językowych (LLM) pojawia się pytanie, czy agenci wykorzystujący takie modele zachowują się inaczej niż systemy oparte na prostych regułach. Modele językowe mogą interpretować kontekst i tworzyć plany, ale są również bardziej kosztowne, mogą generować niespójne decyzje i nie zawsze wybierają działanie odpowiednie do sytuacji.

Celem projektu nie jest z góry wykazanie przewagi LLM. Chcemy empirycznie sprawdzić, w jakich warunkach poszczególne strategie działają lepiej i jakie są kompromisy między skutecznością, kosztem, czasem działania i podatnością na wykrycie.

### Główne pytanie badawcze

Jak rodzaj strategii decyzyjnej agenta wpływa na prawdopodobieństwo osiągnięcia celu, liczbę wykonanych działań, czas działania i wykrywalność w symulowanym środowisku z ograniczeniami i mechanizmami obronnymi?

### Pytania szczegółowe

1. Jakie różnice występują między agentem regułowym a agentem wykorzystującym LLM w tych samych warunkach?
2. Jak zmieniają się wyniki wraz ze wzrostem restrykcyjności środowiska i skuteczności mechanizmów obronnych?
3. Czy bardziej złożona strategia uzasadnia dodatkowy koszt obliczeniowy i czasowy?
4. Czy algorytm genetyczny może poprawić skuteczność agenta regułowego przez automatyczne dostrajanie jego parametrów?
5. Jak stabilne są wyniki poszczególnych metod przy zmianie losowych warunków początkowych?

### Hipotezy do weryfikacji

- H1: Skuteczność agenta zależy od rodzaju strategii oraz poziomu ograniczeń środowiska.
- H2: Agent LLM może lepiej dostosowywać decyzje do zmiennego kontekstu, ale nie musi osiągać wyższego współczynnika sukcesu niż dobrze zaprojektowany agent regułowy.
- H3: Zwiększenie restrykcyjności systemu obronnego zmniejsza współczynnik sukcesu agentów, choć skala efektu zależy od strategii.
- H4: Optymalizacja parametrów reguł może poprawić wyniki względem ręcznie zdefiniowanego baseline'u, ale skuteczność tej poprawy należy zweryfikować na niezależnych scenariuszach testowych.

Hipotezy powinny zostać doprecyzowane po zdefiniowaniu modelu, tak aby każda miała mierzalne zmienne i możliwą do przeprowadzenia procedurę weryfikacji.

## 3. Model symulowanego środowiska

Środowisko ma być abstrakcyjnym systemem składającym się z zasobów, uprawnień, reguł przejść pomiędzy stanami i mechanizmów kontroli dostępu.

Przykładowo system może zawierać kilka logicznych zasobów, z których część jest dostępna, a część chroniona. Agent obserwuje wybrane elementy stanu, podejmuje decyzję, a środowisko ocenia jej rezultat. System obronny analizuje zdarzenia i może generować alert lub blokować dalsze działania.

Model powinien mieć następujące elementy:

### 3.1. Stan środowiska

Stan może być reprezentowany przez strukturę danych zawierającą:

- zbiór zasobów i ich poziomy dostępu;
- aktualne uprawnienia agenta;
- stan poszczególnych zabezpieczeń;
- poziom monitorowania;
- licznik działań i dostępny budżet;
- historię istotnych zdarzeń;
- stan końcowy symulacji.

Stan środowiska powinien być kontrolowany przez silnik symulacji. Agent nie może bezpośrednio zmieniać uprawnień, modyfikować stanu ochrony ani samodzielnie oznaczać własnej akcji jako skutecznej.

### 3.2. Zbiór dozwolonych akcji

Agent nie generuje dowolnego kodu. Wybiera jedną z akcji dostępnych w abstrakcyjnym katalogu, np.:

- odczyt informacji o dostępnym zasobie;
- sprawdzenie dostępności określonego zasobu;
- wykonanie dozwolonej operacji;
- próba wykonania operacji wymagającej wyższych uprawnień;
- oczekiwanie lub zakończenie działania.

Są to wyłącznie operacje symulacyjne. Ich skutki definiuje model, a nie rzeczywisty system operacyjny.

Każda akcja ma określony typ, koszt, czas wykonania i warunki dopuszczalności. Wynik działania jest obliczany przez środowisko.

### 3.3. Warunki zakończenia

Symulacja kończy się, gdy:

- agent osiągnie zdefiniowany cel;
- agent zostanie zablokowany;
- system obronny doprowadzi do zatrzymania agenta;
- agent wyczerpie limit działań lub budżet;
- zostanie osiągnięty maksymalny czas symulacji.

Należy jednoznacznie rozdzielić sukces agenta, wykrycie przez system, faktyczną blokadę oraz zwykłe wyczerpanie limitu. Wykrycie nie musi automatycznie oznaczać blokady.

### 3.4. System obronny

System obronny powinien być osobnym komponentem, niezależnym od strategii agenta. Może korzystać z prostych reguł, progów ryzyka lub punktacji zdarzeń.

Przykładowe parametry:

- prawdopodobieństwo wykrycia zdarzenia określonego typu;
- próg ryzyka uruchamiający alert;
- prawdopodobieństwo blokady po wykryciu;
- koszt monitorowania;
- liczba fałszywych alarmów.

W pierwszym prototypie wystarczą dwa warianty obrony:

1. **Baseline:** środowisko sprawdza dozwolone operacje, ale nie stosuje dodatkowego monitorowania zachowania agenta.
2. **Monitorowana obrona:** analizuje zdarzenia, nalicza ryzyko, generuje alerty i może blokować agenta zgodnie z ustaloną polityką.

Mechanizmy obronne muszą być takie same dla porównywanych agentów w ramach danego eksperymentu.

## 4. Porównywane modele decyzyjne

Architektura ma umożliwiać podłączanie różnych strategii do tego samego środowiska bez modyfikowania silnika symulacji.

### Model A — agent regułowy

Agent podejmuje decyzje na podstawie ręcznie zdefiniowanych reguł, warunków i priorytetów.

Przykładowa logika:

- jeśli cel został osiągnięty, zakończ;
- jeśli agent ma dostęp do informacji wymaganej do następnego kroku, wybierz odpowiednią akcję;
- jeśli nie ma wystarczających informacji, wybierz akcję diagnostyczną;
- jeśli ryzyko przekracza określony próg, wybierz zachowanie przewidziane przez strategię;
- jeśli nie ma dostępnej akcji, zakończ działanie.

Reguły powinny być proste, jawne i możliwe do wyjaśnienia. Warto stworzyć dwa warianty baseline'u, jeśli pozwoli na to czas: prosty agent z priorytetami oraz agent heurystyczny wykorzystujący więcej informacji o stanie.

Rola: punkt odniesienia dla pozostałych metod.

### Model B — agent oparty na LLM

Agent otrzymuje tekstowy opis obserwowanego stanu, dostępnych akcji i celu, po czym wybiera akcję z ustalonego katalogu.

Model językowy nie steruje bezpośrednio silnikiem symulacji. Jego odpowiedź jest parsowana, walidowana i przekazywana do środowiska jako propozycja decyzji.

Wymagane elementy:

- stały format promptu;
- jawna lista dozwolonych akcji;
- ustrukturyzowany format odpowiedzi, najlepiej JSON;
- walidacja nazwy akcji i parametrów;
- obsługa błędnych lub niekompletnych odpowiedzi;
- ograniczenie liczby wywołań i czasu odpowiedzi;
- zapis wersji modelu, konfiguracji, odpowiedzi, opóźnienia i kosztu.

Przykładowy schemat odpowiedzi:

`{"action": "inspect_resource", "target": "resource_2", "reason": "..."}`

Jest to wyłącznie schemat interfejsu. Silnik musi odrzucać niedozwolone akcje i samodzielnie obliczać ich skutki.

Aby porównanie było uczciwe, agent LLM powinien mieć taki sam dostęp do informacji jak agent regułowy albo różnice w obserwacjach muszą być jawnie zdefiniowane jako osobna zmienna eksperymentu. Nie należy przyznawać LLM dodatkowych informacji, a następnie przypisywać całej poprawy samemu modelowi.

### Model C — agent regułowy optymalizowany algorytmem genetycznym (wariant opcjonalny)

Algorytm genetyczny może optymalizować parametry istniejącego agenta regułowego, np. progi decyzyjne, priorytety lub wagi heurystyk.

Przykładowy chromosom może zawierać wektor parametrów:

`θ = [threshold_1, threshold_2, weight_1, weight_2, ...]`

Każdy osobnik reprezentuje jedną konfigurację strategii. Algorytm wykonuje iteracyjnie:

1. generowanie populacji początkowej;
2. ocenę osobników przez uruchomienie symulacji;
3. selekcję lepszych konfiguracji;
4. krzyżowanie i mutację;
5. utworzenie kolejnej generacji;
6. zatrzymanie po osiągnięciu limitu generacji lub braku poprawy.

Funkcja przystosowania powinna odzwierciedlać rzeczywisty cel badawczy, np. skuteczność z karą za koszty i wykrycie:

`fitness = w_s * success_rate - w_d * detection_rate - w_c * normalized_cost`

Wagi muszą zostać uzasadnione, a składowe odpowiednio znormalizowane. Można też zastosować ocenę wielokryterialną, zamiast sprowadzać wszystkie wyniki do jednej liczby.

Najważniejsze zagrożenie metodologiczne to przeuczenie do scenariuszy wykorzystanych podczas optymalizacji. Dlatego najlepsze parametry należy testować na innych ziarnach losowości i konfiguracjach niż te używane do obliczania funkcji przystosowania.

Ten wariant nie jest konieczny do ukończenia projektu. Należy go wdrażać dopiero po uzyskaniu wiarygodnego baseline'u i powtarzalnych eksperymentów.

## 5. Metody symulacji i architektura techniczna

Rekomendowany język i środowisko:

- Python 3.11 lub nowszy, zgodnie z kompatybilnością wybranych bibliotek;
- SimPy do modelowania zdarzeń i czasu symulowanego;
- NumPy do operacji numerycznych i generowania danych;
- pandas do przechowywania oraz analizy wyników;
- Matplotlib do wizualizacji;
- pytest do testów jednostkowych i integracyjnych;
- Git do kontroli wersji.

Podstawą jest **symulacja agentowa (Agent-Based Modeling, ABM)**: agent posiada stan, obserwuje środowisko i podejmuje decyzje. SimPy może obsługiwać dyskretny czas i zdarzenia, np. czas wykonania akcji, reakcje obrony i zakończenie symulacji. Należy jednak uzasadnić, czy pełny model wymaga osobnego silnika zdarzeń, czy wystarczy prosty zegar krokowy. Nie należy wprowadzać złożoności technologicznej bez korzyści dla eksperymentów.

### Proponowany podział modułów

- `config.py` — parametry środowiska i eksperymentów;
- `models.py` — struktury danych, akcje, wyniki i statusy;
- `environment.py` — stan środowiska, zasoby, uprawnienia i skutki akcji;
- `defense.py` — monitoring, punktacja ryzyka, alarmy i blokady;
- `agents.py` — interfejs strategii, agent regułowy i heurystyczny;
- `llm_agent.py` — adapter modelu językowego, walidacja odpowiedzi i rejestrowanie kosztów;
- `simulation.py` — integracja komponentów i przebieg pojedynczej symulacji;
- `metrics.py` — obliczanie wskaźników;
- `experiments.py` — powtarzanie eksperymentów, zarządzanie konfiguracjami i zapis wyników;
- `tests/` — testy jednostkowe i integracyjne;
- `notebooks/` — analiza danych i wykresy.

Każda strategia powinna implementować wspólny interfejs, np. `choose_action(observation)`. Silnik symulacji powinien być niezależny od tego, czy decyzję podjął agent regułowy, czy LLM.

## 6. Dane — źródło, struktura i generowanie

W pierwszym etapie projekt nie wymaga zewnętrznego zbioru danych treningowych. **Podstawowym źródłem danych będą kontrolowane, syntetyczne przebiegi symulacji.** Jest to uzasadnione, ponieważ modelujemy własne środowisko z formalnie określonymi regułami, a celem jest porównanie strategii przy kontrolowanych warunkach.

Dane będą generowane przez uruchamianie symulacji z różnymi parametrami i ziarnami losowości. Każdy przebieg będzie tworzył:

1. konfigurację początkową;
2. sekwencję zdarzeń;
3. wynik końcowy;
4. zestaw metryk;
5. opcjonalne logi decyzji agenta i systemu obronnego.

### 6.1. Konfiguracja scenariusza

Każdy scenariusz powinien zawierać co najmniej:

- identyfikator scenariusza;
- liczbę zasobów;
- poziom restrykcyjności dostępu;
- wariant i parametry systemu obronnego;
- limit działań;
- limit czasu symulowanego;
- parametry losowości;
- definicję celu;
- dostępne akcje i ich koszty.

Konfiguracje najlepiej przechowywać w plikach JSON lub w analogicznej, wersjonowanej formie.

### 6.2. Log pojedynczego zdarzenia

Przykładowy rekord zdarzenia może zawierać:

- `run_id` — identyfikator przebiegu;
- `step` — numer kroku;
- `sim_time` — czas symulowany;
- `agent_type` — typ strategii;
- `observation_id` — identyfikator obserwacji;
- `action_type` — typ wybranej akcji;
- `action_valid` — informacja, czy akcja była dozwolona;
- `action_success` — wynik akcji;
- `risk_score` — wynik oceny ryzyka, jeśli jest używany;
- `alert_triggered` — informacja o alercie;
- `blocked` — informacja o blokadzie;
- `action_cost` — koszt akcji;
- `decision_latency` — rzeczywisty czas podjęcia decyzji, jeżeli jest mierzony.

Należy rozdzielić czas symulowany od rzeczywistego czasu obliczeń. Są to różne wielkości i nie powinny być używane zamiennie.

### 6.3. Wynik pojedynczego przebiegu

Tabela wyników powinna zawierać jeden rekord na przebieg, np.:

- `run_id`;
- `scenario_id`;
- `agent_type`;
- `defense_type`;
- `seed`;
- `terminal_status`;
- `success` — zmienna binarna;
- `detected` — czy agent został wykryty;
- `blocked` — czy agent został zablokowany;
- `steps`;
- `simulated_time`;
- `wall_clock_time`;
- `total_cost`;
- `alert_count`;
- `invalid_action_count`;
- `llm_call_count` i `llm_cost`, jeżeli dotyczy.

Przechowywanie surowych wyników każdego przebiegu jest konieczne. Nie wolno ograniczać się do zapisywania średniej dla całego eksperymentu, ponieważ uniemożliwiłoby to rzetelną analizę rozrzutu i niepewności.

### 6.4. Kontrola jakości danych

Należy zapewnić:

- powtarzalność przez jawne zarządzanie ziarnami losowości;
- walidację konfiguracji przed uruchomieniem;
- spójność nazw statusów i typów akcji;
- brak ujemnych czasów i kosztów, jeśli model ich nie dopuszcza;
- rozdzielenie brakujących danych od wartości zero;
- zachowanie informacji o błędach i przerwanych przebiegach;
- zapis wersji kodu, konfiguracji i modelu LLM.

Wyniki LLM mogą być niestabilne nawet przy niezmienionym scenariuszu. Trzeba uwzględnić zmienność modelu, a nie zakładać, że pojedyncze powtórzenie jest reprezentatywne.

## 7. Projekt eksperymentów

Eksperymenty muszą być zaplanowane tak, aby można było oddzielić wpływ strategii agenta od wpływu parametrów środowiska i systemu obronnego.

### Etap 1 — walidacja modelu

Najpierw należy sprawdzić, czy symulacja poprawnie realizuje definicje stanu, akcji, sukcesu, wykrycia i blokady.

Należy przeprowadzić testy przypadków brzegowych, sprawdzić deterministyczność przy ustalonym ziarnie losowości i zweryfikować, czy agent nie może modyfikować stanu poza dozwolonym interfejsem.

### Etap 2 — baseline

Uruchomić agenta regułowego w kilku konfiguracjach środowiska i obrony. Na tym etapie sprawdzić, czy wyniki zmieniają się w oczekiwanym kierunku, np. czy bardziej restrykcyjne reguły dostępu wpływają na prawdopodobieństwo osiągnięcia celu.

### Etap 3 — porównanie strategii

Porównać co najmniej:

- agenta regułowego;
- agenta heurystycznego, jeśli zostanie wdrożony;
- agenta LLM.

Każdy wariant powinien być testowany na tych samych zestawach scenariuszy i porównywalnych warunkach początkowych.

### Etap 4 — wpływ systemu obronnego

Zbadać wpływ co najmniej dwóch wariantów obrony. Jeśli podstawowy model działa stabilnie, wprowadzić więcej poziomów restrykcyjności lub parametrów monitorowania.

### Etap 5 — optymalizacja, jeśli wystarczy czasu

Dodać algorytm genetyczny do optymalizacji parametrów agenta regułowego. Porównać strategię przed optymalizacją i po niej na niezależnych zestawach testowych.

### 7.1. Liczba powtórzeń

Na etapie prototypowania wystarczy kilka lub kilkanaście przebiegów, aby sprawdzić poprawność działania. W eksperymentach właściwych warto zacząć od około 100 powtórzeń na konfigurację, a następnie zwiększać liczbę na podstawie zmienności wyników i wymaganej precyzji estymacji.

Liczba 100 nie powinna być automatycznie traktowana jako wystarczająca. Dla rzadkich zdarzeń, małych różnic między modelami lub dużego rozrzutu może być koniecznie więcej powtórzeń. Należy raportować liczbę prób i niepewność oszacowań.

### 7.2. Kontrolowanie zmiennych

W porównaniu strategii należy utrzymywać stałe:

- definicję celu;
- katalog dozwolonych akcji;
- reguły środowiska;
- warunki początkowe;
- system obronny w ramach danej serii;
- limit działań i budżet;
- dostępne obserwacje, chyba że ich wpływ jest osobnym przedmiotem badania.

Jeśli środowisko wykorzystuje losowe zdarzenia, porównywanie modeli na wspólnych ziarnach losowości może poprawić porównywalność wyników. Trzeba jednak pamiętać, że wspólne ziarno nie zawsze gwarantuje identyczną sekwencję zdarzeń, jeśli modele wykonują różną liczbę kroków lub zużywają liczby losowe w innej kolejności. W razie potrzeby należy generować scenariusze z góry i odtwarzać je dla wszystkich strategii.

## 8. Metryki i analiza statystyczna

### Podstawowe metryki

**Współczynnik sukcesu**

Odsetek przebiegów, w których agent osiągnął cel:

`success_rate = liczba sukcesów / liczba wszystkich przebiegów`

**Współczynnik wykrycia**

Odsetek przebiegów, w których agent został wykryty. Trzeba jawnie ustalić mianownik, np. wszystkie przebiegi lub przebiegi, w których doszło do zdarzenia mogącego podlegać wykryciu.

**Współczynnik blokady**

Odsetek przebiegów kończących się blokadą agenta. Powinien być raportowany oddzielnie od wykrycia.

**Liczba kroków do zakończenia**

Średnia lub mediana liczby akcji przed zakończeniem przebiegu. Warto rozdzielić wyniki dla sukcesów i niepowodzeń.

**Czas symulowany**

Czas upływający w modelowanym środowisku.

**Czas rzeczywisty**

Rzeczywisty czas wykonywania symulacji lub podejmowania decyzji. Dla LLM należy osobno raportować opóźnienie wywołań modelu.

**Koszt**

Może obejmować umowny koszt akcji w symulacji, koszt monitorowania oraz rzeczywisty koszt wywołań API LLM. Składowe należy raportować osobno, zanim zostaną połączone w jeden wskaźnik.

**Liczba błędnych decyzji**

Odsetek odpowiedzi niezgodnych z formatem, nieistniejących akcji lub działań odrzuconych przez walidator.

### Analiza statystyczna

Należy prezentować nie tylko średnie, ale również rozrzut i niepewność wyników.

- Dla współczynników sukcesu i wykrycia: liczebności, odsetki oraz przedziały ufności dla proporcji.
- Dla liczby kroków, czasu i kosztu: średnie lub mediany, odchylenia standardowe lub rozstępy międzykwartylowe.
- Dla porównań strategii na wspólnych scenariuszach: analiza różnic sparowanych; wybór testu powinien zależeć od rozkładu i rodzaju zmiennej.
- Przy wielu porównaniach: kontrola ryzyka fałszywie dodatnich wyników, jeśli stosowane są testy statystyczne.

Wyniki należy przedstawiać na wykresach: porównanie współczynników sukcesu, wykresy rozkładów liczby kroków, zależność skuteczności od restrykcyjności obrony oraz kosztu od skuteczności.

Wnioski muszą wynikać z danych. Nie należy interpretować małej różnicy jako istotnej przewagi bez analizy niepewności.

## 9. State of the art i literatura

Projekt powinien uwzględniać trzy obszary badań:

1. **Agent-Based Modeling i symulacje systemów dyskretnych** — modelowanie zachowania agentów, interakcji ze środowiskiem, zdarzeń i warunków końcowych.
2. **LLM-based agents i benchmarki** — wykorzystanie modeli językowych do planowania i wyboru działań oraz metody ich oceny w kontrolowanych środowiskach.
3. **Algorytmy ewolucyjne i optymalizacja** — dostrajanie parametrów strategii przez ocenę populacji rozwiązań w powtarzalnych symulacjach.

Jako punkt wyjścia do przeglądu literatury warto rozważyć publikacje i zasoby dotyczące AgentBench, WebArena, oceny agentów językowych, symulacji agentowych wspieranych przez LLM oraz klasycznych algorytmów genetycznych.

Przegląd literatury powinien odpowiedzieć na pytania:

- Jakie benchmarki są już wykorzystywane do porównywania agentów LLM?
- Jakie metryki i protokoły eksperymentalne stosują wcześniejsze badania?
- Jakie ograniczenia mają porównania agentów o różnych możliwościach obserwacji i różnym koszcie?
- Co w naszym eksperymencie jest znane z literatury, a co stanowi specyficzny wkład implementacyjny?

Nie należy twierdzić, że samo zastosowanie LLM w symulacji jest nowatorskie. Potencjalnym wkładem jest opracowanie konkretnego środowiska, kontrolowanego protokołu porównawczego, powtarzalnego zestawu eksperymentów i analizy wpływu zabezpieczeń na zachowanie różnych strategii.

## 10. Plan implementacji

### Faza 1 — specyfikacja modelu

- Narysować diagram stanów agenta i środowiska.
- Formalnie określić cel, sukces, wykrycie, blokadę i warunki zakończenia.
- Zdefiniować katalog akcji i reguły ich oceny.
- Wybrać parametry środowiska oraz metryki.

### Faza 2 — minimalny prototyp

- Zaimplementować modele danych i konfigurację.
- Zbudować abstrakcyjne środowisko.
- Dodać agenta regułowego.
- Dodać podstawowy system obronny.
- Zaimplementować pojedynczy przebieg i logowanie zdarzeń.
- Dodać testy jednostkowe i powtarzalność wyników.

### Faza 3 — eksperymenty baseline

- Uruchamiać serie symulacji z różnymi ziarnami losowości.
- Zapisywać wyniki w CSV.
- Obliczać metryki.
- Przygotować wykresy i sprawdzić, czy model reaguje zgodnie z założeniami.

### Faza 4 — dodatkowe strategie

- Ujednolicić interfejs agenta.
- Dodać drugą strategię regułową lub heurystyczną.
- Zintegrować LLM jako opcjonalny moduł.
- Walidować wszystkie decyzje LLM i mierzyć koszt oraz opóźnienie.
- Wykonać porównanie w tych samych warunkach.

### Faza 5 — analiza i rozszerzenia

- Przeprowadzić analizę statystyczną.
- Sprawdzić wpływ parametrów środowiska i obrony.
- Opcjonalnie dodać algorytm genetyczny.
- Przygotować dokumentację, raport oraz demonstrację działania.

Jeżeli podstawowe eksperymenty nie będą wiarygodne do około ósmego tygodnia semestru, należy zrezygnować z dodatkowych modeli i skupić się na poprawności, testach, jakości danych oraz analizie.

## 11. Testowanie i walidacja

Testy jednostkowe powinny sprawdzać m.in.:

- czy środowisko prawidłowo ocenia dozwolone i niedozwolone akcje;
- czy agent nie może samodzielnie zmienić uprawnień;
- czy system obronny rozróżnia alert i blokadę;
- czy agent regułowy wybiera akcje zgodne z regułami;
- czy nieprawidłowa odpowiedź LLM jest odrzucana;
- czy symulacja kończy się we wszystkich wymaganych warunkach;
- czy czas symulowany nie cofa się;
- czy ten sam scenariusz i ziarno losowości dają powtarzalne wyniki, o ile wszystkie źródła losowości są kontrolowane;
- czy metryki są poprawne dla małych, ręcznie sprawdzonych przykładów.

Walidacja modelu powinna dodatkowo obejmować testy skrajnych konfiguracji i analizę wrażliwości: czy zmiana jednego parametru środowiska wywołuje logicznie uzasadnioną zmianę wyników? Sama zgodność kodu z testami nie dowodzi, że model dobrze reprezentuje badany problem.

## 12. Organizacja pracy zespołu

**Osoba 1 — środowisko i silnik symulacji**

Odpowiada za stan środowiska, akcje, reguły przejść, warunki zakończenia, integrację SimPy i testy silnika.

**Osoba 2 — agenci i system obronny**

Odpowiada za wspólny interfejs decyzyjny, agenta regułowego, wariant heurystyczny, mechanizmy wykrywania oraz późniejszą integrację LLM.

**Osoba 3 — eksperymenty i analiza danych**

Odpowiada za generator eksperymentów, zarządzanie konfiguracjami i ziarnami losowości, zapis wyników, metryki, wykresy i analizę statystyczną.

Wszyscy członkowie zespołu powinni wspólnie ustalić definicje modelu, protokół eksperymentalny i hipotezy. Interfejsy modułów należy uzgodnić przed równoległą implementacją.

## 13. Oczekiwane rezultaty projektu

Na koniec powinny powstać:

1. Działający silnik abstrakcyjnej symulacji agentów AI.
2. Co najmniej jedna dobrze przetestowana strategia regułowa.
3. Porównanie z drugą strategią oraz — jeśli wykonalne — agentem LLM.
4. Oddzielny moduł systemu obronnego z mierzalnymi parametrami.
5. Powtarzalny zestaw eksperymentów i zapis danych na poziomie pojedynczych przebiegów.
6. Raport z metrykami, wykresami, analizą statystyczną i ograniczeniami modelu.
7. Dokumentacja architektury, sposobu uruchomienia, testów i konfiguracji.
8. Opcjonalny eksperyment optymalizacji strategii regułowej algorytmem genetycznym.

Głównym rezultatem naukowym nie musi być nowy algorytm. Wartość projektu może wynikać z rzetelnego porównania metod decyzyjnych w kontrolowanych warunkach, pokazania kompromisów między skutecznością i kosztem oraz sprawdzenia, jak zmienia się zachowanie agentów pod wpływem ograniczeń środowiska.

## 14. Ograniczenia i zagrożenia metodologiczne

- Wyniki dotyczą zdefiniowanej symulacji i nie dowodzą, że agent zachowa się identycznie w rzeczywistym systemie.
- Zbyt prosty model środowiska może premiować konkretną strategię, dlatego należy uzasadnić wybór reguł i wykonać analizę wrażliwości.
- Różne strategie mogą otrzymywać różne informacje lub mieć różne limity obliczeniowe, co zaburza porównanie.
- Wyniki LLM mogą zależeć od wersji modelu, promptu, parametrów generowania i dostępności API.
- Optymalizacja parametrów na tych samych scenariuszach, na których ocenia się wynik, prowadzi do ryzyka przeuczenia.
- Współczynnik sukcesu nie opisuje samodzielnie jakości strategii; należy uwzględnić koszty, wykrywalność, czas i niepewność wyników.
- Liczba modeli nie powinna być ważniejsza niż jakość eksperymentu. Lepiej porównać dwa modele rzetelnie niż trzy powierzchownie.

## 15. Zakres priorytetowy i zakres opcjonalny

**Zakres wymagany:**

- abstrakcyjna symulacja dyskretna;
- agent regułowy;
- środowisko z zasobami i uprawnieniami;
- system obronny;
- logowanie przebiegów;
- powtarzalne eksperymenty;
- metryki i analiza wyników;
- testy oraz dokumentacja.

**Zakres rozszerzony:**

- dodatkowy agent heurystyczny;
- integracja LLM;
- większa liczba konfiguracji środowiska;
- analiza statystyczna różnic między strategiami.

**Zakres opcjonalny:**

- algorytm genetyczny optymalizujący parametry reguł;
- uczenie ze wzmocnieniem;
- interaktywny interfejs do uruchamiania symulacji.

Uczenie ze wzmocnieniem nie powinno być równorzędnym obowiązkowym elementem projektu, ponieważ istotnie zwiększa złożoność implementacji, dobór funkcji nagrody i analizę procesu uczenia.

## 16. Zadanie dla kolejnego etapu pracy

Na podstawie tego opisu pomóż dopracować projekt jako przedsięwzięcie akademickie z zakresu symulacji systemów dyskretnych i agentów AI.

Przy dalszej pracy:

1. Zachowaj rozróżnienie między faktami z opisu projektu, propozycjami projektowymi i założeniami wymagającymi weryfikacji.
2. Wskaż odpowiednią literaturę naukową i aktualne prace dotyczące agentów LLM, benchmarków, ABM, symulacji dyskretnych i algorytmów ewolucyjnych. Nie wymyślaj publikacji ani wyników.
3. Pomóż sformalizować model: stan, akcje, obserwacje, reguły przejść, warunki zakończenia i parametry obrony.
4. Opracuj eksperymenty, które umożliwiają weryfikację hipotez i uczciwe porównanie strategii.
5. Zaproponuj metryki, metodę analizy statystycznej i sposób prezentacji wyników.
6. Uwzględnij wykonalność w trzyosobowym zespole studentów trzeciego roku znających Pythona i podstawy OOP.
7. Oddziel wymagany zakres projektu od opcjonalnych rozszerzeń.
8. Wskazuj słabe punkty metodologiczne, ryzyko przeuczenia, ograniczenia symulacji oraz możliwe błędy w interpretacji wyników.
9. Nie zakładaj, że LLM lub algorytm genetyczny musi osiągnąć lepsze wyniki — projekt ma to sprawdzić, a nie z góry potwierdzić.
10. Traktuj środowisko jako abstrakcyjną symulację; nie proponuj implementowania rzeczywistych technik omijania zabezpieczeń.

Priorytetem jest opracowanie projektu, który ma jasne pytanie badawcze, poprawną metodologię, wykonalną implementację, wiarygodne wyniki i konkretny wkład analityczny.
