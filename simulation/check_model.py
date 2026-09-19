"""Basic physical sanity checks for the robot model."""

import numpy as np

from simulation.dynamics import nonlinear_dynamics


def main():
    upright = np.array([0.0, 0.0, 0.0, 0.0])

    upright_derivative = nonlinear_dynamics(
        t=0.0,
        state=upright,
        tau=0.0,
    )

    print("=== Upright equilibrium ===")
    print(upright_derivative)

    theta = np.deg2rad(5.0)

    forward_tilt = np.array(
        [
            0.0,
            0.0,
            theta,
            0.0,
        ]
    )

    derivative = nonlinear_dynamics(
        t=0.0,
        state=forward_tilt,
        tau=0.0,
    )

    print("\n=== 5 degree forward tilt ===")
    print(f"x_ddot     = {derivative[1]:.4f} m/s^2")
    print(f"theta_ddot = {derivative[3]:.4f} rad/s^2")

    backward_tilt = np.array(
        [
            0.0,
            0.0,
            -theta,
            0.0,
        ]
    )

    derivative_backward = nonlinear_dynamics(
        t=0.0,
        state=backward_tilt,
        tau=0.0,
    )

    print("\n=== 5 degree backward tilt ===")
    print(f"x_ddot     = {derivative_backward[1]:.4f} m/s^2")
    print(f"theta_ddot = {derivative_backward[3]:.4f} rad/s^2")


if __name__ == "__main__":
    main()
