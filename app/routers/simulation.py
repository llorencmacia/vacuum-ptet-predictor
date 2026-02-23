from fastapi import APIRouter, Form, Request
from fastapi.templating import Jinja2Templates
from app.src.services import run_simulation, calculate_kpis
from app.src.plots import build_piecewise_figure, build_polynomial_figure, build_time_figure, build_error_figure
from fastapi.responses import FileResponse
import tempfile
import csv
from datetime import datetime

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.post("/plot")
async def plot(request: Request):
    form_data = await request.form()
    data = {k: float(v) for k, v in form_data.items()}

    # 1. Extraure paràmetres de Referència
    ref_params = {
        "dotm_max": data.get("dotm_max_ref"),
        "b": data.get("b_ref"),
        "e": data.get("e_ref"),
        "f": data.get("f_ref"),
        "g": data.get("g_ref"),
        "x_bp": data.get("P_breakPoint_r")
    }

    # 2. Extraure paràmetres Nous
    new_params = {
        "dotm_max": data.get("dotm_max_new"),
        "b": data.get("b_new"),
        "e": data.get("e_new"),
        "f": data.get("f_new"),
        "g": data.get("g_new"),
        "x_bp": data.get("P_breakPoint_n")
    }

    # 3. Condicions globals
    conditions = {
        "V": data.get("V"),
        "r": data.get("r"),
        "T": data.get("T"),
        "Min_pressure": data.get("Min_pressure")
    }

    ref_results = run_simulation(ref_params, conditions)
    new_results = run_simulation(new_params, conditions)
    kpis = calculate_kpis(ref_results, new_results)

    return {
        "piece_plot": build_piecewise_figure(ref_results, new_results),
        "poly_plot": build_polynomial_figure(ref_results, new_results),
        "time_plot": build_time_figure(ref_results, new_results),
        "error_plot": build_error_figure(ref_results, new_results),
        "reference": {
            "x_time_table": ref_results["x_time_table"].tolist(),
            "t_table": ref_results["t_table"].tolist(),
            "x_time_full": ref_results["x_time_full"].tolist(),
            "t_full": ref_results["t_full"].tolist()
        },
        "new": {
            "x_time_table": new_results["x_time_table"].tolist(),
            "t_table": new_results["t_table"].tolist(),
            "x_time_full": new_results["x_time_full"].tolist(),
            "t_full": new_results["t_full"].tolist()
        },
        "model_data": {
            "reference": {
                "a": ref_results["a"],
                "b": ref_results["b"],
                "c": ref_results["c"],
                "d": ref_results["d"],
                "e": ref_params["e"],
                "f": ref_params["f"],
                "g": ref_params["g"],
                "p_min": conditions.get("Min_pressure") * 1e5,
                "dotm_max": ref_results["dotm_max"],
                "x_bp": ref_params["x_bp"]
            },
            "new": {
                "a": new_results["a"],
                "b": new_results["b"],
                "c": new_results["c"],
                "d": new_results["d"],
                "e": new_params["e"],
                "f": new_params["f"],
                "g": new_params["g"],
                "p_min": conditions.get("Min_pressure") * 1e5,
                "dotm_max": new_results["dotm_max"],
                "x_bp": new_params["x_bp"]
            }
        },
        # "conditions": conditions,
        "kpis": kpis
    }  

@router.post("/download")
async def download(request: Request):
    form = await request.form()
    form = {k: float(v) for k, v in form.items()}

    ref_params = {k.replace("_ref", ""): v for k, v in form.items() if k.endswith("_ref")}
    new_params = {k.replace("_new", ""): v for k, v in form.items() if k.endswith("_new")}
    conditions = {k: v for k, v in form.items() if not k.endswith("_ref") and not k.endswith("_new")}

    ref_results = run_simulation(ref_params, conditions)
    new_results = run_simulation(new_params, conditions)

    # Timestamp segur per filename
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    filename = f"simulation_full_{timestamp}.csv"

    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".csv", mode="w", newline="")
    writer = csv.writer(tmp)

    writer.writerow(["Pressure_ref [bar]", "Time_ref [s]",
                     "Pressure_new [bar]", "Time_new [s]"])

    x_ref = ref_results["x_time_full"]
    t_ref = ref_results["t_full"]
    x_new = new_results["x_time_full"]
    t_new = new_results["t_full"]

    max_len = max(len(x_ref), len(x_new))

    for i in range(max_len):
        row = [
            x_ref[i]/1e5 if i < len(x_ref) else "",
            t_ref[i] if i < len(t_ref) else "",
            x_new[i]/1e5 if i < len(x_new) else "",
            t_new[i] if i < len(t_new) else ""
        ]
        writer.writerow(row)

    tmp.close()

    return FileResponse(
        tmp.name,
        media_type="text/csv",
        filename=filename
    )
