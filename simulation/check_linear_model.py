"""Inspect the linearized state-space model."""

import numpy as np

from simulation.dynamics import linear_state_space


def main():
    A, B = linear_state_space()

    print("A matrix:")
    print(A)

    print("\nB matrix:")
    print(B)

    eigenvalues = np.linalg.eigvals(A)

    print("\nEigenvalues of A:")
    for value in eigenvalues:
        print(f"{value:.6f}")

    if np.any(np.real(eigenvalues) > 0):
        print("\nOPEN-LOOP SYSTEM IS UNSTABLE")
    else:
        print("\nWARNING: model does not appear unstable")


if __name__ == "__main__":
    main()
