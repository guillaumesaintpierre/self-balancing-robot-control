"""Compare open-loop and closed-loop angle responses."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp

from simulation.controllers import design_angle_pd
from simulation.dynamics import nonlinear_dynamics
from simulation.parameters import DT


INITIAL_ANGLE_DEG = 5.0
SIMULATION_TIME = 3.0
FALL_ANGLE_DEG = 45.0


def fall_event(t, state):
    theta = state[2]
    return np.deg2rad(FALL_ANGLE_DEG) - abs(theta)


fall_event.terminal = True
fall_event.direction = -1


def simulate_open_loop():
    initial_state = np.array(
        [
            0.0,
            0.0,
            np.deg2rad(INITIAL_ANGLE_DEG),
            0.0,
        ]
    )

    solution = solve_ivp(
        fun=lambda t, y: nonlinear_dynamics(
            t,
            y,
            tau=0.0,
        ),
        t_span=(0.0, SIMULATION_TIME),
        y0=initial_state,
        events=fall_event,
        max_step=0.001,
        rtol=1e-9,
        atol=1e-11,
    )

    return solution.t, np.rad2deg(solution.y[2])


def simulate_closed_loop():
    controller = design_angle_pd()

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

    number_of_steps = int(SIMULATION_TIME / DT)

    for step in range(number_of_steps):
        theta = state[2]
        theta_dot = state[3]

        tau = controller.compute(
            theta=theta,
            theta_dot=theta_dot,
        )

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

    return time_history, np.rad2deg(state_history[:, 2])


def main():
    t_open, theta_open = simulate_open_loop()
    t_closed, theta_closed = simulate_closed_loop()

    results_dir = Path("simulation/results")
    results_dir.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(8, 5))

    plt.plot(
        t_open,
        theta_open,
        label="Open-loop",
    )

    plt.plot(
        t_closed,
        theta_closed,
        label="Closed-loop PD",
    )

    plt.axhline(
        0.0,
        linestyle="--",
        label="Upright equilibrium",
    )

    plt.axhline(
        FALL_ANGLE_DEG,
        linestyle=":",
        label="Fall threshold",
    )

    plt.xlabel("Time [s]")
    plt.ylabel("Body angle [deg]")
    plt.title("Open-loop vs closed-loop body angle response")
    plt.grid()
    plt.legend()
    plt.tight_layout()

    output = results_dir / "open_vs_closed_loop_angle.png"

    plt.savefig(
        output,
        dpi=200,
    )

    print("Figure saved to:")
    print(output)

    plt.show()


if __name__ == "__main__":
    main()
