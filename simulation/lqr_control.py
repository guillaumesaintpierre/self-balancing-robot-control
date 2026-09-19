"""Nonlinear robot simulation using LQR state feedback."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp

from simulation.dynamics import nonlinear_dynamics
from simulation.lqr_controller import design_lqr
from simulation.metrics import (
    rms,
    settling_time,
)
from simulation.parameters import DT


INITIAL_ANGLE_DEG = 5.0
SIMULATION_TIME = 6.0


def main():

    controller = design_lqr()

    state = np.array(
        [
            0.0,
            0.0,
            np.deg2rad(
                INITIAL_ANGLE_DEG
            ),
            0.0,
        ]
    )

    time_history = [0.0]
    state_history = [
        state.copy()
    ]

    torque_history = []

    number_of_steps = int(
        SIMULATION_TIME / DT
    )

    for step in range(
        number_of_steps
    ):

        torque = controller.compute(
            state
        )

        torque_history.append(
            torque
        )

        solution = solve_ivp(
            fun=lambda t, y:
            nonlinear_dynamics(
                t,
                y,
                tau=torque,
            ),
            t_span=(
                0.0,
                DT,
            ),
            y0=state,
            max_step=DT / 10.0,
            rtol=1e-9,
            atol=1e-11,
        )

        state = solution.y[:, -1]

        current_time = (
            step + 1
        ) * DT

        time_history.append(
            current_time
        )

        state_history.append(
            state.copy()
        )

    time_history = np.asarray(
        time_history
    )

    state_history = np.asarray(
        state_history
    )

    torque_history = np.asarray(
        torque_history
    )

    x = state_history[:, 0]

    x_dot = state_history[:, 1]

    theta_deg = np.rad2deg(
        state_history[:, 2]
    )

    theta_dot = state_history[:, 3]

    # -----------------------
    # Metrics
    # -----------------------

    angle_rms = rms(
        theta_deg
    )

    position_rms = rms(
        x
    )

    angle_settling = settling_time(
        time=time_history,
        signal=theta_deg,
        tolerance=0.5,
    )

    position_settling = settling_time(
        time=time_history,
        signal=x,
        tolerance=0.01,
    )

    print(
        "=== LQR nonlinear simulation ==="
    )

    print(
        f"Final angle: "
        f"{theta_deg[-1]:.6f} deg"
    )

    print(
        f"Final position: "
        f"{x[-1]:.6f} m"
    )

    print(
        f"Final velocity: "
        f"{x_dot[-1]:.6f} m/s"
    )

    print(
        f"Final angular velocity: "
        f"{theta_dot[-1]:.6f} rad/s"
    )

    print(
        f"Maximum position excursion: "
        f"{np.max(np.abs(x)):.4f} m"
    )

    print(
        f"Maximum torque: "
        f"{np.max(np.abs(torque_history)):.4f} N.m"
    )

    print(
        f"RMS angle: "
        f"{angle_rms:.4f} deg"
    )

    print(
        f"RMS position: "
        f"{position_rms:.4f} m"
    )

    if angle_settling is not None:

        print(
            f"Angle settling time: "
            f"{angle_settling:.3f} s"
        )

    if position_settling is not None:

        print(
            "Position settling time "
            f"(+/-1 cm): "
            f"{position_settling:.3f} s"
        )

    # -----------------------
    # Figures
    # -----------------------

    results_dir = Path(
        "simulation/results"
    )

    results_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    plt.figure(
        figsize=(8, 5)
    )

    plt.plot(
        time_history,
        theta_deg,
    )

    plt.axhline(
        0.0,
        linestyle="--",
    )

    plt.xlabel(
        "Time [s]"
    )

    plt.ylabel(
        "Angle [deg]"
    )

    plt.title(
        "LQR — body angle stabilization"
    )

    plt.grid()

    plt.tight_layout()

    plt.savefig(
        results_dir
        / "lqr_angle.png",
        dpi=200,
    )

    plt.figure(
        figsize=(8, 5)
    )

    plt.plot(
        time_history,
        x,
    )

    plt.axhline(
        0.0,
        linestyle="--",
    )

    plt.xlabel(
        "Time [s]"
    )

    plt.ylabel(
        "Position [m]"
    )

    plt.title(
        "LQR — position recovery"
    )

    plt.grid()

    plt.tight_layout()

    plt.savefig(
        results_dir
        / "lqr_position.png",
        dpi=200,
    )

    plt.figure(
        figsize=(8, 5)
    )

    plt.plot(
        time_history[:-1],
        torque_history,
    )

    plt.xlabel(
        "Time [s]"
    )

    plt.ylabel(
        "Torque [N.m]"
    )

    plt.title(
        "LQR — motor torque"
    )

    plt.grid()

    plt.tight_layout()

    plt.savefig(
        results_dir
        / "lqr_torque.png",
        dpi=200,
    )

    plt.close("all")

    print(
        "\nFigures saved in "
        "simulation/results/"
    )


if __name__ == "__main__":
    main()
