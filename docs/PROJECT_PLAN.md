# Plan pracy i organizacja projektu

Ten dokument służy do planowania implementacji, podziału zadań i przygotowywania prezentacji z postępów. Aktualny status zadań powinien być prowadzony w GitHub Projects, a nie ręcznie w kilku miejscach.

## 1. Etapy i kryteria ukończenia

| Etap | Zakres | Kryteria ukończenia |
|---|---|---|
| 0. Fundament | Repozytorium, struktura, zależności, formatowanie, testy, CI | Projekt można zainstalować; testy uruchamiają się lokalnie i w GitHub Actions; `main` pozostaje stabilny. |
| 1. Środowisko | Scenariusz, stan, obserwacja, akcje, budżet, ryzyko, monitoring i blokada | `reset(seed)` i `step(action)` działają; testy przejść, warunków końcowych i wartości granicznych przechodzą. |
| 2. Baseline | Interfejs agenta i RuleAgent | RuleAgent działa w pojedynczym przebiegu; decyzje agenta nie modyfikują bezpośrednio stanu środowiska. |
| 3. Runner i eksperymenty | Pojedyncze i seryjne przebiegi, 36 konfiguracji, logi | Eksperyment można powtórzyć z konfiguracji; każdy wiersz wyników identyfikuje agenta, scenariusz, seed i metryki. |
| 4. LLM | Adapter API, prompt, parsowanie i walidacja odpowiedzi | LLM może zwrócić wyłącznie akcję z katalogu; błędne odpowiedzi są logowane; klucze API nie trafiają do Git. |
| 5. GA | Kodowanie parametrów, fitness, selekcja, krzyżowanie i mutacja | GA stroi RuleAgent na seedach treningowych; najlepszy osobnik jest oceniany na osobnym zbiorze testowym. |
| 6. Analiza | Statystyki, wykresy, analiza wrażliwości i Pareto | Wyniki są porównywane na wspólnych scenariuszach; raport zawiera niepewność oszacowań i ograniczenia. |
| 7. Finalizacja | ODD, walidacja, raport i prezentacja | Model, eksperymenty, wyniki i ograniczenia są opisane tak, aby umożliwić odtworzenie badania. |

## 2. Jak dzielić zadania

Jedno Issue powinno opisywać jeden możliwy do sprawdzenia rezultat. Przykład dobrego zadania:

**Tytuł:** `Implementacja walidacji akcji środowiska`

- Cel: środowisko odrzuca akcje spoza katalogu.
- Zakres: walidacja wejścia w `environment`, komunikat błędu i testy.
- Poza zakresem: implementacja agenta LLM.
- Kryteria akceptacji:
  - poprawne akcje przechodzą walidację;
  - niepoprawna akcja nie zmienia stanu;
  - zachowanie jest pokryte testami.

Przypisujcie Issue do jednej osoby odpowiedzialnej za dowiezienie zadania. Pozostałe osoby mogą konsultować i robić review. Unikajcie przypisywania jednego zadania wszystkim trzem osobom.

## 3. GitHub Projects – tablica zadań

Utwórzcie jedną tablicę typu **Board** z kolumnami:

`Backlog → Ready → In progress → Review → Done`

Przydatne pola:

- `Milestone` – etap 0–7 z planu,
- `Priority` – High / Medium / Low,
- `Area` – Environment / Agents / Experiments / Analysis / Docs / Infrastructure,
- `Assignee` – jedna osoba odpowiedzialna.

Proponowane etykiety:

- `type:feature`, `type:bug`, `type:research`, `type:docs`, `type:chore`,
- `area:environment`, `area:agents`, `area:experiments`, `area:analysis`, `area:docs`,
- `priority:high`, `priority:medium`, `priority:low`.

Nie używajcie jednocześnie wielu mechanizmów do śledzenia tego samego statusu. Tablica jest źródłem prawdy o postępie; README przedstawia jedynie główne etapy projektu.

## 4. Gałęzie i Pull Requesty

Dla trzyosobowego zespołu wystarczy prosty model z krótkimi gałęziami:

- `main` – zawsze wersja możliwa do uruchomienia i zaprezentowania,
- gałęzie zadaniowe tworzone z aktualnego `main`, np. `feat/environment-step`, `feat/rule-agent`, `fix/seed-handling`, `docs/project-plan`.

Przepływ pracy:

1. Utwórzcie Issue z zakresem i kryteriami akceptacji.
2. Utwórzcie gałąź dla zadania.
3. Implementujcie mały, spójny zakres i dodajcie testy.
4. Otwórzcie Pull Request powiązany z Issue.
5. Druga osoba robi review; autor poprawia uwagi.
6. Po przejściu CI i review scalcie PR do `main`.

Nie pracujcie bezpośrednio na `main`. Włączcie ochronę tej gałęzi i wymagajcie przejścia testów CI. Przy małym zespole nie ma potrzeby wprowadzać osobnej gałęzi `develop`, o ile prowadzący nie wymaga innego modelu.

Proponowany format commitów:

- `feat: add environment step logic`
- `fix: prevent state update for invalid action`
- `test: cover terminal conditions`
- `docs: describe experiment protocol`
- `refactor: separate observation from internal state`

## 5. Prezentacje z postępów

Każdą prezentację zapisujcie w `reports/presentations/`, np. `progress-01-environment-design.pdf`. Warto zachować numerację, żeby łatwo pokazać ewolucję projektu.

Proponowany układ prezentacji postępów (5–7 slajdów):

1. **Cel i pytania badawcze** – bez ponownego opowiadania całego wstępu; pokażcie, co jest aktualnie badane.
2. **Stan prac** – ukończone elementy z odnośnikami do Issue/PR.
3. **Architektura i decyzje** – diagram przepływu lub fragment interfejsu, najważniejsze decyzje i ich uzasadnienie.
4. **Demo implementacji** – działający przebieg, test albo log, a nie sam zrzut kodu.
5. **Wstępne wyniki** – wykres/tabela, liczba scenariuszy i przebiegów, seed oraz ograniczenia wyników.
6. **Problemy i ryzyka** – co nie działa, co wymaga decyzji, czego jeszcze nie można wnioskować.
7. **Następny etap** – konkretne zadania, osoby odpowiedzialne i kryteria ukończenia.

Nie pokazujcie wyniku eksperymentu bez informacji o konfiguracji, liczbie przebiegów i sposobie losowania. Wyniki pilotażowe oznaczajcie jako wstępne.

## 6. Notatki i decyzje projektowe

- `docs/decisions/` – krótkie ADR (*Architecture Decision Records*): problem, rozważane opcje, decyzja, uzasadnienie i konsekwencje.
- `docs/meetings/` – tylko wtedy, gdy potrzebujecie zapisywać ustalenia ze spotkań; nazwa pliku w formacie `YYYY-MM-DD.md`.
- `reports/presentations/` – wersje prezentacji postępu.
- `docs/state-of-the-art.md` – przegląd literatury i źródła.

Każda zmiana założeń eksperymentu powinna być odnotowana w dokumentacji i wersjonowana. Nie nadpisujcie po cichu parametrów, które były użyte do wygenerowania opublikowanych wyników.

## 7. Minimalna automatyzacja repozytorium

Po utworzeniu pierwszego kodu dodajcie GitHub Actions uruchamiające przy Pull Requeście:

- instalację zależności,
- testy `pytest`,
- opcjonalnie lint/format check (np. Ruff),
- później kontrolę typów, jeśli zdecydujecie się jej używać.

Na początku nie dodawajcie rozbudowanego pipeline'u, którego zespół nie rozumie lub którego nie potrafi utrzymać.
