"""Closed-loop nonlinear simulation with an angle PD controller."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp

from simulation.controllers import design_angle_pd
from simulation.dynamics import nonlinear_dynamics
from simulation.parameters import DT
from simulation.metrics import (
    rms,
    settling_time,
    overshoot_to_zero,
)

INITIAL_ANGLE_DEG = 5.0
SIMULATION_TIME = 3.0


def main():
    controller = design_angle_pd()

    # Initial state:
    # [x, x_dot, theta, theta_dot]
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

    number_of_steps = int(SIMULATION_TIME / DT)

    for step in range(number_of_steps):

        theta = state[2]
        theta_dot = state[3]

        # Digital controller evaluated at 200 Hz
        tau = controller.compute(
            theta=theta,
            theta_dot=theta_dot,
        )

        torque_history.append(tau)

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

        current_time = (step + 1) * DT

        time_history.append(current_time)
        state_history.append(state.copy())

    
    time_history = np.array(time_history)
    state_history = np.array(state_history)
    torque_history = np.array(torque_history)

    x = state_history[:, 0]
    x_dot = state_history[:, 1]
    theta_deg = np.rad2deg(state_history[:, 2])

    angle_rms = rms(theta_deg)

    angle_settling_time = settling_time(
        time=time_history,
        signal=theta_deg,
        tolerance=0.5,
    )

    angle_overshoot = overshoot_to_zero(
        theta_deg
    )

    torque_rms = rms(
        torque_history
    )
    angle_rms = rms(theta_deg)

    angle_settling_time = settling_time(
        time=time_history,
        signal=theta_deg,
        tolerance=0.5,
    )

    angle_overshoot = overshoot_to_zero(
        theta_deg
    )

    torque_rms = rms(
        torque_history
    )


    print("=== Closed-loop PD simulation ===")

    print(
        f"Initial angle: "
        f"{INITIAL_ANGLE_DEG:.2f} deg"
    )

    print(
        f"Final angle: "
        f"{theta_deg[-1]:.6f} deg"
    )

    print(
        f"Maximum angle magnitude: "
        f"{np.max(np.abs(theta_deg)):.3f} deg"
    )

    print(
        f"Maximum torque: "
        f"{np.max(np.abs(torque_history)):.4f} N.m"
    )

    print(
        f"Final position: "
        f"{x[-1]:.4f} m"
    )

    print(
        f"Final velocity: "
        f"{x_dot[-1]:.4f} m/s"
    )

    results_dir = Path("simulation/results")
    results_dir.mkdir(
        parents=True,
        exist_ok=True,
    )
    print("\n=== Performance metrics ===")

    print(
        f"RMS angle error: "
        f"{angle_rms:.4f} deg"
    )

    if angle_settling_time is not None:
        print(
            f"Settling time (±0.5 deg): "
            f"{angle_settling_time:.3f} s"
        )
    else:
        print(
            "Settling time: not reached"
        )

    print(
        f"Overshoot below zero: "
        f"{angle_overshoot:.4f} deg"
    )

    print(
        f"RMS torque: "
        f"{torque_rms:.5f} N.m"
    )

    print(
        f"Position drift after "
        f"{SIMULATION_TIME:.1f} s: "
        f"{x[-1]:.4f} m"
    )

    # -------------------------
    # ANGLE FIGURE
    # -------------------------

    plt.figure(figsize=(8, 5))

    plt.plot(
        time_history,
        theta_deg,
    )

    plt.axhline(
        0.0,
        linestyle="--",
    )

    plt.xlabel("Time [s]")
    plt.ylabel("Body angle [deg]")

    plt.title(
        "Closed-loop angle stabilization — PD controller"
    )

    plt.grid()

    plt.tight_layout()

    angle_output = (
        results_dir
        / "closed_loop_pd_angle.png"
    )

    plt.savefig(
        angle_output,
        dpi=200,
    )

    # -------------------------
    # POSITION FIGURE
    # -------------------------

    plt.figure(figsize=(8, 5))

    plt.plot(
        time_history,
        x,
    )

    plt.xlabel("Time [s]")
    plt.ylabel("Axle position [m]")

    plt.title(
        "Robot position with angle-only PD control"
    )

    plt.grid()

    plt.tight_layout()

    position_output = (
        results_dir
        / "closed_loop_pd_position.png"
    )

    plt.savefig(
        position_output,
        dpi=200,
    )

    # -------------------------
    # TORQUE FIGURE
    # -------------------------

    plt.figure(figsize=(8, 5))

    plt.plot(
        time_history[:-1],
        torque_history,
    )

    plt.xlabel("Time [s]")
    plt.ylabel("Motor torque command [N.m]")

    plt.title(
        "PD controller torque command"
    )

    plt.grid()

    plt.tight_layout()

    torque_output = (
        results_dir
        / "closed_loop_pd_torque.png"
    )

    plt.savefig(
        torque_output,
        dpi=200,
    )

    print("\nFigures saved:")

    print(angle_output)
    print(position_output)
    print(torque_output)

    plt.show()


if __name__ == "__main__":
    main()
