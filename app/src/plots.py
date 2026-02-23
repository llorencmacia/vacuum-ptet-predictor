import numpy as np
import plotly.graph_objects as go
import plotly.io as pio

def build_time_figure(ref, new):
    fig = go.Figure()
    fig.add_trace(go.Scatter(y=np.array(ref["x_time_full"])/1e5, x=ref["t_full"], mode="lines", name="Reference", line=dict(color="blue")))
    fig.add_trace(go.Scatter(y=np.array(new["x_time_full"])/1e5, x=new["t_full"], mode="lines", name="New", line=dict(color="red")))
    fig.update_layout(title="Evacuation Time vs Pressure", yaxis_title="Pressure [bar]", xaxis_title="Time [s]", template="plotly_white", margin=dict(l=20, r=20, t=40, b=20), height=350)
    return pio.to_html(fig, full_html=False)

def build_error_figure(ref, new):
    error = np.abs(np.array(new["t_full"]) - np.array(ref["t_full"]))
    fig = go.Figure()
    # fig.add_trace(go.Scatter(x=np.array(ref["x_time_full"])/1e5, y=error, mode="lines", name="Absolute Error", line=dict(color="black")))
    fig.add_trace(go.Scatter(x=np.array(ref["t_full"]), y=error, mode="lines", name="Absolute Error", line=dict(color="black")))
    fig.update_layout(title="Absolute Error |t_new - t_ref|", xaxis_title="Time [s]", yaxis_title="Error [s]", template="plotly_white", margin=dict(l=20, r=20, t=40, b=20), height=350)
    return pio.to_html(fig, full_html=False)

def build_piecewise_figure(ref, new):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=np.array(ref["x"])/1e5, y=ref["y_piece"], mode="lines", name="Reference", line=dict(color="blue")))
    fig.add_trace(go.Scatter(x=np.array(new["x"])/1e5, y=new["y_piece"], mode="lines", name="New", line=dict(color="red")))
    fig.update_layout(title="Piecewise Flow Model", xaxis_title="Pressure [bar]", yaxis_title="ṁ(p)", template="plotly_white", margin=dict(l=20, r=20, t=40, b=20), height=350)
    return pio.to_html(fig, full_html=False)

def build_polynomial_figure(ref, new):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=np.array(ref["x"])/1e5, y=ref["y_poly"], mode="lines", name="Reference", line=dict(color="blue")))
    fig.add_trace(go.Scatter(x=np.array(new["x"])/1e5, y=new["y_poly"], mode="lines", name="New", line=dict(color="red")))
    fig.update_layout(title="Polynomial Efficiency Model", xaxis_title="Pressure [bar]", yaxis_title="n(p)", template="plotly_white", margin=dict(l=20, r=20, t=40, b=20), autosize=True, height=350)
    return pio.to_html(fig, full_html=False)