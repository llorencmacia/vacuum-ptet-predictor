import numpy as np

def create_piecewise_from_physical(
    dotm_max,
    pressure_min,
    pressure_bp,
    slope,
    pressure_max=1e5
):
    """
    Construcció físicament coherent d'una funció piecewise lineal.
    """

    # Tram alt (p > bp) 
    a = dotm_max - slope * pressure_max
    b = slope

    # Valor al breakpoint
    dotm_bp = a + b * pressure_bp

    # Tram baix (p <= bp)
    d = dotm_bp / (pressure_bp - pressure_min)
    c = -d * pressure_min

    return a, b, c, d
