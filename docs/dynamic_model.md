# Dynamic Model

## System

The robot is modeled as a two-wheeled inverted pendulum.

Generalized coordinates:

- x: horizontal wheel-axis position
- theta: body angle from vertical

State vector:

X = [x, x_dot, theta, theta_dot]^T

Control input:

tau = total motor torque

## Sign Convention

x > 0: forward motion

theta > 0: forward body tilt

theta = 0: upright equilibrium

## Parameters

| Symbol | Description | Initial estimate |
|---|---|---|
| m | Body mass | 1.0 kg |
| M | Equivalent wheel/motor mass | 0.2 kg |
| l | Axle-to-COM distance | 0.12 m |
| I | Body pitch inertia | 0.0054 kg m^2 |
| r | Wheel radius | 0.035 m |
| g | Gravity | 9.81 m/s^2 |

## Nonlinear Equations

(M+m)x_ddot
+ m l cos(theta) theta_ddot
- m l sin(theta) theta_dot^2
= tau/r

(I + m l^2)theta_ddot
+ m l cos(theta)x_ddot
- m g l sin(theta)
= -tau

## Linearized Equations

Around theta = 0:

(M+m)x_ddot + m l theta_ddot = tau/r

m l x_ddot
+ (I + m l^2)theta_ddot
- m g l theta
= -tau

## State Vector

X = [x, x_dot, theta, theta_dot]^T

## Modeling Assumptions

- rigid chassis
- flat horizontal floor
- pure rolling without slip
- identical left and right motors
- symmetric robot
- small-angle approximation for the linear model
- motor electrical dynamics neglected initially
- wheel backlash and friction neglected initially
- yaw dynamics neglected
- battery voltage considered constant initially

## Future Model Improvements

Later versions may include:

- motor electrical dynamics
- viscous friction
- wheel inertia
- gear friction
- motor dead zone
- battery voltage variation
- sensor noise
- actuator saturation
