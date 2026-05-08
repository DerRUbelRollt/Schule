# Transporter – Erz Transport Spiel

Ein Python-Spiel mit `pygame`, bei dem ein LKW Erz von einer Quelle zu einem Ziel transportieren muss, während ein Hubschrauber versucht die Ladung zu stehlen.

---

## Inhaltsverzeichnis

- [Installation](#installation)
- [Spielanleitung](#spielanleitung)
- [Regeln](#regeln)
- [Projektstruktur](#projektstruktur)
- [Klassendiagramm](#klassendiagramm)
- [Klassen & Methoden](#klassen--methoden)

---

## Installation

```bash
pip install pygame
python main.py
```

Benötigt: **Python 3.8+** und **pygame**

---

## Spielanleitung

| Taste     | Aktion                             |
| --------- | ---------------------------------- |
| `W` / `↑` | LKW nach oben bewegen              |
| `S` / `↓` | LKW nach unten bewegen             |
| `A` / `←` | LKW nach links bewegen             |
| `D` / `→` | LKW nach rechts bewegen            |
| `ESC`     | Zurück zum Menü                    |
| `ENTER`   | Spiel neu starten (nach Spielende) |

**Ablauf:**

1. Fahre mit dem LKW zur **Quelle** – Erz wird automatisch geladen
2. Fahre zum **Ziel** – Erz wird automatisch entladen
3. Fahre zur **Tankstelle** – Tank wird automatisch befüllt
4. Wiederhole bis 80 % des Erzes transportiert sind

---

## Regeln

- **Gewonnen**, wenn ≥ 80 % (N) des Erzes am Ziel abgeliefert wurden
- **Verloren**, wenn:
  - Der Hubschrauber mehr als 20 % (1–N) des Erzes gestohlen hat
  - Der Tank leer ist und das Ziel noch nicht erreicht wurde
- Der Hubschrauber fliegt vom Bildschirmrand an, stiehlt Ladung und flieht wieder aus dem Bild
- Die Karte wird bei jedem Spielstart zufällig neu generiert

### Schwierigkeitsgrade

| Schwierigkeit | Spritverbrauch | Heli-Geschwindigkeit | Angriffspause |
| ------------- | -------------- | -------------------- | ------------- |
| Leicht        | 0.02 / Pixel   | 4                    | 180 Frames    |
| Mittel        | 0.04 / Pixel   | 5                    | 120 Frames    |
| Schwer        | 0.08 / Pixel   | 6                    | 70 Frames     |

---

## Projektstruktur

```
transporter/
├── main.py          # Einstiegspunkt – startet das Spiel
├── config.py        # Alle Konstanten & Schwierigkeitseinstellungen
├── game.py          # Hauptspielschleife, Rendering, Event-Handling
├── game_logic.py    # Spielregeln, Gewinn-/Verlustprüfung
├── menu.py          # Hauptmenü mit Schwierigkeitsauswahl
├── hud.py           # Heads-Up Display (Anzeige von Status-Infos)
├── truck.py         # LKW – spielergesteuertes Fahrzeug
├── helicopter.py    # Hubschrauber – gegnerisches KI-Objekt
├── source.py        # Quelle – Ausgangspunkt des Erzes
├── destination.py   # Ziel – Abgabepunkt des Erzes
└── gas_station.py   # Tankstelle – Nachfüllstation
```

---

## Klassendiagramm

```
┌─────────────┐
│    main.py  │
│  main()     │
└──────┬──────┘
       │ erstellt
       ▼
┌─────────────────────────────────────────────────────────────────┐
│                           Game                                  │
│  - screen, clock, difficulty, in_menu                           │
│  + run()                                                        │
│  + _init_game_objects()                                         │
│  + _generate_random_position()                                  │
│  + _handle_menu_events()                                        │
│  + _handle_game_events()                                        │
│  + _get_movement_input()                                        │
│  + _update()                                                    │
│  + _draw()                                                      │
│  + _draw_roads()                                                │
└──┬──────┬──────┬──────┬──────┬──────┬──────┬──────┬────────────┘
   │      │      │      │      │      │      │      │
   ▼      ▼      ▼      ▼      ▼      ▼      ▼      ▼
┌──────┐ ┌────┐ ┌─────┐ ┌────┐ ┌───┐ ┌────────┐ ┌─────┐ ┌─────┐
│ Menu │ │HUD │ │Truck│ │Heli│ │Src│ │  Dest  │ │ Gas │ │Logic│
└──────┘ └────┘ └─────┘ └────┘ └───┘ └────────┘ └─────┘ └─────┘

GameLogic koordiniert:
  Truck ◄──stiehlt von── Helicopter
  Truck ──lädt von────► Source
  Truck ──liefert an──► Destination
  Truck ──tankt bei───► GasStation

Zustandsmaschine Helicopter:
  OFFSCREEN ──► APPROACHING ──► FLEEING ──► OFFSCREEN
                    │
                  (stiehlt Erz vom Truck)

Zustandsmaschine GameLogic:
  RUNNING ──► WON
  RUNNING ──► LOST
```

---

## Klassen & Methoden

### `config.py` – Konfiguration

Enthält ausschließlich Konstanten. Keine Klassen.

| Konstante               | Beschreibung                                                             |
| ----------------------- | ------------------------------------------------------------------------ |
| `DIFFICULTY_SETTINGS`   | Dict mit Werten pro Schwierigkeitsgrad (Verbrauch, Heli-Speed, Cooldown) |
| `TRUCK_CAPACITY`        | Maximale Ladekapazität des LKW (20 t)                                    |
| `TRUCK_FUEL_MAX`        | Maximaler Tankinhalt (100)                                               |
| `ORE_TOTAL`             | Gesamtmenge Erz (200 t)                                                  |
| `WIN_THRESHOLD`         | Anteil für Sieg (0.80 = 80 %)                                            |
| `MIN_BUILDING_DISTANCE` | Mindestabstand zwischen Gebäuden bei Zufallsplatzierung (150 px)         |

---

### `Truck` – `truck.py`

Repräsentiert den spielergesteuerten LKW.

| Attribut           | Typ     | Beschreibung                        |
| ------------------ | ------- | ----------------------------------- |
| `x`, `y`           | `float` | Aktuelle Position                   |
| `speed`            | `int`   | Bewegungsgeschwindigkeit (px/Frame) |
| `fuel`             | `float` | Aktueller Tankstand                 |
| `fuel_max`         | `float` | Maximaler Tankstand                 |
| `fuel_consumption` | `float` | Verbrauch pro Pixel Bewegung        |
| `capacity`         | `int`   | Maximale Ladekapazität              |
| `cargo`            | `int`   | Aktuell geladenes Erz               |

| Methode                                     | Beschreibung                                                                     |
| ------------------------------------------- | -------------------------------------------------------------------------------- |
| `move(dx, dy, screen_width, screen_height)` | Bewegt den LKW in Richtung `(dx, dy)`, verbraucht Sprit, begrenzt auf Bildschirm |
| `load_ore(available_ore)`                   | Lädt so viel Erz wie möglich, gibt geladene Menge zurück                         |
| `unload_ore()`                              | Entlädt die gesamte Ladung, gibt entladene Menge zurück                          |
| `refuel()`                                  | Füllt den Tank vollständig auf                                                   |
| `has_fuel()`                                | Gibt `True` zurück wenn Sprit vorhanden                                          |
| `get_rect()`                                | Gibt `pygame.Rect` für Kollisionserkennung zurück                                |
| `draw(screen)`                              | Zeichnet den LKW inkl. Ladestand und Spritleiste                                 |

---

### `Helicopter` – `helicopter.py`

KI-gesteuerter Gegner, der Erz vom LKW stiehlt.

**Zustände (`HelicopterState`):**

- `OFFSCREEN` – außerhalb des Bildschirms, wartet auf nächsten Angriff
- `APPROACHING` – fliegt vom Rand auf den LKW zu
- `FLEEING` – flieht nach dem Diebstahl aus dem Bild

| Attribut          | Typ     | Beschreibung                         |
| ----------------- | ------- | ------------------------------------ |
| `x`, `y`          | `float` | Aktuelle Position                    |
| `speed`           | `int`   | Fluggeschwindigkeit                  |
| `steal_amount`    | `int`   | Erzmenge pro Diebstahl (5 t)         |
| `stolen_total`    | `int`   | Gesamtmenge gestohlenes Erz          |
| `state`           | `str`   | Aktueller Zustand                    |
| `attack_cooldown` | `int`   | Verbleibende Warteframes bis Angriff |
| `cooldown_max`    | `int`   | Wartezeit in Frames nach Angriff     |

| Methode                                     | Beschreibung                                                    |
| ------------------------------------------- | --------------------------------------------------------------- |
| `set_screen_size(width, height)`            | Setzt Bildschirmgröße und platziert Heli außerhalb              |
| `update(truck_x, truck_y, truck_has_cargo)` | Aktualisiert Zustand und Position, gibt gestohlene Menge zurück |
| `_get_random_offscreen_point()`             | Berechnet zufälligen Einflug-/Ausflugtpunkt am Bildschirmrand   |
| `_is_offscreen()`                           | Prüft ob Heli außerhalb des sichtbaren Bereichs ist             |
| `_move_towards(target_x, target_y)`         | Bewegt den Heli Richtung Ziel, gibt `True` bei Ankunft zurück   |
| `get_rect()`                                | Gibt `pygame.Rect` für Kollisionserkennung zurück               |
| `draw(screen)`                              | Zeichnet den Hubschrauber (nur wenn sichtbar)                   |

---

### `Source` – `source.py`

Erz-Quelle, von der der LKW lädt.

| Attribut        | Typ     | Beschreibung                             |
| --------------- | ------- | ---------------------------------------- |
| `x`, `y`        | `float` | Position                                 |
| `ore_remaining` | `int`   | Verbleibende Erzmenge                    |
| `ore_total`     | `int`   | Startmenge (für Fortschrittsdarstellung) |

| Methode            | Beschreibung                                                       |
| ------------------ | ------------------------------------------------------------------ |
| `take_ore(amount)` | Entnimmt Erz (max. verfügbare Menge), gibt entnommene Menge zurück |
| `has_ore()`        | Gibt `True` zurück wenn noch Erz vorhanden                         |
| `get_rect()`       | Gibt `pygame.Rect` für Kollisionserkennung zurück                  |
| `draw(screen)`     | Zeichnet den Erzhaufen mit Füllstand-Anzeige                       |

---

### `Destination` – `destination.py`

Ziel-Lager, an dem der LKW Erz abliefert.

| Attribut        | Typ     | Beschreibung             |
| --------------- | ------- | ------------------------ |
| `x`, `y`        | `float` | Position                 |
| `ore_delivered` | `int`   | Bisher abgeliefertes Erz |

| Methode                   | Beschreibung                                      |
| ------------------------- | ------------------------------------------------- |
| `deliver_ore(amount)`     | Nimmt Erz an und erhöht `ore_delivered`           |
| `get_rect()`              | Gibt `pygame.Rect` für Kollisionserkennung zurück |
| `draw(screen, ore_total)` | Zeichnet das Lager inkl. Fortschrittsbalken       |

---

### `GasStation` – `gas_station.py`

Tankstelle zum Nachtanken des LKW.

| Attribut | Typ     | Beschreibung |
| -------- | ------- | ------------ |
| `x`, `y` | `float` | Position     |

| Methode        | Beschreibung                                      |
| -------------- | ------------------------------------------------- |
| `get_rect()`   | Gibt `pygame.Rect` für Kollisionserkennung zurück |
| `draw(screen)` | Zeichnet die Zapfsäule                            |

---

### `GameLogic` – `game_logic.py`

Zentrale Spiellogik – koordiniert alle Objekte und prüft Spielbedingungen.

**Zustände (`GameState`):** `RUNNING`, `WON`, `LOST`

| Attribut        | Typ     | Beschreibung           |
| --------------- | ------- | ---------------------- |
| `state`         | `str`   | Aktueller Spielzustand |
| `win_threshold` | `float` | Siegbedingung (0.80)   |
| `ore_total`     | `int`   | Gesamterzmenge         |

| Methode                                                        | Beschreibung                                                                   |
| -------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| `update(truck, helicopter, source, destination, gas_station)`  | Führt alle Prüfungen und Interaktionen pro Frame aus, gibt Spielzustand zurück |
| `check_win_condition(destination)`                             | `True` wenn ≥ N % geliefert                                                    |
| `check_lose_condition(helicopter, truck, source, destination)` | `True` wenn zu viel gestohlen oder Tank leer und Ziel nicht erreichbar         |
| `try_load_at_source(truck, source)`                            | Lädt Erz wenn LKW an Quelle steht                                              |
| `try_unload_at_destination(truck, destination)`                | Entlädt Erz wenn LKW am Ziel steht                                             |
| `try_refuel(truck, gas_station)`                               | Tankt wenn LKW an Tankstelle steht                                             |
| `process_helicopter_steal(helicopter, truck)`                  | Verarbeitet Diebstahl und korrigiert Ladestand                                 |
| `get_progress(destination)`                                    | Gibt Fortschritt als Wert 0.0–1.0 zurück                                       |

---

### `Game` – `game.py`

Hauptklasse – verwaltet Spielschleife, Rendering und Events.

| Attribut     | Typ                 | Beschreibung                 |
| ------------ | ------------------- | ---------------------------- |
| `screen`     | `pygame.Surface`    | Haupt-Zeichenfläche          |
| `clock`      | `pygame.time.Clock` | FPS-Begrenzung               |
| `difficulty` | `str`               | Gewählter Schwierigkeitsgrad |
| `in_menu`    | `bool`              | Ob das Menü angezeigt wird   |

| Methode                                       | Beschreibung                                              |
| --------------------------------------------- | --------------------------------------------------------- |
| `run()`                                       | Hauptspielschleife                                        |
| `_init_game_objects()`                        | Erstellt alle Spielobjekte mit zufälligen Positionen      |
| `_generate_random_position(existing, margin)` | Berechnet kollisionsfreie Zufallsposition für ein Gebäude |
| `_handle_menu_events()`                       | Verarbeitet Klicks und Tasten im Menü                     |
| `_handle_game_events()`                       | Verarbeitet Ereignisse während des Spiels                 |
| `_get_movement_input()`                       | Liest WASD/Pfeiltasten, gibt `(dx, dy)` zurück            |
| `_update()`                                   | Bewegt LKW und aktualisiert Spiellogik                    |
| `_draw()`                                     | Rendert alle Objekte und das HUD                          |
| `_draw_roads()`                               | Zeichnet Verbindungslinien zwischen Stationen             |

---

### `Menu` – `menu.py`

Startmenü mit Schwierigkeitsauswahl.

| Attribut              | Typ           | Beschreibung                                  |
| --------------------- | ------------- | --------------------------------------------- |
| `selected_difficulty` | `str`         | Aktuell gewählter Schwierigkeitsgrad          |
| `start_button`        | `pygame.Rect` | Klickbereich Start-Button                     |
| `quit_button`         | `pygame.Rect` | Klickbereich Beenden-Button                   |
| `difficulty_buttons`  | `dict`        | Klickbereiche der drei Schwierigkeits-Buttons |

| Methode                                   | Beschreibung                                               |
| ----------------------------------------- | ---------------------------------------------------------- |
| `handle_click(pos)`                       | Gibt `"start"`, `"quit"` oder `"difficulty_<name>"` zurück |
| `draw(screen)`                            | Zeichnet Titel, Schwierigkeits-Buttons und Anleitung       |
| `_draw_button(screen, rect, text, color)` | Hilfsmethode zum Zeichnen eines einzelnen Buttons          |
| `_draw_instructions(screen)`              | Zeichnet die Tastatur-Steuerungsübersicht                  |

---

### `HUD` – `hud.py`

Heads-Up Display – zeigt Spiel-Statusinfos im oberen Bildschirmbereich.

| Methode                                                                                                                      | Beschreibung                                                       |
| ---------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------ |
| `draw(screen, truck_fuel, truck_fuel_max, truck_cargo, truck_capacity, ore_delivered, ore_remaining, ore_stolen, ore_total)` | Zeichnet alle Statusbalken (Sprit, Ladung, Fortschritt, Gestohlen) |
| `_draw_bar(screen, x, y, width, height, ratio, fill_color, bg_color, text)`                                                  | Hilfsmethode zum Zeichnen eines beschrifteten Fortschrittsbalkens  |
| `draw_game_over(screen, won)`                                                                                                | Zeichnet den Sieg- oder Niederlage-Bildschirm mit Neustart-Hinweis |
