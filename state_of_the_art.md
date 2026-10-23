# State of the art: agenci AI w sandboxach (przegląd literatury i wybór modelu)

Dokument roboczy do projektu „Symulacja ucieczki agentów AI: porównanie strategii regułowych, LLM i algorytmu genetycznego".


---

## Spis treści

1. [Najbliższe prace: LLM a bezpieczeństwo i sandboxy](#1-najbliższe-prace-llm-a-bezpieczeństwo-i-sandboxy)
2. [Abstrakcyjne symulatory cyberbezpieczeństwa](#2-abstrakcyjne-symulatory-cyberbezpieczeństwa)
3. [Agenci LLM i benchmarki agentowe](#3-agenci-llm-i-benchmarki-agentowe)
4. [Algorytmy ewolucyjne](#4-algorytmy-ewolucyjne)
5. [Metodologia symulacji](#5-metodologia-symulacji)
6. [Statystyka eksperymentów](#6-statystyka-eksperymentów)
7. [Szczegóły modelowania](#7-szczegóły-modelowania)
8. [Jak wybrać model do projektu](#8-jak-wybrać-model-do-projektu)
9. [Mapa: element projektu → źródło](#10-mapa-element-projektu--źródło)

---

## 1. Najbliższe prace: LLM a bezpieczeństwo i sandboxy

### 1.1. SandboxEscapeBench (praca wyjściowa)

- Marchand R., O Cathain A., Wynne J., Giavridis P. M., Deverett S., Wilkinson J., Gwartz J., Coppock H. (UK AI Security Institute), *Quantifying Frontier LLM Capabilities for Container Sandbox Escape*, 2026.
- arXiv: <https://arxiv.org/abs/2603.02277>
- Wersja w PMLR (vol. 306): <https://proceedings.mlr.press/v306/marchand26a.html>
- Strona instytutu: <https://www.aisi.gov.uk/research/quantifying-frontier-llm-capabilities-for-container-sandbox-escape>
- Repozytorium benchmarku: <https://github.com/UKGovernmentBEIS/sandbox_escape_bench>
- **Co zawiera:** benchmark w formie CTF w narzędziu Inspect AI, z architekturą zagnieżdżonych sandboxów (zewnętrzna warstwa zawiera flagę i nie ma znanych podatności). Model zagrożenia: zmotywowany agent z dostępem do powłoki wewnątrz kontenera. Scenariusze obejmują błędy konfiguracji, błędy przydziału uprawnień, wady jądra oraz słabości środowiska uruchomieniowego i orkiestracji, z trudnością w skali 1–5. Według autorów modele niezawodnie radzą sobie z typowymi błędami konfiguracji i odsłoniętymi interfejsami sterującymi, a na trudniejszych scenariuszach osiągają niezerowy sukces.
- **Co z tego wziąć:** strukturę zmiennych środowiska (klasa słabości E1, głębokość/trudność E2) i motywację problemu. Nie bierzemy technik ataku.
- **Różnica względem naszego projektu:** oni mierzą zdolność modelu na prawdziwych środowiskach. My porównujemy strategie decyzyjne w abstrakcyjnym modelu, więc badamy planowanie i dobór akcji, nie zdolność techniczną.

### 1.2. Inne oceny zdolności cybernetycznych LLM

| Praca | Link | Co z tego wziąć |
|---|---|---|
| Zhang A. K. i in., *Cybench: A Framework for Evaluating Cybersecurity Capabilities and Risks of Language Models* (2024; 40 zadań CTF z 4 konkursów, z podzadaniami; ICLR 2025 wg strony konferencji) | <https://arxiv.org/abs/2408.08926> | Pomysł podzadań (pośrednich kroków) jako miary postępu. Analogia do naszego `progress` 0…D |
| Fang R., Bindu R., Gupta A., Kang D., *LLM Agents can Autonomously Exploit One-day Vulnerabilities* (2024) | <https://arxiv.org/abs/2404.08144> | Wynik, że opis podatności bardzo zmienia skuteczność agenta (87% z opisem CVE, 7% bez). Uzasadnia osobny czynnik „widoczność słabości" |
| Phuong M. i in., *Evaluating Frontier Models for Dangerous Capabilities* (2024) | <https://arxiv.org/abs/2403.13793> | Szerszy kontekst: cyberbezpieczeństwo jako jeden z obszarów oceny zdolności niebezpiecznych |
| Deng G. i in., *PentestGPT: An LLM-empowered Automatic Penetration Testing Tool* (2023) | <https://arxiv.org/abs/2308.06782> | Obserwacja, że LLM radzą sobie z podzadaniami, ale tracą spójny obraz całości. Uzasadnia pytanie o planowanie vs reguły |
| Greenblatt R., Shlegeris B., Sachan K., Roger F., *AI Control: Improving Safety Despite Intentional Subversion* (2023) | <https://arxiv.org/abs/2312.06942> | Kontekst „dlaczego sandbox ma znaczenie": badania nad kontrolą modeli. SandboxEscapeBench powołuje się na ten nurt |

---

## 2. Abstrakcyjne symulatory cyberbezpieczeństwa

To najbliższa metodologicznie rodzina prac, bo pokazuje, jak modelować atak i obronę **bez prawdziwych exploitów**. 

| Symulator | Źródła | Poziom abstrakcji i agenci | Co z tego wziąć |
|---|---|---|---|
| **CybORG** | Baillie C. i in., *CybORG: An Autonomous Cyber Operations Research Gym* (2020): <https://arxiv.org/abs/2002.10667><br>Standen M. i in., *CybORG: A Gym for the Development of Autonomous Cyber Agents* (2021): <https://arxiv.org/abs/2108.09118> | Agenci atakujący (red team) i broniący (blue team); symulacja i emulacja za wspólnym interfejsem | Podział na symulację i emulację; wspólny interfejs agenta niezależny od środowiska. To dokładnie nasz `choose_action(observation)` |
| **NASim** (Network Attack Simulator) | Repozytorium: <https://github.com/Jjschwartz/NetworkAttackSimulator> (autor: Jonathon Schwartz, licencja MIT; interfejs Gymnasium). Powiązana praca: Schwartz J., Kurniawati H., *Autonomous Penetration Testing using Reinforcement Learning* (2019): <https://arxiv.org/abs/1905.05965> | Symulowana sieć z podatnościami, skanami i exploitami jako akcjami abstrakcyjnymi. Tryb częściowej obserwowalności; zapory i eskalacja uprawnień w wersji 0.7.0 | Sformułowanie problemu jako MDP/POMDP; scenariusze definiowane w YAML. Wzór dla `config.py` |
| **CyberBattleSim** (Microsoft) | <https://github.com/microsoft/CyberBattleSim>, strona projektu: <https://www.microsoft.com/en-us/research/project/cyberbattlesim/> | „Wysokopoziomowa abstrakcja sieci i pojęć bezpieczeństwa"; topologia i podatności jako stałe parametry; prosty stochastyczny obrońca z zadanymi prawdopodobieństwami wykrycia i naprawy; interfejs OpenAI Gym | **Najbliższy wzór naszego systemu obronnego** (prawdopodobieństwa i skanowanie). Autorzy sami piszą, że model jest świadomie uproszczony, co jest argumentem bezpieczeństwa i spójnym z naszym podejściem |
| **YAWNING-TITAN** (Dstl) | Repozytorium: <https://github.com/dstl/YAWNING-TITAN> (repozytorium zarchiwizowane 13.03.2025; powiązana publikacja z ICML 2022 Workshop ML4Cyber: Andrew A., Spillard S., Collyer J., Dhir N., *Developing Optimal Causal Cyber-Defence Agents via Cyber Security Simulation*, wskazana w README) | Abstrakcyjna symulacja grafowa; agenci obronni kontra probabilistyczni agenci czerwoni | Pomysł abstrakcji grafowej; **nie opierajcie projektu na tym kodzie**, bo jest archiwalny |
| NASimJax | <https://arxiv.org/abs/2603.19864> (tytuł: *NASimJax: GPU-Accelerated Policy Learning Framework for Penetration Testing*; autorów nie sprawdzałam) | Przyspieszona wersja NASim do uczenia polityk | Tylko jako wskazówka, że linia NASim jest nadal rozwijana |

**Wniosek dla projektu:** istnieje ustalona tradycja abstrakcyjnych symulatorów ataku i obrony, które agenci (głównie RL) trenują na uproszczonych modelach.  **kontrolowane porównanie strategii (reguły, LLM, GA) przy systematycznie zmienianych czynnikach środowiska**

---

## 3. Agenci LLM i benchmarki agentowe

| Praca | Link | Co z tego wziąć |
|---|---|---|
| Yao S. i in., *ReAct: Synergizing Reasoning and Acting in Language Models* (arXiv 2022, wersja ICLR) | <https://arxiv.org/abs/2210.03629> | Wzorzec promptu agenta LLM: na przemian rozumowanie i akcja. Dobry punkt wyjścia dla agenta B |
| Liu X. i in., *AgentBench: Evaluating LLMs as Agents* (2023, ICLR 2024) | <https://arxiv.org/abs/2308.03688> | Osiem interaktywnych środowisk. Autorzy wiążą porażki głównie z słabym długoterminowym rozumowaniem, podejmowaniem decyzji i podążaniem za instrukcjami. Wzór protokołu porównania wielu modeli |
| Zhou S. i in., *WebArena: A Realistic Web Environment for Building Autonomous Agents* (2023) | <https://arxiv.org/abs/2307.13854> | Powtarzalne środowisko i ocena sukcesu funkcjonalna (czy zadanie wykonano). Najlepszy agent GPT-4 uzyskał 14,41% wobec 78,24% u ludzi (wg wersji v4 strony arXiv) |
| Park J. S. i in., *Generative Agents: Interactive Simulacra of Human Behavior* (2023) | <https://arxiv.org/abs/2304.03442> | Przykład agentów LLM w symulacji (pamięć, refleksja, planowanie). Pokazuje, jak łączy się LLM i ABM |
| Wang L. i in., *A Survey on Large Language Model based Autonomous Agents* (2023, wersja v7 z 2025) | <https://arxiv.org/abs/2308.11432> | Przegląd architektur i metod oceny agentów. Dobra pierwsza lektura do sekcji „state of the art" w raporcie |
| Gao C. i in., *Large Language Models Empowered Agent-based Modeling and Simulation: A Survey and Perspectives* (2023) | <https://arxiv.org/abs/2312.11970> | **Przegląd dokładnie na styku ABM i LLM**, z wyzwaniami: percepcja środowiska, generowanie akcji, ewaluacja. Dobry kandydat na główne źródło teoretyczne |

**Ramy do uruchamiania agentów LLM:** Inspect AI (UK AI Security Institute i Meridian Labs) <https://inspect.aisi.org.uk/>. Zawiera m.in. wbudowanego agenta ReAct, narzędzia, logowanie i przeglądarkę transkryptów. W naszym projekcie nie jest konieczny (LLM wybiera akcje z katalogu), ale warto zajrzeć po wzorce logowania i ewaluacji. Używają go autorzy SandboxEscapeBench.

---

## 4. Algorytmy ewolucyjne

| Źródło | Link | Co z tego wziąć |
|---|---|---|
| Fortin F.-A., De Rainville F.-M., Gardner M.-A., Parizeau M., Gagné C., *DEAP: Evolutionary Algorithms Made Easy*, JMLR 13 (2012), s. 2171–2175 | <https://www.jmlr.org/beta/papers/v13/fortin12a.html>, dokumentacja: <https://deap.readthedocs.io/> | Biblioteka Pythona do GA. Gotowe selekcje, krzyżowania, mutacje i pętla `eaSimple` |
| Deb K., Pratap A., Agarwal S., Meyarivan T., *A fast and elitist multiobjective genetic algorithm: NSGA-II*, IEEE Trans. Evol. Comput. 6(2), 2002, s. 182–197 | <https://doi.org/10.1109/4235.996017> | Gdy zamiast jednej liczby fitness chcecie front Pareto (sukces vs koszt vs wykrycie). Odpowiada na RQ4 |
| Salimans T., Ho J., Chen X., Sidor S., Sutskever I., *Evolution Strategies as a Scalable Alternative to Reinforcement Learning* (2017) | <https://arxiv.org/abs/1703.03864> | Argument, że optymalizacja ewolucyjna (bez gradientów) bywa konkurencyjna wobec RL. Uzasadnia wybór GA zamiast RL |

**Uwaga:** podręczników (np. Eiben i Smith o obliczeniach ewolucyjnych) nie weryfikowałam. Sprawdźcie, co jest dostępne w bibliotece uczelni.

---

## 5. Metodologia symulacji

| Źródło | Link | Co z tego wziąć |
|---|---|---|
| Grimm V. i in., *The ODD Protocol for Describing Agent-Based and Other Simulation Models: A Second Update to Improve Clarity, Replication, and Structural Realism*, JASSS 23(2), 2020, art. 7 | <https://www.jasss.org/23/2/7.html> | **Szablon opisu modelu w raporcie**: Overview (cel i wzorce, byty i zmienne stanu, procesy i harmonogram), Design concepts, Details (inicjalizacja, dane wejściowe, podmodele). Spełnia wymóg „sformalizować model" |
| Sargent R. G., *Verification and validation of simulation models*, Journal of Simulation 7(1), 2013, s. 12–24 | kopia dydaktyczna: <https://ics.uu.nl/docs/vakken/msosi/VerificationValidationSargent.pdf> (DOI nie sprawdzony) | Katalog technik walidacji: face validity, testy warunków skrajnych, testy zdegenerowane, analiza wrażliwości, śledzenie (trace) i inne. Podstawa rozdziału „Walidacja" |
| ten Broeke G., van Voorn G., Ligtenberg A., *Which Sensitivity Analysis Method Should I Use for My Agent-Based Model?*, JASSS 19(1), 2016, art. 5 | <https://doi.org/10.18564/jasss.2857> |  zacząć od rozszerzonej analizy OFAT (zmiana jednego czynnika naraz). Regresja i Sobol jako uzupełnienie. Silnik zdarzeń dyskretnych w Pythonie: środowisko, procesy (generatory), zdarzenia `timeout`, zasoby o ograniczonej pojemności |
| ter Hoeven E. i in., *Mesa 3: Agent-based modeling with Python in 2025*, JOSS 10(107), 2025, art. 7668 | <https://joss.theoj.org/papers/10.21105/joss.07668>, kod: <https://github.com/projectmesa/mesa> | Framework ABM w Pythonie.  dopiero przy rozszerzeniu wieloagentowym |
| Towers M. i in., *Gymnasium: A Standard Interface for Reinforcement Learning Environments* (2024) | <https://arxiv.org/abs/2407.17032> | Standard interfejsu środowiska (`reset`, `step`, obserwacja, nagroda, `terminated`/`truncated`). NASim implementuje interfejs Gymnasium, a CyberBattleSim opiera się na starszym OpenAI Gym |

Podręcznik, którego nie weryfikowałam: Law A. M., *Simulation Modeling and Analysis* (klasyczny podręcznik symulacji dyskretnych). Sprawdźcie wydanie.

---

## 6. Statystyka eksperymentów

| Źródło | Link | Co z tego wziąć |
|---|---|---|
| Miller E., *Adding Error Bars to Evals: A Statistical Approach to Language Model Evaluations* (2024) | <https://arxiv.org/abs/2411.00640> | Raportujcie błędy standardowe i przedziały ufności; porównujcie modele przez **różnice parami na tych samych zadaniach**; używajcie błędów skupionych, gdy zadania są grupowane; sprawdzajcie moc testu. To wprost nasz protokół |

Techniki wymienione w opisie projektu (bez osobnych źródeł, to standard statystyczny):

- przedział Wilsona dla proporcji (`statsmodels.stats.proportion.proportion_confint(method="wilson")`),
- test McNemara dla sparowanych wyników binarnych (`statsmodels.stats.contingency_tables.mcnemar`),
- korekta Holma przy wielu porównaniach (`statsmodels.stats.multitest.multipletests(method="holm")`),
- regresja logistyczna do oceny interakcji strategia × środowisko.

Nazwy funkcji podaję z pamięci, sprawdźcie je w dokumentacji używanej wersji biblioteki.

---

## 7. Szczegóły modelowania

### 7.1. Formalizacja: (PO)MDP

Środowisko można opisać jako **częściowo obserwowalny proces decyzyjny Markowa**, tak jak robią to NASim i praca Schwartza i Kurniawati:

| Element | W naszym projekcie |
|---|---|
| Stan *S* (ukryty) | prawdziwa klasa słabości, `progress`, `risk`, `blocked`, pozostały budżet |
| Obserwacja *O* | to, co widzi agent: `known`, `progress`, `risk`, `steps_left` |
| Akcje *A* | `inspect`, `escalate`, `wait`, `stop` (katalog z kosztami) |
| Przejścia *T* | losowe, zależne od klasy słabości i akcji |
| Nagroda *R* (opcjonalnie) | potrzebna tylko, gdy dodacie RL; u nas sukces/koszt/wykrycie liczone na końcu |
| Koniec | `terminated` (cel, blokada) lub `truncated` (budżet, limit czasu) |

Przydatna zgodność: w interfejsie Gymnasium `step()` zwraca `terminated` i `truncated`, co odpowiada rozróżnieniu „cel lub blokada" vs „wyczerpany limit". Wykrycie jest **osobną flagą**, nie powodem zakończenia.

### 7.2. Zegar: krok czy zdarzenia?

- **Jeden agent, tury:** wystarczy zwykła pętla krokowa. SimPy nic nie dodaje, a komplikuje kod (zgodnie z uwagą w opisie projektu).
- **SimPy ma sens**, gdy akcje mają różny czas trwania i nakładają się albo wielu agentów rywalizuje o zasoby (kolejki).
- **Zasada:** zacznijcie od pętli krokowej z zapisem `sim_time`. Przejście na SimPy zostawcie na rozszerzenie.

### 7.3. Losowość i powtarzalność

Osobne strumienie losowości dla każdego komponentu pozwalają zmieniać jedno bez zakłócania pozostałych:

```python
from numpy.random import SeedSequence, default_rng

ss = SeedSequence(scenario_seed)
env_rng, defense_rng, agent_rng = [default_rng(s) for s in ss.spawn(3)]
```

Aby porównywać agentów na tych samych warunkach (wspólne liczby losowe), **wygenerujcie z góry losowania dla scenariusza indeksowane numerem kroku** i odtwarzajcie je dla każdego agenta:

```python
u_success = env_rng.random(max_steps)   # losowanie sukcesu akcji w kroku t
u_block   = defense_rng.random(max_steps)  # losowanie blokady w kroku t
```

Zastrzeżenie: to poprawia porównywalność, ale nie daje identycznej sekwencji zdarzeń, bo agenci wykonują różne akcje. Nie zakładajcie, że wspólne ziarno wystarcza (jak zauważa opis projektu).

### 7.4. Ile przebiegów

Dla szacowania proporcji przybliżony wzór na połowę szerokości przedziału ufności to *h ≈ 1,96·√(p(1−p)/n)*. W najgorszym przypadku (*p* = 0,5):

| Pożądana połowa szerokości *h* | Potrzebne *n* na konfigurację |
|---|---|
| ±0,10 | ok. 97 |
| ±0,05 | ok. 385 |

To uzasadnia „około 100 przebiegów" jako **minimum dla przybliżonych wyników** i pokazuje, że wąskie przedziały wymagają kilkuset. Dla różnic między agentami mogą być potrzebne jeszcze większe próby, zwłaszcza dla rzadkich zdarzeń.

### 7.5. Analiza wyników

Model liczący interakcję strategii z czynnikami (RQ1, RQ3):

```python
import statsmodels.formula.api as smf

# df: jeden wiersz = jeden przebieg; success = 0/1
m = smf.logit(
    "success ~ C(agent) * (C(weakness) + C(depth) + C(monitoring) + C(budget))",
    data=df,
).fit()
print(m.summary())
```

Zaczynajcie od efektów głównych i interakcji agenta z każdym czynnikiem. Pełna interakcja pięcioczynnikowa łatwo prowadzi do idealnej separacji i niestabilnych estymat. Dla parowania agentów na wspólnych scenariuszach:

```python
from statsmodels.stats.proportion import proportion_confint
from statsmodels.stats.contingency_tables import mcnemar

lo, hi = proportion_confint(k_success, n_runs, alpha=0.05, method="wilson")

# tablica: [[oba sukces, tylko A], [tylko B, oba porażka]]
res = mcnemar([[a, b], [c, d]], exact=True)
```

### 7.6. Analiza wrażliwości i walidacja

- **Wrażliwość:** zacznijcie od OFAT (zmiana jednego parametru naraz, np. `p_block` ∈ {0,3; 0,5; 0,7}), zgodnie z zaleceniem ten Broeke i in. Sobol wymaga tysięcy przebiegów, więc dla agentów regułowych możliwy, dla LLM nie.
- **Walidacja** (Sargent): testy warunków skrajnych (np. `p_success` = 1 i brak obrony, więc sukces w `depth` krokach), testy zdegenerowane, śledzenie pojedynczego przebiegu (trace), kontrola kierunku zmian (czy większa restrykcyjność zmniejsza sukces).

### 7.7. Algorytm genetyczny dla agenta A (szkic z DEAP)

```python
import random
from deap import base, creator, tools, algorithms

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

tb = base.Toolbox()
tb.register("attr", random.random)
tb.register("individual", tools.initRepeat, creator.Individual, tb.attr, n=4)  # θ = [próg, wagi...]
tb.register("population", tools.initRepeat, list, tb.individual)

def evaluate(ind):
    # średni fitness z N przebiegów na ZIARNACH TRENINGOWYCH
    return (fitness_on_train_seeds(ind),)

tb.register("evaluate", evaluate)
tb.register("mate", tools.cxBlend, alpha=0.3)
tb.register("mutate", tools.mutGaussian, mu=0.0, sigma=0.1, indpb=0.3)
tb.register("select", tools.selTournament, tournsize=3)

pop = tb.population(n=30)
pop, log = algorithms.eaSimple(pop, tb, cxpb=0.6, mutpb=0.3, ngen=20, verbose=False)
best = tools.selBest(pop, 1)[0]
# po GA: ocena `best` na ZIARNACH TESTOWYCH, niewidzianych w optymalizacji
```

Szczegóły, o których łatwo zapomnieć:

- **Szum fitness.** Ocena z kilkunastu przebiegów jest losowa, więc dwie oceny tego samego osobnika różnią się. Używajcie tych samych ziaren treningowych dla całej populacji i oceniajcie najlepszego ponownie na większej próbie.
- **Zakres genów.** `cxBlend` i `mutGaussian` mogą wyjść poza [0, 1]. Przycinajcie wartości (clipping) albo mapujcie gen na zakres parametru.
- **Przeuczenie.** Wynik GA raportujcie wyłącznie na zbiorze testowym, osobnym od treningowego.
- **Funkcja przystosowania.** `fitness = w_s·success − w_d·detected − w_c·cost_norm`. Wagi uzasadnijcie, a przy wątpliwościach użyjcie NSGA-II (front Pareto) zamiast jednej liczby.

### 7.8. Agent LLM (B): wymagania techniczne

- Prompt w stylu ReAct: opis stanu → lista dozwolonych akcji → odpowiedź w JSON.
- Walidacja: nazwa akcji z katalogu, parametry poprawne; błędna odpowiedź liczona jako `invalid_action` (np. jedna ponowna próba, potem akcja domyślna `wait`).
- Zapis na każdy krok: model (dokładny identyfikator), temperatura, prompt, odpowiedź, opóźnienie, liczba tokenów.
- Nawet przy temperaturze 0 wyniki mogą się różnić między wywołaniami. Nie zakładajcie determinizmu, powtarzajcie przebiegi.
- Koszt przed startem: `koszt ≈ przebiegi × średnia liczba kroków × (tokeny_we × cena_we + tokeny_wy × cena_wy)`. Zmierzcie tokeny w pilocie na 10–20 przebiegach, a ceny weźcie z aktualnego cennika wybranego dostawcy.

---

## 8. Jak wybrać model do projektu

„Model" może znaczyć dwie rzeczy, więc obie są poniżej: (A) jak zamodelować środowisko, (B) których agentów porównywać.

### 8.1. Krok 1: zacznijcie od pytania, nie od narzędzia

Zapiszcie jednym zdaniem, **co symulacja ma pokazać**. Dla nas: *jak strategia agenta i cechy środowiska wspólnie wpływają na sukces, koszt i wykrywalność*. To wymaga:

- pełnej kontroli nad czynnikami środowiska (E1–E4),
- powtarzalności i wielu przebiegów,
- wspólnego interfejsu dla różnych agentów (reguły, LLM, GA).

### 8.2. Krok 2: porównajcie podejścia do modelowania środowiska

| Podejście | Kiedy pasuje | Zalety | Wady i ryzyka |
|---|---|---|---|
| **Własne środowisko krokowe w czystym Pythonie, interfejs w stylu Gymnasium** | jeden agent, tury, pełna kontrola nad parametrami | prosty kod, łatwe testy, łatwo podłączyć LLM i GA, później także RL | brak gotowego czasu zdarzeń i kolejek |
| **Symulacja zdarzeń dyskretnych (SimPy)** | wielu agentów konkurujących o zasoby, różne czasy akcji | naturalne kolejki i czas symulowany | narzut złożoności, gdy nie ma współbieżności |
| **ABM (Mesa 3)** | rozszerzenie wieloagentowe, interakcje i zbieranie danych | gotowa struktura agentów i kolektory danych | narzut frameworku, wiele funkcji zbędnych w rdzeniu |
| **Gotowy symulator (NASim, CyberBattleSim, CybORG)** | chcecie RL i porównywalności z literaturą | sprawdzone środowiska, interfejs Gym | nie obsługuje Waszych czynników E1–E4, nauka cudzego kodu, ryzyko utrzymania (YAWNING-TITAN jest archiwalny) |
| **Prawdziwe sandboxy (SandboxEscapeBench, Inspect)** | pytanie o zdolność modelu na realnych systemach | realizm | wymaga infrastruktury i zabezpieczeń; **poza zakresem** projektu i jego ograniczeniami bezpieczeństwa |

### 
### 8.3. Rekomendacja

1. **Rdzeń:** własne środowisko krokowe w czystym Pythonie z interfejsem zbliżonym do Gymnasium (`reset(seed)`, `step(action)`, obserwacja, `terminated`/`truncated`, `info`).
   - Daje najwięcej kontroli nad czynnikami, a LLM i GA podłączają się bez zmian w silniku.
   - Jeśli w przyszłości dodacie RL, interfejs będzie już zgodny.
2. **SimPy** wprowadzajcie dopiero przy rozszerzeniu wieloagentowym z kolejkami i różnymi czasami akcji.
3. **Mesa** niepotrzebna w rdzeniu. Rozważcie ją tylko, jeśli zależy Wam na gotowym schedulerze i kolektorach danych w wersji wieloagentowej.
4. **Gotowe symulatory** źródło wzorców (CyberBattleSim: obrona, NASim: częściowa obserwowalność i YAML)
5. **Opis modelu** w raporcie wg protokołu ODD, a **walidację** wg katalogu Sargenta.


### 

---


---

##  9. Mapa: element projektu → źródło

| Element projektu | Na czym oprzeć | Sekcja |
|---|---|---|
| Motywacja problemu | SandboxEscapeBench, AI Control, Phuong i in. | 1 |
| Typy słabości i skala trudności (E1, E2) | SandboxEscapeBench | 1.1 |
| Postęp w podzadaniach (`progress`) | Cybench | 1.2 |
| Widoczność słabości (czynnik pomocniczy) | Fang i in. | 1.2 |
| Abstrakcyjne środowisko ataku i obrony | CyberBattleSim, NASim, CybORG | 2 |
| Wspólny interfejs agentów | CybORG, Gymnasium | 2, 5 |
| Obrona stochastyczna (wykrycie, blokada) | CyberBattleSim | 2 |
| Formalizacja (PO)MDP | Schwartz i Kurniawati, NASim | 2, 7.1 |
| Agent LLM | ReAct, AgentBench, Gao i in. | 3 |
| Algorytm genetyczny | DEAP, NSGA-II, Salimans i in. | 4 |
| Opis modelu w raporcie | ODD (Grimm i in.) | 5 |
| Walidacja modelu | Sargent | 5 |
| Analiza wrażliwości | ten Broeke i in. | 5 |
| Statystyka i przedziały ufności | Miller | 6 |
| Silnik zdarzeń (opcjonalnie) | SimPy | 5, 7.2 |
| Rozszerzenie wieloagentowe | SimPy lub Mesa 3 | 5, 8 |
