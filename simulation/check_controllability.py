"""Check controllability of the linearized robot model."""

import numpy as np

from simulation.dynamics import linear_state_space


def main():

    A, B = linear_state_space()

    controllability_matrix = np.hstack(
        [
            B,
            A @ B,
            A @ A @ B,
            A @ A @ A @ B,
        ]
    )

    rank = np.linalg.matrix_rank(
        controllability_matrix
    )

    number_of_states = A.shape[0]

    print("=== Controllability Analysis ===")

    print(
        f"Number of states: {number_of_states}"
    )

    print(
        f"Controllability rank: {rank}"
    )

    if rank == number_of_states:

        print(
            "SYSTEM IS FULLY CONTROLLABLE"
        )

    else:

        print(
            "WARNING: system is not fully controllable"
        )


if __name__ == "__main__":
    main()
