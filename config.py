"""
Konfigurationsdatei für das Transporter-Spiel.
Enthält alle Schwierigkeitsgrad-Konstanten und Spieleinstellungen.
"""

# Fenster-Einstellungen
WINDOW_TITLE = "Transporter - Erz Transport Spiel"
FPS = 60

# Farben
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
BLUE = (70, 130, 180)
DARK_BLUE = (30, 60, 120)
GREEN = (34, 139, 34)
RED = (220, 20, 60)
YELLOW = (255, 215, 0)
ORANGE = (255, 140, 0)
BROWN = (139, 69, 19)
LIGHT_BLUE = (173, 216, 230)

# Spielfeld-Layout (Proportional zum Bildschirm)
SOURCE_POS_RATIO = (0.05, 0.15)       # Quelle oben links
DESTINATION_POS_RATIO = (0.85, 0.35)  # Ziel rechts mitte
GAS_STATION_POS_RATIO = (0.45, 0.85)  # Tankstelle unten mitte
HELICOPTER_HOME_RATIO = (0.5, 0.1)    # Hubschrauber Startposition

# --- Schwierigkeitsgrad-Einstellungen ---

DIFFICULTY_EASY = "Leicht"
DIFFICULTY_MEDIUM = "Mittel"
DIFFICULTY_HARD = "Schwer"

# Spritverbrauch pro Pixel je Schwierigkeitsgrad
DIFFICULTY_SETTINGS = {
    DIFFICULTY_EASY: {
        "fuel_consumption": 0.02,
        "helicopter_speed": 4,
        "helicopter_cooldown": 180,
    },
    DIFFICULTY_MEDIUM: {
        "fuel_consumption": 0.04,
        "helicopter_speed": 5,
        "helicopter_cooldown": 120,
    },
    DIFFICULTY_HARD: {
        "fuel_consumption": 0.08,
        "helicopter_speed": 6,
        "helicopter_cooldown": 70,
    },
}

# Mindestabstand zwischen zufällig platzierten Gebäuden (Pixel)
MIN_BUILDING_DISTANCE = 150

# LKW Einstellungen
TRUCK_CAPACITY = 20          # Ladekapazität des LKW (Tonnen Erz)
TRUCK_FUEL_MAX = 100.0       # Maximaler Tankinhalt
TRUCK_FUEL_CONSUMPTION = 0.04  # Default-Spritverbrauch pro Pixel Bewegung
TRUCK_SPEED = 3              # Geschwindigkeit des LKW (Pixel pro Frame)

# Erz Einstellungen
ORE_TOTAL = 200              # Gesamtmenge an Erz (Tonnen)

# Hubschrauber Einstellungen
HELICOPTER_SPEED = 5         # Geschwindigkeit des Hubschraubers
HELICOPTER_STEAL_AMOUNT = 5  # Menge die pro Diebstahl gestohlen wird

# Gewinn-/Verlust-Schwellwert
WIN_THRESHOLD = 0.80         # N = 80% - Anteil der zum Gewinnen transportiert werden muss
