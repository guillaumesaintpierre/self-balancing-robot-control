# Control Design

## Angle PD

The first controller stabilizes body pitch using a model-based PD law.

Initial condition:

theta(0) = 5 deg

Performance:

- settling time: 0.410 s
- RMS angle error: 1.1034 deg
- maximum torque: 0.0379 N.m

The controller successfully stabilizes body angle but does not regulate position.

## Cascaded Controller

A slower position/velocity loop generates an angle reference for the inner balance controller.

Performance:

- final position: approximately 0 m
- maximum position excursion: 0.0596 m
- position settling time: 1.555 s
- angle settling time: 1.620 s
- RMS angle: 0.9950 deg
- maximum torque: 0.0379 N.m

This controller successfully regulates both balance and position.

## LQR State Feedback

The full state vector is:

X = [x, x_dot, theta, theta_dot]^T

The control law is:

tau = -K X

The system controllability matrix has full rank:

rank(C) = 4

Therefore the complete linearized system is controllable.

## LQR Tuning

Several Q/R configurations were evaluated using the nonlinear robot model.

The selected configuration is:

Q = diag(30, 3, 100, 5)

R = 1000

This configuration was selected as the best compromise between:

- angle stabilization
- position recovery
- position excursion
- control effort

Performance:

- RMS angle: 0.6339 deg
- RMS position: 0.0183 m
- angle settling time: 0.975 s
- position settling time: 2.075 s
- maximum position excursion: 0.0439 m
- maximum torque: 0.0880 N.m
- RMS torque: 0.00527 N.m

## Control Architecture Comparison

| Metric | Cascaded Controller | Selected LQR |
|---|---:|---:|
| RMS angle | 0.9950 deg | 0.6339 deg |
| Angle settling | 1.620 s | 0.975 s |
| Position settling | 1.555 s | 2.075 s |
| Maximum position excursion | 0.0596 m | 0.0439 m |
| Maximum torque | 0.0379 N.m | 0.0880 N.m |

The LQR provides faster and more accurate angle stabilization and reduces maximum position excursion.

This improvement requires higher peak control torque.

The cascaded controller provides faster final position recovery with substantially lower peak torque.

Therefore neither controller is universally superior: their behavior reflects different design objectives and control trade-offs.
