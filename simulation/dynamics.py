"""Dynamic models for the self-balancing robot."""

import numpy as np

from simulation.parameters import (
    G,
    BODY_MASS,
    WHEEL_EQUIV_MASS,
    COM_HEIGHT,
    BODY_INERTIA,
    WHEEL_RADIUS,
)


def nonlinear_dynamics(t, state, tau=0.0):
    """
    Nonlinear equations of motion.

    State:
        state = [x, x_dot, theta, theta_dot]

    Parameters:
        x         horizontal axle position [m]
        x_dot     horizontal velocity [m/s]
        theta     body pitch angle from vertical [rad]
        theta_dot pitch angular velocity [rad/s]

    Input:
        tau       total motor torque [N.m]

    Returns:
        [x_dot, x_ddot, theta_dot, theta_ddot]
    """

    x, x_dot, theta, theta_dot = state

    m = BODY_MASS
    M = WHEEL_EQUIV_MASS
    l = COM_HEIGHT
    I = BODY_INERTIA
    r = WHEEL_RADIUS

    a = M + m
    b = m * l
    c = I + m * l**2

    mass_matrix = np.array(
        [
            [a, b * np.cos(theta)],
            [b * np.cos(theta), c],
        ]
    )

    rhs = np.array(
        [
            tau / r + b * np.sin(theta) * theta_dot**2,
            -tau + m * G * l * np.sin(theta),
        ]
    )

    x_ddot, theta_ddot = np.linalg.solve(mass_matrix, rhs)

    return np.array(
        [
            x_dot,
            x_ddot,
            theta_dot,
            theta_ddot,
        ]
    )


def linear_state_space():
    """
    Linearized state-space model around theta = 0.

    X_dot = A X + B tau
    """

    m = BODY_MASS
    M = WHEEL_EQUIV_MASS
    l = COM_HEIGHT
    I = BODY_INERTIA
    r = WHEEL_RADIUS

    a = M + m
    b = m * l
    c = I + m * l**2

    delta = a * c - b**2
    d = m * G * l

    A = np.array(
        [
            [0.0, 1.0, 0.0, 0.0],
            [0.0, 0.0, -(b * d) / delta, 0.0],
            [0.0, 0.0, 0.0, 1.0],
            [0.0, 0.0, (a * d) / delta, 0.0],
        ]
    )

    B = np.array(
        [
            [0.0],
            [(c / r + b) / delta],
            [0.0],
            [-(b / r + a) / delta],
        ]
    )

    return A, B


def linear_dynamics(t, state, tau=0.0):
    """Linearized robot dynamics."""

    A, B = linear_state_space()

    state = np.asarray(state)

    return A @ state + B[:, 0] * tau
