import os
import json
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

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

fig = go.Figure()

fig.add_trace(go.Candlestick(
    x=df.index,
    open=df["open"],
    high=df["high"],
    low=df["low"],
    close=df["close"],
    name=symbol,
    increasing_line_color="#26a69a",
    decreasing_line_color="#ef5350",
))

for s in supports:
    fig.add_hline(
        y=s["price"],
        line=dict(color="rgba(38, 166, 154, 0.6)", width=1, dash="dot"),
        annotation_text=f"S {s['price']:.2f} (×{s['times_touched']})",
        annotation_position="left",
        annotation_font=dict(color="#26a69a", size=10),
    )

for r in resistances:
    fig.add_hline(
        y=r["price"],
        line=dict(color="rgba(239, 83, 80, 0.6)", width=1, dash="dot"),
        annotation_text=f"R {r['price']:.2f} (×{r['times_touched']})",
        annotation_position="right",
        annotation_font=dict(color="#ef5350", size=10),
    )

fig.update_layout(
    title=f"{symbol} — Supports & Resistances",
    xaxis_title="Date",
    yaxis_title="Price (USD)",
    xaxis_rangeslider_visible=False,
    height=600,
    template="plotly_dark",
    showlegend=False,
)

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
