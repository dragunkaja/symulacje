# Symulacja naruszenia środowiska sandbox przez agentów AI

**Porównanie strategii regułowych, agentów LLM i strategii optymalizowanych algorytmem genetycznym**  
Projekt semestralny z przedmiotu *Symulacje systemów dyskretnych*.

> Projekt badawczy i symulacyjny. Środowisko ma charakter abstrakcyjny: nie uruchamiamy prawdziwych exploitów, nie testujemy rzeczywistych systemów i nie wykonujemy operacji na zewnętrznej infrastrukturze.

## Cel projektu

Celem jest zbudowanie kontrolowanego, powtarzalnego symulatora środowiska sandbox, w którym można porównywać różne strategie podejmowania decyzji przez agentów AI. Badamy, jak rodzaj strategii oraz parametry środowiska wpływają na osiągnięcie celu, koszt działania i wykrywalność agenta.

Najważniejsze pytanie badawcze:

**Który agent najskuteczniej osiąga cel w abstrakcyjnym środowisku sandbox i jakie cechy środowiska wpływają na jego skuteczność?**

### Pytania badawcze

- **RQ1 – zależność od środowiska:** Czy ranking strategii pozostaje taki sam w różnych konfiguracjach środowiska?
- **RQ2 – odporność:** Które cechy środowiska najmocniej obniżają skuteczność wszystkich agentów?
- **RQ3 – specyficzność:** Które cechy środowiska szkodzą jednej strategii bardziej niż pozostałym?
- **RQ4 – kompromis:** Jak wygląda kompromis między skutecznością, kosztem i wykrywalnością? Czy można wskazać rozwiązania niezdominowane na froncie Pareto?

## Zakres i model środowiska

Środowisko jest abstrakcyjnym modelem probabilistycznym. „Słabość” oznacza parametr określający prawdopodobieństwo powodzenia akcji, a nie rzeczywistą podatność ani instrukcję jej wykorzystania.

W projekcie uwzględniamy cztery czynniki środowiska:

| Czynnik | Warianty | Znaczenie |
|---|---|---|
| **E1 – klasa słabości** | błąd konfiguracji, nadmiar uprawnień, wada komponentu | Określa klasę abstrakcyjnej słabości i związane z nią parametry powodzenia akcji. |
| **E2 – głębokość** | 1, 3 lub 5 kroków do celu | Określa liczbę postępów potrzebnych do osiągnięcia celu. |
| **E3 – monitorowanie** | wyłączone / włączone | Określa, czy działa mechanizm alertów, wykrywania i blokowania. |
| **E4 – budżet kroków** | niski / wysoki | Ogranicza liczbę akcji dostępnych agentowi. Konkretne limity należy ustalić w konfiguracji eksperymentu. |

Iloczyn wariantów daje **36 konfiguracji środowiska (3 × 3 × 2 × 2)**. Każdy wariant powinien być opisany w pliku konfiguracyjnym, a nie zaszyty na stałe w logice symulatora.

Wartości liczbowe pokazane w prezentacji – np. prawdopodobieństwa powodzenia 0,70 / 0,50 / 0,25, próg alertu 0,5 czy przykładowy budżet 10 kroków – są **wartościami ilustracyjnymi**, a nie zatwierdzonym zestawem parametrów eksperymentu.

## Porównywane strategie

Wszystkie strategie korzystają z tego samego interfejsu, otrzymują tę samą obserwację i działają w tych samych scenariuszach.

| Strategia | Sposób działania | Rola w eksperymencie |
|---|---|---|
| **A. RuleAgent** | Ręcznie zaprojektowane reguły, priorytety i parametr określający skłonność do ryzyka. | Baseline, czyli punkt odniesienia dla pozostałych metod. |
| **B. LLMAgent** | Otrzymuje opis obserwacji i katalog dozwolonych akcji; zwraca wybór w ustrukturyzowanym formacie JSON. Odpowiedź jest walidowana. | Sprawdzenie, czy decyzje modelu językowego poprawiają planowanie i dobór akcji. |
| **C. GeneticAgent / GA-tuned RuleAgent** | Algorytm genetyczny optymalizuje parametry agenta regułowego A. | Sprawdzenie, czy automatyczne strojenie poprawia wynik baseline. To nie jest niezależny od RuleAgent typ polityki – GA dostraja jego parametry. |

Wspólny cykl działania:

`obserwacja → choose_action(observation) → walidacja akcji → step(action) → wynik i log`

Agent **proponuje** akcję, ale nie zmienia samodzielnie stanu środowiska. Walidacja i wszystkie skutki akcji należą do silnika symulacji. Niepoprawne odpowiedzi LLM powinny być rejestrowane jako `invalid_action`; zasady ponowienia lub użycia akcji zastępczej trzeba ustalić i stosować jednakowo we wszystkich eksperymentach.

### Katalog akcji w pierwszym modelu

- `inspect` – abstrakcyjne rozpoznanie stanu środowiska,
- `escalate` – abstrakcyjna akcja zwiększająca postęp i ryzyko,
- `wait` – oczekiwanie, które może obniżać ryzyko,
- `stop` – zakończenie działania agenta.

