"""
GasStation (Tankstelle) Klasse für das Transporter-Spiel.
Die Tankstelle ermöglicht dem LKW das Nachtanken.
"""

import pygame
from config import RED, BLACK, WHITE, YELLOW, DARK_GRAY


class GasStation:
    """
    Repräsentiert die Tankstelle im Spiel.

    Attribute:
        x, y: Position der Tankstelle
    """

    def __init__(self, x: float, y: float):
        """Initialisiert die Tankstelle an der gegebenen Position."""
        self.x: float = x
        self.y: float = y
        self.width: int = 60
        self.height: int = 50

    def get_rect(self) -> pygame.Rect:
        """Gibt das Interaktions-Rechteck der Tankstelle zurück."""
        return pygame.Rect(
            int(self.x - self.width // 2),
            int(self.y - self.height // 2),
            self.width,
            self.height
        )

    def draw(self, screen: pygame.Surface) -> None:
        """
        Zeichnet die Tankstelle auf den Bildschirm.

        Args:
            screen: Pygame Surface zum Zeichnen.
        """
        x = int(self.x)
        y = int(self.y)

        # Zapfsäule
        pillar_rect = pygame.Rect(x - 10, y - 15, 20, 35)
        pygame.draw.rect(screen, RED, pillar_rect)
        pygame.draw.rect(screen, BLACK, pillar_rect, 2)

        # Dach/Überdachung
        roof_rect = pygame.Rect(x - 25, y - 22, 50, 6)
        pygame.draw.rect(screen, DARK_GRAY, roof_rect)
        pygame.draw.rect(screen, BLACK, roof_rect, 1)

        # Zapfhahn
        pygame.draw.line(screen, BLACK, (x + 10, y - 5), (x + 20, y - 10), 3)
        pygame.draw.circle(screen, BLACK, (x + 20, y - 10), 3)

        # Preis-/Anzeige
        display_rect = pygame.Rect(x - 7, y - 12, 14, 10)
        pygame.draw.rect(screen, YELLOW, display_rect)
        pygame.draw.rect(screen, BLACK, display_rect, 1)

        # Label
        font = pygame.font.SysFont("Arial", 14)
        label = font.render("TANKSTELLE", True, BLACK)
        label_rect = label.get_rect(center=(x, y + 28))

        bg_rect = label_rect.inflate(10, 4)
        pygame.draw.rect(screen, (200, 220, 255), bg_rect)
        pygame.draw.rect(screen, BLACK, bg_rect, 1)
        screen.blit(label, label_rect)
