# Bill of Materials

## Core Electronics

| Component | Selected Part | Quantity | Status |
|---|---|---:|---|
| Microcontroller | ESP32-S3 DevKitC-1 | 1 | Selected |
| IMU | Adafruit LSM6DSOX | 1 | Selected |
| Motor | Pololu 47:1 25D MP 12V + Encoder | 2 | Selected |
| Motor Driver | Cytron MDD3A | 1 | Selected |
| Wheels | 70 mm | 2 | Selected |
| Battery | 3S LiPo 11.1V 1000-1300mAh | 1 | Selected |
| 5V Regulator | Pololu D24V10F5 | 1 | Selected |
| Power Switch | >= 5A DC | 1 | TBD |
| Chassis | 3D Printed | 1 | Design pending |
| Screws / Spacers | M3 | - | TBD |

## Target Robot Parameters

| Parameter | Target |
|---|---|
| Total mass | 1.0–1.3 kg |
| Height | ~250 mm |
| Width | ~180 mm |
| Wheel diameter | 70 mm |
| Wheel radius | 35 mm |
| Wheel track | ~160 mm |
| COM above axle | 100–130 mm |
| Battery voltage | 11.1 V nominal |
| Control frequency | 200 Hz |

## Electrical Accessories

| Component | Specification | Quantity | Status |
|---|---|---:|---|
| Main power switch | >= 5 A DC | 1 | Selected |
| Inline fuse holder | Automotive / compact inline | 1 | Selected |
| Fuse | 5 A | 2 | Selected |
| Resistor | 10 kOhm | 4 | Selected |
| Resistor | 20 kOhm | 4 | Selected |
| Battery connector | XT30 pair | 1 | Selected |
| Logic connectors | JST / Dupont | Several | Selected |
| Prototype board | Small perfboard | 1 | Selected |
| Heat-shrink tubing | Assorted | - | Selected |
| Motor power wire | ~18-20 AWG | - | Selected |
| Signal wire | ~24-28 AWG | - | Selected |
| 3S LiPo balance charger | 3S compatible | 1 | Required |
| M3 screws / nuts | Assorted | - | Required |
| M3 spacers | Assorted | - | Required |

## Electrical Design Notes

- Motors are powered directly from the 3S battery through the MDD3A.
- The ESP32 is powered from the regulated 5 V rail.
- The IMU is powered from the ESP32 3.3 V rail.
- Encoders are powered from the regulated 5 V rail.
- Encoder A/B signals use 10 kOhm / 20 kOhm resistor dividers before entering the ESP32.
- All electronic modules share a common ground.
- Motor current must never pass through the ESP32 or the 5 V regulator.@
