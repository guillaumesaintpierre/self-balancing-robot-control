"""LQR state-feedback controller."""

from dataclasses import dataclass

import numpy as np
from scipy.linalg import solve_continuous_are

from simulation.dynamics import linear_state_space


@dataclass
class LQRController:

    gain: np.ndarray
    torque_limit: float = 0.6

    def compute(
        self,
        state,
        reference=None,
    ):

        state = np.asarray(
            state,
            dtype=float,
        )

        if reference is None:

            reference = np.zeros(4)

        error = (
            state
            - np.asarray(
                reference,
                dtype=float,
            )
        )

        torque = float(
            -(self.gain @ error)[0]
        )

        return float(
            np.clip(
                torque,
                -self.torque_limit,
                self.torque_limit,
            )
        )


def design_lqr():

    A, B = linear_state_space()

    Q = np.diag(
        [
            10.0,   # position
            1.0,    # velocity
            100.0,  # angle
            5.0,    # angular velocity
        ]
    )

    R = np.array(
        [
            [1000.0]
        ]
    )

    P = solve_continuous_are(
        A,
        B,
        Q,
        R,
    )

    K = (
        np.linalg.inv(R)
        @ B.T
        @ P
    )

    return LQRController(
        gain=K
    )


def main():

    A, B = linear_state_space()

    controller = design_lqr()

    K = controller.gain

    closed_loop_matrix = (
        A - B @ K
    )

    eigenvalues = np.linalg.eigvals(
        closed_loop_matrix
    )

    print(
        "=== LQR Controller ==="
    )

    print("\nGain K:")

    print(K)

    print(
        "\nClosed-loop eigenvalues:"
    )

    for value in eigenvalues:

        print(
            f"{value:.6f}"
        )

    if np.all(
        np.real(eigenvalues) < 0
    ):

        print(
            "\nCLOSED-LOOP SYSTEM IS STABLE"
        )


if __name__ == "__main__":
    main()
