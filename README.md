# Reliable Smart Parking

This repository contains our Group 14 Micro:bit smart-parking group project and a small reliability improvement I added afterwards.

## The original group project

The original system used two Micro:bit V2 boards. The entry and exit boards communicated through Radio group 10. They controlled servo barriers, HC-SR04 ultrasonic sensors and an I2C OLED. A separate parking board showed whether two spaces were free, used NeoPixels as a guide, and sounded a buzzer when a car was too close. There was also a simple RGB ambient-light program.

The original code is kept in `original/`:

- `entry_node.py` opens the entrance gate and tracks available spaces.
- `exit_node.py` reads the entry time, displays the stay duration and releases a space.
- `parking_node.py` controls the two parking spaces, LEDs, NeoPixel strip and alarm.
- `environmental_lighting.py` controls the RGB lighting effect.

## 运行仿真测试

在项目根目录执行：

```text
python -m unittest discover -s tests -v
```

当前实现只使用 Python 标准库，不需要安装依赖。

## Small reliability upgrade

The old parking code made the red/green decision from one ultrasonic reading. That worked in a simple demonstration, but one bad reading could make a space change state incorrectly.

The added `parking_system.py` keeps the hardware reading separate from the decision logic:

```text
EMPTY -- two readings below 10 cm --> OCCUPIED
OCCUPIED -- two readings above 12 cm --> EMPTY
```

The different 10 cm and 12 cm thresholds stop the indicator from flickering when a car is close to the boundary. This is deliberately a small change. The Radio messages, OLED, servo control, NeoPixel guidance and lighting program are not replaced.

## Test it without a Micro:bit

Run the Python tests with:

```text
python -m unittest discover -s tests -v
```

The tests cover an ultrasonic spike, car arrival, car departure, boundary readings and invalid settings. The code uses only the Python standard library.

To connect the logic to the original parking program, keep the existing `get_distance(trig, echo)` function and pass its result to `ParkingController.update(distance_cm)`. Use the returned `ParkingState` to choose the red or green LED output.

## Hardware reference from the original project

 - Entry and exit gate: servo on pin 0, ultrasonic trigger/echo on pins 1/2, OLED I2C on pins 20/19.
 - Parking space 1: ultrasonic pins 0/1 and LEDs on pins 2/3.
 - Parking space 2: ultrasonic pins 8/9 and LEDs on pins 10/12.
 - NeoPixel strip: pin 16.
 - Buzzer: pin 15.

Check the actual wiring and LED polarity before powering the circuit. The Python tests check the decision logic, not the electrical connections.

## CV description

> Improved a two-node Micro:bit smart-parking system by adding median filtering and consecutive-confirmation logic for noisy ultrasonic occupancy readings, and validated the change with Python unit tests.

