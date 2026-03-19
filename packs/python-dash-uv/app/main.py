"""
main.py — Ragnar DevOS Python-Dash-uv Starter App

แอป Dash ตัวอย่างที่มี DuckDB connection และ Plotly chart
ใช้เป็น starting point สำหรับ project จริง
"""

import os

import duckdb
import pandas as pd
import plotly.graph_objects as go
from dash import Dash, Input, Output, callback, dcc, html

# --------- Config ---------
# ดึงค่า config จาก environment variables
APP_HOST = os.environ.get("APP_HOST", "0.0.0.0")
APP_PORT = int(os.environ.get("APP_PORT", "8050"))
APP_DEBUG = os.environ.get("APP_DEBUG", "true").lower() == "true"
DUCKDB_PATH = os.environ.get("DUCKDB_PATH", ":memory:")

# --------- Database ---------


def get_connection() -> duckdb.DuckDBPyConnection:
    """สร้าง DuckDB connection"""
    return duckdb.connect(DUCKDB_PATH)


def init_sample_data(conn: duckdb.DuckDBPyConnection) -> None:
    """สร้าง sample data สำหรับ demo (ใช้เฉพาะตอน development)"""
    conn.execute("""
        CREATE TABLE IF NOT EXISTS daily_revenue (
            date DATE,
            revenue DOUBLE,
            category VARCHAR
        )
    """)

    # ตรวจว่ามีข้อมูลแล้วหรือยัง
    count = conn.execute("SELECT COUNT(*) FROM daily_revenue").fetchone()[0]
    if count > 0:
        return

    # ใส่ sample data 30 วัน
    conn.execute("""
        INSERT INTO daily_revenue
        SELECT
            CURRENT_DATE - INTERVAL (i) DAY AS date,
            50000 + RANDOM() * 50000 AS revenue,
            CASE WHEN i % 3 = 0 THEN 'Product A'
                 WHEN i % 3 = 1 THEN 'Product B'
                 ELSE 'Product C' END AS category
        FROM generate_series(0, 29) t(i)
    """)


def load_revenue_data() -> pd.DataFrame:
    """โหลดข้อมูล revenue จาก DuckDB"""
    with get_connection() as conn:
        init_sample_data(conn)
        df = conn.execute("""
            SELECT
                date,
                SUM(revenue) AS total_revenue,
                COUNT(*) AS transaction_count
            FROM daily_revenue
            GROUP BY date
            ORDER BY date
        """).df()
    return df


# --------- Dash App ---------

app = Dash(__name__, title="Ragnar DevOS — Dashboard")

# expose server สำหรับ gunicorn
server = app.server

# Layout
app.layout = html.Div(
    style={
        "fontFamily": "system-ui, -apple-system, sans-serif",
        "maxWidth": "1200px",
        "margin": "0 auto",
        "padding": "24px",
        "backgroundColor": "#f8fafc",
        "minHeight": "100vh",
    },
    children=[
        # Header
        html.Div(
            style={"marginBottom": "32px"},
            children=[
                html.H1(
                    "Ragnar DevOS",
                    style={"color": "#1e293b", "margin": "0", "fontSize": "28px"},
                ),
                html.P(
                    "AI-native Engineering Operating System — Dashboard",
                    style={"color": "#64748b", "margin": "4px 0 0 0"},
                ),
            ],
        ),

        # Refresh interval (อัพเดตทุก 60 วินาที)
        dcc.Interval(id="interval-refresh", interval=60_000, n_intervals=0),

        # Summary cards
        html.Div(
            id="summary-cards",
            style={
                "display": "grid",
                "gridTemplateColumns": "repeat(auto-fit, minmax(200px, 1fr))",
                "gap": "16px",
                "marginBottom": "24px",
            },
        ),

        # Revenue chart
        html.Div(
            style={
                "backgroundColor": "white",
                "borderRadius": "12px",
                "padding": "24px",
                "boxShadow": "0 1px 3px rgba(0,0,0,0.1)",
            },
            children=[
                html.H2(
                    "Daily Revenue (30 วันล่าสุด)",
                    style={"color": "#1e293b", "marginTop": "0", "fontSize": "18px"},
                ),
                dcc.Graph(id="revenue-chart", style={"height": "400px"}),
            ],
        ),
    ],
)


