"""Small demo for the ultrasonic reliability upgrade."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from parking_system import ParkingState, simulate


def main():
    readings = [20, 20, 6, 60, 7, 6, 6, 20, 21, 20]
    states = simulate(readings)
    for index, (reading, state) in enumerate(zip(readings, states), 1):
        print(f"sample {index:02d}: {reading:>4} cm -> {state.value}")


if __name__ == "__main__":
    main()

