"""Explore LQR Q/R tuning for the self-balancing robot."""

import numpy as np
from scipy.integrate import solve_ivp

from simulation.dynamics import nonlinear_dynamics
from simulation.lqr_controller import design_lqr
from simulation.metrics import rms, settling_time
from simulation.parameters import DT


INITIAL_ANGLE_DEG = 5.0
SIMULATION_TIME = 6.0


CONFIGURATIONS = [
    {
        "name": "baseline",
        "q_position": 10.0,
        "q_velocity": 1.0,
        "q_angle": 100.0,
        "q_angular_velocity": 5.0,
        "r_torque": 1000.0,
    },
    {
        "name": "position_priority",
        "q_position": 30.0,
        "q_velocity": 3.0,
        "q_angle": 100.0,
        "q_angular_velocity": 5.0,
        "r_torque": 1000.0,
    },
    {
        "name": "balanced_aggressive",
        "q_position": 25.0,
        "q_velocity": 2.0,
        "q_angle": 150.0,
        "q_angular_velocity": 7.0,
        "r_torque": 750.0,
    },
    {
        "name": "low_control_effort",
        "q_position": 15.0,
        "q_velocity": 2.0,
        "q_angle": 120.0,
        "q_angular_velocity": 5.0,
        "r_torque": 1500.0,
    },
]


def simulate(configuration):

    controller = design_lqr(
        q_position=configuration["q_position"],
        q_velocity=configuration["q_velocity"],
        q_angle=configuration["q_angle"],
        q_angular_velocity=configuration[
            "q_angular_velocity"
        ],
        r_torque=configuration["r_torque"],
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

    number_of_steps = int(
        SIMULATION_TIME / DT
    )

    for step in range(number_of_steps):

        torque = controller.compute(
            state
        )

        torque_history.append(torque)

        solution = solve_ivp(
            fun=lambda t, y: nonlinear_dynamics(
                t,
                y,
                tau=torque,
            ),
            t_span=(0.0, DT),
            y0=state,
            max_step=DT / 10.0,
            rtol=1e-8,
            atol=1e-10,
        )

        state = solution.y[:, -1]

        time_history.append(
            (step + 1) * DT
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

    position = state_history[:, 0]

    angle_deg = np.rad2deg(
        state_history[:, 2]
    )

    return {
        "name": configuration["name"],

        "angle_rms": rms(
            angle_deg
        ),

        "position_rms": rms(
            position
        ),

        "angle_settling": settling_time(
            time_history,
            angle_deg,
            tolerance=0.5,
        ),

        "position_settling": settling_time(
            time_history,
            position,
            tolerance=0.01,
        ),

        "max_position": np.max(
            np.abs(position)
        ),

        "max_torque": np.max(
            np.abs(torque_history)
        ),

        "rms_torque": rms(
            torque_history
        ),
    }


def main():

    print(
        "=== LQR tuning study ==="
    )

    for configuration in CONFIGURATIONS:

        result = simulate(
            configuration
        )

        print(
            "\n-------------------------"
        )

        print(
            result["name"]
        )

        print(
            f"RMS angle: "
            f"{result['angle_rms']:.4f} deg"
        )

        print(
            f"RMS position: "
            f"{result['position_rms']:.4f} m"
        )

        print(
            f"Angle settling: "
            f"{result['angle_settling']:.3f} s"
        )

        print(
            f"Position settling: "
            f"{result['position_settling']:.3f} s"
        )

        print(
            f"Max position: "
            f"{result['max_position']:.4f} m"
        )

        print(
            f"Max torque: "
            f"{result['max_torque']:.4f} N.m"
        )

        print(
            f"RMS torque: "
            f"{result['rms_torque']:.5f} N.m"
        )


if __name__ == "__main__":
    main()
