# Electrical Architecture Design Review

## System Overview

The self-balancing robot uses a 3S LiPo battery to power both the motor subsystem and the embedded electronics.

The power architecture is divided into two branches:

Battery
|
+--> Motor Power --> Cytron MDD3A --> Left / Right Motors
|
+--> Logic Power --> 5 V Buck --> ESP32 + Encoders
                               |
                               +--> 3.3 V --> IMU

All subsystems share a common electrical ground.

## Selected Hardware

| Subsystem | Component |
|---|---|
| Microcontroller | ESP32-S3 DevKitC-1 N8R8 |
| IMU | LSM6DSOX |
| Motors | 2x Pololu 47:1 25D MP 12 V with encoders |
| Motor Driver | Cytron MDD3A |
| Battery | 3S LiPo 11.1 V |
| Logic Regulator | Pololu D24V10F5 |
| Wheels | 70 mm |

## Design Verification

### Battery to Motor Driver

Maximum LiPo voltage:

12.6 V

MDD3A operating range:

4–16 V

Result:

PASS

### Motor Current

Approximate stall current per motor:

1.8 A

Two motors:

3.6 A maximum theoretical combined stall current

MDD3A capability:

3 A continuous per channel

Result:

PASS

### Logic Power

Battery voltage is reduced to regulated 5 V before powering the ESP32.

The 12.6 V battery voltage is never connected directly to the ESP32.

Result:

PASS

### IMU

The LSM6DSOX is powered from the ESP32 3.3 V rail.

Communication:

I2C

SDA -> GPIO8
SCL -> GPIO9

Result:

PASS

### Encoders

Encoder supply:

5 V

Encoder outputs:

0–5 V

ESP32 input logic:

3.3 V

Each encoder A/B output therefore uses a resistor divider:

10 kOhm series resistor
20 kOhm resistor to ground

Resulting maximum GPIO voltage:

approximately 3.33 V

Result:

PASS

### Ground Reference

The following systems share a common ground:

- Battery
- Motor driver
- Buck regulator
- ESP32
- IMU
- Encoders

Result:

PASS

### ESP32 USB Safety

USB power and external 5 V power must not be connected simultaneously without appropriate isolation.

Development rule:

USB debugging -> robot 5 V supply disconnected

Battery operation -> USB power disconnected

Result:

PASS

## Final Pin Mapping

| Function | GPIO |
|---|---:|
| Left Encoder A | GPIO4 |
| Left Encoder B | GPIO5 |
| Right Encoder A | GPIO6 |
| Right Encoder B | GPIO7 |
| IMU SDA | GPIO8 |
| IMU SCL | GPIO9 |
| Motor Left A | GPIO10 |
| Motor Left B | GPIO11 |
| Motor Right A | GPIO12 |
| Motor Right B | GPIO13 |
| IMU INT1 | GPIO14 |

## Hardware Safety Rules

1. Never connect the LiPo battery directly to the ESP32.
2. Never bypass the main fuse.
3. Never reverse battery polarity.
4. Never connect a 5 V encoder output directly to an ESP32 GPIO.
5. Always verify common ground before enabling motors.
6. Test motor direction with the robot lifted from the floor.
7. Implement an emergency motor shutdown in firmware.
8. Disconnect the battery before modifying wiring.
9. Avoid simultaneous USB and external 5 V powering of the ESP32.
10. Stop testing if the motor driver, battery, regulator or motors become abnormally hot.

## Design Review Status

Electrical architecture: APPROVED

Pin mapping: APPROVED

Power architecture: APPROVED

Encoder interface: APPROVED

Motor driver sizing: APPROVED

Ready for modeling and simulation.
