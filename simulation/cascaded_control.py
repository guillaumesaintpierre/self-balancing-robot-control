"""Cascaded position + angle control simulation."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp

from simulation.controllers import (
    design_angle_pd,
    PositionVelocityController,
)
from simulation.dynamics import nonlinear_dynamics
from simulation.metrics import (
    rms,
    settling_time,
)
from simulation.parameters import DT


INITIAL_ANGLE_DEG = 5.0
SIMULATION_TIME = 6.0

INNER_FREQUENCY = 200
OUTER_FREQUENCY = 50

OUTER_UPDATE_STEPS = int(
    INNER_FREQUENCY / OUTER_FREQUENCY
)


def main():

    angle_controller = design_angle_pd()

    outer_controller = PositionVelocityController(
        position_gain=0.10,
        velocity_gain=0.10,
        angle_limit_deg=5.0,
    )

    state = np.array(
        [
            0.0,
            0.0,
            np.deg2rad(INITIAL_ANGLE_DEG),
            0.0,
        ]
    )

    time_history = [0.0]
    state_history = [state.copy()]

    torque_history = []
    theta_ref_history = []

    theta_ref = 0.0

    number_of_steps = int(
        SIMULATION_TIME / DT
    )

    for step in range(number_of_steps):

        x = state[0]
        x_dot = state[1]
        theta = state[2]
        theta_dot = state[3]

        # Outer loop at 50 Hz
        if step % OUTER_UPDATE_STEPS == 0:

            theta_ref = (
                outer_controller.compute_theta_ref(
                    position=x,
                    velocity=x_dot,
                )
            )

        # Inner angle loop at 200 Hz

        angle_error = theta - theta_ref

        tau = angle_controller.compute(
            theta=angle_error,
            theta_dot=theta_dot,
        )

        torque_history.append(tau)
        theta_ref_history.append(theta_ref)

        solution = solve_ivp(
            fun=lambda t, y: nonlinear_dynamics(
                t,
                y,
                tau=tau,
            ),
            t_span=(0.0, DT),
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

    time_history = np.array(
        time_history
    )

    state_history = np.array(
        state_history
    )

    torque_history = np.array(
        torque_history
    )

    theta_ref_history = np.array(
        theta_ref_history
    )

    x = state_history[:, 0]
    x_dot = state_history[:, 1]

    theta_deg = np.rad2deg(
        state_history[:, 2]
    )

    theta_ref_deg = np.rad2deg(
        theta_ref_history
    )

    # ----------------------------
    # Metrics
    # ----------------------------

    angle_rms = rms(theta_deg)

    position_rms = rms(x)

    position_settling = settling_time(
        time=time_history,
        signal=x,
        tolerance=0.01,
    )

    angle_settling = settling_time(
        time=time_history,
        signal=theta_deg,
        tolerance=0.5,
    )

    print(
        "=== Cascaded control simulation ==="
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
        f"Maximum position excursion: "
        f"{np.max(np.abs(x)):.4f} m"
    )

    print(
        f"Maximum theta_ref: "
        f"{np.max(np.abs(theta_ref_deg)):.3f} deg"
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
            f"Position settling time "
            f"(±1 cm): "
            f"{position_settling:.3f} s"
        )

    # ----------------------------
    # Figures
    # ----------------------------

    results_dir = Path(
        "simulation/results"
    )

    results_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    # ANGLE

    plt.figure(
        figsize=(8, 5)
    )

    plt.plot(
        time_history,
        theta_deg,
        label="Body angle",
    )

    plt.plot(
        time_history[:-1],
        theta_ref_deg,
        "--",
        label="Angle reference",
    )

    plt.axhline(
        0.0,
        linestyle=":",
    )

    plt.xlabel("Time [s]")
    plt.ylabel("Angle [deg]")

    plt.title(
        "Cascaded control — body angle"
    )

    plt.grid()
    plt.legend()
    plt.tight_layout()

    plt.savefig(
        results_dir
        / "cascaded_angle.png",
        dpi=200,
    )

    # POSITION

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

    plt.xlabel("Time [s]")
    plt.ylabel("Position [m]")

    plt.title(
        "Cascaded control — position recovery"
    )

    plt.grid()
    plt.tight_layout()

    plt.savefig(
        results_dir
        / "cascaded_position.png",
        dpi=200,
    )

    # VELOCITY

    plt.figure(
        figsize=(8, 5)
    )

    plt.plot(
        time_history,
        x_dot,
    )

    plt.axhline(
        0.0,
        linestyle="--",
    )

    plt.xlabel("Time [s]")
    plt.ylabel("Velocity [m/s]")

    plt.title(
        "Cascaded control — velocity"
    )

    plt.grid()
    plt.tight_layout()

    plt.savefig(
        results_dir
        / "cascaded_velocity.png",
        dpi=200,
    )

    # TORQUE

    plt.figure(
        figsize=(8, 5)
    )

    plt.plot(
        time_history[:-1],
        torque_history,
    )

    plt.xlabel("Time [s]")
    plt.ylabel("Torque [N.m]")

    plt.title(
        "Cascaded control — motor torque"
    )

    plt.grid()
    plt.tight_layout()

    plt.savefig(
        results_dir
        / "cascaded_torque.png",
        dpi=200,
    )

    plt.close("all")

    print(
        "\nFigures saved in "
        "simulation/results/"
    )


if __name__ == "__main__":
    main()
