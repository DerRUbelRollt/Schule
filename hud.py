"""
HUD (Heads-Up Display) Klasse für das Transporter-Spiel.
Zeigt Spielinformationen wie Fortschritt, Sprit und Status an.
"""

import pygame
from game_logic import LoseReason
from config import (
    WHITE, BLACK, BLUE, GREEN, RED, YELLOW, ORANGE,
    DARK_GRAY, WIN_THRESHOLD, ORE_TOTAL
)


class HUD:
    """
    Heads-Up Display - zeigt alle relevanten Spielinformationen.

    Attribute:
        screen_width: Breite des Bildschirms
        screen_height: Höhe des Bildschirms
    """

    def __init__(self, screen_width: int, screen_height: int):
        """
        Initialisiert das HUD.

        Args:
            screen_width: Bildschirmbreite
            screen_height: Bildschirmhöhe
        """
        self.screen_width: int = screen_width
        self.screen_height: int = screen_height
        self.font = pygame.font.SysFont("Arial", 16)
        self.font_bold = pygame.font.SysFont("Arial", 16, bold=True)
        self.font_large = pygame.font.SysFont("Arial", 20, bold=True)

    def draw(self, screen: pygame.Surface, truck_fuel: float, truck_fuel_max: float,
             truck_cargo: int, truck_capacity: int, ore_delivered: int,
             ore_remaining: int, ore_stolen: int, ore_total: int) -> None:
        """
        Zeichnet das HUD auf den Bildschirm.

        Args:
            screen: Pygame Surface.
            truck_fuel: Aktueller Tankstand.
            truck_fuel_max: Maximaler Tankstand.
            truck_cargo: Aktuelle Ladung.
            truck_capacity: Maximale Ladung.
            ore_delivered: Geliefertes Erz.
            ore_remaining: Verbleibendes Erz an Quelle.
            ore_stolen: Gestohlenes Erz.
            ore_total: Gesamtmenge.
        """
        # HUD-Hintergrund oben
        hud_rect = pygame.Rect(0, 0, self.screen_width, 55)
        hud_surface = pygame.Surface((self.screen_width, 55), pygame.SRCALPHA)
        hud_surface.fill((0, 0, 0, 150))
        screen.blit(hud_surface, (0, 0))

        # Sprit-Anzeige
        self._draw_bar(screen, 10, 8, 150, 18, truck_fuel / truck_fuel_max,
                       GREEN, RED, f"Sprit: {truck_fuel:.0f}/{truck_fuel_max:.0f}")

        # Ladung-Anzeige
        cargo_ratio = truck_cargo / truck_capacity if truck_capacity > 0 else 0
        self._draw_bar(screen, 10, 32, 150, 18, cargo_ratio,
                       ORANGE, DARK_GRAY, f"Ladung: {truck_cargo}/{truck_capacity}t")

        # Fortschritt-Anzeige
        progress = ore_delivered / ore_total if ore_total > 0 else 0
        win_text = f"Geliefert: {ore_delivered}/{ore_total}t ({progress*100:.0f}%)"
        self._draw_bar(screen, 180, 8, 200, 18, progress,
                       BLUE, DARK_GRAY, win_text)

        # Schwellwert-Markierung auf Fortschrittsbalken
        threshold_x = 180 + int(200 * WIN_THRESHOLD)
        pygame.draw.line(screen, YELLOW, (threshold_x, 8), (threshold_x, 26), 2)

        # Gestohlen-Anzeige
        stolen_ratio = ore_stolen / ore_total if ore_total > 0 else 0
        max_steal = ore_total * (1 - WIN_THRESHOLD)
        stolen_text = f"Gestohlen: {ore_stolen}/{int(max_steal)}t"
        stolen_color = RED if ore_stolen > max_steal * 0.7 else YELLOW
        self._draw_bar(screen, 180, 32, 200, 18,
                       min(ore_stolen / max_steal, 1.0) if max_steal > 0 else 0,
                       stolen_color, DARK_GRAY, stolen_text)

        # Steuerung-Hinweis rechts
        controls = self.font.render("[WASD/Pfeiltasten] Bewegen  [ESC] Menü", True, WHITE)
        controls_rect = controls.get_rect(midright=(self.screen_width - 10, 28))
        screen.blit(controls, controls_rect)

    def _draw_bar(self, screen: pygame.Surface, x: int, y: int,
                  width: int, height: int, ratio: float,
                  fill_color: tuple, bg_color: tuple, text: str) -> None:
        """
        Zeichnet einen Fortschrittsbalken mit Text.

        Args:
            screen: Pygame Surface.
            x, y: Position.
            width, height: Größe.
            ratio: Füllstand (0.0 bis 1.0).
            fill_color: Farbe der Füllung.
            bg_color: Hintergrundfarbe.
            text: Beschriftung.
        """
        # Hintergrund
        pygame.draw.rect(screen, bg_color, (x, y, width, height))
        # Füllung
        fill_width = int(width * min(ratio, 1.0))
        pygame.draw.rect(screen, fill_color, (x, y, fill_width, height))
        # Rahmen
        pygame.draw.rect(screen, WHITE, (x, y, width, height), 1)
        # Text
        text_surface = self.font.render(text, True, WHITE)
        text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
        screen.blit(text_surface, text_rect)

    def draw_game_over(self, screen: pygame.Surface, won: bool,
                       lose_reason: str | None = None) -> None:
        """
        Zeichnet den Game-Over-Bildschirm (Gewinn oder Verlust).

        Args:
            screen: Pygame Surface.
            won: True wenn gewonnen, False wenn verloren.
            lose_reason: Spezifischer Niederlage-Grund.
        """
        # Halbtransparenter Overlay
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))

        # Ergebnis-Text
        if won:
            text = "GEWONNEN!"
            color = GREEN
            sub_text = "Du hast genug Erz transportiert!"
        else:
            text = "VERLOREN!"
            color = RED
            if lose_reason == LoseReason.HELICOPTER_STOLE_ALL:
                sub_text = "Der Hubschrauber hat alles geklaut!"
            elif lose_reason == LoseReason.OUT_OF_FUEL:
                sub_text = "Der Sprit ist leer!"
            else:
                sub_text = "Du hast verloren!"

        result_surface = self.font_large.render(text, True, color)
        result_rect = result_surface.get_rect(
            center=(self.screen_width // 2, self.screen_height // 2 - 30)
        )
        screen.blit(result_surface, result_rect)

        sub_surface = self.font.render(sub_text, True, WHITE)
        sub_rect = sub_surface.get_rect(
            center=(self.screen_width // 2, self.screen_height // 2 + 10)
        )
        screen.blit(sub_surface, sub_rect)

        # Neustart-Hinweis
        restart_text = self.font.render(
            "Drücke ENTER für Neustart oder ESC für Menü", True, YELLOW
        )
        restart_rect = restart_text.get_rect(
            center=(self.screen_width // 2, self.screen_height // 2 + 50)
        )
        screen.blit(restart_text, restart_rect)
