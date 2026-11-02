# Współpraca przy projekcie

## Zanim zaczniesz

1. Pobierz repozytorium i przełącz się na aktualny `main`.
2. Utwórz osobną gałąź dla jednego zadania.
3. Sprawdź opis Issue i kryteria akceptacji.
4. Nie commituj kluczy API, plików `.env`, dużych logów ani lokalnego środowiska Python.

## Zasady implementacji

- Silnik środowiska odpowiada za zmianę stanu. Agent zwraca wyłącznie propozycję akcji.
- Każda nowa reguła przejścia powinna mieć test, w tym – gdy ma to sens – test warunku brzegowego.
- Parametry eksperymentów przechowujemy w konfiguracji, nie jako rozproszone stałe w kodzie.
- Wyniki powinny zawierać identyfikator agenta, scenariusza, seed i wersję/identyfikator konfiguracji.
- Zmiany wpływające na porównywalność eksperymentów opisujemy w dokumentacji decyzji.
- Zachowujemy czytelne nazwy i małe funkcje; nie łączymy logiki środowiska, agenta i analizy w jednym module.

## Pull Request

Przed otwarciem PR:

- uruchom testy;
- sprawdź, czy kod nie zawiera sekretów ani dużych plików wynikowych;
- zaktualizuj dokumentację, jeśli zmieniło się zachowanie lub interfejs;
- opisz, jak ręcznie sprawdzić zmianę, jeżeli test automatyczny nie wystarcza.

Każdy PR powinien mieć review co najmniej jednej osoby poza autorem i przejść wymagane kontrole CI.

## Konwencja commitów

Używamy krótkich prefiksów opisujących rodzaj zmiany: `feat`, `fix`, `test`, `docs`, `refactor`, `chore`.

Przykład: `feat: add rule-based agent`.
