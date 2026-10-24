# Reliable Smart Parking

This repository contains a Micro:bit smart parking system developed by Group 14, together with a small reliability improvement made after the original group project.

## Original project

The original system used two Micro:bit V2 boards and several ultrasonic sensors. Its main functions were automatic entrance and exit barriers, wireless communication, an OLED display, red and green parking LEDs, a NeoPixel guidance strip, a buzzer warning, and an RGB lighting program.

The original MicroPython programs are kept in the `original` folder:

- `entry_node.py`
- `exit_node.py`
- `parking_node.py`
- `environmental_lighting.py`

## Reliability improvement

In the original parking program, the LED state was decided from one ultrasonic distance reading. A single incorrect reading could make a parking space appear empty or occupied at the wrong time.

The new `parking_system.py` keeps the original hardware idea, but separates the sensor decision from the Micro:bit hardware code.

It adds three small changes:

1. The median of the latest five distance readings reduces the effect of an occasional sensor spike.
2. A space must be detected twice below 10 cm before becoming `OCCUPIED`.
3. A space must be detected twice above 12 cm before becoming `EMPTY`.

The different entry and exit thresholds prevent the LED from changing repeatedly when a vehicle is close to the boundary. The entrance, exit, radio, OLED, servo and lighting functions are not redesigned.

## Run the tests

The Python part uses only the standard library. From the project folder, run:

```text
python -m unittest discover -s tests -v
```

The tests cover an ultrasonic spike, a vehicle entering, a vehicle leaving, readings close to the threshold, and invalid filter settings.

## Run the simulation

To print an example sequence of sensor readings and the resulting states:

```text
python simulation/run_simulation.py
```

The simulation is not a replacement for testing the real circuit. It is a quick way to check the filtering and state logic before downloading code to a Micro:bit.

## Using the logic with the original parking program

Keep the original `get_distance(trig, echo)` function and pass its result to the controller:

```python
from parking_system import ParkingController, ParkingState

controller = ParkingController(sample_count=5, confirmations=2)
distance_cm = get_distance(trig1, echo1)
state = controller.update(distance_cm)

if state == ParkingState.OCCUPIED:
    led1_red.write_digital(0)
    led1_green.write_digital(1)
else:
    led1_red.write_digital(1)
    led1_green.write_digital(0)
```

The same controller pattern can be used for the second parking space.

## Hardware pin reference

These pins are taken from the original group project. Check the physical circuit before using them again.

- Entry and exit gate: servo on pin 0, ultrasonic trigger and echo on pins 1 and 2, OLED I2C on pins 20 and 19.
- Parking space 1: ultrasonic pins 0 and 1, LEDs on pins 2 and 3.
- Parking space 2: ultrasonic pins 8 and 9, LEDs on pins 10 and 12.
- NeoPixel strip: pin 16.
- Buzzer: pin 15.

## Project structure

```text
original/                     Original MicroPython programs
parking_system.py             Filter and parking-state logic
tests/                        Python unit tests
simulation/run_simulation.py  Small command-line simulation
README.md                     Project documentation
```

