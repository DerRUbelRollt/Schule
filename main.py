"""
Transporter - Erz Transport Spiel
==================================

Ein Pygame-basiertes Spiel bei dem ein LKW Erz von einer Quelle
zu einem Ziel transportieren muss, während ein Hubschrauber
versucht das Erz zu stehlen.

Einstiegspunkt des Spiels.
"""

from game import Game


def main() -> None:
    """Startet das Transporter-Spiel."""
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
