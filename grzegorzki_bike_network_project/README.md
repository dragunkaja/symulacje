# Grzegórzki – przygotowanie grafu rowerowego

Projekt przygotowuje skierowany graf sieci rowerowej Krakowa, dopasowuje do niego sześć liczników, wykonuje podstawową walidację i tworzy mapy.

## 1. Co znajduje się w projekcie?

- `sensors.csv` – współrzędne sześciu liczników.
- `data/raw/network_existing.graphml` – oryginalny graf przekazany przez użytkowniczkę; zachowany bez zmian do porównania.
- `src/config.py` – ustawienia projektu.
- `src/build_network.py` – pobranie lub wczytanie grafu i dodanie atrybutów.
- `src/match_sensors.py` – znalezienie najbliższych skierowanych krawędzi dla liczników.
- `src/validate_graph.py` – kontrola struktury, długości i osiągalności.
- `src/visualize_graph.py` – mapa PNG i interaktywna mapa HTML.
- `run_pipeline.py` – uruchomienie całego procesu.

## 2. Instalacja

Zalecany Python 3.11 lub 3.12.

W terminalu, w katalogu projektu:

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

macOS / Linux:

```bash
source .venv/bin/activate
```

Instalacja bibliotek:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Pobranie nowej sieci z OpenStreetMap wymaga połączenia z internetem.

## 3. Uruchomienie

```bash
python run_pipeline.py
```

Domyślnie projekt pobiera świeżą sieć OSMnx z `network_type="bike"`.

Obszar pobierania jest wyznaczany automatycznie:
1. tworzymy otoczkę wypukłą sześciu punktów pomiarowych;
2. powiększamy ją o 1000 metrów;
3. pobieramy sieć rowerową dla tego poligonu.

Graf jest skierowany i wielokrawędziowy (`MultiDiGraph`). Zachowuje kierunki, równoległe połączenia i identyfikatory krawędzi.

## 4. Użycie istniejącego grafu

W `src/config.py` można zmienić:

```python
NETWORK_SOURCE = "download"
```

na:

```python
NETWORK_SOURCE = "existing"
```

Wtedy użyty zostanie oryginalny plik `data/raw/network_existing.graphml`.

Nie jest to zalecane jako wersja końcowa, ponieważ w analizie przekazanego pliku:
- Dworzec Główny znajdował się około 395,6 m od najbliższej krawędzi;
- Kopernika około 30,1 m;
- Grzegórzecka około 20,0 m;
- graf miał 35 składowych spójności słabej;
- występowały krawędzie z `access=no`.

## 5. Pliki wynikowe

Po uruchomieniu:

### `data/processed/`
- `network.graphml` – graf do dalszej pracy w OSMnx/NetworkX.
- `network_nodes.gpkg` – węzły grafu.
- `network_edges.gpkg` – skierowane krawędzie grafu.
- `sensor_edge_candidates.csv` – kandydaci dopasowania liczników do krawędzi.
- `sensor_match_summary.csv` – minimalna odległość każdego licznika od sieci.
- `sensor_edge_map_template.csv` – edytowalny szablon mapowania.
- `sensor_reachability.csv` – wstępna macierz osiągalności między licznikami.
- `validation_report.txt` – raport walidacji.

### `outputs/`
- `network_overview.png` – statyczna mapa sieci i liczników.
- `network_map.html` – interaktywna mapa do otwarcia w przeglądarce.

## 6. Ważne: dopasowanie licznika nie jest automatycznym potwierdzeniem

`match_sensors.py` wyszukuje najbliższą krawędź lub krawędzie o niemal identycznej odległości (np. dwa kierunki tej samej drogi).

Wyniki trafiają do `sensor_edge_candidates.csv`.

Przed użyciem liczników w symulacji należy:
1. otworzyć `outputs/network_map.html`;
2. sprawdzić położenie punktów względem dróg;
3. sprawdzić kandydatów w `sensor_edge_candidates.csv`;
4. w `sensor_edge_map_template.csv` wybrać właściwe krawędzie;
5. ustawić `use_in_model=True`, `confirmed=True`;
6. ustawić `direction` zgodnie z rzeczywistym sposobem pomiaru, np. `forward`, `reverse` lub `both`.

Nie należy automatycznie przypisywać licznika do najbliższej drogi, jeśli odległość jest duża. W takim przypadku najpierw trzeba sprawdzić współrzędne lub zakres pobranego grafu.

## 7. Atrybuty przydatne dla przyszłych agentów

Każda skierowana krawędź zachowuje m.in.:
- `u`, `v`, `key` – identyfikatory końców i klucz krawędzi;
- `edge_id` – stabilny identyfikator w formacie `u|v|key`;
- `length_m` – długość odcinka w metrach;
- `highway`, `name`, `osmid`;
- `oneway`, `access`, `bicycle`, `cycleway`, `surface` – jeżeli są dostępne w OSM.

`reference_travel_time_s_15kmh` jest wyłącznie wartością referencyjną. W przyszłym ABM czas przejazdu będzie wyliczany indywidualnie dla agenta z jego prędkości.

Nie przypisujemy jeszcze pojemności krawędzi ani przepustowości – wymagają osobnych danych lub jawnych założeń eksperymentalnych.

## 8. Ograniczenia danych

OSMnx buduje sieć na podstawie tagów OpenStreetMap. `network_type="bike"` oznacza sieć zgodną z filtrem rowerowym OSMnx, ale nie gwarantuje, że każdy tag w OSM jest aktualny lub kompletny. Warstwę ZTP/MSIP warto później wykorzystać do kontroli i uzupełnienia infrastruktury.

Współrzędne liczników są zapisane w EPSG:4326 (latitude/longitude). Odległości i bufory są liczone w EPSG:2180.
