import numpy as np
from app.src.models import generate_curves
from app.src.integration import compute_evacuation_time
from app.src.curve_builder import create_piecewise_from_physical

def run_simulation(specific_params, conditions):
    # 1. Extreure valors base (mapeig de noms de l'HTML als del builder)
    # Busquem tant el nom curt com el llarg que has posat a l'HTML
    dotm_max = specific_params.get("dotm_max", 0.0086)
    p_bp = (specific_params.get("P_breakPoint_r") or 
            specific_params.get("P_breakPoint_n") or 
            specific_params.get("x_bp", 0.25)) * 1e5 # Pascal
    slope = specific_params.get("b", 2e-7)
    p_min = conditions.get("Min_pressure", 0.2) * 1e5 # Pascal
    # 2. Definim el límit físic de l'ejector una mica més avall (per sota de p_min)
    # Si l'usuari diu 0.2 bar (20.000 Pa), fem que l'ejector realment "mori" a 0.18 bar (18.000 Pa)
    p_min_physical = p_min * 0.9  # Parem un % més avall

    
    # 2. Calcular a, b, c, d usant curve_builder.py
    a, b, c, d = create_piecewise_from_physical(
        dotm_max=dotm_max,
        pressure_min=p_min_physical,
        pressure_bp=p_bp,
        slope=slope
    )
    
    # 3. Preparar el diccionari complet per al model
    full_params = {
        "a": a, "b": b, "c": c, "d": d,
        "x_bp": p_bp,
        "e": specific_params.get("e", 0),
        "f": specific_params.get("f", 0),
        "g": specific_params.get("g", 0),
        "V": conditions.get("V", 0.5),
        "r": conditions.get("r", 287),
        "T": conditions.get("T", 298)
    }

    # Generar corbes (models.py)
    x, y_piece, y_poly = generate_curves(full_params, pressure=p_min/1e5)

    # Càlcul de temps
    x_time_full, t_full = compute_evacuation_time(full_params, x_min=p_min_physical, x_max=max(x))

    # Taula de pressions per a la comparativa
    pressures_table = np.arange(0.2, 1.01, 0.1) * 1e5
    pressures_table = pressures_table[::-1]
    x_time_table, t_table = compute_evacuation_time(full_params, pressures=pressures_table)

    return {
        "x": x, "y_piece": y_piece, "y_poly": y_poly,
        "x_time_full": x_time_full, "t_full": t_full,
        "x_time_table": x_time_table, "t_table": t_table,
        "p_min": p_min, "dotm_max": dotm_max,
        "x_bp": p_bp, "a": a, "b": b, "c": c, "d": d,
        "e": full_params["e"], "f": full_params["f"], "g": full_params["g"]
    }

def calculate_kpis(ref_results, new_results):
    ptet_ref = float(ref_results["t_table"][-1])
    ptet_new = float(new_results["t_table"][-1])
    delta_pct = 100 * (ptet_new - ptet_ref) / ptet_ref if ptet_ref != 0 else 0
    max_abs_error = float(np.max(np.abs(new_results["t_full"] - ref_results["t_full"])))
    
    return {
        "ptet_ref": round(ptet_ref, 2),
        "ptet_new": round(ptet_new, 2),
        "delta_pct": round(delta_pct, 2),
        "max_abs_error": round(max_abs_error, 3)
    }