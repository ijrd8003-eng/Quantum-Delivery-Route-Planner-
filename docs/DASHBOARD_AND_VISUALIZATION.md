# Dashboard & Visualization Guide 🖥️📊

This document describes the interactive Streamlit web dashboard (`app/dashboard.py`) and standalone visualization modules located in the `visualization/` directory.

---

## 🖥️ Streamlit Interactive Web Application

The project includes an interactive web interface built with **Streamlit**.

### Launch Command
```bash
streamlit run app/dashboard.py
```

---

## 🎨 Dashboard Page Breakdown

### 1. Overview Dashboard
- **Key Metrics Display**: Displays total locations, fleet vehicle count, optimal classical cost, QAOA route cost, and quantum accuracy percentage.
- **System Status Cards**: Indicates dataset validation status, Ising Hamiltonian availability, and execution results.

### 2. Interactive Route Explorer
- **Spatial Map**: Plots depot and customer locations in 2D coordinate space.
- **Route Line Overlays**: Visualizes and compares classical tour trajectories against QAOA-decoded quantum routes side-by-side.

### 3. Quantum Circuit & Parameter Explorer
- **Variational Parameters**: Visualizes optimized $\vec{\gamma}$ (cost angle) and $\vec{\beta}$ (mixer angle) values across ansatz layers.
- **Ansatz Inspector**: Displays QAOA circuit depth, qubit count ($N^2$), CNOT entangling gate count, and single-qubit rotation counts.

### 4. Comparative Benchmark Analytics
- **Cost Comparison Bar Charts**: Interactive Plotly bar charts contrasting Classical vs Quantum route distances.
- **Speed Comparison Gauges**: Visualizes execution speed ratios and timing metrics.
- **Probability Histogram**: Renders measurement bitstring frequency distributions from Qiskit Aer simulations.

---

## 📐 Visualization Modules Reference

### 1. `visualization/delivery_graph.py`
- **Purpose**: Constructs a `NetworkX` graph representation of delivery locations and depot node topology.
- **Key Function**: `draw_delivery_network(locations_df)`
- **Output**: Network topology graph rendering.

### 2. `visualization/route_plot.py`
- **Purpose**: Generates 2D Matplotlib spatial route maps with node labels, direction arrows, and travel sequence annotations.
- **Key Function**: `plot_route(locations_df, route_indices, title)`
- **Output**: Route trajectory map saved to `visualization/outputs/qaoa_route.png`.

### 3. `visualization/probability_distribution.py`
- **Purpose**: Renders measurement probability histograms showing top bitstring candidates and highlight optimal valid route bitstrings.
- **Key Function**: `plot_counts_histogram(counts_dict)`
- **Output**: Histogram chart saved to `visualization/outputs/probability_distribution.png`.

### 4. `visualization/charts.py`
- **Purpose**: Generates interactive Plotly charts for comparative benchmarking.
- **Key Functions**:
  - `create_cost_comparison_chart(classical_cost, quantum_cost)`
  - `create_speed_comparison_chart(classical_time, quantum_time)`
  - `create_accuracy_gauge(accuracy_percentage)`
