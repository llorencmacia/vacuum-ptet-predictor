import numpy as np

def piecewise_function(x, a, b, c, d, x_bp):
    valors = np.where(x > x_bp, a + b*x, c + d*x)
    # Si la pressió x baixa per sota del p_min_physical, 
    # posem un floor de seguretat per evitar divisions per zero o dotM negatius
    return np.maximum(valors, 1e-12)

def polynomial_function(x, e, f, g):
    return e + f*x + g*x**2

def generate_curves(params, pressure=0.2, n_points=1000):
    # x_min=min(pressure)
    x_min=pressure
    x_max=1
    x = np.linspace(x_min, x_max, n_points)
    x = x*1e5

    y_piece = piecewise_function(
        x,
        params["a"], params["b"],
        params["c"], params["d"],
        params["x_bp"]
    )

    y_poly = polynomial_function(
        x,
        params["e"], params["f"], params["g"]
    )

    return x, y_piece, y_poly
