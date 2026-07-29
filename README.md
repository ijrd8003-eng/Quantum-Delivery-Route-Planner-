# Quantum Delivery Route Planner 🚚⚛️

An end-to-end Hybrid Quantum-Classical Route Optimization platform that solves the **Vehicle Routing Problem (VRP)** and **Traveling Salesperson Problem (TSP)** using **QAOA (Quantum Approximate Optimization Algorithm)** on Qiskit Aer simulators alongside classical benchmarks (**Google OR-Tools** and **Held-Karp Dynamic Programming**).

---

## 🌟 Overview

The **Quantum Delivery Route Planner** provides a complete pipeline to convert physical delivery locations into mathematical optimization models, execute quantum variational algorithms, decode measurement samples, and visualize comparative benchmarks against state-of-the-art classical solvers.

Key objectives:
- **Optimization Encoding**: Transform spatial delivery coordinates into a Quadratic Unconstrained Binary Optimization (QUBO) model and convert it to an Ising Hamiltonian ($H_C$).
- **Quantum Execution**: Solve $H_C$ using QAOA with parameter optimization via COBYLA on Qiskit Aer.
- **Classical Benchmarking**: Compare QAOA route cost, speed, and accuracy against Google OR-Tools and exact Held-Karp DP.
- **Interactive UI**: Explore network graphs, probability distributions, convergence plots, and comparative analytics in a Streamlit web application.

---

## 🏗️ Project Architecture & Directory Structure

```
DeliveryRoutePlanner/
├── app/
│   └── dashboard.py               # Streamlit multi-page interactive web application
├── classical/
│   ├── classical_result.py        # Data structures for classical solver results
│   └── tsp_solver.py              # Google OR-Tools & Held-Karp DP TSP solver
├── comparison/
│   ├── compare_results.py         # Comparative benchmark execution & reporter
│   ├── metrics.py                 # Performance ratio, accuracy & quality metrics
│   ├── noise_analysis.py          # Quantum noise simulation utilities
│   └── statistical_analysis.py    # Statistical sampling & confidence analysis
├── data/
│   ├── raw/
│   │   └── delivery_locations.csv # Input delivery node coordinates & metadata
│   ├── processed/
│   │   ├── distance_matrix.csv    # Computed pairwise Euclidean distance matrix
│   │   ├── ising_model.pkl        # Serialized Ising Hamiltonian operator & offset
│   │   └── validated_vrp_dataset.json # Validated VRP parameters & node metadata
├── docs/                          # Detailed project documentation & diagrams
│   ├── DOCUMENTATION.md           # Master Documentation Hub
│   ├── ARCHITECTURE.md            # System design & mathematical formulation
│   ├── PIPELINE_GUIDE.md          # Step-by-step pipeline execution breakdown
│   ├── QUANTUM_VS_CLASSICAL.md    # QAOA vs OR-Tools benchmark comparison
│   └── DASHBOARD_AND_VISUALIZATION.md # Streamlit dashboard & plotting guide
├── optimization/
│   ├── cost_function.py           # Objective function cost evaluators
│   ├── graph_encoder.py           # Network graph encoding utilities
│   ├── ising_converter.py        # QUBO-to-Ising Hamiltonian converter
│   ├── problem_encoder.py         # Distance matrix & VRP dataset generator
│   ├── quadratic_program.py       # Qiskit QuadraticProgram instance
│   ├── qubo_builder.py            # TSP binary decision variable matrix builder
│   └── vrp_qubo.py                # Vehicle Routing Problem QUBO formulation
├── ortools/
│   ├── constraints.py             # Capacity & time-window constraint definitions
│   ├── data_model.py              # Data model parser for OR-Tools Routing
│   ├── distance_matrix.py         # Integer matrix generator for OR-Tools
│   └── export_dataset.py          # Dataset exporter for OR-Tools benchmarks
├── quantum/
│   ├── ansatz.py                  # Custom QAOA ansatz circuit components
│   ├── backend.py                 # Quantum backend initializers (Simulator/IBM)
│   ├── circuit_builder.py        # Parametric QAOA circuit constructor
│   ├── decoder.py                 # Measurement bitstring TSP route decoder
│   ├── hardware.py                # Hardware transpilation & execution manager
│   ├── qaoa.py                    # QAOA variational algorithm solver
│   ├── result_processor.py       # Quantum sample & statistics processor
│   └── simulator.py               # Qiskit Aer SamplerV2 circuit execution
├── results/
│   ├── classical/                 # Saved classical solver JSON outputs
│   ├── comparison/                # Comparative evaluation metrics & JSON reports
│   └── simulator/                 # Quantum measurement counts & decoded routes
├── visualization/
│   ├── charts.py                  # Plotly comparison bar & pie charts
│   ├── delivery_graph.py          # NetworkX delivery graph visualizer
│   ├── probability_distribution.py # QAOA bitstring probability histogram
│   └── route_plot.py              # Matplotlib spatial route map plotter
├── config.py                      # Global configuration settings
├── main.py                        # End-to-end 11-step pipeline master runner
└── requirements.txt               # Python package dependencies
```

