```

## Control Development

The control system will be developed progressively:

1. Dynamic model of the inverted pendulum
2. Open-loop simulation
3. PD/PID stabilization in simulation
4. IMU-based state estimation
5. Embedded balance controller
6. Wheel encoder integration
7. Cascaded velocity/balance controller
8. Position stabilization
9. LQR state-feedback controller as a stretch goal

## Performance Targets

| Metric | Target |
|---|---:|
| Autonomous balancing | > 60 s |
| Control loop frequency | 200 Hz |
| Telemetry frequency | >= 100 Hz |
| Safety cutoff | ±30° |
| Push recovery | Yes |
| Wheel encoder feedback | Yes |
| Closed-loop simulation | Stable |
| Experimental validation | Yes |

## Repository Structure

```text
self-balancing-robot-control/
│
├── firmware/       Embedded control software
├── simulation/     Dynamic model and controller simulations
├── analysis/       Experimental data processing and plots
├── mechanical/     CAD and mechanical design
├── electronics/    Wiring diagrams and bill of materials
├── tests/          Validation procedures
├── docs/           Technical documentation
├── media/          Images and demonstration media
│
├── requirements.txt
└── README.md
```

## Final Deliverables

- Working physical self-balancing robot
- Dynamic model
- Python simulation environment
- PD/PID balance controller
- State estimation
- Embedded firmware
- Wheel encoder feedback
- Experimental telemetry
- Performance analysis
- Mechanical design files
- Electronics documentation
- Technical report
- Demonstration video

## Development Roadmap

### Week 1 — Modeling and Simulation

Physics, system architecture, dynamic modeling, simulation and control design.

### Week 2 — Sensors and Actuators

IMU calibration, motor control, encoders and embedded software architecture.

### Week 3 — Robot Integration

Mechanical assembly, electronics integration and first balancing experiments.

### Week 4 — Control and Validation

Controller tuning, performance evaluation, advanced control and final documentation.

## Current Status

**Day 1 / 30 — Project definition and repository setup**

- [x] Repository created
- [x] Project scope defined
- [x] Repository architecture defined
- [x] Initial BOM created
- [ ] Hardware architecture finalized
- [ ] Dynamic model implemented
- [ ] Simulation implemented
- [ ] Physical robot assembled
- [ ] Balance controller validated

---

Developed by **Guillaume Saint-Pierre**  
Mechanical Engineering — EPFL / DTU# Self-Balancing Robot Control

> Model-based control, simulation and embedded implementation of a two-wheeled self-balancing robot.

## Overview

This project aims to design, model, simulate, build and experimentally validate a two-wheeled self-balancing robot based on the inverted pendulum problem.

The objective is not only to obtain a robot that balances, but to develop the complete engineering pipeline:

**Physics → Modeling → Simulation → State Estimation → Control → Embedded Systems → Hardware → Experimental Validation**

## Project Objectives

The project combines:

- Dynamic modeling
- Control theory
- State estimation
- Embedded programming
- Sensor integration
- Motor control
- Mechanical design
- Experimental validation
- Data analysis

## System Architecture

```text
IMU + Wheel Encoders
        |
        v
Sensor Calibration
        |
        v
State Estimation
        |
        v
Balance Controller
        |
        v
Motor Command
        |
        v
Motor Driver
        |
        v
DC Motors
        |
        v
Robot Dynamics
        |
        +------------------> Sensor Feedback

