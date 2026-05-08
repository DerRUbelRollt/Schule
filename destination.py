"""
Destination (Ziel) Klasse für das Transporter-Spiel.
Das Ziel ist der Ort an dem das Erz abgeliefert werden muss.
"""

import pygame
from config import GREEN, BLACK, WHITE, DARK_GRAY


class Destination:
    """
    Repräsentiert das Ziel (Lager) im Spiel.

    Attribute:
        x, y: Position des Ziels
        ore_delivered: Bisher abgeliefertes Erz
    """

    def __init__(self, x: float, y: float):
        """Initialisiert das Ziel ohne abgeliefertes Erz."""
        self.x: float = x
        self.y: float = y
        self.ore_delivered: int = 0
        self.width: int = 80
        self.height: int = 60

    def deliver_ore(self, amount: int) -> None:
        """
        Liefert Erz am Ziel ab.

        Args:
            amount: Menge des abgelieferten Erzes.
        """
        self.ore_delivered += amount

    def get_rect(self) -> pygame.Rect:
        """Gibt das Interaktions-Rechteck des Ziels zurück."""
        return pygame.Rect(
            int(self.x - self.width // 2),
            int(self.y - self.height // 2),
            self.width,
            self.height
        )

    def draw(self, screen: pygame.Surface, ore_total: int) -> None:
        """
        Zeichnet das Ziel auf den Bildschirm.

        Args:
            screen: Pygame Surface zum Zeichnen.
            ore_total: Gesamte Erzmenge (für Fortschrittsanzeige).
        """
        x = int(self.x)
        y = int(self.y)

        # Lagerhaus-Form
        base_rect = pygame.Rect(x - 35, y - 10, 70, 40)
        pygame.draw.rect(screen, DARK_GRAY, base_rect)
        pygame.draw.rect(screen, BLACK, base_rect, 2)

        # Dach
        roof_points = [
            (x - 40, y - 10),
            (x, y - 30),
            (x + 40, y - 10)
        ]
        pygame.draw.polygon(screen, (100, 100, 120), roof_points)
        pygame.draw.polygon(screen, BLACK, roof_points, 2)

        # Tor
        gate_rect = pygame.Rect(x - 12, y + 5, 24, 25)
        pygame.draw.rect(screen, (60, 60, 60), gate_rect)
        pygame.draw.rect(screen, BLACK, gate_rect, 1)

        # Label
        font = pygame.font.SysFont("Arial", 14)
        label = font.render("ZIEL", True, BLACK)
        label_rect = label.get_rect(center=(x, y - 42))

        bg_rect = label_rect.inflate(10, 4)
        pygame.draw.rect(screen, (200, 220, 255), bg_rect)
        pygame.draw.rect(screen, BLACK, bg_rect, 1)
        screen.blit(label, label_rect)

        # Fortschrittsanzeige
        if ore_total > 0:
            progress = self.ore_delivered / ore_total
            bar_width = 60
            bar_height = 8
            bar_x = x - bar_width // 2
            bar_y = y + 35

            pygame.draw.rect(screen, (200, 200, 200), (bar_x, bar_y, bar_width, bar_height))
            pygame.draw.rect(screen, GREEN, (bar_x, bar_y, int(bar_width * progress), bar_height))
            pygame.draw.rect(screen, BLACK, (bar_x, bar_y, bar_width, bar_height), 1)

            amount_text = font.render(f"{self.ore_delivered}t", True, WHITE)
            amount_rect = amount_text.get_rect(center=(x, y + 50))
            screen.blit(amount_text, amount_rect)
