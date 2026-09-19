"""Open-loop simulation of the self-balancing robot."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp

from simulation.dynamics import nonlinear_dynamics, linear_dynamics


INITIAL_ANGLE_DEG = 5.0
FALL_ANGLE_DEG = 45.0
MAX_SIMULATION_TIME = 2.0


def fall_event(t, state):
    """Stop the simulation when the robot reaches the fall angle."""

    theta = state[2]

    return np.deg2rad(FALL_ANGLE_DEG) - abs(theta)


fall_event.terminal = True
fall_event.direction = -1


def main():
    initial_state = np.array(
        [
            0.0,                        # x [m]
            0.0,                        # x_dot [m/s]
            np.deg2rad(INITIAL_ANGLE_DEG),
            0.0,                        # theta_dot [rad/s]
        ]
    )

    nonlinear_solution = solve_ivp(
        fun=lambda t, state: nonlinear_dynamics(
            t,
            state,
            tau=0.0,
        ),
        t_span=(0.0, MAX_SIMULATION_TIME),
        y0=initial_state,
        events=fall_event,
        max_step=0.001,
        rtol=1e-9,
        atol=1e-11,
    )

    fall_time = nonlinear_solution.t[-1]

    linear_solution = solve_ivp(
        fun=lambda t, state: linear_dynamics(
            t,
            state,
            tau=0.0,
        ),
        t_span=(0.0, fall_time),
        y0=initial_state,
        t_eval=nonlinear_solution.t,
        rtol=1e-9,
        atol=1e-11,
    )

    nonlinear_angle_deg = np.rad2deg(
        nonlinear_solution.y[2]
    )

    linear_angle_deg = np.rad2deg(
        linear_solution.y[2]
    )

    print("=== Open-loop simulation ===")
    print(f"Initial angle: {INITIAL_ANGLE_DEG:.1f} deg")
    print(f"Fall threshold: {FALL_ANGLE_DEG:.1f} deg")
    print(f"Fall time: {fall_time:.3f} s")

    print(
        "Final nonlinear angle: "
        f"{nonlinear_angle_deg[-1]:.2f} deg"
    )

    print(
        "Axle displacement at fall: "
        f"{nonlinear_solution.y[0, -1]:.4f} m"
    )

    results_dir = Path("simulation/results")
    results_dir.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(8, 5))

    plt.plot(
        nonlinear_solution.t,
        nonlinear_angle_deg,
        label="Nonlinear model",
    )

    plt.plot(
        linear_solution.t,
        linear_angle_deg,
        "--",
        label="Linearized model",
    )

    plt.axhline(
        FALL_ANGLE_DEG,
        linestyle=":",
        label="Fall threshold",
    )

    plt.xlabel("Time [s]")
    plt.ylabel("Body angle [deg]")
    plt.title(
        "Open-loop instability — 5° initial perturbation"
    )

    plt.grid()
    plt.legend()
    plt.tight_layout()

    output = results_dir / "open_loop_divergence.png"

    plt.savefig(
        output,
        dpi=200,
    )

    print(f"Figure saved to: {output}")

    plt.show()


if __name__ == "__main__":
    main()

