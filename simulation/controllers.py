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
@dataclass
class PositionVelocityController:
    """Outer-loop controller for position and velocity."""

    position_gain: float = 0.10
    velocity_gain: float = 0.10
    angle_limit_deg: float = 5.0

    def compute_theta_ref(
        self,
        position,
        velocity,
        position_ref=0.0,
        velocity_ref=0.0,
    ):
        """
        Compute desired body angle.

        Positive position/velocity error produces
        a corrective backward lean.
        """

        position_error = position - position_ref
        velocity_error = velocity - velocity_ref

        theta_ref = (
            -self.position_gain * position_error
            -self.velocity_gain * velocity_error
        )

        angle_limit = np.deg2rad(
            self.angle_limit_deg
        )

        return float(
            np.clip(
                theta_ref,
                -angle_limit,
                angle_limit,
            )
        )