# --------- Callbacks ---------


@callback(
    Output("summary-cards", "children"),
    Output("revenue-chart", "figure"),
    Input("interval-refresh", "n_intervals"),
)
def update_dashboard(n_intervals: int) -> tuple:
    """อัพเดต dashboard เมื่อ interval trigger หรือ page load"""
    df = load_revenue_data()

    # คำนวณ summary metrics
    total_revenue = df["total_revenue"].sum()
    avg_daily = df["total_revenue"].mean()
    latest_day = df.iloc[-1]["total_revenue"] if not df.empty else 0
    prev_day = df.iloc[-2]["total_revenue"] if len(df) > 1 else latest_day
    change_pct = ((latest_day - prev_day) / prev_day * 100) if prev_day else 0

    # สร้าง summary cards
    def make_card(title: str, value: str, subtitle: str = "", color: str = "#3b82f6") -> html.Div:
        """สร้าง summary card component"""
        return html.Div(
            style={
                "backgroundColor": "white",
                "borderRadius": "12px",
                "padding": "20px",
                "boxShadow": "0 1px 3px rgba(0,0,0,0.1)",
                "borderLeft": f"4px solid {color}",
            },
            children=[
                html.P(title, style={"color": "#64748b", "margin": "0", "fontSize": "13px"}),
                html.P(value, style={"color": "#1e293b", "margin": "4px 0", "fontSize": "24px", "fontWeight": "700"}),
                html.P(subtitle, style={"color": "#94a3b8", "margin": "0", "fontSize": "12px"}),
            ],
        )

    change_color = "#10b981" if change_pct >= 0 else "#ef4444"
    change_sign = "+" if change_pct >= 0 else ""

    cards = [
        make_card(
            "รายได้รวม (30 วัน)",
            f"฿{total_revenue:,.0f}",
            "ผลรวมทั้งหมด",
            "#3b82f6",
        ),
        make_card(
            "รายได้เฉลี่ย/วัน",
            f"฿{avg_daily:,.0f}",
            "average daily revenue",
            "#8b5cf6",
        ),
        make_card(
            "รายได้วันล่าสุด",
            f"฿{latest_day:,.0f}",
            f"{change_sign}{change_pct:.1f}% vs เมื่อวาน",
            change_color,
        ),
    ]

    # สร้าง revenue chart
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=df["date"],
        y=df["total_revenue"],
        name="Daily Revenue",
        marker_color="#3b82f6",
        marker_opacity=0.8,
        hovertemplate="<b>%{x}</b><br>Revenue: ฿%{y:,.0f}<extra></extra>",
    ))

    fig.add_trace(go.Scatter(
        x=df["date"],
        y=df["total_revenue"].rolling(7, min_periods=1).mean(),
        name="7-day avg",
        line={"color": "#f59e0b", "width": 2, "dash": "dash"},
        hovertemplate="<b>7-day avg</b>: ฿%{y:,.0f}<extra></extra>",
    ))

    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        xaxis={"title": "Date", "gridcolor": "#f1f5f9"},
        yaxis={"title": "Revenue (THB)", "gridcolor": "#f1f5f9", "tickformat": ",.0f"},
        legend={"orientation": "h", "yanchor": "bottom", "y": 1.02},
        margin={"t": 40, "b": 40, "l": 60, "r": 20},
        hovermode="x unified",
    )

    return cards, fig


# --------- Entry Point ---------

if __name__ == "__main__":
    print(f"🚀 Starting Ragnar DevOS Dashboard on http://{APP_HOST}:{APP_PORT}")
    app.run(host=APP_HOST, port=APP_PORT, debug=APP_DEBUG)
