"""
Helicopter (Hubschrauber) Klasse für das Transporter-Spiel.
Der Hubschrauber stiehlt Erz vom LKW während der Fahrt.
"""

import pygame
import math
import random
from config import HELICOPTER_SPEED, HELICOPTER_STEAL_AMOUNT, DARK_GRAY, BLACK, GREEN


class HelicopterState:
    """Zustände des Hubschraubers."""
    IDLE = "idle"
    ATTACKING = "attacking"
    FLEEING = "fleeing"
    OFFSCREEN = "offscreen"
    APPROACHING = "approaching"


class Helicopter:
    """
    Repräsentiert den Hubschrauber (Gegner) im Spiel.

    Der Hubschrauber fliegt zum LKW, stiehlt Erz und kehrt
    dann zur Home-Position zurück.

    Attribute:
        x, y: Aktuelle Position
        home_x, home_y: Ausgangsposition
        speed: Bewegungsgeschwindigkeit
        steal_amount: Menge die pro Diebstahl gestohlen wird
        stolen_total: Gesamtmenge gestohlenes Erz
        state: Aktueller Zustand (idle, attacking, returning)
    """

    def __init__(self, x: float, y: float):
        """Initialisiert den Hubschrauber an seiner Home-Position."""
        self.x: float = x
        self.y: float = y
        self.home_x: float = x
        self.home_y: float = y
        self.speed: int = HELICOPTER_SPEED
        self.steal_amount: int = HELICOPTER_STEAL_AMOUNT
        self.stolen_total: int = 0
        self.state: str = HelicopterState.OFFSCREEN
        self.width: int = 70
        self.height: int = 35
        self.attack_cooldown: int = 0
        self.cooldown_max: int = 120
        self.rotor_angle: float = 0.0
        self.screen_width: int = 0
        self.screen_height: int = 0
        self.flee_target: tuple = None

    def set_screen_size(self, width: int, height: int) -> None:
        """
        Setzt die Bildschirmgröße für Fluchtziel-Berechnung.

        Args:
            width: Bildschirmbreite
            height: Bildschirmhöhe
        """
        self.screen_width = width
        self.screen_height = height
        # Starte außerhalb des Bildschirms
        self.x = -100
        self.y = -100

    def _get_random_offscreen_point(self) -> tuple:
        """Berechnet einen zufälligen Punkt außerhalb des Bildschirms."""
        side = random.choice(["top", "bottom", "left", "right"])
        margin = 120
        if side == "top":
            return (random.randint(0, self.screen_width), -margin)
        elif side == "bottom":
            return (random.randint(0, self.screen_width), self.screen_height + margin)
        elif side == "left":
            return (-margin, random.randint(0, self.screen_height))
        else:
            return (self.screen_width + margin, random.randint(0, self.screen_height))

    def _is_offscreen(self) -> bool:
        """Prüft ob der Hubschrauber außerhalb des Bildschirms ist."""
        margin = 80
        return (self.x < -margin or self.x > self.screen_width + margin or
                self.y < -margin or self.y > self.screen_height + margin)

    def update(self, truck_x: float, truck_y: float, truck_has_cargo: bool) -> int:
        """
        Aktualisiert den Hubschrauber-Zustand.

        Ablauf: OFFSCREEN -> APPROACHING -> ATTACKING -> FLEEING -> OFFSCREEN

        Args:
            truck_x: X-Position des LKW
            truck_y: Y-Position des LKW
            truck_has_cargo: Ob der LKW Ladung hat

        Returns:
            Menge des gestohlenen Erzes in diesem Frame (0 wenn kein Diebstahl).
        """
        self.rotor_angle += 15
        stolen = 0

        if self.state == HelicopterState.OFFSCREEN:
            if self.attack_cooldown > 0:
                self.attack_cooldown -= 1
            elif truck_has_cargo:
                # Vom Bildschirmrand aus anfliegen
                entry = self._get_random_offscreen_point()
                self.x = entry[0]
                self.y = entry[1]
                self.state = HelicopterState.APPROACHING

        elif self.state == HelicopterState.APPROACHING:
            reached = self._move_towards(truck_x, truck_y)
            if reached:
                stolen = self.steal_amount
                self.stolen_total += stolen
                self.flee_target = self._get_random_offscreen_point()
                self.state = HelicopterState.FLEEING

        elif self.state == HelicopterState.FLEEING:
            reached = self._move_towards(self.flee_target[0], self.flee_target[1])
            if reached or self._is_offscreen():
                self.state = HelicopterState.OFFSCREEN
                self.attack_cooldown = self.cooldown_max

        return stolen

    def _move_towards(self, target_x: float, target_y: float) -> bool:
        """
        Bewegt den Hubschrauber zum Zielpunkt.

        Args:
            target_x: X-Koordinate des Ziels
            target_y: Y-Koordinate des Ziels

        Returns:
            True wenn das Ziel erreicht wurde.
        """
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx * dx + dy * dy)

        if distance < self.speed:
            self.x = target_x
            self.y = target_y
            return True

        direction_x = dx / distance
        direction_y = dy / distance

        self.x += direction_x * self.speed
        self.y += direction_y * self.speed
        return False

    def get_rect(self) -> pygame.Rect:
        """Gibt das Kollisions-Rechteck des Hubschraubers zurück."""
        return pygame.Rect(
            int(self.x - self.width // 2),
            int(self.y - self.height // 2),
            self.width,
            self.height
        )

    def draw(self, screen: pygame.Surface) -> None:
        """
        Zeichnet den Hubschrauber auf den Bildschirm.
        Wird nur gezeichnet wenn er sichtbar ist.

        Args:
            screen: Pygame Surface zum Zeichnen.
        """
        # Nicht zeichnen wenn offscreen
        if self.state == HelicopterState.OFFSCREEN:
            return
        if self._is_offscreen():
            return
        x = int(self.x)
        y = int(self.y)

        # Rumpf
        body_points = [
            (x - 25, y),
            (x - 15, y - 10),
            (x + 15, y - 10),
            (x + 25, y),
            (x + 15, y + 10),
            (x - 15, y + 10)
        ]
        pygame.draw.polygon(screen, (60, 100, 60), body_points)
        pygame.draw.polygon(screen, BLACK, body_points, 2)

        # Heckausleger
        pygame.draw.line(screen, DARK_GRAY, (x + 25, y), (x + 45, y - 5), 3)

        # Heckrotor
        pygame.draw.circle(screen, BLACK, (x + 45, y - 5), 6, 2)

        # Hauptrotor
        rotor_length = 35
        rad = math.radians(self.rotor_angle)
        r_x1 = x + int(rotor_length * math.cos(rad))
        r_y1 = y - 15 + int(5 * math.sin(rad))
        r_x2 = x - int(rotor_length * math.cos(rad))
        r_y2 = y - 15 - int(5 * math.sin(rad))
        pygame.draw.line(screen, DARK_GRAY, (r_x1, r_y1), (r_x2, r_y2), 3)

        # Rotormast
        pygame.draw.line(screen, BLACK, (x, y - 10), (x, y - 15), 2)

        # Kufen
        pygame.draw.line(screen, BLACK, (x - 15, y + 10), (x - 15, y + 15), 2)
        pygame.draw.line(screen, BLACK, (x + 15, y + 10), (x + 15, y + 15), 2)
        pygame.draw.line(screen, BLACK, (x - 20, y + 15), (x + 20, y + 15), 2)

        # Status-Indikator
        if self.state == HelicopterState.APPROACHING:
            pygame.draw.circle(screen, (255, 0, 0), (x, y - 22), 4)
        elif self.state == HelicopterState.FLEEING:
            pygame.draw.circle(screen, (255, 255, 0), (x, y - 22), 4)
