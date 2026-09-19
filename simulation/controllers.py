"""Controllers for the self-balancing robot."""

from dataclasses import dataclass

import numpy as np

from simulation.dynamics import linear_state_space


@dataclass
class AnglePDController:
    """PD controller for body pitch stabilization."""

    kp: float
    kd: float
    torque_limit: float = 0.6

    def compute(self, theta, theta_dot):
        """
        Compute total motor torque command.

        Sign convention:

        theta > 0 means forward tilt.

        With the current robot model, positive motor torque
        generates a corrective negative angular acceleration.
        """

        tau = self.kp * theta + self.kd * theta_dot

        return float(
            np.clip(
                tau,
                -self.torque_limit,
                self.torque_limit,
            )
        )


def design_angle_pd(
    natural_frequency=8.0,
    damping_ratio=0.9,
):
    """
    Design PD gains from the linearized pitch dynamics.

    Desired dynamics:

        theta_ddot
        + 2*zeta*wn*theta_dot
        + wn^2*theta
        = 0
    """

    A, B = linear_state_space()

    a_theta = A[3, 2]
    b_tau = B[3, 0]

    wn = natural_frequency
    zeta = damping_ratio

    kp = (-wn**2 - a_theta) / b_tau

    kd = (-2.0 * zeta * wn) / b_tau

    return AnglePDController(
        kp=kp,
        kd=kd,
    )


if __name__ == "__main__":

    controller = design_angle_pd()

    print("=== Angle PD Controller ===")

    print(
        f"Kp = {controller.kp:.6f} N.m/rad"
    )

    print(
        f"Kd = {controller.kd:.6f} N.m.s/rad"
    )

    print(
        f"Torque limit = "
        f"{controller.torque_limit:.3f} N.m"
    )
