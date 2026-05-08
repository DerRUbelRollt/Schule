"""
Source (Quelle) Klasse für das Transporter-Spiel.
Die Quelle enthält das Erz das transportiert werden muss.
"""

import pygame
from config import BROWN, BLACK, WHITE, ORANGE, ORE_TOTAL


class Source:
    """
    Repräsentiert die Erz-Quelle im Spiel.

    Attribute:
        x, y: Position der Quelle
        ore_remaining: Verbleibende Erzmenge
        ore_total: Gesamte Erzmenge zu Spielbeginn
    """

    def __init__(self, x: float, y: float):
        """Initialisiert die Quelle mit der vollen Erzmenge."""
        self.x: float = x
        self.y: float = y
        self.ore_remaining: int = ORE_TOTAL
        self.ore_total: int = ORE_TOTAL
        self.width: int = 80
        self.height: int = 60

    def take_ore(self, amount: int) -> int:
        """
        Entnimmt Erz aus der Quelle.

        Args:
            amount: Gewünschte Entnahmemenge.

        Returns:
            Tatsächlich entnommene Menge.
        """
        taken = min(amount, self.ore_remaining)
        self.ore_remaining -= taken
        return taken

    def has_ore(self) -> bool:
        """Prüft ob noch Erz vorhanden ist."""
        return self.ore_remaining > 0

    def get_rect(self) -> pygame.Rect:
        """Gibt das Interaktions-Rechteck der Quelle zurück."""
        return pygame.Rect(
            int(self.x - self.width // 2),
            int(self.y - self.height // 2),
            self.width,
            self.height
        )

    def draw(self, screen: pygame.Surface) -> None:
        """
        Zeichnet die Quelle auf den Bildschirm.

        Args:
            screen: Pygame Surface zum Zeichnen.
        """
        x = int(self.x)
        y = int(self.y)

        # Erzhaufen (Trapez-Form)
        fill_ratio = self.ore_remaining / self.ore_total
        base_width = 70
        top_width = int(40 * fill_ratio)
        height = int(45 * fill_ratio) + 10

        points = [
            (x - base_width // 2, y + 20),
            (x + base_width // 2, y + 20),
            (x + top_width // 2, y + 20 - height),
            (x - top_width // 2, y + 20 - height)
        ]
        pygame.draw.polygon(screen, BROWN, points)
        pygame.draw.polygon(screen, BLACK, points, 2)

        # Label
        font = pygame.font.SysFont("Arial", 14)
        label = font.render("QUELLE", True, BLACK)
        label_rect = label.get_rect(center=(x, y - 35))

        # Label-Hintergrund
        bg_rect = label_rect.inflate(10, 4)
        pygame.draw.rect(screen, (200, 220, 255), bg_rect)
        pygame.draw.rect(screen, BLACK, bg_rect, 1)
        screen.blit(label, label_rect)

        # Mengenanzeige
        amount_text = font.render(f"{self.ore_remaining}t", True, WHITE)
        amount_rect = amount_text.get_rect(center=(x, y + 30))
        screen.blit(amount_text, amount_rect)
