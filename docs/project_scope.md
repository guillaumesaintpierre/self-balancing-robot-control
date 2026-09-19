# Project Scope — Self-Balancing Robot

## Objective

Design, model, simulate, build and experimentally validate a two-wheeled self-balancing robot based on the inverted pendulum problem.

The project combines:

- dynamics and physical modeling
- control theory
- state estimation
- embedded systems
- electronics
- mechanical design
- experimental validation

## Final System

The robot will use:

- an IMU to measure body motion
- wheel encoders to estimate wheel velocity and position
- an embedded microcontroller for real-time control
- two DC geared motors for actuation
- a motor driver for bidirectional motor control

## Control Pipeline

IMU + Encoders
→ Calibration
→ State Estimation
→ Balance Controller
→ Motor Command
→ Motor Driver
→ Robot Dynamics
→ Sensor Feedback

## Controller Development

The controller will be developed progressively:

1. Open-loop dynamic model
2. Closed-loop simulation
3. PD/PID balance controller
4. Embedded balance controller
5. Cascaded velocity/balance controller
6. LQR controller as a stretch goal

## Performance Targets

| Metric | Target |
|---|---|
| Autonomous balancing | > 60 s |
| Control frequency | 200 Hz |
| Telemetry frequency | >= 100 Hz |
| Safety cutoff angle | ±30 deg |
| Push recovery | Yes |
| Encoder feedback | Yes |
| Closed-loop simulation | Stable |
| Experimental validation | Yes |

## Final Deliverables

- physical self-balancing robot
- nonlinear and/or linear dynamic model
- simulation environment
- embedded control firmware
- sensor calibration code
- experimental data logs
- performance plots
- wiring documentation
- mechanical design files
- technical report
- clean GitHub repository
- final demonstration video
