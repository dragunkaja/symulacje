# ADR-0001: Wybór silnika symulacji

- **Status:** do zatwierdzenia przez zespół
- **Data:** 2026-11-02

## Kontekst

Prezentacja projektu (slajd 8) wymienia model kolejkowania, współbieżności i ograniczonych zasobów oraz wskazuje ABM/SimPy jako rozważane podejście. Późniejszy dokument state of the art rekomenduje rozpoczęcie od własnego środowiska krokowego w Pythonie, z interfejsem zbliżonym do Gymnasium. SimPy ma sens przy wielu agentach, różnych czasach trwania akcji lub kolejkach. Mesa może być rozważona przy rozszerzeniu wieloagentowym.

## Rozważane opcje

1. Własny silnik krokowy w Pythonie.
2. SimPy – symulacja zdarzeń dyskretnych.
3. Mesa – framework agent-based modeling.
4. Gotowy symulator, np. NASim lub CyberBattleSim.

## Proponowana decyzja

Rozpocząć od własnego silnika krokowego z metodami `reset(seed)`, `observe()` i `step(action)`. Zachować wspólny interfejs agenta `choose_action(observation)`. Nie wprowadzać SimPy ani Mesa do rdzenia, dopóki model nie będzie wymagał współbieżności, kolejek lub wielu aktywnych agentów.

## Uzasadnienie

- W pierwszym etapie porównujemy strategie w kontrolowanym środowisku z turami.
- Własny silnik daje bezpośrednią kontrolę nad czynnikami E1–E4 i ułatwia testowanie.
- Interfejs podobny do Gymnasium pozwala podłączać kolejne strategie bez modyfikowania silnika.
- Ogranicza to złożoność implementacji na początku projektu.

## Konsekwencje i warunek ponownego rozpatrzenia

Jeżeli wymagania przedmiotu lub docelowy model będą wymagały kolejek, współbieżności, różnych czasów akcji lub współpracy wielu agentów, należy ponownie rozważyć SimPy/Mesa. Zespół powinien potwierdzić tę decyzję z prowadzącym, ponieważ slajd 8 prezentacji wskazuje również na model kolejkowania i współbieżność.
