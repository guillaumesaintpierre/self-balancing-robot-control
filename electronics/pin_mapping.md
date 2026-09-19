# ESP32-S3 Pin Mapping

## Microcontroller

ESP32-S3 DevKitC-1

## IMU — LSM6DSOX

| Signal | ESP32-S3 Pin |
|---|---|
| SDA | GPIO8 |
| SCL | GPIO9 |
| INT1 | GPIO14 |
| VIN | 3.3V |
| GND | GND |

The LSM6DSOX communicates with the ESP32 using I2C.

Default I2C address:

0x6A

## Left Motor Encoder

| Signal | ESP32-S3 Pin |
|---|---|
| Encoder A | GPIO4 |
| Encoder B | GPIO5 |
| VCC | 5V |
| GND | GND |

## Right Motor Encoder

| Signal | ESP32-S3 Pin |
|---|---|
| Encoder A | GPIO6 |
| Encoder B | GPIO7 |
| VCC | 5V |
| GND | GND |

## Cytron MDD3A Motor Driver

The MDD3A uses dual PWM control.

### Left Motor
### Encoder voltage protection

The Pololu encoder outputs operate at the encoder supply voltage.

The encoders are powered from 5 V, while the ESP32 GPIOs operate at 3.3 V.

Each A/B signal therefore uses a 10k / 20k resistor divider before entering the ESP32.
| Signal | ESP32-S3 Pin |
|---|---|
| M1A | GPIO10 |
| M1B | GPIO11 |

### Right Motor

| Signal | ESP32-S3 Pin |
|---|---|
| M2A | GPIO12 |
| M2B | GPIO13 |

## Reserved Pins

GPIO15 — future push button / emergency input

GPIO16 — future telemetry or additional sensor

GPIO17 — future telemetry or additional sensor

GPIO18 — future expansion

## Pins Intentionally Avoided

GPIO0 — boot strapping

GPIO3 — strapping pin

GPIO19 / GPIO20 — USB

GPIO35 / GPIO36 / GPIO37 — may be used by flash/PSRAM

GPIO43 / GPIO44 — UART programming / debugging

GPIO45 / GPIO46 — strapping pins

## Final Mapping Summary

IMU SDA        -> GPIO8
IMU SCL        -> GPIO9
IMU INT1       -> GPIO14

Encoder Left A -> GPIO4
Encoder Left B -> GPIO5

Encoder Right A -> GPIO6
Encoder Right B -> GPIO7

Motor Left A   -> GPIO10
Motor Left B   -> GPIO11

Motor Right A  -> GPIO12
Motor Right B  -> GPIO13
