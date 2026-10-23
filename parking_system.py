"""Hardware-independent reliability upgrade for Group 14's parking project."""

from collections import deque
from enum import Enum


class ParkingState(Enum):
    EMPTY = "empty"
    OCCUPIED = "occupied"


class MedianFilter:
    """Reduce ultrasonic spikes using the median of recent distances."""

    def __init__(self, sample_count=5):
        if sample_count < 1 or sample_count % 2 == 0:
            raise ValueError("sample_count must be a positive odd number")
        self.samples = deque(maxlen=sample_count)

    def update(self, distance_cm):
        if distance_cm < 0:
            raise ValueError("distance_cm cannot be negative")
        self.samples.append(float(distance_cm))
        ordered = sorted(self.samples)
        return ordered[len(ordered) // 2]


class ParkingController:
    """Filter readings and confirm occupancy changes before updating LEDs."""

    def __init__(self, sample_count=5, occupied_below_cm=10,
                 empty_above_cm=12, confirmations=2):
        if not 0 < occupied_below_cm < empty_above_cm:
            raise ValueError("occupied threshold must be below empty threshold")
        if confirmations < 1:
            raise ValueError("confirmations must be positive")
        self.filter = MedianFilter(sample_count)
        self.occupied_below_cm = occupied_below_cm
        self.empty_above_cm = empty_above_cm
        self.confirmations = confirmations
        self.state = ParkingState.EMPTY
        self._pending_ticks = 0

    def update(self, distance_cm):
        distance_cm = self.filter.update(distance_cm)

        target = self.state
        if self.state == ParkingState.EMPTY and distance_cm < self.occupied_below_cm:
            target = ParkingState.OCCUPIED
        elif self.state == ParkingState.OCCUPIED and distance_cm > self.empty_above_cm:
            target = ParkingState.EMPTY

        if target != self.state:
            self._pending_ticks += 1
            if self._pending_ticks >= self.confirmations:
                self.state = target
                self._pending_ticks = 0
        else:
            self._pending_ticks = 0

        return self.state


def simulate(readings, sample_count=5, **options):
    """Run raw ultrasonic distances and return the state per sample."""
    controller = ParkingController(sample_count, **options)
    return [controller.update(reading) for reading in readings]

