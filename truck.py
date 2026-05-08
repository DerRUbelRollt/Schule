"""
Truck (LKW) Klasse für das Transporter-Spiel.
Der LKW transportiert Erz von der Quelle zum Ziel und verbraucht dabei Sprit.
"""

import pygame
import math
from config import (
    TRUCK_CAPACITY, TRUCK_FUEL_MAX, TRUCK_FUEL_CONSUMPTION,
    TRUCK_SPEED, YELLOW, ORANGE, DARK_GRAY, BLACK, WHITE, RED, GREEN
)


class Truck:
    """
    Repräsentiert den LKW (Transporter) im Spiel.

    Attribute:
        x, y: Aktuelle Position
        speed: Bewegungsgeschwindigkeit
        fuel: Aktueller Tankfüllstand
        fuel_max: Maximaler Tankfüllstand
        capacity: Maximale Ladekapazität
        cargo: Aktuell geladenes Erz
        fuel_consumption: Spritverbrauch pro Pixel
    """

    def __init__(self, x: float, y: float):
        """Initialisiert den LKW an der gegebenen Position."""
        self.x: float = x
        self.y: float = y
        self.speed: int = TRUCK_SPEED
        self.fuel: float = TRUCK_FUEL_MAX
        self.fuel_max: float = TRUCK_FUEL_MAX
        self.capacity: int = TRUCK_CAPACITY
        self.cargo: int = 0
        self.fuel_consumption: float = TRUCK_FUEL_CONSUMPTION
        self.width: int = 60
        self.height: int = 35
        self.target: tuple = None
        self.moving: bool = False

    def move(self, dx: int, dy: int, screen_width: int, screen_height: int) -> None:
        """
        Bewegt den LKW in die angegebene Richtung (WASD/Pfeiltasten).

        Args:
            dx: Richtung horizontal (-1, 0, 1)
            dy: Richtung vertikal (-1, 0, 1)
            screen_width: Bildschirmbreite für Begrenzung
            screen_height: Bildschirmhöhe für Begrenzung
        """
        if dx == 0 and dy == 0:
            self.moving = False
            return

        # Normalisieren bei diagonaler Bewegung
        if dx != 0 and dy != 0:
            length = math.sqrt(dx * dx + dy * dy)
            dx = dx / length
            dy = dy / length

        move_distance = self.speed
        fuel_needed = move_distance * self.fuel_consumption

        if self.fuel >= fuel_needed:
            new_x = self.x + dx * move_distance
            new_y = self.y + dy * move_distance

            # Bildschirmbegrenzung (HUD-Bereich oben berücksichtigen)
            new_x = max(self.width // 2, min(screen_width - self.width // 2, new_x))
            new_y = max(60 + self.height // 2, min(screen_height - self.height // 2, new_y))

            self.x = new_x
            self.y = new_y
            self.fuel -= fuel_needed
            self.moving = True
        else:
            self.moving = False

    def load_ore(self, available_ore: int) -> int:
        """
        Lädt Erz auf den LKW.

        Args:
            available_ore: Verfügbare Erzmenge an der Quelle.

        Returns:
            Tatsächlich geladene Menge.
        """
        load_amount = min(self.capacity - self.cargo, available_ore)
        self.cargo += load_amount
        return load_amount

    def unload_ore(self) -> int:
        """
        Entlädt das gesamte Erz am Ziel.

        Returns:
            Entladene Menge.
        """
        unloaded = self.cargo
        self.cargo = 0
        return unloaded

    def refuel(self) -> None:
        """Tankt den LKW vollständig auf."""
        self.fuel = self.fuel_max

    def has_fuel(self) -> bool:
        """Prüft ob der LKW noch Sprit hat."""
        return self.fuel > 0

    def get_rect(self) -> pygame.Rect:
        """Gibt das Kollisions-Rechteck des LKW zurück."""
        return pygame.Rect(
            int(self.x - self.width // 2),
            int(self.y - self.height // 2),
            self.width,
            self.height
        )

    def draw(self, screen: pygame.Surface) -> None:
        """
        Zeichnet den LKW auf den Bildschirm.

        Args:
            screen: Pygame Surface zum Zeichnen.
        """
        x = int(self.x)
        y = int(self.y)

        # Fahrerkabine
        cabin_rect = pygame.Rect(x - 30, y - 15, 20, 30)
        pygame.draw.rect(screen, DARK_GRAY, cabin_rect)
        pygame.draw.rect(screen, BLACK, cabin_rect, 2)

        # Ladefläche
        cargo_rect = pygame.Rect(x - 10, y - 18, 40, 36)
        pygame.draw.rect(screen, YELLOW, cargo_rect)
        pygame.draw.rect(screen, BLACK, cargo_rect, 2)

        # Erz auf der Ladefläche anzeigen
        if self.cargo > 0:
            fill_ratio = self.cargo / self.capacity
            ore_height = int(30 * fill_ratio)
            ore_rect = pygame.Rect(x - 8, y + 16 - ore_height, 36, ore_height)
            pygame.draw.rect(screen, ORANGE, ore_rect)

        # Räder
        pygame.draw.circle(screen, BLACK, (x - 20, y + 20), 6)
        pygame.draw.circle(screen, BLACK, (x + 10, y + 20), 6)
        pygame.draw.circle(screen, BLACK, (x + 25, y + 20), 6)

        # Spritanzeige über dem LKW
        fuel_bar_width = 50
        fuel_bar_height = 6
        fuel_x = x - fuel_bar_width // 2
        fuel_y = y - 28

        pygame.draw.rect(screen, RED, (fuel_x, fuel_y, fuel_bar_width, fuel_bar_height))
        fuel_fill = int(fuel_bar_width * (self.fuel / self.fuel_max))
        pygame.draw.rect(screen, GREEN, (fuel_x, fuel_y, fuel_fill, fuel_bar_height))
        pygame.draw.rect(screen, BLACK, (fuel_x, fuel_y, fuel_bar_width, fuel_bar_height), 1)
