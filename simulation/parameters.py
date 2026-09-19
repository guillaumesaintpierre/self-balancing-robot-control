"""Physical parameters for the self-balancing robot."""

G = 9.81

# Initial design estimates.
# These values will be replaced by measured values after assembly.

BODY_MASS = 1.0          # kg
WHEEL_EQUIV_MASS = 0.20  # kg

COM_HEIGHT = 0.12        # m
BODY_INERTIA = 0.0054    # kg*m^2

WHEEL_RADIUS = 0.035     # m
WHEEL_DIAMETER = 0.070   # m

CONTROL_FREQUENCY = 200  # Hz
DT = 1.0 / CONTROL_FREQUENCY
