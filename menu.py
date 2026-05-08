"""
Menu Klasse für das Transporter-Spiel.
Stellt das Hauptmenü mit Start-Button, Schwierigkeitsauswahl
und Spielinformationen dar.
"""

import pygame
from config import (
    WHITE, BLACK, BLUE, DARK_BLUE, GRAY, DARK_GRAY,
    LIGHT_BLUE, WINDOW_TITLE,
    DIFFICULTY_EASY, DIFFICULTY_MEDIUM, DIFFICULTY_HARD
)


class Menu:
    """
    Repräsentiert das Hauptmenü des Spiels.

    Bietet Optionen zum Starten, Beenden und Schwierigkeitsauswahl.

    Attributes:
        screen_width: Breite des Bildschirms
        screen_height: Höhe des Bildschirms
        selected_difficulty: Aktuell gewählte Schwierigkeit
    """

    def __init__(self, screen_width: int, screen_height: int):
        """
        Initialisiert das Menü.

        Args:
            screen_width: Bildschirmbreite
            screen_height: Bildschirmhöhe
        """
        self.screen_width: int = screen_width
        self.screen_height: int = screen_height
        self.selected_difficulty: str = DIFFICULTY_MEDIUM
        self.title_font = None
        self.button_font = None
        self.info_font = None
        self._init_fonts()

        # Button-Bereiche
        button_width = 250
        button_height = 50
        center_x = screen_width // 2

        self.start_button = pygame.Rect(
            center_x - button_width // 2,
            screen_height // 2 - 20,
            button_width, button_height
        )
        self.quit_button = pygame.Rect(
            center_x - button_width // 2,
            screen_height // 2 + 60,
            button_width, button_height
        )

        # Schwierigkeits-Buttons
        diff_btn_width = 120
        diff_btn_height = 36
        diff_y = screen_height // 2 - 90
        total_width = 3 * diff_btn_width + 2 * 15
        start_x = center_x - total_width // 2

        self.difficulty_buttons = {
            DIFFICULTY_EASY: pygame.Rect(
                start_x, diff_y, diff_btn_width, diff_btn_height
            ),
            DIFFICULTY_MEDIUM: pygame.Rect(
                start_x + diff_btn_width + 15, diff_y, diff_btn_width, diff_btn_height
            ),
            DIFFICULTY_HARD: pygame.Rect(
                start_x + 2 * (diff_btn_width + 15), diff_y, diff_btn_width, diff_btn_height
            ),
        }

    def _init_fonts(self) -> None:
        """Initialisiert die Schriftarten."""
        self.title_font = pygame.font.SysFont("Arial", 48, bold=True)
        self.button_font = pygame.font.SysFont("Arial", 24)
        self.info_font = pygame.font.SysFont("Arial", 16)

    def handle_click(self, pos: tuple) -> str:
        """
        Verarbeitet einen Mausklick im Menü.

        Args:
            pos: (x, y) Klick-Position.

        Returns:
            "start", "quit", "difficulty_<name>" oder "".
        """
        if self.start_button.collidepoint(pos):
            return "start"
        elif self.quit_button.collidepoint(pos):
            return "quit"

        for diff_name, rect in self.difficulty_buttons.items():
            if rect.collidepoint(pos):
                self.selected_difficulty = diff_name
                return f"difficulty_{diff_name}"

        return ""

    def draw(self, screen: pygame.Surface) -> None:
        """
        Zeichnet das Menü auf den Bildschirm.

        Args:
            screen: Pygame Surface zum Zeichnen.
        """
        screen.fill(LIGHT_BLUE)

        # Titel-Banner
        banner_rect = pygame.Rect(0, 30, self.screen_width, 80)
        pygame.draw.rect(screen, BLUE, banner_rect)
        pygame.draw.rect(screen, DARK_BLUE, banner_rect, 3)

        title_text = self.title_font.render("TRANSPORTER", True, WHITE)
        title_rect = title_text.get_rect(center=(self.screen_width // 2, 70))
        screen.blit(title_text, title_rect)

        # Untertitel
        subtitle = self.info_font.render("Erz-Transport Spiel", True, DARK_GRAY)
        subtitle_rect = subtitle.get_rect(center=(self.screen_width // 2, 130))
        screen.blit(subtitle, subtitle_rect)

        # Schwierigkeits-Label
        diff_label = self.button_font.render("Schwierigkeit:", True, BLACK)
        diff_label_rect = diff_label.get_rect(
            center=(self.screen_width // 2, self.screen_height // 2 - 120)
        )
        screen.blit(diff_label, diff_label_rect)

        # Schwierigkeits-Buttons
        diff_colors = {
            DIFFICULTY_EASY: (34, 139, 34),
            DIFFICULTY_MEDIUM: (255, 165, 0),
            DIFFICULTY_HARD: (220, 20, 60),
        }
        for diff_name, rect in self.difficulty_buttons.items():
            color = diff_colors[diff_name]
            is_selected = (diff_name == self.selected_difficulty)

            if is_selected:
                highlight = rect.inflate(6, 6)
                pygame.draw.rect(screen, (255, 255, 0), highlight, border_radius=6)

            pygame.draw.rect(screen, color, rect, border_radius=6)
            pygame.draw.rect(screen, BLACK, rect, 2, border_radius=6)

            text = self.info_font.render(diff_name, True, WHITE)
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)

        # Start-Button
        self._draw_button(screen, self.start_button, "Spiel starten", BLUE)

        # Quit-Button
        self._draw_button(screen, self.quit_button, "Beenden", DARK_GRAY)

        # Spielanleitung
        self._draw_instructions(screen)

    def _draw_button(self, screen: pygame.Surface, rect: pygame.Rect,
                     text: str, color: tuple) -> None:
        """
        Zeichnet einen Button.

        Args:
            screen: Pygame Surface.
            rect: Button-Rechteck.
            text: Button-Beschriftung.
            color: Button-Farbe.
        """
        shadow_rect = rect.copy()
        shadow_rect.x += 3
        shadow_rect.y += 3
        pygame.draw.rect(screen, DARK_GRAY, shadow_rect, border_radius=8)

        pygame.draw.rect(screen, color, rect, border_radius=8)
        pygame.draw.rect(screen, BLACK, rect, 2, border_radius=8)

        text_surface = self.button_font.render(text, True, WHITE)
        text_rect = text_surface.get_rect(center=rect.center)
        screen.blit(text_surface, text_rect)

    def _draw_instructions(self, screen: pygame.Surface) -> None:
        """Zeichnet die Spielanleitung unter den Buttons."""
        instructions = [
            "Steuerung:",
            "W/↑ - Hoch    S/↓ - Runter",
            "A/← - Links   D/→ - Rechts",
            "",
            "Ziel: Transportiere 80% des Erzes zum Ziel!",
            "Fahre zur Quelle zum Laden, zum Ziel zum Abladen.",
            "Achtung: Der Hubschrauber stiehlt dein Erz!"
        ]

        start_y = self.screen_height // 2 + 140
        for i, line in enumerate(instructions):
            color = DARK_BLUE if i == 0 else BLACK
            text = self.info_font.render(line, True, color)
            text_rect = text.get_rect(center=(self.screen_width // 2, start_y + i * 22))
            screen.blit(text, text_rect)
