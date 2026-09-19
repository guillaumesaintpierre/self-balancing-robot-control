"""Performance metrics for robot simulations."""

import numpy as np


def rms(values):
    """Root-mean-square value."""
    values = np.asarray(values)

    return float(
        np.sqrt(
            np.mean(values**2)
        )
    )


def settling_time(
    time,
    signal,
    tolerance,
):
    """
    Return the first time after which the signal
    permanently remains inside +/- tolerance.
    """

    time = np.asarray(time)
    signal = np.asarray(signal)

    inside = np.abs(signal) <= tolerance

    for index in range(len(signal)):
        if np.all(inside[index:]):
            return float(time[index])

    return None


def overshoot_to_zero(signal):
    """
    Overshoot for a positive initial condition
    converging toward zero.

    Returns the largest excursion below zero.
    """

    signal = np.asarray(signal)

    minimum = np.min(signal)

    return float(
        max(
            0.0,
            -minimum,
        )
    )