---

## ⚡ Quick Start

### 1. Prerequisites
- Python 3.9+ installed
- Recommended: Virtual environment (`venv` or `conda`)

### 2. Installation
```bash
# Clone the repository
git clone https://github.com/your-username/DeliveryRoutePlanner.git
cd DeliveryRoutePlanner

# Create & activate virtual environment
python -m venv .venv
# On Windows (PowerShell):
.venv\Scripts\Activate.ps1
# On Linux/macOS:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## 🚀 Execution Guide

### Option A: Run the Master End-to-End Pipeline
Execute all 11 sequential steps in the optimization, quantum execution, classical solver, and visualization pipeline:
```bash
python main.py
```

### Option B: Launch the Interactive Dashboard
Launch the Streamlit web dashboard to inspect interactive maps, quantum circuit details, and comparative metrics:
```bash
streamlit run app/dashboard.py
```

---

## 📚 Detailed Documentation

Explore in-depth documentation in the [`docs/`](file:///c:/Users/ASUS/Desktop/DeliveryRoutePlanner/docs) directory:

| Document | Description |
| :--- | :--- |
| **[Master Documentation Hub](file:///c:/Users/ASUS/Desktop/DeliveryRoutePlanner/docs/DOCUMENTATION.md)** | Comprehensive index, setup instructions, technology stack, and navigation guide. |
| **[Architecture & Math Guide](file:///c:/Users/ASUS/Desktop/DeliveryRoutePlanner/docs/ARCHITECTURE.md)** | Detailed mathematical formulations for VRP/TSP, QUBO binary mapping, Ising Hamiltonian translation, and QAOA ansatz. |
| **[Pipeline Execution Guide](file:///c:/Users/ASUS/Desktop/DeliveryRoutePlanner/docs/PIPELINE_GUIDE.md)** | Step-by-step breakdown of all 11 stages in `main.py`, data interfaces, and artifact schemas. |
| **[Quantum vs Classical Benchmarking](file:///c:/Users/ASUS/Desktop/DeliveryRoutePlanner/docs/QUANTUM_VS_CLASSICAL.md)** | Comparative performance evaluation between QAOA variational solver and OR-Tools / Held-Karp algorithms. |
| **[Dashboard & Visualization Guide](file:///c:/Users/ASUS/Desktop/DeliveryRoutePlanner/docs/DASHBOARD_AND_VISUALIZATION.md)** | Guide to the Streamlit UI components, NetworkX graph generators, and Plotly visualization modules. |

---

## 🔬 Core Technologies

- **Quantum Computing**: [Qiskit](https://qiskit.org/), `qiskit-aer`, `qiskit-algorithms`, `qiskit-optimization`
- **Classical Optimization**: [Google OR-Tools](https://developers.google.com/optimization), NetworkX, NumPy, SciPy
- **Data Processing**: Pandas, Python `pickle`, `json`
- **Visualization & UI**: [Streamlit](https://streamlit.io/), Matplotlib, Plotly, NetworkX