Są to symbole w modelu symulacyjnym, a nie komendy systemowe ani rzeczywiste techniki cyberbezpieczeństwa.

### Rozszerzenia poza pierwszą wersją

W prezentacji wskazano jako możliwy dalszy kierunek współpracę wielu agentów. Nie należy jednak mieszać tego rozszerzenia z pierwszym eksperymentem, którego celem jest porównanie trzech strategii w kontrolowanych warunkach. Dokument state of the art wymienia też widoczność słabości jako dodatkowy czynnik, ale nie należy ona do bazowego układu 36 konfiguracji E1–E4. Oba pomysły warto rozważyć dopiero po uruchomieniu i zwalidowaniu wersji bazowej.

## Architektura symulatora

Podstawowy podział odpowiedzialności:

1. **Environment** przechowuje stan, generuje obserwację, wykonuje akcję, aktualizuje postęp i ryzyko oraz obsługuje mechanizm obronny.
2. **Agent** otrzymuje wyłącznie obserwację i zwraca propozycję akcji przez `choose_action(observation)`.
3. **Simulation runner** prowadzi pojedynczy przebieg lub serię przebiegów i zapisuje wyniki.
4. **Experiment layer** uruchamia agentów na zestawie konfiguracji i ziaren losowych.
5. **Analysis** agreguje wyniki, liczy statystyki i przygotowuje wykresy.

Docelowy kontrakt środowiska jest inspirowany interfejsem Gymnasium:

- `reset(seed)` – inicjalizacja scenariusza,
- `observe()` – zwrócenie obserwacji dostępnej agentowi,
- `step(action)` – walidacja i wykonanie abstrakcyjnej akcji,
- `terminated` – zakończenie po osiągnięciu celu lub blokadzie,
- `truncated` – zakończenie po wyczerpaniu budżetu albo limitu kroków,
- `info` – dodatkowe dane do logowania i analizy.

Stan wewnętrzny środowiska i obserwacja agenta powinny być oddzielone. W proponowanym modelu agent widzi m.in. `known`, `progress`, `risk` i `steps_left`; nie musi znać wszystkich wewnętrznych parametrów środowiska.

## Metryki

W każdym przebiegu należy zapisać co najmniej:

| Metryka | Opis |
|---|---|
| `success` | Czy agent osiągnął cel. |
| `detected` | Czy działanie agenta zostało wykryte. |
| `blocked` | Czy mechanizm obronny zablokował działanie. |
| `steps` | Liczba wykonanych kroków. |
| `simulation_cost` | Łączny koszt akcji według modelu symulacyjnego. |
| `invalid_actions` | Liczba niepoprawnych decyzji agenta, szczególnie istotna dla LLM. |
| `api_cost` | Koszt wywołań modelu LLM, jeśli występuje. |
| `latency` / `tokens` | Czas odpowiedzi oraz liczba tokenów dla agenta LLM, jeśli dostawca udostępnia te dane. |

Wyniki powinny być zapisywane na poziomie pojedynczego przebiegu, aby można było je później ponownie agregować i analizować.

## Metodologia eksperymentów

- Porównujemy agentów na wspólnych konfiguracjach środowiska i tych samych zestawach ziaren losowych.
- Losowość środowiska, obrony i agenta warto rozdzielić na osobne strumienie. Dla porównań można wcześniej generować losowania scenariusza i odtwarzać je w kolejnych eksperymentach. Samo użycie tego samego `seed` nie gwarantuje identycznej sekwencji zdarzeń, gdy agenci wykonują inne akcje.
- Najpierw wykonujemy pilotaż, a następnie ustalamy liczbę przebiegów na podstawie wymaganej precyzji. Dokument state of the art wskazuje około 100 przebiegów jako orientacyjne minimum do wstępnych oszacowań; dla przedziału ufności proporcji o połowie szerokości około ±0,05, w najgorszym przypadku, potrzeba około 385 przebiegów na konfigurację.
- Dla GA oddzielamy ziarna treningowe od testowych. Wynik końcowy raportujemy na ziarnach niewykorzystanych podczas optymalizacji.
- Dla LLM zapisujemy dokładny identyfikator modelu, temperaturę, prompt, odpowiedź, wynik walidacji, opóźnienie i tokeny. Nie zakładamy pełnej deterministyczności nawet przy temperaturze 0.
- Zaczynamy od analizy wrażliwości OFAT, czyli zmiany jednego czynnika naraz.

Planowane metody analizy obejmują przedziały ufności Wilsona dla proporcji, test McNemara dla sparowanych wyników binarnych, korektę Holma przy wielu porównaniach oraz regresję logistyczną do badania interakcji strategii z czynnikami środowiska. Kompromis między sukcesem, kosztem i wykryciem można analizować z użyciem frontu Pareto.

## State of the art i podstawa metodologiczna

Pełniejszy przegląd literatury, notatki i mapowanie źródeł na elementy projektu znajdują się w [docs/state-of-the-art.md](docs/state-of-the-art.md).

