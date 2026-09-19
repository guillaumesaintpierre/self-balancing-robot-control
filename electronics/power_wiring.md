# Power and Wiring Architecture

## Power Architecture

The robot uses a 3S LiPo battery as the main power source.

Nominal battery voltage: 11.1 V  
Maximum charged voltage: 12.6 V

The battery powers two separate branches:

1. Motor power
2. Logic power

## Main Power Distribution

Battery 3S LiPo
        |
        +---- Main Power Switch
        |
        +---- 5 A Fuse
        |
        +-------------------------+
        |                         |
        |                         |
        v                         v
    Cytron MDD3A             5 V Buck Converter
        |                         |
        |                         +---- ESP32-S3 5V pin
        |                         |
        |                         +---- Encoder Vcc
        |
        +---- Left Motor
        |
        +---- Right Motor

All grounds are connected together.

## Battery

Battery type:

3S LiPo

Nominal voltage:

11.1 V

Fully charged voltage:

12.6 V

Capacity target:

1000–1300 mAh

Recommended discharge capability:

>= 25C

## Main Safety Components

The battery positive terminal passes through:

1. Main power switch
2. Inline fuse
3. Power distribution

Recommended fuse:

5 A

The fuse protects the wiring and electronics against accidental short circuits.

## Motor Driver

Motor driver:

Cytron MDD3A

Battery positive:

MDD3A VIN+

Battery negative:

MDD3A GND

Motor 1 output:

Left DC motor

Motor 2 output:

Right DC motor

Control signals:

M1A -> ESP32 GPIO10
M1B -> ESP32 GPIO11

M2A -> ESP32 GPIO12
M2B -> ESP32 GPIO13

ESP32 ground and MDD3A ground must be connected.

## ESP32 Power

The ESP32-S3 is NOT powered directly from the LiPo battery.

The battery voltage is converted to regulated 5 V using:

Pololu D24V10F5

Connections:

Battery + -> Buck VIN

Battery - -> Buck GND

Buck 5V -> ESP32 5V

Buck GND -> ESP32 GND

## IMU Power

LSM6DSOX breakout:

VIN -> ESP32 3.3V

GND -> Common GND

SDA -> GPIO8

SCL -> GPIO9

INT1 -> GPIO14

## Encoder Power

The Pololu Hall encoders require more than 3.3 V.

Therefore:

Encoder Vcc -> 5 V rail

Encoder GND -> Common GND

Each encoder consumes only a small current.

## Encoder Level Shifting

Encoder A/B outputs can reach 5 V.

ESP32 GPIO inputs operate at 3.3 V.

Therefore every encoder signal passes through a resistor divider.

For each signal:

Encoder output
      |
     10k
      |
      +------> ESP32 GPIO
      |
     20k
      |
     GND

The divider produces approximately:

5 V * 20k / (10k + 20k) = 3.33 V

Four resistor dividers are required:

Left Encoder A

Left Encoder B

Right Encoder A

Right Encoder B

## Encoder GPIO Mapping

Left Encoder A:

GPIO4

Left Encoder B:

GPIO5

Right Encoder A:

GPIO6

Right Encoder B:

GPIO7

## Ground Architecture

The following devices MUST share a common electrical ground:

- LiPo battery
- MDD3A
- 5 V regulator
- ESP32-S3
- LSM6DSOX
- Left encoder
- Right encoder

Without a common ground, the control signals do not have a valid common reference.

## Complete Electrical Flow

3S LiPo
   |
Switch
   |
Fuse
   |
   +-----------------------------+
   |                             |
   v                             v
MDD3A                         5V Buck
   |                             |
   |                    +--------+--------+
   |                    |                 |
   v                    v                 v
Motors                ESP32            Encoders
                         |
                         |
                    3.3V output
                         |
                         v
                        IMU

Encoder A/B
   |
Voltage Divider
5V -> 3.3V
   |
   v
ESP32 GPIO

ESP32 PWM
   |
   v
MDD3A
   |
   v
Motors


## ESP32 Power Safety


The ESP32-S3 DevKitC-1 can be powered either from USB or from the external 5 V pin.

These power supply methods must not be used simultaneously unless proper power isolation is implemented.

During development:

- USB connected -> external 5 V supply disconnected
- Robot powered from battery -> USB power disconnected

Serial telemetry can later be implemented with appropriate isolation or by using wireless telemetry.
