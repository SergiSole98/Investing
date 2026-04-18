import os
import sys
import json
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

sys.path.insert(0, os.path.dirname(__file__))

from application.calculate_rsi import calculate_rsi
from infrastructure.json_repository import load_candles as load_candle_objects

BASE_DIR = os.path.dirname(__file__)
EXCLUDED = {"application", "domain", "infrastructure", "__pycache__"}

SUP_FILL   = "rgba(0, 230, 118, 0.18)"
SUP_LINE   = "#00e676"
SUP_VLINE  = "rgba(0, 230, 118, 0.6)"
SUP_FONT   = "#00e676"

RES_FILL   = "rgba(255, 82, 82, 0.18)"
RES_LINE   = "#ff5252"
RES_VLINE  = "rgba(255, 82, 82, 0.6)"
RES_FONT   = "#ff5252"


def list_symbols() -> list[str]:
    return [
        d for d in os.listdir(BASE_DIR)
        if os.path.isdir(os.path.join(BASE_DIR, d)) and d not in EXCLUDED
    ]


def load_candles(symbol: str) -> pd.DataFrame:
    path = os.path.join(BASE_DIR, symbol, "historical_data.json")
    with open(path) as f:
        data = json.load(f)
    df = pd.DataFrame(data)
    df["datetime"] = pd.to_datetime(df["datetime"])
    return df.set_index("datetime")


def load_poc(symbol: str) -> dict:
    path = os.path.join(BASE_DIR, symbol, "POC", "poc.json")
    with open(path) as f:
        return json.load(f)


# ── Layout ──────────────────────────────────────────────────────────────────

st.set_page_config(page_title="Market POC Viewer", layout="wide")
st.title("Support & Resistance Viewer")

symbols = list_symbols()
if not symbols:
    st.warning("No symbols found. Run main.py first.")
    st.stop()

symbol = st.sidebar.selectbox("Symbol", symbols)

st.sidebar.divider()
st.sidebar.subheader("Visibility")
show_candles    = st.sidebar.toggle("Candlestick", value=True)
show_supports   = st.sidebar.toggle("Supports",    value=True)
show_resistances = st.sidebar.toggle("Resistances", value=True)

candles_path = os.path.join(BASE_DIR, symbol, "historical_data.json")
poc_path     = os.path.join(BASE_DIR, symbol, "POC", "poc.json")

if not os.path.exists(candles_path):
    st.error(f"No historical data for {symbol}. Run main.py first.")
    st.stop()

if not os.path.exists(poc_path):
    st.error(f"No POC data for {symbol}. Run main.py first.")
    st.stop()

df             = load_candles(symbol)
poc            = load_poc(symbol)
candle_objects = load_candle_objects(symbol)
rsi_values     = calculate_rsi(candle_objects)
rsi_series     = pd.Series(rsi_values, index=df.index)

summary     = poc["summary"]
supports    = poc["supports"]
resistances = poc["resistances"]

# ── Summary cards ───────────────────────────────────────────────────────────

col1, col2, col3, col4 = st.columns(4)
col1.metric("Supports",    summary["total_supports"])
col2.metric("Resistances", summary["total_resistances"])
col3.metric("Period Start", summary["period_start"])
col4.metric("Period End",   summary["period_end"])

st.divider()

# ── Chart ───────────────────────────────────────────────────────────────────

fig = make_subplots(
    rows=2, cols=1,
    shared_xaxes=True,
    row_heights=[0.7, 0.3],
    vertical_spacing=0.04,
)

if show_candles:
    fig.add_trace(go.Candlestick(
        x=df.index,
        open=df["open"],
        high=df["high"],
        low=df["low"],
        close=df["close"],
        name=symbol,
        increasing_line_color="#26a69a",
        decreasing_line_color="#ef5350",
    ), row=1, col=1)

if show_supports:
    for s in supports:
        fig.add_hrect(
            y0=s["price_range"]["min"],
            y1=s["price_range"]["max"],
            fillcolor=SUP_FILL,
            line=dict(color=SUP_LINE, width=1),
            row=1, col=1,
        )
        fig.add_hline(
            y=s["price_center"],
            line=dict(color=SUP_LINE, width=2),
            annotation_text=f"▶ S {s['price_center']:.2f}  ×{s['touches']}",
            annotation_position="left",
            annotation_font=dict(color=SUP_FONT, size=11, family="monospace"),
            annotation_bgcolor="rgba(0,0,0,0.5)",
            row=1, col=1,
        )
        fig.add_vline(
            x=s["last_touch"],
            line=dict(color=SUP_VLINE, width=1.5, dash="dash"),
            row=1, col=1,
        )

if show_resistances:
    for r in resistances:
        fig.add_hrect(
            y0=r["price_range"]["min"],
            y1=r["price_range"]["max"],
            fillcolor=RES_FILL,
            line=dict(color=RES_LINE, width=1),
            row=1, col=1,
        )
        fig.add_hline(
            y=r["price_center"],
            line=dict(color=RES_LINE, width=2),
            annotation_text=f"▶ R {r['price_center']:.2f}  ×{r['touches']}",
            annotation_position="right",
            annotation_font=dict(color=RES_FONT, size=11, family="monospace"),
            annotation_bgcolor="rgba(0,0,0,0.5)",
            row=1, col=1,
        )
        fig.add_vline(
            x=r["last_touch"],
            line=dict(color=RES_VLINE, width=1.5, dash="dash"),
            row=1, col=1,
        )

fig.add_trace(go.Scatter(
    x=rsi_series.index,
    y=rsi_series.values,
    line=dict(color="#b39ddb", width=1.5),
    name="RSI(14)",
), row=2, col=1)

fig.add_hline(y=70, line=dict(color="rgba(255, 82, 82, 0.6)",   width=1, dash="dash"), row=2, col=1)
fig.add_hline(y=30, line=dict(color="rgba(0, 230, 118, 0.6)", width=1, dash="dash"), row=2, col=1)

fig.update_layout(
    title=f"{symbol} — Supports & Resistances",
    xaxis_rangeslider_visible=False,
    height=750,
    template="plotly_dark",
    showlegend=False,
)
fig.update_yaxes(title_text="Price (USD)", row=1, col=1)
fig.update_yaxes(title_text="RSI", range=[0, 100], row=2, col=1)

st.plotly_chart(fig, use_container_width=True)

# ── Tables ───────────────────────────────────────────────────────────────────

col_sup, col_res = st.columns(2)

with col_sup:
    st.subheader("Supports")
    df_sup = pd.DataFrame(supports)[["price_center", "price_range", "touches", "last_touch"]]
    df_sup["price_range"] = df_sup["price_range"].apply(
        lambda x: f"{x['min']:.2f} – {x['max']:.2f}"
    )
    df_sup.columns = ["Price", "Range", "Touches", "Last Touch"]
    st.dataframe(df_sup, use_container_width=True, hide_index=True)

with col_res:
    st.subheader("Resistances")
    df_res = pd.DataFrame(resistances)[["price_center", "price_range", "touches", "last_touch"]]
    df_res["price_range"] = df_res["price_range"].apply(
        lambda x: f"{x['min']:.2f} – {x['max']:.2f}"
    )
    df_res.columns = ["Price", "Range", "Touches", "Last Touch"]
    st.dataframe(df_res, use_container_width=True, hide_index=True)
