import numpy as np
from scipy.integrate import quad

from app.src.curve_builder import create_piecewise_from_physical


def piecewise_dotm(p, a, b, c, d, pressure_bp):
    if p > pressure_bp:
        return a + b*p
    else:
        return c + d*p

def polynomial_n(p, e, f, g):
    return e + f*p + g*p**2

def integrand(x, params):
    k = piecewise_dotm(
        x,
        params["a"], params["b"],
        params["c"], params["d"],
        params["x_bp"]
    )
    n = polynomial_n(
        x,
        params["e"], params["f"], params["g"]
    )

    konst = -params["V"] / (params["r"] * params["T"])
    return konst / (k * n)

def compute_evacuation_time(params, x_min=None, x_max=None, pressures=None):

    if pressures is not None:
        x_time = np.array(pressures)
    else:
        n_points = 1000
        x_time = np.linspace(x_min+20, x_max, n_points)

    # Pressió inicial (suposem la més alta)
    x_start = np.max(x_time)

    times = []

    for x_target in x_time:
        val, _ = quad(integrand, x_start, x_target, args=(params,))
        times.append(val)

    return x_time, np.array(times)