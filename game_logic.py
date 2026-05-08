"""
GameLogic Klasse für das Transporter-Spiel.
Enthält die gesamte Spiellogik: Gewinn-/Verlustbedingungen,
Interaktionen zwischen Objekten und Spielzustands-Verwaltung.
"""

from config import WIN_THRESHOLD, ORE_TOTAL
from truck import Truck
from helicopter import Helicopter
from source import Source
from destination import Destination
from gas_station import GasStation


class GameState:
    """Mögliche Spielzustände."""
    RUNNING = "running"
    WON = "won"
    LOST = "lost"


class LoseReason:
    """Mögliche Niederlage-Gründe."""
    HELICOPTER_STOLE_ALL = "helicopter_stole_all"
    OUT_OF_FUEL = "out_of_fuel"


class GameLogic:
    """
    Verwaltet die Spiellogik und Regeln des Transporter-Spiels.

    Verantwortlich für:
    - Prüfung der Gewinn-/Verlustbedingungen
    - Interaktion zwischen Spielobjekten (Laden, Entladen, Tanken)
    - Berechnung des Spielfortschritts

    Attribute:
        state: Aktueller Spielzustand
        win_threshold: Prozentsatz zum Gewinnen (N)
        ore_total: Gesamtmenge des Erzes
    """

    def __init__(self):
        """Initialisiert die Spiellogik."""
        self.state: str = GameState.RUNNING
        self.lose_reason: str | None = None
        self.win_threshold: float = WIN_THRESHOLD
        self.ore_total: int = ORE_TOTAL

    def check_win_condition(self, destination: Destination) -> bool:
        """
        Prüft ob die Gewinnbedingung erfüllt ist.

        Gewonnen wenn N% oder mehr des Erzes transportiert wurden.

        Args:
            destination: Das Ziel-Objekt.

        Returns:
            True wenn gewonnen.
        """
        delivered_ratio = destination.ore_delivered / self.ore_total
        return delivered_ratio >= self.win_threshold

    def check_lose_condition(self, helicopter: Helicopter, truck: Truck,
                             source: Source, destination: Destination) -> str | None:
        """
        Prüft ob die Verlustbedingung erfüllt ist.

        Verloren wenn:
        - Hubschrauber mehr als (1-N)% gestohlen hat
        - Nicht gewonnen und LKW hat keinen Sprit mehr

        Args:
            helicopter: Der Hubschrauber.
            truck: Der LKW.
            source: Die Quelle.
            destination: Das Ziel.

        Returns:
            Den Niederlage-Grund oder None.
        """
        # Bedingung 1: Hubschrauber hat zu viel gestohlen
        max_steal = self.ore_total * (1 - self.win_threshold)
        if helicopter.stolen_total > max_steal:
            return LoseReason.HELICOPTER_STOLE_ALL

        # Bedingung 2: Nicht mehr fahrfähig und nicht genug geliefert
        if not truck.can_move() and not self.check_win_condition(destination):
            # Prüfen ob noch genug Erz theoretisch transportierbar wäre
            remaining_needed = (self.ore_total * self.win_threshold) - destination.ore_delivered
            if remaining_needed > 0:
                return LoseReason.OUT_OF_FUEL

        return None

    def try_load_at_source(self, truck: Truck, source: Source) -> bool:
        """
        Versucht Erz an der Quelle zu laden.

        Args:
            truck: Der LKW.
            source: Die Quelle.

        Returns:
            True wenn Erz geladen wurde.
        """
        truck_rect = truck.get_rect()
        source_rect = source.get_rect()

        if truck_rect.colliderect(source_rect) and source.has_ore():
            available = source.take_ore(truck.capacity - truck.cargo)
            if available > 0:
                truck.cargo += available
                return True
        return False

    def try_unload_at_destination(self, truck: Truck, destination: Destination) -> bool:
        """
        Versucht Erz am Ziel zu entladen.

        Args:
            truck: Der LKW.
            destination: Das Ziel.

        Returns:
            True wenn Erz entladen wurde.
        """
        truck_rect = truck.get_rect()
        dest_rect = destination.get_rect()

        if truck_rect.colliderect(dest_rect) and truck.cargo > 0:
            amount = truck.unload_ore()
            destination.deliver_ore(amount)
            return True
        return False

    def try_refuel(self, truck: Truck, gas_station: GasStation) -> bool:
        """
        Versucht den LKW an der Tankstelle zu betanken.

        Args:
            truck: Der LKW.
            gas_station: Die Tankstelle.

        Returns:
            True wenn getankt wurde.
        """
        truck_rect = truck.get_rect()
        station_rect = gas_station.get_rect()

        if truck_rect.colliderect(station_rect):
            truck.refuel()
            return True
        return False

    def process_helicopter_steal(self, helicopter: Helicopter, truck: Truck) -> int:
        """
        Verarbeitet den Diebstahl des Hubschraubers.

        Args:
            helicopter: Der Hubschrauber.
            truck: Der LKW.

        Returns:
            Tatsächlich gestohlene Menge.
        """
        stolen = helicopter.update(truck.x, truck.y, truck.cargo > 0)

        if stolen > 0:
            actual_stolen = min(stolen, truck.cargo)
            truck.cargo -= actual_stolen
            # Differenz korrigieren wenn weniger gestohlen wurde als berechnet
            if actual_stolen < stolen:
                helicopter.stolen_total -= (stolen - actual_stolen)
            return actual_stolen
        return 0

    def update(self, truck: Truck, helicopter: Helicopter,
               source: Source, destination: Destination,
               gas_station: GasStation) -> str:
        """
        Aktualisiert den Spielzustand.

        Args:
            truck: Der LKW.
            helicopter: Der Hubschrauber.
            source: Die Quelle.
            destination: Das Ziel.
            gas_station: Die Tankstelle.

        Returns:
            Aktueller Spielzustand als String.
        """
        if self.state != GameState.RUNNING:
            return self.state

        self.lose_reason = None

        # Hubschrauber-Diebstahl verarbeiten
        self.process_helicopter_steal(helicopter, truck)

        # Automatische Interaktionen prüfen
        self.try_load_at_source(truck, source)
        self.try_unload_at_destination(truck, destination)
        self.try_refuel(truck, gas_station)

        # Gewinn-/Verlustbedingungen prüfen
        if self.check_win_condition(destination):
            self.state = GameState.WON
        else:
            lose_reason = self.check_lose_condition(helicopter, truck, source, destination)
            if lose_reason is not None:
                self.lose_reason = lose_reason
                self.state = GameState.LOST

        return self.state

    def get_progress(self, destination: Destination) -> float:
        """
        Berechnet den Fortschritt in Prozent.

        Args:
            destination: Das Ziel.

        Returns:
            Fortschritt als Wert zwischen 0.0 und 1.0.
        """
        return destination.ore_delivered / self.ore_total
