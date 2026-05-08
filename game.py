"""
Game Klasse für das Transporter-Spiel.
Hauptspielschleife, Event-Handling und Rendering.
"""

import pygame
import sys
import random
import math
from config import (
    WINDOW_TITLE, FPS, WHITE, LIGHT_BLUE,
    DIFFICULTY_SETTINGS, DIFFICULTY_MEDIUM,
    MIN_BUILDING_DISTANCE
)
from truck import Truck
from helicopter import Helicopter
from source import Source
from destination import Destination
from gas_station import GasStation
from game_logic import GameLogic, GameState
from menu import Menu
from hud import HUD


class Game:
    """
    Hauptklasse des Transporter-Spiels.

    Verwaltet die Spielschleife, Events und das Rendering.
    Verbindet Menü, Spielobjekte und Spiellogik.

    Attribute:
        screen: Pygame Display Surface
        clock: Pygame Clock für FPS-Begrenzung
        running: Ob das Spiel läuft
        in_menu: Ob das Menü angezeigt wird
    """

    def __init__(self):
        """Initialisiert Pygame und das Spielfenster."""
        pygame.init()

        # Bildschirmgröße ermitteln (anpassbar an Display)
        info = pygame.display.Info()
        self.screen_width: int = min(info.current_w - 100, 1024)
        self.screen_height: int = min(info.current_h - 100, 700)

        self.screen: pygame.Surface = pygame.display.set_mode(
            (self.screen_width, self.screen_height)
        )
        pygame.display.set_caption(WINDOW_TITLE)

        self.clock: pygame.time.Clock = pygame.time.Clock()
        self.running: bool = True
        self.in_menu: bool = True

        # Menü initialisieren
        self.menu: Menu = Menu(self.screen_width, self.screen_height)

        # Schwierigkeitsgrad
        self.difficulty: str = DIFFICULTY_MEDIUM

        # Spielobjekte (werden bei Spielstart initialisiert)
        self.truck: Truck = None
        self.helicopter: Helicopter = None
        self.source: Source = None
        self.destination: Destination = None
        self.gas_station: GasStation = None
        self.game_logic: GameLogic = None
        self.hud: HUD = None

    def _generate_random_position(self, existing_positions: list,
                                   margin: int = 80) -> tuple:
        """
        Erzeugt eine zufällige Position mit Mindestabstand zu bestehenden.

        Args:
            existing_positions: Liste bereits platzierter (x, y) Positionen.
            margin: Rand zum Bildschirmrand.

        Returns:
            (x, y) Tupel der neuen Position.
        """
        hud_height = 60
        for _ in range(200):
            x = random.randint(margin, self.screen_width - margin)
            y = random.randint(hud_height + margin, self.screen_height - margin)

            too_close = False
            for px, py in existing_positions:
                dist = math.sqrt((x - px) ** 2 + (y - py) ** 2)
                if dist < MIN_BUILDING_DISTANCE:
                    too_close = True
                    break

            if not too_close:
                return (x, y)

        # Fallback falls kein Platz gefunden
        return (random.randint(margin, self.screen_width - margin),
                random.randint(hud_height + margin, self.screen_height - margin))

    def _init_game_objects(self) -> None:
        """Initialisiert alle Spielobjekte mit zufälligen Positionen."""
        positions = []

        source_pos = self._generate_random_position(positions)
        positions.append(source_pos)

        dest_pos = self._generate_random_position(positions)
        positions.append(dest_pos)

        gas_pos = self._generate_random_position(positions)
        positions.append(gas_pos)

        heli_pos = self._generate_random_position(positions)

        # Schwierigkeitsgrad-Einstellungen laden
        settings = DIFFICULTY_SETTINGS[self.difficulty]

        # Spielobjekte erstellen
        self.source = Source(source_pos[0], source_pos[1])
        self.destination = Destination(dest_pos[0], dest_pos[1])
        self.gas_station = GasStation(gas_pos[0], gas_pos[1])
        self.truck = Truck(source_pos[0], source_pos[1] + 60)
        self.truck.fuel_consumption = settings["fuel_consumption"]
        self.helicopter = Helicopter(heli_pos[0], heli_pos[1])
        self.helicopter.set_screen_size(self.screen_width, self.screen_height)
        self.helicopter.speed = settings["helicopter_speed"]
        self.helicopter.cooldown_max = settings["helicopter_cooldown"]
        self.game_logic = GameLogic()
        self.hud = HUD(self.screen_width, self.screen_height)

    def run(self) -> None:
        """Hauptspielschleife."""
        while self.running:
            self.clock.tick(FPS)

            if self.in_menu:
                self._handle_menu_events()
                self.menu.draw(self.screen)
            else:
                self._handle_game_events()
                self._update()
                self._draw()

            pygame.display.flip()

        pygame.quit()
        sys.exit()

    def _handle_menu_events(self) -> None:
        """Verarbeitet Events im Menü."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                action = self.menu.handle_click(event.pos)
                if action == "start":
                    self.difficulty = self.menu.selected_difficulty
                    self._init_game_objects()
                    self.in_menu = False
                elif action == "quit":
                    self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.difficulty = self.menu.selected_difficulty
                    self._init_game_objects()
                    self.in_menu = False
                elif event.key == pygame.K_ESCAPE:
                    self.running = False

    def _handle_game_events(self) -> None:
        """Verarbeitet Events während des Spiels."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if self.game_logic.state in (GameState.WON, GameState.LOST):
                    if event.key == pygame.K_RETURN:
                        self._init_game_objects()
                    elif event.key == pygame.K_ESCAPE:
                        self.in_menu = True
                elif event.key == pygame.K_ESCAPE:
                    self.in_menu = True

    def _get_movement_input(self) -> tuple:
        """
        Liest die aktuelle Bewegungsrichtung aus gehaltenen Tasten.

        Returns:
            (dx, dy) Tupel mit Richtungswerten (-1, 0, 1).
        """
        keys = pygame.key.get_pressed()
        dx = 0
        dy = 0

        # WASD und Pfeiltasten
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dy -= 1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dy += 1
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx -= 1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx += 1

        return dx, dy

    def _update(self) -> None:
        """Aktualisiert den Spielzustand pro Frame."""
        if self.game_logic.state != GameState.RUNNING:
            return

        # LKW per WASD/Pfeiltasten bewegen
        dx, dy = self._get_movement_input()
        self.truck.move(dx, dy, self.screen_width, self.screen_height)

        # Spiellogik aktualisieren
        self.game_logic.update(
            self.truck, self.helicopter,
            self.source, self.destination,
            self.gas_station
        )

    def _draw(self) -> None:
        """Zeichnet alle Spielobjekte und UI-Elemente."""
        # Hintergrund
        self.screen.fill(LIGHT_BLUE)

        # Straßen/Wege zeichnen
        self._draw_roads()

        # Spielobjekte zeichnen
        self.source.draw(self.screen)
        self.destination.draw(self.screen, self.game_logic.ore_total)
        self.gas_station.draw(self.screen)
        self.truck.draw(self.screen)
        self.helicopter.draw(self.screen)

        # HUD zeichnen
        self.hud.draw(
            self.screen,
            self.truck.fuel, self.truck.fuel_max,
            self.truck.cargo, self.truck.capacity,
            self.destination.ore_delivered,
            self.source.ore_remaining,
            self.helicopter.stolen_total,
            self.game_logic.ore_total
        )

        # Game-Over-Anzeige
        if self.game_logic.state == GameState.WON:
            self.hud.draw_game_over(self.screen, won=True)
        elif self.game_logic.state == GameState.LOST:
            self.hud.draw_game_over(self.screen, won=False)

    def _draw_roads(self) -> None:
        """Zeichnet Verbindungswege zwischen den Stationen."""
        road_color = (180, 180, 180)
        road_width = 4

        # Quelle -> Ziel
        pygame.draw.line(
            self.screen, road_color,
            (int(self.source.x), int(self.source.y)),
            (int(self.destination.x), int(self.destination.y)),
            road_width
        )
        # Quelle -> Tankstelle
        pygame.draw.line(
            self.screen, road_color,
            (int(self.source.x), int(self.source.y)),
            (int(self.gas_station.x), int(self.gas_station.y)),
            road_width
        )
        # Tankstelle -> Ziel
        pygame.draw.line(
            self.screen, road_color,
            (int(self.gas_station.x), int(self.gas_station.y)),
            (int(self.destination.x), int(self.destination.y)),
            road_width
        )
        # Tankstelle -> Quelle (Rückweg)
        pygame.draw.line(
            self.screen, road_color,
            (int(self.gas_station.x), int(self.gas_station.y)),
            (int(self.source.x), int(self.source.y)),
            road_width
        )