Najważniejsze inspiracje:

- [SandboxEscapeBench](https://proceedings.mlr.press/v306/marchand26a.html) – motywacja problemu oraz klasy słabości i poziomy trudności; w naszym projekcie wykorzystujemy wyłącznie abstrakcyjne parametry, bez technik ataku.
- [CyberBattleSim](https://github.com/microsoft/CyberBattleSim), [NASim](https://github.com/Jjschwartz/NetworkAttackSimulator) i [CybORG](https://arxiv.org/abs/2108.09118) – wzorce abstrakcyjnego środowiska, obrony i wspólnego interfejsu agentów.
- [ReAct](https://arxiv.org/abs/2210.03629), [AgentBench](https://arxiv.org/abs/2308.03688) i [WebArena](https://arxiv.org/abs/2307.13854) – inspiracje dla agenta LLM oraz powtarzalnej ewaluacji.
- [DEAP](https://deap.readthedocs.io/) i [NSGA-II](https://doi.org/10.1109/4235.996017) – optymalizacja parametrów i analiza kompromisów wielokryterialnych.
- [ODD Protocol](https://www.jasss.org/23/2/7.html) – struktura opisu modelu symulacyjnego.
- [Sargent](https://ics.uu.nl/docs/vakken/msosi/VerificationValidationSargent.pdf) – podejście do weryfikacji i walidacji modelu.

## Plan implementacji

Projekt rozwijamy etapami. Kolejność pozwala najpierw uzyskać działającą i testowalną symulację, a dopiero później podłączać kolejne strategie.

- [ ] **Etap 0 – fundament repozytorium:** struktura projektu, środowisko Python, podstawowe testy i konfiguracja CI.
- [ ] **Etap 1 – model środowiska:** stan, obserwacja, akcje, `reset`, `step`, budżet, ryzyko i obrona.
- [ ] **Etap 2 – RuleAgent:** pierwsza strategia baseline i testy pojedynczego przebiegu.
- [ ] **Etap 3 – eksperymenty bazowe:** 36 konfiguracji, wiele ziaren, zapis wyników i podstawowe wykresy.
- [ ] **Etap 4 – LLMAgent:** adapter dostawcy, prompt, walidacja JSON, obsługa błędów i logowanie kosztu.
- [ ] **Etap 5 – algorytm genetyczny:** optymalizacja parametrów RuleAgent na ziarnach treningowych i ocena na testowych.
- [ ] **Etap 6 – analiza i raport:** przedziały ufności, testy statystyczne, analiza wrażliwości i front Pareto.
- [ ] **Etap 7 – dokumentacja końcowa:** opis modelu wg ODD, walidacja, wyniki, ograniczenia i prezentacja końcowa.

Szczegółowy podział prac, kryteria ukończenia etapów i sposób przygotowywania prezentacji postępów opisuje [docs/PROJECT_PLAN.md](docs/PROJECT_PLAN.md).

## Proponowana struktura repozytorium

```text
.
├── README.md
├── CONTRIBUTING.md
├── pyproject.toml                 # konfiguracja projektu i narzędzi Python
├── requirements.txt               # zależności, jeśli zespół wybierze ten sposób
├── configs/                       # konfiguracje 36 scenariuszy i eksperymentów
├── docs/
│   ├── state-of-the-art.md         # przegląd literatury
│   ├── PROJECT_PLAN.md             # etapy, zadania i prezentacje postępów
│   └── decisions/                  # uzasadnione decyzje architektoniczne (ADR)
├── src/
│   └── sandbox_sim/
│       ├── agents/                 # interfejs i implementacje agentów
│       ├── environment/            # stan, scenariusz, przejścia i obrona
│       ├── simulation/             # pojedyncze i seryjne przebiegi
│       ├── experiments/            # uruchamianie porównań
│       └── analysis/               # statystyki i wykresy
├── tests/                          # testy jednostkowe i integracyjne
├── examples/                       # krótkie przykłady uruchomienia
├── reports/
│   ├── presentations/             # prezentacje z kolejnych etapów
│   └── figures/                    # wybrane wykresy do raportów
└── results/                        # wyniki eksperymentów (duże pliki poza Git)
    ├── raw/
    └── processed/
```

Struktura jest docelowa – katalogi można dodawać w miarę implementacji. Nie twórzcie pustych modułów tylko po to, aby od razu odwzorować całe drzewo.

## Współpraca

Zasady pracy na gałęziach, Pull Requestów i przeglądu kodu opisuje [CONTRIBUTING.md](CONTRIBUTING.md). Szczegółowy plan etapów i prezentacji postępów znajduje się w [docs/PROJECT_PLAN.md](docs/PROJECT_PLAN.md).

## Zespół

- Aleksandra Dousa
- Kaja Dragun
- Julia Dorobis

## Status

Projekt jest rozwijany etapami. Zakres koncepcyjny i plan badań opisują prezentacja projektu oraz dokument state of the art; szczegóły implementacji, parametry eksperymentów i wyniki będą uzupełniane w kolejnych iteracjach.
