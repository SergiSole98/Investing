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

candles_path = os.path.join(BASE_DIR, symbol, "historical_data.json")
poc_path = os.path.join(BASE_DIR, symbol, "POC", "poc.json")

if not os.path.exists(candles_path):
    st.error(f"No historical data for {symbol}. Run main.py first.")
    st.stop()

if not os.path.exists(poc_path):
    st.error(f"No POC data for {symbol}. Run main.py first.")
    st.stop()

df = load_candles(symbol)
poc = load_poc(symbol)

candle_objects = load_candle_objects(symbol)
rsi_values = calculate_rsi(candle_objects)
rsi_series = pd.Series(rsi_values, index=df.index)

summary = poc["summary"]
supports = poc["supports"]
resistances = poc["resistances"]

# ── Summary cards ───────────────────────────────────────────────────────────

col1, col2, col3 = st.columns(3)
col1.metric("Control Points", summary["total_control_points"])
col2.metric("Period Start", summary["period_start"])
col3.metric("Period End", summary["period_end"])

st.divider()

# ── Chart ───────────────────────────────────────────────────────────────────

fig = make_subplots(
    rows=2, cols=1,
    shared_xaxes=True,
    row_heights=[0.7, 0.3],
    vertical_spacing=0.04,
)

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

for s in supports:
    fig.add_hline(
        y=s["price"],
        line=dict(color="rgba(38, 166, 154, 0.6)", width=1, dash="dot"),
        annotation_text=f"S {s['price']:.2f} (×{s['times_touched']})",
        annotation_position="left",
        annotation_font=dict(color="#26a69a", size=10),
        row=1, col=1,
    )

for r in resistances:
    fig.add_hline(
        y=r["price"],
        line=dict(color="rgba(239, 83, 80, 0.6)", width=1, dash="dot"),
        annotation_text=f"R {r['price']:.2f} (×{r['times_touched']})",
        annotation_position="right",
        annotation_font=dict(color="#ef5350", size=10),
        row=1, col=1,
    )

fig.add_trace(go.Scatter(
    x=rsi_series.index,
    y=rsi_series.values,
    line=dict(color="#b39ddb", width=1.5),
    name="RSI(14)",
), row=2, col=1)

fig.add_hline(y=70, line=dict(color="rgba(239, 83, 80, 0.5)", width=1, dash="dash"), row=2, col=1)
fig.add_hline(y=30, line=dict(color="rgba(38, 166, 154, 0.5)", width=1, dash="dash"), row=2, col=1)

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
    df_sup = pd.DataFrame(supports)
    df_sup["price_range"] = df_sup["price_range"].apply(
        lambda x: f"{x['min']:.2f} – {x['max']:.2f}"
    )
    df_sup.columns = ["Price", "Range", "Times Touched", "Last Touch"]
    st.dataframe(df_sup, use_container_width=True, hide_index=True)

with col_res:
    st.subheader("Resistances")
    df_res = pd.DataFrame(resistances)
    df_res["price_range"] = df_res["price_range"].apply(
        lambda x: f"{x['min']:.2f} – {x['max']:.2f}"
    )
    df_res.columns = ["Price", "Range", "Times Touched", "Last Touch"]
    st.dataframe(df_res, use_container_width=True, hide_index=True)
