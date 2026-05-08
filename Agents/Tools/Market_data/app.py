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

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EXCLUDED = {"application", "domain", "infrastructure", "__pycache__"}

SUP_FILL   = "rgba(0, 230, 118, 0.18)"
SUP_LINE   = "#00e676"
SUP_VLINE  = "rgba(0, 230, 118, 0.6)"
SUP_FONT   = "#00e676"

RES_FILL   = "rgba(255, 82, 82, 0.18)"
RES_LINE   = "#ff5252"
RES_VLINE  = "rgba(255, 82, 82, 0.6)"
RES_FONT   = "#ff5252"

MA10_LINE = "#ffd54f"
MA30_LINE = "#42a5f5"


def list_symbols() -> list[str]:
    symbols = []
    for d in os.listdir(BASE_DIR):
        if d in EXCLUDED or not os.path.isdir(os.path.join(BASE_DIR, d)):
            continue
        top = os.path.join(BASE_DIR, d)
        if os.path.exists(os.path.join(top, "historical_data.json")):
            symbols.append(d)
        else:
            for sub in os.listdir(top):
                if os.path.isdir(os.path.join(top, sub)) and os.path.exists(
                    os.path.join(top, sub, "historical_data.json")
                ):
                    symbols.append(f"{d}/{sub}")
    return sorted(symbols)


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


def filter_period(df: pd.DataFrame, period: str) -> pd.DataFrame:
    if period == "All":
        return df

    end = df.index.max()
    offsets = {
        "1W": pd.Timedelta(days=7),
        "1M": pd.DateOffset(months=1),
        "3M": pd.DateOffset(months=3),
        "6M": pd.DateOffset(months=6),
        "1Y": pd.DateOffset(years=1),
    }
    start = end - offsets[period]
    return df[df.index >= start]


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
show_ma10       = st.sidebar.toggle("MA(10)",       value=True)
show_ma30       = st.sidebar.toggle("MA(30)",       value=True)

candles_path = os.path.join(BASE_DIR, symbol, "historical_data.json")
poc_path     = os.path.join(BASE_DIR, symbol, "POC", "poc.json")

if not os.path.exists(candles_path):
    st.error(f"No historical data for {symbol}. Run main.py first.")
    st.stop()

if not os.path.exists(poc_path):
    st.error(f"No POC data for {symbol}. Run main.py first.")
    st.stop()

df             = load_candles(symbol)
df["MA10"]     = df["close"].rolling(window=10).mean()
df["MA30"]     = df["close"].rolling(window=30).mean()
period         = st.sidebar.selectbox(
    "Period",
    ["1W", "1M", "3M", "6M", "1Y", "All"],
    index=4,
)
period_df      = filter_period(df, period)
chart_df       = period_df
poc            = load_poc(symbol)
candle_objects = load_candle_objects(symbol)
rsi_values     = calculate_rsi(candle_objects)
rsi_series     = pd.Series(rsi_values, index=df.index)
chart_rsi      = rsi_series.loc[chart_df.index]

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
        x=chart_df.index,
        open=chart_df["open"],
        high=chart_df["high"],
        low=chart_df["low"],
        close=chart_df["close"],
        name=symbol,
        increasing_line_color="#26a69a",
        decreasing_line_color="#ef5350",
    ), row=1, col=1)

if show_ma10:
    fig.add_trace(go.Scatter(
        x=chart_df.index,
        y=chart_df["MA10"],
        mode="lines",
        line=dict(color=MA10_LINE, width=1.8),
        name="MA(10)",
        hovertemplate="MA(10): %{y:.2f}<extra></extra>",
    ), row=1, col=1)

if show_ma30:
    fig.add_trace(go.Scatter(
        x=chart_df.index,
        y=chart_df["MA30"],
        mode="lines",
        line=dict(color=MA30_LINE, width=1.8),
        name="MA(30)",
        hovertemplate="MA(30): %{y:.2f}<extra></extra>",
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
    x=chart_rsi.index,
    y=chart_rsi.values,
    line=dict(color="#b39ddb", width=1.5),
    name="RSI(14)",
), row=2, col=1)

fig.add_hline(y=70, line=dict(color="rgba(255, 82, 82, 0.6)",   width=1, dash="dash"), row=2, col=1)
fig.add_hline(y=30, line=dict(color="rgba(0, 230, 118, 0.6)", width=1, dash="dash"), row=2, col=1)

fig.update_layout(
    title=f"{symbol} — Supports & Resistances",
    xaxis_rangeslider_visible=False,
    height=850,
    template="plotly_dark",
    showlegend=True,
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1,
    ),
)
fig.update_yaxes(title_text="Price (USD)", row=1, col=1)
fig.update_yaxes(title_text="RSI", range=[0, 100], row=2, col=1)

st.plotly_chart(fig, use_container_width=True)

# ── Tables ───────────────────────────────────────────────────────────────────

col_sup, col_res = st.columns(2)

with col_sup:
    st.subheader("Supports")
    if supports:
        df_sup = pd.DataFrame(supports)[["price_center", "price_range", "touches", "last_touch"]]
        df_sup["price_range"] = df_sup["price_range"].apply(
            lambda x: f"{x['min']:.2f} – {x['max']:.2f}"
        )
        df_sup.columns = ["Price", "Range", "Touches", "Last Touch"]
        st.dataframe(df_sup, use_container_width=True, hide_index=True)
    else:
        st.info("No supports found.")

with col_res:
    st.subheader("Resistances")
    if resistances:
        df_res = pd.DataFrame(resistances)[["price_center", "price_range", "touches", "last_touch"]]
        df_res["price_range"] = df_res["price_range"].apply(
            lambda x: f"{x['min']:.2f} – {x['max']:.2f}"
        )
        df_res.columns = ["Price", "Range", "Touches", "Last Touch"]
        st.dataframe(df_res, use_container_width=True, hide_index=True)
    else:
        st.info("No resistances found.")
