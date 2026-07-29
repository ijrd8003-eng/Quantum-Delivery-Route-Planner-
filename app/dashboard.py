"""
dashboard.py

Streamlit Dashboard for the
Quantum Delivery Route Planner Capstone.

Displays:
  - KPI Summary Cards
  - Delivery Network Map
  - QAOA Optimized Route Map
  - QAOA Probability Distribution
  - Classical vs Quantum Comparison Charts
  - Comparison Table

Run with:
    streamlit run app/dashboard.py

Author:
"""

import json
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import pandas as pd
import streamlit as st

# -------------------------------------------------------
# Page Configuration
# -------------------------------------------------------

st.set_page_config(
    page_title="Quantum Delivery Route Planner",
    page_icon="⚛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------------------------------
# Custom CSS
# -------------------------------------------------------

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .main { background: #0f0f23; }

    .stApp {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a3e 50%, #0f1f3d 100%);
    }

    .metric-card {
        background: linear-gradient(135deg, #1e1e3f, #2a2a5f);
        border: 1px solid #3a3a7a;
        border-radius: 16px;
        padding: 20px 24px;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0,0,0,0.4);
        margin-bottom: 8px;
    }

    .metric-value {
        font-size: 2.2rem;
        font-weight: 700;
        margin: 6px 0;
    }

    .metric-label {
        font-size: 0.85rem;
        color: #9090c0;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }

    .section-header {
        color: #a0c0ff;
        font-size: 1.3rem;
        font-weight: 600;
        border-bottom: 2px solid #3a3a7a;
        padding-bottom: 8px;
        margin: 20px 0 16px 0;
    }

    .badge-quantum {
        background: linear-gradient(90deg, #ff5722, #ff9800);
        color: white;
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
    }

    .badge-classical {
        background: linear-gradient(90deg, #2196F3, #03a9f4);
        color: white;
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
    }

    .stDataFrame { border-radius: 10px; }
    .stPlotlyChart { border-radius: 12px; }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------
# Paths
# -------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

# -------------------------------------------------------
# Data Loaders
# -------------------------------------------------------

@st.cache_data
def load_locations():
    path = BASE_DIR / "data" / "raw" / "delivery_locations.csv"
    if path.exists():
        return pd.read_csv(path)
    return pd.DataFrame()


@st.cache_data
def load_distance_matrix():
    path = BASE_DIR / "data" / "processed" / "distance_matrix.csv"
    if path.exists():
        return pd.read_csv(path, index_col=0)
    return pd.DataFrame()


@st.cache_data
def load_quantum_results():
    path = BASE_DIR / "results" / "simulator" / "processed_results.json"
    if path.exists():
        with open(path) as f:
            return json.load(f)
    return {}


@st.cache_data
def load_counts():
    path = BASE_DIR / "results" / "simulator" / "counts.json"
    if path.exists():
        with open(path) as f:
            return json.load(f)
    return {}


@st.cache_data
def load_classical_result():
    path = BASE_DIR / "results" / "classical" / "classical_result.json"
    if path.exists():
        with open(path) as f:
            return json.load(f)
    return {}


@st.cache_data
def load_comparison():
    path = BASE_DIR / "results" / "comparison" / "comparison_result.json"
    if path.exists():
        with open(path) as f:
            return json.load(f)
    return {}


@st.cache_data
def load_decoded():
    path = BASE_DIR / "results" / "simulator" / "decoded_solution.json"
    if path.exists():
        with open(path) as f:
            return json.load(f)
    return {}


# -------------------------------------------------------
# Load All Data
# -------------------------------------------------------

locations = load_locations()
dist_matrix = load_distance_matrix()
quantum = load_quantum_results()
counts = load_counts()
classical = load_classical_result()
comparison = load_comparison()
decoded = load_decoded()

q_stats = quantum.get("statistics", {})
q_cost = float(q_stats.get("route_cost") or 0)
q_time = float(q_stats.get("execution_time", 2.5))
q_prob = float(q_stats.get("best_probability", 0))
q_unique = int(q_stats.get("unique_solutions", 0))
q_shots = int(q_stats.get("total_shots", 0))

c_cost = float(classical.get("route_cost", 0))
c_time = float(classical.get("execution_time", 0))

accuracy_pct = 0.0
if comparison:
    perf = comparison.get("performance", {})
    accuracy_pct = perf.get("solution_quality", {}).get("accuracy_pct", 0)

# -------------------------------------------------------
# Header
# -------------------------------------------------------

st.markdown("""
<div style="text-align:center; padding: 30px 0 10px 0;">
    <h1 style="font-size:2.5rem; font-weight:700; color:#a0c0ff; margin:0;">
        ⚛️ Quantum Delivery Route Planner
    </h1>
    <p style="color:#7070a0; font-size:1.0rem; margin-top:8px;">
        QAOA Simulation vs Classical OR-Tools — Capstone Research Dashboard
    </p>
</div>
""", unsafe_allow_html=True)

st.divider()

# -------------------------------------------------------
# Sidebar
# -------------------------------------------------------

with st.sidebar:
    st.markdown("### ⚛️ Project Info")
    st.markdown("""
    **Quantum Delivery Route Planner**

    Solves the Traveling Salesperson Problem (TSP)
    using the Quantum Approximate Optimization
    Algorithm (QAOA) on a Qiskit Aer simulator.

    ---
    """)

    st.markdown("### 📊 Pipeline Status")

    def status_badge(label, path):
        exists = Path(path).exists()
        icon = "✅" if exists else "❌"
        st.markdown(f"{icon} `{label}`")

    status_badge("distance_matrix.csv", BASE_DIR / "data/processed/distance_matrix.csv")
    status_badge("ising_model.pkl", BASE_DIR / "data/processed/ising_model.pkl")
    status_badge("qaoa_result.pkl", BASE_DIR / "results/simulator/qaoa_result.pkl")
    status_badge("counts.json", BASE_DIR / "results/simulator/counts.json")
    status_badge("decoded_solution.json", BASE_DIR / "results/simulator/decoded_solution.json")
    status_badge("processed_results.json", BASE_DIR / "results/simulator/processed_results.json")
    status_badge("classical_result.json", BASE_DIR / "results/classical/classical_result.json")
    status_badge("comparison_result.json", BASE_DIR / "results/comparison/comparison_result.json")

    st.markdown("---")
    st.markdown("### 🔧 QAOA Settings")
    st.info(f"**Qubits:** {q_stats.get('total_shots') and '16'}\n\n**Shots:** {q_shots}\n\n**Unique:** {q_unique}")


# -------------------------------------------------------
# KPI Cards
# -------------------------------------------------------

st.markdown('<div class="section-header">📈 Key Performance Indicators</div>', unsafe_allow_html=True)

col1, col2, col3, col4, col5 = st.columns(5)

def kpi_card(col, label, value, color, unit=""):
    with col:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value" style="color:{color};">{value}{unit}</div>
        </div>
        """, unsafe_allow_html=True)

kpi_card(col1, "QAOA Route Cost", f"{q_cost:.1f}", "#FF5722")
kpi_card(col2, "Classical Cost", f"{c_cost:.1f}", "#2196F3")
kpi_card(col3, "Best Probability", f"{q_prob:.4f}", "#9C27B0")
kpi_card(col4, "Unique Solutions", f"{q_unique:,}", "#00BCD4")
kpi_card(col5, "Quantum Accuracy", f"{accuracy_pct:.1f}", "#4CAF50", "%")

st.markdown("<br>", unsafe_allow_html=True)

# -------------------------------------------------------
# Map & Route Section
# -------------------------------------------------------

st.markdown('<div class="section-header">🗺️ Delivery Network & Routes</div>', unsafe_allow_html=True)

map_col, route_col = st.columns(2)

# --- Delivery Network Map ---
with map_col:
    st.markdown("**Delivery Network (All Connections)**")

    if not locations.empty:
        fig, ax = plt.subplots(figsize=(6, 5))
        fig.patch.set_facecolor("#1a1a2e")
        ax.set_facecolor("#16213e")

        # Draw all edges
        for i, row_i in locations.iterrows():
            for j, row_j in locations.iterrows():
                if i < j:
                    ax.plot(
                        [row_i["x"], row_j["x"]],
                        [row_i["y"], row_j["y"]],
                        color="#3a3a7a", linewidth=0.8, alpha=0.4
                    )

        # Nodes
        for _, row in locations.iterrows():
            color = "#FF5722" if row["type"] == "Depot" else "#2196F3"
            size = 200 if row["type"] == "Depot" else 120
            marker = "s" if row["type"] == "Depot" else "o"
            ax.scatter(row["x"], row["y"], s=size, color=color, marker=marker, zorder=3)
            ax.text(row["x"] + 1.5, row["y"] + 1.5, row["name"], color="white", fontsize=8)

        ax.set_title("Delivery Network", color="white", fontsize=11)
        ax.tick_params(colors="white")
        ax.grid(alpha=0.2, color="#3a3a7a")
        for spine in ax.spines.values():
            spine.set_edgecolor("#3a3a7a")

        depot_p = mpatches.Patch(color="#FF5722", label="Depot")
        cust_p = mpatches.Patch(color="#2196F3", label="Customer")
        ax.legend(handles=[depot_p, cust_p], facecolor="#1a1a2e", labelcolor="white")

        st.pyplot(fig, use_container_width=True)
        plt.close(fig)
    else:
        st.warning("delivery_locations.csv not found.")

# --- QAOA Route Map ---
with route_col:
    st.markdown("**QAOA Optimized Route**")

    route = decoded.get("decoded_route", [])

    if not locations.empty and route:
        location_map = {row["name"]: (row["x"], row["y"]) for _, row in locations.iterrows()}

        fig, ax = plt.subplots(figsize=(6, 5))
        fig.patch.set_facecolor("#1a1a2e")
        ax.set_facecolor("#16213e")

        # All nodes
        for _, row in locations.iterrows():
            color = "#FF5722" if row["type"] == "Depot" else "#2196F3"
            size = 200 if row["type"] == "Depot" else 120
            marker = "s" if row["type"] == "Depot" else "o"
            ax.scatter(row["x"], row["y"], s=size, color=color, marker=marker, zorder=3)
            ax.text(row["x"] + 1.5, row["y"] + 1.5, row["name"], color="white", fontsize=8)

        # Route path
        route_x, route_y = [], []
        for node in route:
            if node in location_map:
                x, y = location_map[node]
                route_x.append(x)
                route_y.append(y)

        if route_x:
            ax.plot(route_x, route_y, color="#4CAF50", linewidth=2.5,
                    marker="o", markersize=6, zorder=2, label="QAOA Route")
            # Arrows
            for i in range(len(route_x) - 1):
                ax.annotate(
                    "", xy=(route_x[i+1], route_y[i+1]),
                    xytext=(route_x[i], route_y[i]),
                    arrowprops=dict(arrowstyle="->", color="#80FF80", lw=1.5)
                )

        ax.set_title(f"QAOA Route  (Cost: {q_cost:.2f})", color="white", fontsize=11)
        ax.tick_params(colors="white")
        ax.grid(alpha=0.2, color="#3a3a7a")
        for spine in ax.spines.values():
            spine.set_edgecolor("#3a3a7a")
        ax.legend(facecolor="#1a1a2e", labelcolor="white")

        st.pyplot(fig, use_container_width=True)
        plt.close(fig)
    else:
        st.warning("Route data not available. Run the full pipeline first.")

# -------------------------------------------------------
# Probability Distribution
# -------------------------------------------------------

st.markdown('<div class="section-header">📊 QAOA Measurement Probability Distribution</div>', unsafe_allow_html=True)

if counts:
    total = sum(counts.values())
    probs = {k: v/total for k, v in counts.items()}
    top_n = 20
    top = sorted(probs.items(), key=lambda x: x[1], reverse=True)[:top_n]

    labels = [x[0][:8] + ".." if len(x[0]) > 8 else x[0] for x in top]
    values = [x[1] for x in top]

    fig, ax = plt.subplots(figsize=(14, 4))
    fig.patch.set_facecolor("#1a1a2e")
    ax.set_facecolor("#16213e")

    bar_colors = ["#FF5722" if i == 0 else "#9C27B0" for i in range(len(labels))]
    bars = ax.bar(range(len(labels)), values, color=bar_colors, edgecolor="#333")

    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels, rotation=45, ha="right", fontsize=7, color="white")
    ax.set_ylabel("Probability", color="white")
    ax.set_title(f"Top {top_n} Measurement Outcomes (Total shots: {total:,})", color="white")
    ax.tick_params(colors="white")
    ax.grid(axis="y", alpha=0.3, color="#3a3a7a")
    for spine in ax.spines.values():
        spine.set_edgecolor("#3a3a7a")

    st.pyplot(fig, use_container_width=True)
    plt.close(fig)
else:
    st.info("Run `quantum/simulator.py` to generate counts.json")

# -------------------------------------------------------
# Comparison Charts
# -------------------------------------------------------

st.markdown('<div class="section-header">⚖️ Classical vs Quantum Comparison</div>', unsafe_allow_html=True)

comp_col1, comp_col2, comp_col3 = st.columns(3)

plot_kwargs = dict(
    facecolor="#1a1a2e"
)

def dark_axes(ax):
    ax.set_facecolor("#16213e")
    ax.tick_params(colors="white")
    for spine in ax.spines.values():
        spine.set_edgecolor("#3a3a7a")
    ax.grid(axis="y", alpha=0.3, color="#3a3a7a")
    ax.title.set_color("white")
    ax.yaxis.label.set_color("white")


with comp_col1:
    st.markdown("**Route Cost**")
    fig, ax = plt.subplots(figsize=(4, 3))
    fig.patch.set_facecolor("#1a1a2e")
    labels = ["Classical", "QAOA"]
    vals = [c_cost or 1, q_cost or 1]
    bars = ax.bar(labels, vals, color=["#2196F3", "#FF5722"], edgecolor="white", linewidth=0.5)
    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width()/2, b.get_height(), f"{v:.1f}",
                ha="center", va="bottom", color="white", fontweight="bold", fontsize=10)
    ax.set_title("Route Cost", fontsize=11)
    dark_axes(ax)
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

with comp_col2:
    st.markdown("**Execution Time (s)**")
    fig, ax = plt.subplots(figsize=(4, 3))
    fig.patch.set_facecolor("#1a1a2e")
    vals = [c_time or 0.001, q_time or 2.5]
    bars = ax.bar(["Classical", "QAOA"], vals, color=["#2196F3", "#FF5722"], edgecolor="white", linewidth=0.5)
    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width()/2, b.get_height(), f"{v:.3f}s",
                ha="center", va="bottom", color="white", fontweight="bold", fontsize=10)
    ax.set_title("Execution Time", fontsize=11)
    ax.set_ylabel("Seconds")
    dark_axes(ax)
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

with comp_col3:
    st.markdown("**Solution Diversity**")
    fig, ax = plt.subplots(figsize=(4, 3))
    fig.patch.set_facecolor("#1a1a2e")
    vals = [1, q_unique or 1]
    bars = ax.bar(["Classical", "QAOA"], vals, color=["#2196F3", "#FF5722"], edgecolor="white", linewidth=0.5)
    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width()/2, b.get_height(), f"{v:,}",
                ha="center", va="bottom", color="white", fontweight="bold", fontsize=10)
    ax.set_title("Unique Solutions", fontsize=11)
    dark_axes(ax)
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

# -------------------------------------------------------
# Comparison Table
# -------------------------------------------------------

st.markdown('<div class="section-header">📋 Detailed Comparison Table</div>', unsafe_allow_html=True)

if comparison:
    perf = comparison.get("performance", {})
    cost_c = perf.get("cost_comparison", {})
    speed_c = perf.get("speed_comparison", {})
    qual_c = perf.get("solution_quality", {})
    div_c = perf.get("solution_diversity", {})

    table_data = {
        "Metric": [
            "Route Cost",
            "Execution Time",
            "Unique Solutions",
            "Solution Accuracy",
            "Optimality Gap",
            "Cost Winner",
            "Speed Winner"
        ],
        "Classical (OR-Tools)": [
            f"{c_cost:.4f}",
            f"{c_time:.6f}s",
            "1",
            "100% (Reference)",
            "0%",
            "✓" if cost_c.get("winner") == "Classical" else "",
            "✓" if speed_c.get("faster_method") == "Classical" else ""
        ],
        "Quantum (QAOA)": [
            f"{q_cost:.4f}",
            f"{q_time:.4f}s",
            f"{q_unique:,}",
            f"{qual_c.get('accuracy_pct', 0):.2f}%",
            f"{qual_c.get('optimality_gap_pct', 0):.2f}%",
            "✓" if cost_c.get("winner") == "Quantum" else "",
            "✓" if speed_c.get("faster_method") == "Quantum" else ""
        ]
    }

    df_table = pd.DataFrame(table_data)
    st.dataframe(df_table, use_container_width=True, hide_index=True)
else:
    st.info("Run the full pipeline to generate comparison data.")

# -------------------------------------------------------
# Route Details
# -------------------------------------------------------

st.markdown('<div class="section-header">🗺️ Route Details</div>', unsafe_allow_html=True)

route_col_q, route_col_c = st.columns(2)

with route_col_q:
    st.markdown('<span class="badge-quantum">QUANTUM (QAOA)</span>', unsafe_allow_html=True)
    q_route = decoded.get("decoded_route", [])
    if q_route:
        st.code(" → ".join(q_route))
        st.metric("Total Cost", f"{q_cost:.4f}", delta=None)
        st.metric("Best Bitstring Probability", f"{q_prob:.4f}", delta=None)
    else:
        st.info("No decoded route. Run decoder.py first.")

with route_col_c:
    st.markdown('<span class="badge-classical">CLASSICAL (OR-Tools)</span>', unsafe_allow_html=True)
    c_route_names = classical.get("route_names", [])
    if c_route_names:
        st.code(" → ".join(c_route_names))
        st.metric("Total Cost", f"{c_cost:.4f}", delta=None)
        st.metric("Execution Time", f"{c_time:.6f}s", delta=None)
    else:
        st.info("No classical route. Run tsp_solver.py first.")

# -------------------------------------------------------
# Distance Matrix
# -------------------------------------------------------

with st.expander("📐 View Distance Matrix"):
    if not dist_matrix.empty:
        st.dataframe(dist_matrix.round(2), use_container_width=True)
    else:
        st.info("Run problem_encoder.py to generate distance_matrix.csv")

# -------------------------------------------------------
# Footer
# -------------------------------------------------------

st.divider()
st.markdown("""
<div style="text-align:center; color:#5050a0; font-size:0.85rem; padding:10px 0;">
    ⚛️ Quantum Delivery Route Planner Capstone &nbsp;|&nbsp;
    Powered by Qiskit · OR-Tools · Streamlit
</div>
""", unsafe_allow_html=True)
